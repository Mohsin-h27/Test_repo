"""
Full Python simulation for resources from Slack APIs,
with in-memory state, JSON persistence, and embedded tests.

Run this notebook end-to-end to execute tests verifying correctness of each method.
"""
import json
import uuid
import unittest
from unittest.mock import patch
import random
import time
import os
import re
import string
import hashlib
import datetime
import urllib.parse
from typing import Dict, Any, List, Optional

# ---------------------------------------------------------------------------------------
# In-Memory Database Structure
# ---------------------------------------------------------------------------------------
# Initialize the DB as a global variable (simulating a JSON file)
DB: Dict[str, Any] = {
  "users": {},
  "channels": {
    "1234": {
      "messages": [
        {
            "ts": "",
            "user": "",
            "text": "",
            "reactions": [],
        }
      ],
      "conversations":{},
      'id':'1234',
      'name': '',
      "files": {}
    }
  },
  "files": {},
  "reminders": {},
  "usergroups": {},
  "scheduled_messages": [],
  "ephemeral_messages": []
}


# -------------------------------------------------------------------
# Persistence Helpers
# -------------------------------------------------------------------
def save_state(filepath: str):
    """Saves the current API state to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(DB, f)

def load_state(filepath: str):
    """Loads the API state from a JSON file."""
    global DB
    try:
        with open(filepath, 'r') as f:
            DB = json.load(f)
    except FileNotFoundError:
        pass

# -------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------
def _parse_query(query: str) -> Dict[str, Any]:
    """Parses the Slack Query Language into structured filters.

    Args:
        query (str): The Slack Query Language string.

    Returns:
        Dict[str, Any]: A dictionary containing the parsed filters.
    """
    filters = {
        "text": [],
        "excluded": [],
        "user": None,
        "channel": None,
        "date_after": None,
        "date_before": None,
        "date_during": None,
        "has": set(),
        "to": None,
        "wildcard": None,
        "boolean": "AND"
    }

    tokens = query.split()
    for token in tokens:
        if token.startswith("from:@"):
            filters["user"] = token.split("from:@")[1]
        elif token.startswith("in:#"):
            filters["channel"] = token.split("in:#")[1]
        elif token.startswith("after:"):
            filters["date_after"] = token.split("after:")[1]
        elif token.startswith("before:"):
            filters["date_before"] = token.split("before:")[1]
        elif token.startswith("during:"):
            filters["date_during"] = token.split("during:")[1]
        elif token.startswith("has:"):
            filters["has"].add(token.split("has:")[1])
        elif token.startswith("to:"):
            filters["to"] = token.split("to:")[1]
        elif '*' in token:
            filters["wildcard"] = token
        elif token == "OR":
            filters["boolean"] = "OR"
        elif token.startswith("-"):
            filters["excluded"].append(token[1:])
        else:
            filters["text"].append(token)

    return filters

def _matches_filters(msg: Dict[str, Any], filters: Dict[str, Any], channel_name: str) -> bool:
    """Checks if a message matches the parsed filters.

    Args:
        msg (Dict[str, Any]): The message to check.
        filters (Dict[str, Any]): The parsed filters (output of _parse_query).
        channel_name (str): The name of the channel.

    Returns:
        bool: True if the message matches the filters, False otherwise.
    """
    # Channel filter
    if filters["channel"] and channel_name != filters["channel"]:
        return False

    # User filter
    if filters["user"] and msg["user"] != filters["user"]:
        return False

    # Convert timestamp to date
    msg_ts = datetime.datetime.fromtimestamp(float(msg["ts"])).date()

    # Date filters
    if filters["date_after"]:
        date_after = datetime.datetime.strptime(filters["date_after"], "%Y-%m-%d").date()
        if msg_ts <= date_after:
            return False
    if filters["date_before"]:
        date_before = datetime.datetime.strptime(filters["date_before"], "%Y-%m-%d").date()
        if msg_ts >= date_before:
            return False
    if filters["date_during"]:
        during_value = filters["date_during"]

        # Year-only filter (e.g., during:2024)
        if re.fullmatch(r"\d{4}", during_value):
            if msg_ts.year != int(during_value):
                return False

        # Year and Month filter (e.g., during:2024-03)
        elif re.fullmatch(r"\d{4}-\d{2}", during_value):
            year, month = map(int, during_value.split("-"))
            if msg_ts.year != year or msg_ts.month != month:
                return False

        # Full Date filter (e.g., during:2024-03-23)
        elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", during_value):
            date_during = datetime.datetime.strptime(during_value, "%Y-%m-%d").date()
            if msg_ts != date_during:
                return False

    # Text filters
    text_match = any(word.lower() in msg["text"].lower() for word in filters["text"])
    excluded_match = any(word.lower() in msg["text"].lower() for word in filters["excluded"])
    if filters["boolean"] == "AND":
        if filters["text"] and not text_match:
            return False
    else:  # OR condition
        if filters["text"] and not text_match:
            return False

    if excluded_match:
        return False

    # Has filters
    if "link" in filters["has"] and not msg.get("links"):
        return False
    if "reaction" in filters["has"] and not msg.get("reactions"):
        return False
    if "star" in filters["has"] and not msg.get("is_starred"):
        return False

    # Wildcard search
    if filters["wildcard"]:
        pattern = filters["wildcard"].replace('*', '.*')
        if not re.search(pattern, msg["text"], re.IGNORECASE):
            return False

    return True
# ---------------------------------------------------------------------------------------
# AdminUsers Class & Methods
# ---------------------------------------------------------------------------------------
class AdminUsers:
    """
    Represents the /admin.users resource.
    """

    @staticmethod
    def invite(email: str, channel_ids: str = None, real_name: str = None, team_id: str = None) -> dict:
        """
        Invite a user to a Slack workspace.

        Args:
            email (str): Email address of the user to invite.
            channel_ids (str, optional): A comma-separated list of channel IDs to which to add the user. Optional.
            real_name (str, optional): Full name of the user. Optional.
            team_id (str, optional): The ID of the team to invite the user to. Optional.

        Returns:
            dict: A dictionary representing the result of the invite operation.
        """
        if "users" not in DB:
            DB["users"] = {}
        if "channels" not in DB:
          DB["channels"] = {}

        for user_id, user_data in DB["users"].items():
            if user_data.get("profile", {}).get("email") == email:
                return {"ok": False, "error": "already_invited"}

        base_id = hashlib.sha1(email.encode()).hexdigest()[:8].upper()
        user_id = f"U{base_id}"

        if user_id in DB["users"]:
            random.seed(base_id)
            suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=2))
            user_id = f"{user_id}{suffix}"

        user_data = {
            "id": user_id,
            "team_id": team_id,
            "name": email.split("@")[0],
            "real_name": real_name or email.split("@")[0].capitalize(),
            "profile": {
                "email": email,
                "display_name": email.split("@")[0].capitalize()[:5],
                "image": "default_base64_image",
                "image_crop_x": 0,
                "image_crop_y": 0,
                "image_crop_w": 100,
                "title": "Invited User"
            },
            "is_admin": False,
            "is_bot": False,
            "deleted": False,
            "presence": "away"
        }
        DB["users"][user_id] = user_data
        if channel_ids:
            channel_list = channel_ids.split(",")
            for channel_id in channel_list:
                if channel_id in DB["channels"]:
                    if "conversations" not in DB["channels"][channel_id]:
                        DB["channels"][channel_id]["conversations"] = {}
                    if "members" not in DB["channels"][channel_id]["conversations"]:
                        DB["channels"][channel_id]['conversations']["members"] = []
                    DB["channels"][channel_id]['conversations']["members"].append(user_id)
        return {"ok": True, "user": user_data}
# ---------------------------------------------------------------------------------------
# Chat Classes & Methods
# ---------------------------------------------------------------------------------------
class Chat:
    """Represents the chat API resource."""

    @staticmethod
    def meMessage(user_id: str, channel: str, text: str) -> dict:
        """
        Share a me message into a channel.

        Args:
            user_id (str): User ID.
            channel (str): Channel to send message to.
            text (str): Text of the message to send.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        if not channel:
            return {"ok": False, "error": "invalid_channel"}
        if not text:
            return {"ok": False, "error": "invalid_text"}

        # Ensure channel exists
        if channel not in DB["channels"]:
            DB["channels"][channel] = {}
            DB["channels"][channel]['messages'] = []
        if "messages" not in DB["channels"][channel]:
            DB["channels"][channel]['messages'] = []

        # Generate a timestamp
        ts = str(time.time())

        # Store message following the schema
        message = {"user": user_id, "text": text, "ts": ts}
        DB["channels"][channel]['messages'].append(message)

        return {"ok": True, "channel": channel, "text": text, "ts": ts}

    @staticmethod
    def delete(channel: str, ts: str) -> dict:
        """
        Deletes a message.

        Args:
            channel (str): Channel containing the message.
            ts (str): Timestamp of the message to be deleted.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        if not channel:
            return {"ok": False, "error": "missing_channel"}
        if not ts:
            return {"ok": False, "error": "missing_timestamp"}

        if channel not in DB["channels"]:
            return {"ok": False, "error": "channel_not_found"}

        messages = DB["channels"][channel]['messages']

        # Find and remove the message by timestamp
        for i, msg in enumerate(messages):
            if msg["ts"] == ts:
                del messages[i]
                return {"ok": True}

        return {"ok": False, "error": "message_not_found"}

    @staticmethod
    def deleteScheduledMessage(channel: str, scheduled_message_id: str, as_user: bool = False) -> dict:
        """
        Deletes a pending scheduled message from the queue.

        Args:
            channel (str): Channel from which the scheduled message should be removed.
            scheduled_message_id (str): The ID of the scheduled message.
            as_user (bool): Whether to delete the message as the authenticated user.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        if not channel:
            return {"ok": False, "error": "missing_channel"}
        if not scheduled_message_id:
            return {"ok": False, "error": "missing_scheduled_message_id"}

        # Iterate and find scheduled message, remove by ID. More efficient than key lookup.
        for i, msg in enumerate(DB["scheduled_messages"]):
            if msg.get("message_id") == int(scheduled_message_id) and msg.get("channel") == channel:
                del DB["scheduled_messages"][i]
                return {"ok": True}

        return {"ok": False, "error": "scheduled_message_not_found"}

    @staticmethod
    def postEphemeral(channel: str, user: str, attachments: str = None, blocks: list = None, text: str = None, as_user: bool = None, icon_emoji: str = None, icon_url: str = None, link_names: bool = None, markdown_text: str = None, parse: str = None, thread_ts: str = None, username: str = None) -> dict:
        """
        Sends an ephemeral message to a user in a channel.

        Args:
            channel (str): Channel to send the message to.
            user (str): User to send the message to.
            attachments (str, optional): JSON-based array of structured attachments.
            blocks (list, optional): A JSON-based array of structured blocks.
            text (str, optional): Message text.
            as_user (bool, optional): Pass true to post the message as the authed user.
            icon_emoji (str, optional): Emoji to use as the icon.
            icon_url (str, optional): URL to an image to use as the icon.
            link_names (bool, optional): Find and link channel names and usernames.
            markdown_text (str, optional): Message text formatted in markdown.
            parse (str, optional): Change how messages are treated.
            thread_ts (str, optional): Provide another message's ts value to post this message in a thread.
            username (str, optional): Set your bot's or your user name.

        Returns:
            dict: A dictionary representing the API response.
        """
        if not channel or not user:
            return {"ok": False, "error": "missing_required_arguments"}

        # Simulate sending the message (store in DB)
        message = {
            "channel": channel,
            "user": user,
            "text": text,
            "attachments": attachments,
            "blocks": blocks,
            "as_user": as_user,
            "icon_emoji": icon_emoji,
            "icon_url": icon_url,
            "link_names": link_names,
            "markdown_text": markdown_text,
            "parse": parse,
            "thread_ts": thread_ts,
            "username": username
        }
        DB["ephemeral_messages"].append(message)  #Store on the correct place

        return {"ok": True, "message": message}

    @staticmethod
    def postMessage(
                    channel: str,
                    ts: str = None,
                    attachments: Optional[str] = None,
                    blocks: Optional[List[Dict]] = None,
                    text: Optional[str] = None,
                    as_user: Optional[bool] = None,
                    icon_emoji: Optional[str] = None,
                    icon_url: Optional[str] = None,
                    link_names: Optional[bool] = None,
                    markdown_text: Optional[str] = None,
                    metadata: Optional[str] = None,
                    mrkdwn: Optional[bool] = None,
                    parse: Optional[str] = None,
                    reply_broadcast: Optional[bool] = None,
                    thread_ts: Optional[str] = None,
                    unfurl_links: Optional[bool] = None,
                    unfurl_media: Optional[bool] = None,
                    username: Optional[str] = None) -> Dict[str, Any]:
        """
        Sends a message to a channel.

        Args:
            channel: Channel ID.
            ts: Message timestamp.
            attachments: JSON-based array of structured attachments.
            blocks: A JSON-based array of structured blocks.
            text: Message text.
            as_user: Post as user (legacy).
            icon_emoji: Emoji to use as the icon.
            icon_url: URL to an image to use as the icon.
            link_names: Find and link user groups.
            markdown_text: Message text formatted in markdown.
            metadata: JSON object with event_type and event_payload fields.
            mrkdwn: Disable Slack markup parsing.
            parse: Change how messages are treated.
            reply_broadcast: Make reply visible to everyone.
            thread_ts: Provide another message's ts value to make this message a reply.
            unfurl_links: Enable unfurling of primarily text-based content.
            unfurl_media: Disable unfurling of media content.
            username: Set your bot's user name.

        Returns:
            A dictionary representing the API response.
        """
        # Input Validation
        if not channel:
            return {"ok": False, "error": "no_channel"}


        # Simulate message sending and store in DB
        message = {
            "channel": channel,
            "text": text,
            "attachments": attachments,
            "blocks": blocks,
            "user": username or "bot",  # Default to "bot" if username is not provided
            "ts": ts if ts else str(time.time()),  # Use time.time() for consistency
            "as_user": as_user,
            "icon_emoji": icon_emoji,
            "icon_url": icon_url,
            "link_names": link_names,
            "markdown_text": markdown_text,
            "metadata": metadata,
            "mrkdwn": mrkdwn,
            "parse": parse,
            "reply_broadcast": reply_broadcast,
            "thread_ts": thread_ts,
            "unfurl_links": unfurl_links,
            "unfurl_media": unfurl_media,
            "username": username
        }

        if channel not in DB["channels"]:
                return {"ok": False, "error": "channel_not_found"}

        if thread_ts is not None:
            if 'messages' not in DB["channels"][channel]:
                return {"ok": False, "error": "thread_not_found"}
            for msg in DB["channels"][channel]['messages']:
                if msg["ts"] == thread_ts:
                    if 'replies' not in msg:
                        DB["channels"][channel]['messages'][DB["channels"][channel]['messages'].index(msg)]['replies'] = []
                    DB["channels"][channel]['messages'][DB["channels"][channel]['messages'].index(msg)]['replies'].append(message)
                    msg = DB["channels"][channel]['messages'][DB["channels"][channel]['messages'].index(msg)]
                    return {"ok": True, "message": msg}

            return {"ok": False, "error": "thread_not_found"}


        if 'messages' not in DB["channels"][channel]:
            DB["channels"][channel]['messages'] = []
        DB["channels"][channel]['messages'].append(message)

        return {"ok": True, "message": message}

    @staticmethod
    def list_scheduled_Messages(channel: str = None, cursor: str = None, latest: str = None, limit: int = None, oldest: str = None, team_id: str = None):
        """
        Returns a list of scheduled messages.

        Args:
            channel (str, optional): The channel of the scheduled messages. Defaults to None.
            cursor (str, optional): For pagination purposes. Defaults to None.
            latest (str, optional): A Unix timestamp of the latest value in the time range. Defaults to None.
            limit (int, optional): Maximum number of original entries to return. Defaults to None.
            oldest (str, optional): A Unix timestamp of the oldest value in the time range. Defaults to None.
            team_id (str, optional): encoded team id to list channels in, required if org token is used. Defaults to None.

        Returns:
            dict: A dictionary containing the list of scheduled messages and pagination information.
        """
        # Access the global DB - No need for global keyword, we are not modifying at the top level

        # Filter scheduled messages based on provided arguments
        filtered_messages = DB.get("scheduled_messages", [])  # safer access
        if channel:
            filtered_messages = [msg for msg in filtered_messages if msg.get("channel") == channel]

        # Apply time range filtering using integers for comparison
        if oldest:
            try:
                oldest_int = int(float(oldest))  # Handle potential float strings
                filtered_messages = [msg for msg in filtered_messages if msg.get("post_at") >= oldest_int]
            except ValueError:
                return {"error": "invalid_oldest_timestamp", "ok": False}
        if latest:
            try:
                latest_int = int(float(latest))
                filtered_messages = [msg for msg in filtered_messages if msg.get("post_at") <= latest_int]
            except ValueError:
                return {"error": "invalid_latest_timestamp", "ok": False}
        # Apply limit and pagination
        if limit is not None:  # Check if limit is provided
            try:
                limit = int(limit)  # Ensure limit is an integer
                if limit < 0:
                    raise ValueError("Limit must be non-negative")
            except ValueError:
                return {"error": "invalid_limit", "ok": False}


            if cursor:
                try:
                    cursor_index = int(cursor)
                    filtered_messages = filtered_messages[cursor_index:]
                except (ValueError, IndexError):
                    return {"error": "invalid_cursor", "ok": False}

            next_cursor = None
            if len(filtered_messages) > limit:
                next_cursor = str(cursor_index + limit) if cursor else str(limit)  # Calculate next cursor
                filtered_messages = filtered_messages[:limit] #Apply limit

        else:
            next_cursor = None # If no limit, no next cursor.

        response = {
            "ok": True,
            "scheduled_messages": filtered_messages,
            "response_metadata": {"next_cursor": next_cursor},
        }
        return response

    @staticmethod
    def scheduleMessage(user_id :str, channel: str, post_at: int, attachments: str = None, blocks: list = None, text: str = None, as_user: bool = False, link_names: bool = False, markdown_text: str = None, metadata: str = None, parse: str = None, reply_broadcast: bool = False, thread_ts: str = None, unfurl_links: bool = True, unfurl_media: bool = False):
        """
        Schedules a message to be sent to a channel.

        Args:
            user_id (str): User ID.
            channel (str): Channel to send the message to.
            post_at (int): Unix timestamp for when to send the message.
            attachments (str, optional): JSON-based array of structured attachments.
            blocks (list, optional): A JSON-based array of structured blocks.
            text (str, optional): Message text.
            as_user (bool, optional): Post as the authed user. Defaults to False.
            link_names (bool, optional): Find and link user groups. Defaults to False.
            markdown_text (str, optional): Message text formatted in markdown.
            metadata (str, optional): JSON object with event_type and event_payload fields.
            parse (str, optional): Change how messages are treated.
            reply_broadcast (bool, optional): Whether reply should be made visible to everyone. Defaults to False.
            thread_ts (str, optional): Provide another message's ts value to make this message a reply.
            unfurl_links (bool, optional): Enable unfurling of primarily text-based content. Defaults to True.
            unfurl_media (bool, optional): Disable unfurling of media content. Defaults to False.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        if not channel:
            return {"ok": False, "error": "missing_channel"}
        if not post_at:
            return {"ok": False, "error": "missing_post_at"}
        try:
            post_at = int(float(post_at))
        except ValueError:
            return {"ok": False, "error": "invalid_post_at"}

        message_id = len(DB.get("scheduled_messages", [])) + 1  # Generate sequential ID
        message = {
            "message_id": message_id,
            "user_id": user_id,
            "channel": channel,
            "post_at": post_at,
            "attachments": attachments,
            "blocks": blocks,
            "text": text,
            "as_user": as_user,
            "link_names": link_names,
            "markdown_text": markdown_text,
            "metadata": metadata,
            "parse": parse,
            "reply_broadcast": reply_broadcast,
            "thread_ts": thread_ts,
            "unfurl_links": unfurl_links,
            "unfurl_media": unfurl_media,
        }

        DB["scheduled_messages"].append(message) # Append the message

        return {"ok": True, "message_id": message_id, "scheduled_message_id":str(message_id)} #Added scheduled_message_id

    @staticmethod
    def update(
        channel: str,
        ts: str,
        attachments: Optional[str] = None,
        blocks: Optional[str] = None,
        text: Optional[str] = None,
        as_user: Optional[bool] = None,
        file_ids: Optional[List[str]] = None,
        link_names: Optional[bool] = None,
        markdown_text: Optional[str] = None,
        parse: Optional[str] = None,
        reply_broadcast: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Updates a message.

        Args:
            channel: Channel containing the message.
            ts: Timestamp of the message to be updated.
            attachments: A JSON-text: The updated message text.
            as_user: Update the message as the authed user.
            file_ids: Array of new file ids.
            link_names: Find and link channel names and usernames.
            markdown_text: Message text formatted in markdown.
            parse: Change how messages are treated.
            reply_broadcast: Broadcast an existing thread reply.

        Returns:
            A dictionary representing the API response.
        """
        # Input validation
        if not channel:
            return {"ok": False, "error": "channel_not_found"}
        if not ts:
            return {"ok": False, "error": "invalid_timestamp"}

        if channel not in DB["channels"]:
             return {"ok": False, "error": "channel_not_found"}

        # Find the message in the correct channel
        message = None
        if "messages" not in DB["channels"][channel]:
            DB["channels"][channel]['messages'] = []
        for i, msg in enumerate(DB["channels"][channel]['messages']):
            if msg["ts"] == ts:
                message = msg
                message_index = i # Store the index for updating.
                break  # Exit loop once found

        if message is None:
            return {"ok": False, "error": "message_not_found"}

        # Update fields if provided.
        if attachments is not None:
            message["attachments"] = attachments
        if blocks is not None:
            message["blocks"] = blocks
        if text is not None:
            message["text"] = text
        if as_user is not None:
            message["as_user"] = as_user
        if file_ids is not None:
            message["file_ids"] = file_ids
        if link_names is not None:
            message["link_names"] = link_names
        if markdown_text is not None:
            message["markdown_text"] = markdown_text
        if parse is not None:
            message["parse"] = parse
        if reply_broadcast is not None:
            message["reply_broadcast"] = reply_broadcast

        # Update the message directly in the list using the index.
        DB["channels"][channel]['messages'][message_index] = message

        return {"ok": True, "ts": ts, "channel": channel, "message": message}
# ---------------------------------------------------------------------------------------
# Conversations Classes & Methods
# ---------------------------------------------------------------------------------------
class Conversations:
    """
    Simulates the /conversations resource.
    """

    @staticmethod
    def leave(user_id: str, channel: str) -> dict:
        """
        Leaves a conversation.

        Args:
            user_id (str): User ID of the user leaving the conversation.
            channel (str): Conversation to leave.

        Returns:
            dict: A dictionary representing the API response.
        """

        if not user_id:
            return {"ok": False, "error": "missing_user_id"}

        if not channel:
            return {"ok": False, "error": "missing_channel"}

        if channel not in DB["channels"]:
            return {"ok": False, "error": "channel_not_found"}

        if 'members' not in DB["channels"][channel]['conversations']:
             DB["channels"][channel]['conversations']["members"] = []

        if user_id not in DB["channels"][channel]['conversations']["members"]:
            return {"ok": False, "error": "not_in_conversation"}

        DB["channels"][channel]['conversations']["members"].remove(user_id)
        return {"ok": True}

    @staticmethod
    def invite(channel: str, users: str, force: bool = False):
        """
        Invites users to a channel.

        Args:
            channel (str): The ID of the channel to invite users to.
            users (str): A comma separated list of user IDs.
            force (bool, optional): Continue inviting valid users even if some are invalid. Defaults to False.

        Returns:
            dict: A dictionary representing the API response.
        """
        if not channel:
            return {"ok": False, "error": "missing_channel"}
        if not users:
            return {"ok": False, "error": "missing_users"}


        user_list = users.split(",")
        valid_users = []
        invalid_users = []

        for user_id in user_list:
            if user_id in DB["users"]:  # Simple validation: User IDs start with "U"
                valid_users.append(user_id)
            else:
                invalid_users.append(user_id)

        if not force and invalid_users:
            return {"ok": False, "error": "invalid_user_ids", "invalid_users": invalid_users}

        # Simulate adding users to the channel
        if channel not in DB["channels"]:
            return {"ok": False, "error": "channel_not_found"}


        if 'conversations' not in DB["channels"][channel]:
            DB["channels"][channel]['conversations'] = {}
        if "members" not in DB["channels"][channel]['conversations']:
            DB["channels"][channel]['conversations']["members"] = []

        for user_id in valid_users:
            if user_id not in DB["channels"][channel]['conversations']["members"]:
                DB["channels"][channel]['conversations']["members"].append(user_id)

        return {"ok": True, "channel": channel, "invited": valid_users}

    @staticmethod
    def archive(channel: str):
        """Archives a conversation.

        Args:
            channel (str): ID of conversation to archive.

        Returns:
            dict: A dictionary representing the API response.
        """

        if not channel:
            return {"ok": False, "error": "missing_channel"}

        if channel not in DB["channels"]:
            return {"ok": False, "error": "channel_not_found"}

        DB["channels"][channel]["is_archived"] = True
        return {"ok": True}

    @staticmethod
    def join(user_id :str, channel: str):
        """
        Joins an existing conversation.

        Args:
            user_id (str): User ID of the user joining the conversation.
            channel (str): ID of conversation to join.

        Returns:
            dict: A dictionary representing the API response.
        """
        if not user_id:
            return {"ok": False, "error": "missing_user_id"}
        if not channel:
            return {"ok": False, "error": "missing_channel"}
        if user_id not in DB["users"]:
            return {"ok": False, "error": "user_not_found"}

        # Simulate joining the conversation
        if channel not in DB["channels"]:
            return {"ok": False, "error": "channel_not_found"}

        if 'conversations' not in DB["channels"][channel]:
            DB["channels"][channel]['conversations'] = {"members": []}
        elif "members" not in DB["channels"][channel]['conversations']:
            DB["channels"][channel]['conversations']["members"] = []


        if user_id not in DB["channels"][channel]['conversations']["members"]:
            DB["channels"][channel]['conversations']["members"].append(user_id)
            return {"ok": True, "channel": channel}
        else:
            return {"ok": False, "error": "already_in_channel"}

    @staticmethod
    def kick(channel: str, user_id: str) -> dict:
        """Removes a user from a conversation.

        Args:
            channel: ID of conversation to remove user from.
            user_id: ID of user to remove from conversation.

        Returns:
            A dictionary indicating the result of the kick operation.
        """
        if not channel:
            return {"ok": False, "error": "missing_channel"}
        if not user_id:
            return {"ok": False, "error": "missing_user_id"}

        if channel not in DB["channels"]:
            return {"ok": False, "error": "channel_not_found"}

        if 'conversations' not in DB["channels"][channel]:
            DB["channels"][channel]['conversations'] = {}
        if "members" not in DB["channels"][channel]['conversations']:
            DB["channels"][channel]['conversations']["members"] = []
        if user_id not in DB["channels"][channel]['conversations']["members"]:
            return {"ok": False, "error": "user_not_in_channel"}

        DB["channels"][channel]['conversations']["members"].remove(user_id)
        return {"success": True, "message": f"User {user_id} kicked from channel {channel}"}

    @staticmethod
    def mark_read(channel: str, ts: str):
        """
        Sets the read cursor in a channel.

        Args:
            channel (str): Channel or conversation ID.
            ts (str): Timestamp of the message to mark as read.

        Returns:
            dict: A dictionary indicating success or failure.
        """
        if not channel:
            return {"ok": False, "error": "missing_channel"}
        if not ts:
            return {"ok": False, "error": "missing_timestamp"}

        # Simulate setting the read cursor
        if channel not in DB["channels"]:
            return {"ok": False, "error": "channel_not_found"}

        if 'conversations' not in DB["channels"][channel]:
             DB["channels"][channel]['conversations'] = {}

        DB["channels"][channel]['conversations']["read_cursor"] = ts
        return {"ok": True}

    @staticmethod
    def history(channel: str, cursor: str = None, include_all_metadata: bool = False,
                inclusive: bool = False, latest: str = None, limit: int = 100, oldest: str = "0") -> dict:
        """
        Fetches a conversation's history of messages and events.

        Args:

            channel (str): Conversation ID.
            cursor (str, optional): Pagination cursor. Defaults to None.
            include_all_metadata (bool, optional): Return all metadata. Defaults to False.
            inclusive (bool, optional): Include messages with oldest/latest timestamps. Defaults to False.
            latest (str, optional): Only messages before this timestamp. Defaults to None (current time).
            limit (int, optional): Maximum number of items to return. Defaults to 100. Max 999.
            oldest (str, optional): Only messages after this timestamp. Defaults to "0".

        Returns:
            dict: A dictionary containing the conversation history.
        """
        if not channel:
            return {"ok": False,"error": "missing_channel"}

        if channel not in DB["channels"]:
            return {"ok": False,"error": "channel_not_found"}

        if limit > 999:
            limit = 999

        # Simulate fetching history from DB

        if "messages" not in DB["channels"][channel]:
            DB["channels"][channel]["messages"] = []

        history = DB["channels"][channel]["messages"]

        # Filter by timestamp
        if latest is None:
            latest = str(time.time())

        filtered_history = [
            message for message in history
            if float(oldest) <= float(message['ts']) <= float(latest)
        ]
        if inclusive:
             filtered_history = [
                message for message in history
                if float(oldest) <= float(message['ts']) <= float(latest)
            ]
        else:
            filtered_history = [
                message for message in history
                if float(oldest) < float(message['ts']) < float(latest)
            ]

        # Apply limit and cursor
        start_index = 0
        if cursor:
            try:
                start_index = next(i for i,v in enumerate(filtered_history) if v['ts'] == cursor) + 1
            except StopIteration:
                return {"ok":True, "messages": [], "response_metadata": {"next_cursor": None}}

        end_index = min(start_index + limit, len(filtered_history))
        messages = filtered_history[start_index:end_index]

        next_cursor = None
        if end_index < len(filtered_history):
            next_cursor = filtered_history[end_index]['ts']

        response = {
            "ok": True,
            "messages": messages,
            "has_more": end_index < len(filtered_history),
            "response_metadata": {"next_cursor": next_cursor}
        }

        return response

    @staticmethod
    def open_conversation(channel: str = None, prevent_creation: bool = False, return_im: bool = False, users: str = None):
        """
        Opens or resumes a direct message or multi-person direct message.

        Args:
            channel (str, optional): Resume a conversation by supplying an IM or MPIM ID. Defaults to None.
            prevent_creation (bool, optional): Prevents creating a new direct message or multi-person DM. Defaults to False.
            return_im (bool, optional): If True, returns the full IM channel definition in the response. Defaults to False.
            users (str, optional): Comma-separated list of users. Defaults to None.

        Returns:
            dict: A dictionary representing the API response.
        """

        if not channel and not users:
            return {"ok": False, "error": "missing_channel_or_users"}

        if channel and users:
            return {"ok": False, "error": "invalid_arguments", "message": "Provide either 'channel' or 'users', not both."}

        if channel:
            # Resume an existing conversation
            conversation = DB["channels"].get(channel)
            if conversation:
                return {"ok": True, "channel": conversation}
            return {"ok": False, "error": "channel_not_found"}

        if users:
            user_list = sorted(users.split(","))  # Ensure consistent ordering for multi-person DMs
            conversation_id = "C" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

            channel_data = DB["channels"].get(conversation_id, {})

            if "conversations" in channel_data:
                return {"ok": True, "channel": channel_data["conversations"]}

            if prevent_creation:
                return {"ok": False, "error": "conversation_not_found"}

            # Create a new conversation
            new_conversation = {"id": conversation_id, "users": user_list}

            DB["channels"].setdefault(conversation_id, {"conversations": {}, "messages": []})
            DB["channels"][conversation_id]["id"] = conversation_id
            DB["channels"][conversation_id]["name"] = ",".join(user_list)
            DB["channels"][conversation_id]["conversations"] = new_conversation

            return {"ok": True, "channel": new_conversation}

        return {"ok": False, "error": "unknown_error"}

    @staticmethod
    def list_channels(cursor: str = None, exclude_archived: bool = False, limit: int = 100, team_id: str = None, types: str = "public_channel"):
        """
        Lists all channels in a Slack team.

        Args:
            token (str): Authentication token bearing required scopes.
            cursor (str, optional): Paginate through collections of data. Defaults to None.
            exclude_archived (bool, optional): Exclude archived channels. Defaults to False.
            limit (int, optional): The maximum number of items to return. Defaults to 100.
            team_id (str, optional): Encoded team id. Defaults to None.
            types (str, optional): Channel types. Defaults to "public_channel".

        Returns:
            dict: A dictionary representing the API response.
        """

        # Argument validation
        if limit > 1000:
            return {"ok": False, "error": "invalid_limit"}

        valid_types = ["public_channel", "private_channel", "mpim", "im"]
        if types:
            requested_types = [t.strip() for t in types.split(",")]
            for t in requested_types:
                if t not in valid_types:
                    return {"ok": False, "error": "invalid_types"}
        else:
            requested_types = ["public_channel"] # Default

        # Simulate fetching channels from the DB based on parameters
        channels = []
        all_channels = DB.get("channels", {}).values()
        for channel in all_channels:
            # Apply filters based on arguments (exclude_archived, types, team_id)
            if exclude_archived and channel.get("is_archived", False):
                continue

            channel_type = channel.get("type", "public_channel") # Assume public_channel if type is not defined
            if channel_type not in requested_types:
                continue
            if team_id is not None and channel.get("team_id") != team_id:
                continue

            channels.append(channel)

        # Apply limit and cursor for pagination (simplified)
        start_index = 0
        if cursor:
            try:
                start_index = int(cursor)
            except ValueError:
                return {"ok": False, "error": "invalid_cursor"}

        end_index = min(start_index + limit, len(channels))
        channels_page = channels[start_index:end_index]

        next_cursor = str(end_index) if end_index < len(channels) else None

        response = {
            "ok": True,
            "channels": channels_page,
            "response_metadata": {"next_cursor": next_cursor},
        }

        return response

    @staticmethod
    def close(channel: str):
        """
        Closes a direct message or multi-person direct message.

        Args:
            channel (str): Conversation to close.

        Returns:
            dict: A dictionary representing the API response.
        """

        if not channel:
            return {"ok": False, "error": "missing_channel"}

        # Simulate closing the conversation
        if channel in DB.get("channels", {}):
            DB["channels"][channel]["is_open"] = False
            return {"ok": True}
        else:
            return {"ok": False, "error": "channel_not_found"}

    @staticmethod
    def rename(channel: str, name: str):
        """
        Renames a conversation.

        Args:

            channel (str): ID of conversation to rename.
            name (str): New name for conversation.

        Returns:
            dict: A dictionary representing the API response.
        """


        if not channel:
            return {"ok": False, "error": "missing_channel"}

        if channel not in DB["channels"]:
            return {"ok": False, "error": "channel_not_found"}

        for channel_id in DB["channels"]:
            if DB['channels'][channel_id].get("name") == name:
                return {"ok": False, "error": "name_taken"}

        DB["channels"][channel]["name"] = name
        return {"ok": True, "channel": {"id": channel, "name": name}}

    @staticmethod
    def members(channel: str, cursor: str = None, limit: int = 100):
        """
        Retrieve members of a conversation.

        Args:

            channel (str): ID of the conversation.
            cursor (str, optional): Pagination cursor. Defaults to None.limit (int, optional): Maximum number of items to return. Defaults to 100.

        Returns:
            dict: A dictionary containing the members and pagination information.
        """


        if not channel:
            return {"ok": False, "error": "missing_channel"}

        # Simulate retrieving members from the database
        if channel not in DB["channels"]:
            return {"ok": False, "error": "channel_not_found"}

        if 'conversations' not in DB["channels"][channel] or "members" not in DB["channels"][channel]['conversations']:
            DB["channels"][channel].setdefault('conversations', {}).setdefault("members", [])

        members = DB["channels"][channel]['conversations']["members"]

        # Apply pagination
        start_index = 0
        if cursor:
            try:
                start_index = int(cursor)
            except ValueError:
                return {"ok": False, "error": "invalid_cursor"}

        end_index = min(start_index + limit, len(members))
        paged_members = members[start_index:end_index]

        next_cursor = str(end_index) if end_index < len(members) else ""

        return {
            "ok": True,
            "members": paged_members,
            "response_metadata": {"next_cursor": next_cursor},
        }

    @staticmethod
    def create_channel(name: str, is_private: bool = False, team_id: str = None):
        """
        Initiates a public or private channel-based conversation.

        Args:

            name (str): Name of the channel.
            is_private (bool, optional): Create a private channel. Defaults to False.
            team_id (str, optional): Encoded team id. Defaults to None.

        Returns:
            dict: A dictionary representing the API response.
        """

        if not name:
            return {"ok": False, "error": "missing_name"}

        #Check if channel exists with that name
        for channel in DB["channels"]:
            if DB["channels"][channel].get('name') == name:
                return {"ok": False, "error": "name_taken"}

        base_id = base_id = hashlib.sha1(name.encode()).hexdigest()[:8].upper()
        channel_id = f"C{base_id}"

        if channel_id in DB["channels"]:
            # Use a random state based on hash to generate a deterministic suffix
            random.seed(base_id)  # Seeded to ensure repeatability
            suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=2))
            channel_id = f"{channel_id}{suffix}"

        channel = {
            "id": channel_id,
            "name": name,
            "is_private": is_private,
            "team_id": team_id,
            "conversations" : {},
            "messages": []
        }

        DB["channels"][channel_id] = channel

        return {"ok": True, "channel": channel}

    @staticmethod
    def setPurpose(channel: str, purpose: str) -> dict:
        """
        Sets the channel description.

        Args:

            channel (str): Channel to set the description of.
            purpose (str): The description.

        Returns:
            dict: A dictionary representing the API response.
        """


        if not channel:
            return {"ok": False, "error": "missing_channel"}
        if not purpose:
            return {"ok": False, "error": "missing_purpose"}

        if channel not in DB["channels"]:
            return {"ok": False, "error": "channel_not_found"}

        if 'conversations' not in DB['channels'][channel]:
            DB['channels'][channel]['conversations'] = {}
        DB["channels"][channel]['conversations']["purpose"] = purpose
        return {"ok": True,  "purpose": purpose}

    @staticmethod
    def setConversationTopic(channel: str, topic: str) -> dict:
        """
        Sets the topic for a conversation.

        Args:

            channel (str): Conversation to set the topic of.
            topic (str): The new topic string.

        Returns:
            dict: A dictionary representing the API response.
        """

        if not channel:
            return {"ok": False, "error": "missing_channel"}
        if not topic:
            return {"ok": False, "error": "missing_topic"}

        # Simulate setting the topic in the database
        if channel not in DB["channels"]:
            return {"ok": False, "error": "channel_not_found"}

        if 'conversations' not in DB['channels'][channel]:
             DB['channels'][channel]['conversations'] = {}

        DB['channels'][channel]['conversations']['topic'] = topic

        return {"ok": True, "topic": topic}

    @staticmethod
    def replies(channel: str, ts: str, cursor: str = None, include_all_metadata: bool = False,
                inclusive: bool = False, latest: str = None, limit: int = 1000, oldest: str = "0") -> dict:
        """
        Retrieve a thread of messages posted to a conversation.

        Args:

            channel (str): Conversation ID.
            ts (str): Timestamp of the parent message or a message in the thread.
            cursor (str, optional): Pagination cursor. Defaults to None.
            include_all_metadata (bool, optional): Return all metadata. Defaults to False.
            inclusive (bool, optional): Include messages with oldest/latest timestamps. Defaults to False.
            latest (str, optional): Only messages before this timestamp. Defaults to None.
            limit (int, optional): Maximum number of items to return. Defaults to 1000.
            oldest (str, optional): Only messages after this timestamp. Defaults to "0".

        Returns:
            dict: A dictionary containing the API response.
        """

        # Simulate API behavior
        if not channel or not ts:
            return {"ok": False, "error": "missing_required_arguments"}

        if channel not in DB["channels"]:
             return {"ok": False, "error": "channel_not_found"}

        # Simulate fetching replies from the DB based on channel and ts
        if "messages" not in DB["channels"][channel]:
            return {"ok": True, "messages": [], "has_more": False}

        parent_message = None
        for msg in DB["channels"][channel]["messages"]:
            if msg["ts"] == ts:
                parent_message = msg
                break
        if not parent_message:
            return {"ok":False, "error": "thread_not_found"}

        if "replies" not in parent_message:
            replies = []
        else:
            replies = parent_message["replies"]

        #Apply TimeStamp Filtering
        if latest is None:
            latest = str(time.time())

        filtered_replies = [
            message for message in replies
            if float(oldest) <= float(message['ts']) <= float(latest)
        ]

        if inclusive:
            filtered_replies = [
            message for message in replies
            if float(oldest) <= float(message['ts']) <= float(latest)
        ]

        else:
            filtered_replies = [
            message for message in replies
            if float(oldest) < float(message['ts']) < float(latest)
        ]

        # Apply limit and cursor
        start_index = 0
        if cursor:
            try:
                start_index = next(i for i,v in enumerate(filtered_replies) if v['ts'] == cursor) + 1
            except StopIteration:
                return {"ok":True, "messages": [], "has_more": False, "response_metadata":{"next_cursor":""}}
        end_index = min(start_index + limit, len(filtered_replies))
        messages = filtered_replies[start_index:end_index]

        next_cursor = ""

        if end_index < len(filtered_replies):
            next_cursor = filtered_replies[end_index]['ts']

        response = {
            "ok": True,
            "messages": messages,
            "has_more":  end_index < len(filtered_replies),
            "response_metadata":{"next_cursor": next_cursor}
        }
        return response
# ---------------------------------------------------------------------------------------
# Files Classes & Methods
# ---------------------------------------------------------------------------------------

class Files:
    """
    Manages file-related operations within the Slack-like application.
    """

    @staticmethod
    def get_file_info(file_id: str, cursor: str = None, limit: int = 100):
        """
        Gets information about a file, including comments.

        Args:

            file_id (str): The ID of the file.
            cursor (str, optional): Pagination cursor. Defaults to None.
            limit (int, optional): Maximum number of items to return. Defaults to 100.

        Returns:
            dict: A dictionary representing the API response.
        """

        if not file_id:
            return {"ok": False, "error": "missing_file_id"}

        if file_id not in DB.get("files", {}):
            return {"ok": False, "error": "file_not_found"}

        file_data = DB["files"][file_id]

        # Simulate pagination for comments
        comments = file_data.get("comments", [])
        start_index = 0
        if cursor:
            try:
                start_index = int(cursor)
            except ValueError:
                return {"ok": False, "error": "invalid_cursor"}

        end_index = min(start_index + limit, len(comments))
        paginated_comments = comments[start_index:end_index]

        next_cursor = str(end_index) if end_index < len(comments) else None

        #  Construct the 'channels' list based on channel IDs
        channel_ids = []
        for channel_id in DB["channels"]:
            if "files" in DB["channels"][channel_id] and file_id in DB["channels"][channel_id]["files"]:
                channel_ids.append(channel_id)

        response = {
            "ok": True,
            "file": {
                "id": file_data["id"],
                "name": file_data.get("filename"),
                "title": file_data.get("title"),
                "filetype": file_data.get("filetype"),
                "channels": channel_ids,  #  List of channel IDs where the file is shared
                "comments": paginated_comments,
            },
            "response_metadata": {"next_cursor": next_cursor}
        }
        return response

    @staticmethod
    def share_file(file_id: str, channel_ids: str):
        """
        Shares an existing file into specified channels.

        Args:

            file_id (str): The ID of the file to share.
            channel_ids (str): Comma-separated list of channel IDs.

        Returns:
            dict: A dictionary representing the API response.
        """


        if not file_id:
            return {"ok": False, "error": "missing_file_id"}
        if not channel_ids:
            return {"ok": False, "error": "missing_channel_ids"}

        if file_id not in DB.get("files", {}):
            return {"ok": False, "error": "file_not_found"}

        channel_id_list = channel_ids.split(",")
        for channel_id in channel_id_list:
            if channel_id not in DB["channels"]:
                return {"ok": False, "error": "invalid_channel_id", "channel_id": channel_id}

        # Add file_id to each channel's files (using a dictionary for efficiency)
        for channel_id in channel_id_list:
            if "files" not in DB["channels"][channel_id]:
                DB["channels"][channel_id]["files"] = {}  # Use a dictionary
            DB["channels"][channel_id]["files"][file_id] = True  # Add the file ID

        return {"ok": True, "file_id": file_id, "shared_to_channels": channel_id_list}

    @staticmethod
    def add_remote_file(external_id: str, external_url: str, title: str, filetype: str = None, indexable_file_contents: str = None):
        """
        Adds a file from a remote service.

        Args:

            external_id (str): Creator defined GUID for the file.
            external_url (str): URL of the remote file.
            title (str): Title of the file being shared.
            filetype (str, optional): Type of file. Defaults to None.
            indexable_file_contents (str, optional):  Content for search. Defaults to None.

        Returns:
            dict: A dictionary representing the result of the add operation.
        """


        if not external_id:
            return {"ok": False, "error": "missing_external_id"}
        if not external_url:
            return {"ok": False, "error": "missing_external_url"}
        if not title:
            return {"ok": False, "error": "missing_title"}

        file_id = str(uuid.uuid4())  # Generate unique file ID

        new_file = {
            "id": file_id,
            "external_id": external_id,
            "external_url": external_url,
            "title": title,
            "filetype": filetype,
            "indexable_file_contents": indexable_file_contents,
            "comments": []  # Initialize comments
            # Add other relevant fields as needed
        }

        if 'files' not in DB:
            DB['files'] = {}  # Use a dictionary for files, keyed by file_id
        DB['files'][file_id] = new_file

        return {"ok": True, "file_id": file_id}

    @staticmethod
    def delete_file(file_id: str) -> dict:
        """
        Deletes a file.

        Args:

            file_id (str): ID of file to delete.

        Returns:
            dict: A dictionary representing the API response.
        """


        if not file_id:
            return {"ok": False, "error": "missing_file_id"}

        if file_id not in DB.get("files", {}):
            return {"ok": False, "error": "file_not_found"}

        # Remove from main files dictionary
        del DB["files"][file_id]

        # Remove file_id from all channels
        for channel_id in DB["channels"]:
            if "files" in DB["channels"][channel_id] and file_id in DB["channels"][channel_id]["files"]:
                del DB["channels"][channel_id]["files"][file_id]

        return {"ok": True}

    @staticmethod
    def upload_file(channels: str = None, content: str = None, file_path=None, filename: str = None,
               filetype: str = None, initial_comment: str = None, thread_ts: str = None, title: str = None):
        """
        Uploads or creates a file.

        Args:

            channels (str, optional): Comma-separated list of channel IDs.
            content (str, optional): File contents (string).
            file_path (str, optional): Path to a local file.
            filename (str, optional): Filename.  Required if file_path is used.
            filetype (str, optional): A file type identifier.
            initial_comment (str, optional): Initial comment.
            thread_ts (str, optional): Parent message timestamp for threading.
            title (str, optional): Title of the file.

        Returns:
            dict: A dictionary representing the API response.
        """

        if not content and not file_path:
            return {"ok": False, "error": "missing_content_or_file"}

        if file_path and not filename:
            return {"ok": False, "error": "missing_filename"}

        if channels:
            channel_list = channels.split(",")
            for channel in channel_list:
                if channel not in DB["channels"]:
                    return {"ok": False, "error": "invalid_channel", "channel": channel}

        # Simulate content if file_path is provided.
        if file_path:
            content = "Simulated file content"

        file_id = str(uuid.uuid4())  # Use UUID
        file_data = {
            "id": file_id,
            "filename": filename or "untitled",
            "filetype": filetype,
            "title": title,
            "initial_comment": initial_comment,
            "thread_ts": thread_ts,
            "content": content,
            "comments": []
        }

        if "files" not in DB:
            DB["files"] = {}
        DB["files"][file_id] = file_data

        # Associate the file with channels during upload
        if channels:
            for channel_id in channels.split(","):
                if "files" not in DB["channels"][channel_id]:
                    DB["channels"][channel_id]["files"] = {}
                DB["channels"][channel_id]["files"][file_id] = True

        return {"ok": True, "file": file_data}


    @staticmethod
    def finish_external_upload(files: list, channel_id: str = None, initial_comment: str = None, thread_ts: str = None):
        """
        Finishes an external file upload.

        Args:

            files (list): List of file information (id, title, etc.).
            channel_id (str, optional): Channel ID where the file will be shared.
            initial_comment (str, optional): Initial comment for the file.
            thread_ts (str, optional): Parent message timestamp for threading.

        Returns:
            dict: A dictionary representing the API response.
        """

        if not files:
            return {"ok": False, "error": "missing_files"}

        if channel_id and channel_id not in DB["channels"]:
             return {"ok":False, "error": "invalid_channel"}


        for file_info in files:
            file_id = file_info.get("id")
            if not file_id:
                return {"ok": False, "error": "missing_file_id", "missing_id_in_file": file_info}

            #Check If File Exists:
            if "files" not in DB or file_id not in DB.get("files",{}):
                return {"ok":False, "error": "file_not_found", "file_id": file_id}

            #Update Existing File
            DB["files"][file_id].update({
                "title": file_info.get("title"),
                "initial_comment": initial_comment,
                "thread_ts": thread_ts,
            })

            # Associate with channel if provided
            if channel_id:
                if "files" not in DB["channels"][channel_id]:
                    DB["channels"][channel_id]["files"] = {}
                DB["channels"][channel_id]["files"][file_id] = True

        return {"ok": True}

    @staticmethod
    def list_files(channel_id: str = None, user_id: str = None, ts_from: str = None, ts_to: str = None, types: str = None, cursor: str = None, limit: int = 100):
        """
        Lists files, optionally filtered by channel, user, and time.

        Args:
            channel_id (str, optional): Filter files in a specific channel.
            user_id (str, optional): Filter files by a specific user.
            ts_from (str, optional): Filter files created after this timestamp.
            ts_to (str, optional): Filter files created before this timestamp.
            types (str, optional): Comma-separated list of file types.
            cursor (str, optional): Pagination cursor.
            limit (int, optional): Maximum number of items per page.

        Returns:
            dict: A dictionary containing the list of files and pagination metadata.
        """

        if channel_id:
            if channel_id not in DB["channels"]:
                return {"ok": False, "error": "channel_not_found"}

            # Get file IDs for the specified channel
            channel_files = DB["channels"][channel_id].get("files", {})
            file_ids = list(channel_files.keys())  # Get file ids that belong to channel.

            # Retrieve file details from the main files dictionary using the obtained IDs
            filtered_files = [DB["files"][file_id] for file_id in file_ids if file_id in DB["files"]]
        else:
            # Get all Files if no channel is provided
            filtered_files = list(DB.get("files", {}).values())

        # Apply filters, if no channel filter
        if not channel_id:
            if user_id:
                filtered_files = [f for f in filtered_files if f.get("user_id") == user_id]
            if ts_from:
                filtered_files = [f for f in filtered_files if f.get("created", "") >= ts_from]
            if ts_to:
                filtered_files = [f for f in filtered_files if f.get("created", "") <= ts_to]
            if types:
                types_list = types.split(",")
                filtered_files = [f for f in filtered_files if f.get("filetype") in types_list]

        # Pagination
        start_index = 0
        if cursor:
            try:
                start_index = int(cursor)
            except ValueError:
                return {"ok": False, "error": "invalid_cursor"}

        end_index = min(start_index + limit, len(filtered_files))
        paginated_files = filtered_files[start_index:end_index]

        next_cursor = str(end_index) if end_index < len(filtered_files) else None

        return {
            "ok": True,
            "files": paginated_files,
            "response_metadata": {"next_cursor": next_cursor}
        }


    @staticmethod
    def remove_remote_file(file_id: str = None, external_id: str = None):
        """
        Removes a remote file.  Handles both file ID and external ID.

        Args:

            file_id (str, optional): The ID of the file to remove.
            external_id (str, optional): The external ID of the file to remove.

        Returns:
            dict: A dictionary representing the API response.
        """

        if not file_id and not external_id:
            return {"ok": False, "error": "missing_file_id_or_external_id"}

        file_to_remove = None

        if file_id:
            if file_id not in DB.get("files", {}):
                return {"ok": False, "error": "file_not_found"}
            file_to_remove = file_id

        elif external_id:
             # Find the file with the given external_id.
            for file_key, file_data in DB.get("files", {}).items():
                if file_data.get("external_id") == external_id:
                    file_to_remove = file_key
                    break #Exit the loop once found.
            if file_to_remove is None:
                return {"ok": False, "error": "file_not_found"}

        # Remove from main files dictionary
        del DB["files"][file_to_remove]

        # Remove file_id from all channels
        for channel_id in DB["channels"]:
            if "files" in DB["channels"][channel_id] and file_to_remove in DB["channels"][channel_id]["files"]:
                del DB["channels"][channel_id]["files"][file_to_remove]

        return {"ok": True}

    @staticmethod
    def get_external_upload_url(filename: str, length: int, alt_txt: str = None, snippet_type: str = None):
        """
        Gets a URL for an external file upload.

        Args:

            filename (str): Name of the file.
            length (int): Size of the file in bytes.
            alt_txt (str, optional): Alt text for screen readers.
            snippet_type (str, optional): snippet_type (str, optional): Snippet type.

        Returns:
            dict: A dictionary with the upload URL and file ID.
        """


        if not filename:
            return {"ok": False, "error": "missing_filename"}
        if not isinstance(length, int) or length <= 0:
            return {"ok": False, "error": "invalid_length"}

        file_id = str(uuid.uuid4())  # Generate unique file ID

        # In a real scenario, you might store pending uploads.
        # For simplicity, were not persisting this.

        upload_url = f"https://example.com/upload/{file_id}"  # Mock URL

        return {"ok": True, "upload_url": upload_url, "file_id": file_id}
# ---------------------------------------------------------------------------------------
# Reactions Classes & Methods
# ---------------------------------------------------------------------------------------

class Reactions:
    """
    Simulates the Reactions API.  Manages reactions on messages within channels.
    """

    @staticmethod
    def get(channel_id: str, message_ts: str, full: bool = False):
        """
        Gets reactions for a specific message in a channel.

        Args:

            channel_id (str): ID of the channel.
            message_ts (str): Timestamp of the message.
            full (bool, optional): If true, return all reaction details. Defaults to False.

        Returns:
            dict: A dictionary containing the reactions.
        """

        if not channel_id:
            return {"ok": False, "error": "missing_channel_id"}
        if not message_ts:
            return {"ok": False, "error": "missing_message_ts"}

        if channel_id not in DB["channels"]:
            return {"ok": False, "error": "channel_not_found"}

        messages = DB["channels"][channel_id].get("messages", [])
        message = None
        for msg in messages:
            if str(msg["ts"]) == str(message_ts):
                message = msg
                break

        if not message:
            return {"ok": False, "error": "message_not_found"}

        reactions = message.get("reactions", [])

        if full:
            return {"ok": True, "reactions": reactions}
        else:
            #  Return a summarized view (e.g., counts)
            summary = {}
            for reaction in reactions:
                name = reaction["name"]
                if name in summary:
                    summary[name] += 1
                else:
                    summary[name] = 1
            return {"ok": True, "reactions": summary}

    @staticmethod
    def add(user_id: str, channel_id: str, name: str, message_ts: str) -> dict:
        """
        Adds a reaction to a message.

        Args:
            user_id (str): User ID.
            channel_id (str): ID of the channel.
            name (str): Reaction (emoji) name.
            message_ts (str): Timestamp of the message.

        Returns:
            dict: A dictionary representing the API response.
        """
        if not all([user_id, channel_id, name, message_ts]):
            return {"ok": False, "error": "missing_required_arguments"}

        if channel_id not in DB["channels"]:
            return {"ok": False, "error": "channel_not_found"}

        messages = DB["channels"][channel_id].get("messages", [])
        message = next((msg for msg in messages if msg["ts"] == message_ts), None)

        if not message:
            return {"ok": False, "error": "message_not_found"}

        if "reactions" not in message:
            message["reactions"] = []

        # Check if the user already reacted with this emoji
        for reaction in message["reactions"]:
            if reaction["name"] == name and user_id in reaction["users"]:
                return {"ok": False, "error": "already_reacted"}

        # Add the reaction (or update existing)
        found = False
        for reaction in message["reactions"]:
            if reaction["name"] == name:
                reaction["users"].append(user_id)
                reaction["count"] += 1
                found = True
                break

        if not found:
            message["reactions"].append({
                "name": name,
                "users": [user_id],
                "count": 1
            })

        # Update the DB
        for i, msg in enumerate(DB["channels"][channel_id]["messages"]):
            if msg["ts"] == message_ts:
                DB["channels"][channel_id]["messages"][i] = message
                break

        return {"ok": True, "message": DB["channels"][channel_id]["messages"][i]}


    @staticmethod
    def list(user_id: str = None, full: bool = False, cursor: str = None, limit: int = 100):
        """
        Lists reactions made by a user (or all users if user_id is None).

        Args:

            user_id (str, optional): Show reactions made by this user. Defaults to None (all users).
            full (bool, optional): If true, return all reaction details. Defaults to False.
            cursor (str, optional): Parameter for pagination. Defaults to None.
            limit (int, optional): The maximum number of items to return. Defaults to 100.

        Returns:
            dict: A dictionary containing the list of reactions and pagination metadata.
        """

        all_reactions = []
        for channel_id, channel_data in DB["channels"].items():
            for message in channel_data.get("messages", []):
                for reaction in message.get("reactions", []):
                    if user_id is None or (user_id in reaction["users"]):
                        reaction_info = {
                            "channel": channel_id,
                            "message_ts": message["ts"],
                            "name": reaction["name"],
                            "count": reaction["count"],
                            "users": reaction["users"] if full else None, #Only include users if full is True.
                        }
                        all_reactions.append(reaction_info)

        # Pagination
        start_index = 0
        if cursor:
            try:
                start_index = int(cursor)
            except ValueError:
                return {"ok": False, "error": "invalid_cursor"}

        end_index = min(start_index + limit, len(all_reactions))
        paginated_reactions = all_reactions[start_index:end_index]

        next_cursor = str(end_index) if end_index < len(all_reactions) else None

        return {
            "ok": True,
            "reactions": paginated_reactions,
            "response_metadata": {"next_cursor": next_cursor}
        }

    @staticmethod
    def remove(user_id: str, name: str, channel_id: str, message_ts: str) -> dict:
        """
        Removes a reaction from a message.

        Args:
            user_id (str): User ID.
            name (str): Reaction (emoji) name.
            channel_id (str): ID of the channel.
            message_ts (str): Timestamp of the message.

        Returns:
            dict: A dictionary representing the API response.
        """
        if not all([user_id, name, channel_id, message_ts]):
            return {"ok": False, "error": "missing_required_arguments"}

        if channel_id not in DB["channels"]:
            return {"ok": False, "error": "channel_not_found"}

        messages = DB["channels"][channel_id].get("messages", [])
        message = next((msg for msg in messages if msg["ts"] == message_ts), None)

        if not message:
            return {"ok": False, "error": "message_not_found"}

        if "reactions" not in message:
            return {"ok": False, "error": "no_reactions_on_message"}

        reactions = message.get("reactions", [])
        reaction_index = next((i for i, r in enumerate(reactions) if r["name"] == name), None)

        if reaction_index is None:
            return {"ok": False, "error": "reaction_not_found"}

        if user_id not in reactions[reaction_index]["users"]:
            return {"ok": False, "error": "user_has_not_reacted"}

        # Remove the user from the reaction
        reactions[reaction_index]["users"].remove(user_id)
        reactions[reaction_index]["count"] -= 1

        #Update the message
        message["reactions"] = reactions

        # If no users are left, remove the entire reaction
        if reactions[reaction_index]["count"] == 0:
            del message["reactions"][reaction_index]

        # Update the DB
        for i, msg in enumerate(DB["channels"][channel_id]["messages"]):
            if msg["ts"] == message_ts:
                DB["channels"][channel_id]["messages"][i] = message
                break

        return {"ok": True}
# ---------------------------------------------------------------------------------------
# Reminders Classes & Methods
# ---------------------------------------------------------------------------------------


class Reminders:
    """
    Simulates the /reminders API resource.  Manages reminders for users.
    """

    @staticmethod
    def delete(reminder_id: str) -> dict:
        """
        Deletes a reminder.

        Args:
            user_id (str): User ID.
            reminder_id (str): The ID of the reminder.

        Returns:
            dict: A dictionary representing the API response.
        """

        if not reminder_id:
            return {"ok": False, "error": "missing_reminder_id"}


        if reminder_id not in DB.get("reminders", {}):
            return {"ok": False, "error": "reminder_not_found"}

        del DB["reminders"][reminder_id]
        return {"ok": True}

    @staticmethod
    def info(reminder_id: str) -> dict:
        """
        Gets information about a reminder.

        Args:

            reminder_id (str): The ID of the reminder.

        Returns:
            dict: A dictionary containing information about the reminder.
        """

        if not reminder_id:
            return {"ok": False, "error": "missing_reminder_id"}

        reminder_data = DB.get("reminders", {}).get(reminder_id)

        if not reminder_data:
            return {"ok": False, "error": "reminder_not_found"}

        return {"ok": True, "reminder": reminder_data}

    @staticmethod
    def complete(reminder_id: str, complete_ts: str) -> dict:
        """
        Marks a reminder as complete.

        Args:

            reminder_id (str): The ID of the reminder.
            complete_ts (str): Timestamp for when it was completed.

        Returns:
            dict: A dictionary representing the API response.
        """


        if not reminder_id:
            return {"ok": False, "error": "missing_reminder_id"}
        if not complete_ts:
            return {"ok": False, "error": "missing_complete_ts"}

        try:
            int(float(complete_ts))
        except ValueError:
            return {"ok": False, "error": 'invalid_complete_ts'}

        if reminder_id not in DB.get("reminders", {}):
            return {"ok": False, "error": "reminder_not_found"}

        if DB["reminders"][reminder_id]["complete_ts"] is not None:
            return {"ok": False, "error": "already_complete"}

        DB["reminders"][reminder_id]["complete_ts"] = complete_ts
        return {"ok": True}

    @staticmethod
    def list_reminders(user_id: str) -> dict:
        """
        Lists all reminders created by or for a given user.

        Args:
            user_id (str): User ID.

        Returns:
            dict: A dictionary containing the list of reminders.
        """

        if not user_id:
            return {"ok": False, "error": "missing_user_id"}

        if user_id not in DB["users"]:
            return {"ok": False, "error": "user_not_found"}

        reminders = []
        for reminder_id, reminder_data in DB.get("reminders", {}).items():
            if reminder_data.get("creator_id", user_id) == user_id:
                reminders.append(reminder_data)

        return {"ok": True, "reminders": reminders}

    @staticmethod
    def add(user_id: str, text: str, ts: str, channel_id:str = None) -> dict:
        """
        Creates a reminder.

        Args:
            user_id (str, optional):  User ID to remind.
            text (str): The content of the reminder.
            ts (str):  When this reminder should happen (unix timestamp).
            channel_id (str, optional): Channel ID to remind in.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        if not all([user_id, text, ts]):
            return {"ok": False, "error": "missing_required_arguments"}

        if user_id not in DB["users"]:
            return {"ok": False, "error": "user_not_found"}
        try:
            int(float(ts))
        except ValueError:
            return {"ok": False, "error": "invalid_time"}

        reminder_id = str(uuid.uuid4())
        reminder = {
            "id": reminder_id,
            "creator_id": user_id,
            "user_id": user_id,  # Remind the specified user, or the creator
            "text": text,
            "time": ts,
            "complete_ts": None,  # Null initially, set when completed
            "channel_id": channel_id,
        }

        if "reminders" not in DB:
            DB["reminders"] = {}
        DB["reminders"][reminder_id] = reminder

        return {"ok": True, "reminder": reminder}
# ---------------------------------------------------------------------------------------
# Users Classes & Methods
# ---------------------------------------------------------------------------------------


class Users:
    """
    Represents the /users resource.
    """
    @staticmethod
    def conversations(user_id: str, cursor: str = None, exclude_archived: bool = False, limit: int = 100, types: str = None) -> dict:
        """
        Lists conversations the specified user may access.

        Args:
            user_id (str): The ID of the user whose conversations to list.
            cursor (str, optional): Paginate through collections of data by setting the cursor parameter to the next_cursor attribute returned by a previous request's response. Default value fetches the first page.
            exclude_archived (bool, optional): Set to true to exclude archived channels from the list.
            limit (int, optional): The maximum number of items to return. Fewer than the requested number of items may be returned, even if the end of the list hasn't been reached. Must be an integer no larger than 1000. Default is 100.
            types (str, optional): Mix and match channel types by providing a comma-separated list of any combination of public_channel, private_channel, mpim, im.

        Returns:
            dict: A dictionary representing the result of the conversations operation.
        """
        if "channels" not in DB:
            DB["channels"] = {}
        if "users" not in DB:
            DB["users"] = {}

        conversations = []
        all_channels = list(DB["channels"].values())

        if types:
            allowed_types = types.split(",")
        else:
            allowed_types = ["public_channel", "private_channel", "mpim", "im"]

        filtered_channels = []
        for channel in all_channels:
            if channel.get("type") in allowed_types:
                if exclude_archived and channel.get("is_archived"):
                    continue
                if user_id not in channel.get("conversation", {}).get("members", []):
                    continue
                filtered_channels.append(channel)

        start = 0
        if cursor:
            try:
                start = int(cursor)
            except ValueError:
                return {"ok": False, "error": "invalid_cursor"}

        end = min(start + limit, len(filtered_channels))
        conversations = filtered_channels[start:end]

        next_cursor = str(end) if end < len(filtered_channels) else None

        return {"ok": True, "channels": conversations, "next_cursor": next_cursor}

    @staticmethod
    def setPresence(user_id: str, presence: str) -> dict:
        """
        Manually sets user presence.

        Args:
            user_id (str): User ID.
            presence (str): Either 'active' or 'away'.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        if not user_id:
            return {"ok": False, "error": "missing_user_id"}

        if not presence or presence not in ("active" "away"):
            return {"ok": False, "error": "invalid_presence"}

        if user_id not in DB["users"]:
            return {"ok": False, "error": "user_not_found"}

        DB["users"][user_id]["presence"] = presence
        return {"ok": True}

    @staticmethod
    def setPhoto(user_id: str, image: str, crop_x: int = None, crop_y: int = None, crop_w: int = None) -> dict:
        """
        Sets the user's profile image.

        Args:
            user_id (str): User ID.
            image (str): Base64 encoded image data.
            crop_x (int, optional): X coordinate of top-left corner of crop box.
            crop_y (int, optional): Y coordinate of top-left corner of crop box.
            crop_w (int, optional): Width/height of crop box.

        Returns:
            dict: A dictionary representing the API response.
        """
        if not user_id:
            return {"ok": False, "error": "missing_user_id"}

        if not image:
            return {"ok": False, "error": "missing_image"}

        if user_id not in DB["users"]:
            return {"ok": False, "error": "user_not_found"}

        if "profile" not in DB["users"][user_id]:
            DB["users"][user_id]["profile"] = {}


        # Basic validation of crop parameters (optional, but good practice)
        if any(arg is not None and not isinstance(arg, int) for arg in [crop_x, crop_y, crop_w]):
            return {"ok": False, "error": "invalid_crop_params"}
        if any(arg is not None and arg < 0 for arg in [crop_x, crop_y, crop_w]):
            return {"ok": False, "error": "invalid_crop_params"}

        DB["users"][user_id]["profile"]["image"] = image #Store the image
        #Optionally store crop data
        if crop_x is not None and crop_y is not None and crop_w is not None:
             DB["users"][user_id]["profile"]["image_crop_x"] = crop_x
             DB["users"][user_id]["profile"]["image_crop_y"] = crop_y
             DB["users"][user_id]["profile"]["image_crop_w"] = crop_w

        return {"ok": True}

    @staticmethod
    def deletePhoto(user_id: str) -> dict:
        """
        Deletes the user's profile photo.

        Args:
            user_id (str): User ID.

        Returns:
            A dictionary representing the API response.
        """
        if not user_id:
            return {"ok": False, "error": "missing_user_id"}

        if user_id not in DB["users"] or "image" not in DB["users"][user_id]["profile"]:
            return {"ok": False, "error": "no_photo_to_delete"}

        del DB["users"][user_id]["profile"]["image"]

        #Remove crop info if it exists.
        if "image_crop_x" in DB["users"][user_id]["profile"]:
             del DB["users"][user_id]["profile"]["image_crop_x"]
        if "image_crop_y" in DB["users"][user_id]["profile"]:
             del DB["users"][user_id]["profile"]["image_crop_y"]
        if "image_crop_w" in DB["users"][user_id]["profile"]:
             del DB["users"][user_id]["profile"]["image_crop_w"]
        return {"ok": True}

    @staticmethod
    def info(user_id: str, include_locale: bool = False) -> dict:
        """
        Gets information about a user.

        Args:
            user_id (str): User ID to get info on.
            include_locale (bool, optional): Whether to include locale. Defaults to False.

        Returns:
            dict: User information.
        """

        if not user_id or not isinstance(user_id, str):
            return {"ok": False, "error": "invalid_user_id"}

        user_data = DB.get("users", {}).get(user_id)
        if not user_data:
            return {"ok": False, "error": "user_not_found"}

        result = {"ok": True, "user": user_data}
        if include_locale:
            result["user"]["locale"] = "en-US"  # Example. Could get from user data if stored.
        return result

    @staticmethod
    def getPresence(user_id: str = None) -> dict:
        """
        Gets user presence information.

        Args:
            user_id (str, optional): User ID to get presence info on. Defaults to the authed user.

        Returns:
            dict: A dictionary containing presence information.
        """

        if not user_id:
            return {"ok": False, "error": "invalid_user_id"}

        if user_id not in DB["users"]:
            return {"ok": False, "error": "user_not_found"}

        #Return the user's presence, or offline if it's not been set.
        presence = DB["users"][user_id].get("presence", "away")
        return {"ok": True, "presence": presence}

    @staticmethod
    def set_user_profile(profile: dict, user_id: str) -> dict:
        """
        Set a user's profile information.

        Args:
            profile (dict): Dictionary of profile fields to set.
            user_id (str, optional): ID of user to change. Defaults to the authenticated user.

        Returns:
            dict: A dictionary representing the API response.
        """

        if not profile or not isinstance(profile, dict):
            return {"ok": False, "error": "invalid_profile"}

        if not user_id:
            return {"ok": False, "error": "invalid_user_id"}

        if user_id not in DB["users"]:
            return {"ok": False, "error": "user_not_found"}

        if "profile" not in DB["users"].get(user_id, {}):
            DB["users"][user_id]["profile"] = {}

        #Set all fields from input
        for key, value in profile.items():
            DB["users"][user_id]["profile"][key] = value

        return {"ok": True, "profile": DB["users"][user_id]["profile"]}

    @staticmethod
    def list(cursor: str = None, include_locale: bool = False, limit: int = 100, team_id: str = None) -> dict:
        """
        Lists all users in a Slack team.

        Args:
            cursor (str, optional): Pagination cursor.
            include_locale (bool, optional): Include locale information.
            limit (int, optional): Maximum number of items to return.
            team_id (str, optional):  Team ID to filter users by.

        Returns:
            dict: A dictionary containing the list of users and pagination metadata.
        """

        # Filter users by team_id, if provided.
        if team_id:
            filtered_users = [user for user_id, user in DB.get("users", {}).items() if user.get("team_id") == team_id]
        else:
            filtered_users = list(DB.get("users", {}).values())

        # Pagination
        start_index = 0
        if cursor:
            try:
                start_index = int(cursor)
            except ValueError:
                return {"ok": False, "error": "invalid_cursor"}

        end_index = min(start_index + limit, len(filtered_users))
        paginated_users = filtered_users[start_index:end_index]

        # Include locale if requested.
        if include_locale:
            for user in paginated_users:
                user["locale"] = "en-US" # Example - would get from user data if available

        next_cursor = str(end_index) if end_index < len(filtered_users) else None

        return {
            "ok": True,
            "members": paginated_users,  # Use 'members' to match Slack API
            "response_metadata": {"next_cursor": next_cursor},
        }

    @staticmethod
    def identity(user_id: str) -> dict:
        """
        Get a user's identity.

        Args:
            user_id (str): User ID.

        Returns:
            A dictionary containing the user's identity information.
        """
        if not user_id:
            return {"ok": False, "error": "missing_user_id"}

        if user_id not in DB["users"]:
            return {"ok": False, "error": "user_not_found"}

        user_data = DB["users"][user_id]
        identity_data = {
            "ok": True,
            "user": {
                "name": user_data["name"],
                "id": user_data["id"],
            },
            "team": {
                 "id": user_data["team_id"]
            }

        }
        return identity_data

    @staticmethod
    def lookupByEmail(email: str) -> dict:
        """
        Find a user with an email address.

        Args:
            email (str): An email address belonging to a user.

        Returns:
            dict: User data if found, or an error message.
        """
        if not email:
            return {"ok": False, "error": "invalid_email"}

        for user_id, user_data in DB.get("users", {}).items():
            if user_data.get("profile", {}).get("email") == email:
                return {"ok": True, "user": user_data}

        return {"ok": False, "error": "users_not_found"}

# ---------------------------------------------------------------------------------------
# Usergroups Classes & Methods
# ---------------------------------------------------------------------------------------
class Usergroups:
    """
    Manages user groups within a Slack-like application.
    """

    @staticmethod
    def create(name: str, handle: str = None, team_id: str = None, description: str = None, channel_ids: list[str] = None, created_at: str = str(time.time()),) -> dict:
        """
        Creates a new User Group.

        Args:
            name (str): Name of the User Group.
            created_at (str): Timestamp when the User Group was created.
            handle (str, optional): A mention handle for the User Group.
            team_id (str, optional): ID of the team the User Group belongs to.
            description (str, optional): Description of the User Group.
            channel_ids (list[str], optional): List of channel IDs to include in the User Group.

        Returns:
            dict: A dictionary representing the created User Group, or an error.
        """

        if not name:
            return {"ok": False, "error": "invalid_name"}

        if channel_ids:
            for channel_id in channel_ids:
                if channel_id not in DB["channels"]:
                    return {"ok": False, "error": "invalid_channel_id", "channel_id": channel_id}

        # Check for duplicate usergroup name (case-insensitive)
        for usergroup_id, usergroup_data in DB.get("usergroups", {}).items():
            if usergroup_data["name"].lower() == name.lower():
                return {"ok": False, "error": "name_already_exists"}
          # Check for duplicate usergroup handle (case-insensitive)
            if handle:
                if usergroup_data["handle"] and usergroup_data['handle'].lower() == handle.lower():
                    return {"ok": False, "error": "handle_already_exists"}

        usergroup_id = str(uuid.uuid4())
        new_usergroup = {
            "id": usergroup_id,
            "team_id": team_id,
            "is_usergroup": True,
            "name": name,
            "handle": handle,
            "description": description,
            "date_create": created_at,  #  Use a constant, or pass as argument.
            "date_update": "",
            "date_delete": 0,
            "auto_type": None,
            "created_by": "",
            "updated_by": "",
            "deleted_by": None,
            "prefs": {
                "channels": channel_ids or [],  # Store channel IDs
                "groups": []
            },
            "users": [],  # Initially empty
            "user_count": 0,
            "disabled": False,
        }

        if "usergroups" not in DB:
            DB["usergroups"] = {}
        DB["usergroups"][usergroup_id] = new_usergroup

        return {"ok": True, "usergroup": new_usergroup}

    @staticmethod
    def list(team_id = None, include_disabled: bool = False, include_count: bool = False, include_users: bool = False) -> dict:
        """
        Lists all User Groups for a team.

        Args:
            team_id (str, optional): ID of the team to list User Groups for.
            include_disabled (bool, optional): Include disabled User Groups.
            include_count (bool, optional): Include the number of users.
            include_users (bool, optional): Include the list of user IDs.

        Returns:
            dict: A dictionary containing the list of user groups.
        """

        usergroups = []
        for usergroup_id, usergroup_data in DB.get("usergroups", {}).items():
            if not include_disabled and usergroup_data.get("disabled", False):
                continue

            # Create a copy to avoid modifying the original in the DB
            usergroup_info = usergroup_data.copy()

            if not include_count:
                usergroup_info.pop("user_count", None)  # Remove if not requested

            if not include_users:
                usergroup_info.pop("users", None) #Remove if not requested

            usergroups.append(usergroup_info)

        if team_id:
            usergroups = [usergroup for usergroup in usergroups if usergroup.get("team_id") == team_id]

        return {"ok": True, "usergroups": usergroups}

    @staticmethod
    def update(usergroup_id: str, name: str = None, handle: str = None, description: str = None, channel_ids: List[str] = None, date_update: str =None) -> dict:
        """
        Updates an existing User Group.

        Args:
            usergroup_id (str): The ID of the User Group to update.
            name (str, optional): New name for the User Group.
            handle (str, optional): New handle for the User Group.
            description (str, optional): New description for the User Group.
            channel_ids (list[str], optional): New list of channel IDs.
            date_update (str, optional): Timestamp when the User Group was last updated.

        Returns:
            dict: A dictionary representing the updated User Group, or an error.
        """

        if not usergroup_id or not isinstance(usergroup_id, str):
            return {"ok": False, "error": "invalid_usergroup_id"}

        if usergroup_id not in DB.get("usergroups", {}):
            return {"ok": False, "error": "usergroup_not_found"}

        usergroup = DB["usergroups"][usergroup_id]

        # Check for duplicate usergroup name (case-insensitive) if name is updated
        if name:
            for id, data in DB.get("usergroups", {}).items():
                if id != usergroup_id and data["name"].lower() == name.lower():
                    return {"ok": False, "error": "name_already_exists"}
        # Check for duplicate usergroup handle (case-insensitive) if handle is updated.
        if handle:
          for id, data in DB.get("usergroups", {}).items():
                if id != usergroup_id and data["handle"].lower() == handle.lower():
                    return {"ok": False, "error": "handle_already_exists"}
        # Validate channel_ids
        if channel_ids is not None:
            if not isinstance(channel_ids, list):
                return {"ok": False, "error": "invalid_channel_ids"}
            for channel_id in channel_ids:
                if channel_id not in DB["channels"]:
                     return {"ok": False, "error": "invalid_channel_id", "channel_id": channel_id}
            usergroup["prefs"]["channels"] = channel_ids

        if name is not None:
            usergroup["name"] = name
        if handle is not None:
            usergroup["handle"] = handle
        if description is not None:
            usergroup["description"] = description


        usergroup["date_update"] = date_update if date_update else str(time.time())
        usergroup["updated_by"] = ""

        return {"ok": True, "usergroup": usergroup}

    @staticmethod
    def disable(usergroup_id: str, date_delete = None) -> dict:
        """
        Disables a User Group.

        Args:
            usergroup_id (str): The ID of the User Group to disable.
            date_delete (str, optional): Timestamp when the User Group was deleted.

        Returns:
            dict: A dictionary representing the API response.
        """
        if not usergroup_id or not isinstance(usergroup_id, str):
            return {"ok": False, "error": "invalid_usergroup_id"}

        if usergroup_id not in DB.get("usergroups", {}):
            return {"ok": False, "error": "usergroup_not_found"}

        if DB["usergroups"][usergroup_id]["disabled"]:
            return {"ok": False, "error": "usergroup_already_disabled"}

        DB["usergroups"][usergroup_id]["disabled"] = True
        DB["usergroups"][usergroup_id]["date_delete"] = date_delete if date_delete else str(time.time())
        DB["usergroups"][usergroup_id]["deleted_by"] = ""

        return {"ok": True}

    @staticmethod
    def enable(usergroup_id: str) -> dict:
        """
        Enables a User Group.

        Args:
            usergroup_id (str): The ID of the User Group to enable.

        Returns:
            dict: A dictionary representing the API response.
        """
        if not usergroup_id or not isinstance(usergroup_id, str):
            return {"ok": False, "error": "invalid_usergroup_id"}

        if usergroup_id not in DB.get("usergroups", {}):
            return {"ok": False, "error": "usergroup_not_found"}

        DB["usergroups"][usergroup_id]["disabled"] = False
        DB["usergroups"][usergroup_id]["date_delete"] = 0  # Reset deleted timestamp
        DB["usergroups"][usergroup_id]["deleted_by"] = None # Reset the user who deleted it
        return {"ok": True}

class UsergroupUsers:
    """
    Manages users within a user group.
    """

    @staticmethod
    def update(usergroup_id: str, user_ids: list[str], date_update: str = None) -> dict:
        """
        Updates the list of users in a User Group.

        Args:

            usergroup_id (str): The ID of the User Group.
            user_ids (list[str]): List of user IDs to set as members.
            date_update (str, optional): Timestamp when the User Group was last updated.

        Returns:
            dict: A dictionary representing the updated User Group, or an error.
        """
        if not usergroup_id:
            return {"ok": False, "error": "invalid_usergroup_id"}
        if not user_ids or not isinstance(user_ids, list):
            return {"ok": False, "error": "invalid_user_ids"}

        if usergroup_id not in DB.get("usergroups", {}):
            return {"ok": False, "error": "usergroup_not_found"}

        # Validate that all provided user_ids exist
        for user_id in user_ids:
            if user_id not in DB["users"]:
                return {"ok": False, "error": "user_not_found", "user_id": user_id}

        DB["usergroups"][usergroup_id]["users"] = user_ids
        DB["usergroups"][usergroup_id]["user_count"] = len(user_ids)
        DB["usergroups"][usergroup_id]["updated_by"] = ""
        DB["usergroups"][usergroup_id]["date_update"] = date_update if date_update else str(time.time())

        return {"ok": True, "usergroup": DB["usergroups"][usergroup_id]}

    @staticmethod
    def list(usergroup_id: str, include_disabled: bool = False) -> dict:
        """
        Lists all users in a User Group.

        Args:

            usergroup_id (str): The ID of the User Group.
            include_disabled (bool, optional): Include disabled users. Defaults to False.

        Returns:
            dict: A dictionary containing the list of users, or an error.
        """
        if not usergroup_id or not isinstance(usergroup_id, str):
            return {"ok": False, "error": "invalid_usergroup_id"}

        if usergroup_id not in DB.get("usergroups", {}):
            return {"ok": False, "error": "usergroup_not_found"}

        # Get the list of user IDs
        user_ids = DB["usergroups"][usergroup_id]["users"]

        # Retrieve user details for each user ID
        users = []

        for user_id in user_ids:
            if user_id in DB["users"]: #Check user exists, and if include_disabled is false, check enabled.
                users.append(DB["users"][user_id])
            else: #User not found, inconsistency
                return {"ok": False, "error": "inconsistent_data", "message": f"User {user_id} in usergroup but not in users DB."}
        return {"ok": True, "users": users}

# -------------------------------------------------------------------
# Search Class & Methods
# -------------------------------------------------------------------

class Search:
    @staticmethod
    def search_messages(query: str) -> List[Dict[str, Any]]:
        """Simulates Slack's search.messages API method.

        Args:
            query (str): The search query.

        Returns:
            List[Dict[str, Any]]: List of matching messages.
        """
        filters = _parse_query(query)
        results = []

        for channel in DB["channels"].values():
            for msg in channel["messages"]:
                if _matches_filters(msg, filters, channel.get("name", '')):
                    results.append(msg)

        return results

    @staticmethod
    def search_files(query: str) -> List[Dict[str, Any]]:
        """Simulates Slack's search.files API method.

        Args:
            query (str): The search query.

        Returns:
            List[Dict[str, Any]]: List of matching files.
        """
        filters = _parse_query(query)
        results = []

        for channel in DB["channels"].values():
            if filters["channel"] and channel["name"] != filters["channel"]:
                continue
            for file_info in channel["files"].values():
                if filters["text"] and not any(
                    word.lower() in file_info["name"].lower() for word in filters["text"]
                ):
                    continue
                if "star" in filters["has"] and not file_info.get("is_starred"):
                    continue
                results.append(file_info)

        return results

    @staticmethod
    def search_all(query: str) -> Dict[str, List[Dict[str, Any]]]:
        """Simulates Slack's search.all API method, ensuring OR logic works properly.

        Args:
            query (str): The search query.

        Returns:
            Dict[str, List[Dict[str, Any]]]: Dictionary containing matching messages and files.
        """
        filters = _parse_query(query)

        message_results = Search.search_messages(query) if filters["boolean"] == "AND" else []
        file_results = Search.search_files(query) if filters["boolean"] == "AND" else []

        if filters["boolean"] == "OR":
            # If OR is specified, run both searches separately and merge results
            message_results = Search.search_messages(" ".join(filters["text"])) + message_results
            file_results = Search.search_files(" ".join(filters["text"])) + file_results

        return {"messages": message_results, "files": file_results}

# Import PyDrive and associated libraries.
# This only needs to be done once per notebook.
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

# Authenticate and create the PyDrive client.
# This only needs to be done once per notebook.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

# List .txt files in the root.
#
# Search query reference:
# https://developers.google.com/drive/v2/web/search-parameters
listed = drive.ListFile({'q': "title contains '.txt' and 'root' in parents"}).GetList()
for file in listed:
  print('title {}, id {}'.format(file['title'], file['id']))
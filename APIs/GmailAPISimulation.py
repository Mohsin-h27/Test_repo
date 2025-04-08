"""
Full Python simulation for all resources from the Gmail API Discovery JSON,
with in-memory state, JSON persistence, and embedded tests.

Run this notebook end-to-end to execute tests verifying correctness of each method.
"""
import json
import unittest
import os
import shlex
from typing import Dict, Any, List, Optional, Union

# ---------------------------------------------------------------------------------------
# In-Memory Database Structure
# ---------------------------------------------------------------------------------------
# We keep all user data under DB['users'][userId], which is itself a dictionary storing:
#   - 'profile': dict
#   - 'drafts': { draftId: {...}, ...}
#   - 'messages': { messageId: {...}, ...}
#   - 'threads': { threadId: {...}, ...}
#   - 'labels': { labelId: {...}, ...}
#   - 'settings': {
#       'imap': {},
#       'pop': {},
#       'vacation': {},
#       'language': {},
#       'autoForwarding': {},
#       'sendAs': {
#           sendAsEmail: {
#               'smimeInfo': { smimeId: {...}, ...}
#               ...
#           },
#           ...
#       },d
#     },
#   - 'history': [],
#   - 'watch': {}
#
# Additionally, DB['counters'] holds numeric counters used for generating unique IDs.

DB = {
    'users': {
        'me': {
            'profile': {
                'emailAddress': 'me@example.com',
                'messagesTotal': 0,
                'threadsTotal': 0,
                'historyId': '1'
            },
            'drafts': {},
            'messages': {},
            'threads': {},
            'labels': {},
            'settings': {
                'imap': {},
                'pop': {},
                'vacation': {'enableAutoReply': False},
                'language': {'displayLanguage': 'en'},
                'autoForwarding': {'enabled': False},
                'sendAs': {}
            },
            'history': [],
            'watch': {},
        }
    },
    'counters': {
        'message': 0,
        'thread': 0,
        'draft': 0,
        'label': 0,
        'history': 0,
        'smime': 0
    }
}

# ---------------------------------------------------------------------------------------
# Persistence Class
# ---------------------------------------------------------------------------------------
class GmailAPI:
    """
    The top-level class that handles the in-memory DB and provides
    save/load functionality for JSON-based state persistence.
    """

    @staticmethod
    def save_state(filepath: str) -> None:
        """
        Saves the current state of the in-memory database to a JSON file.

        Args:
            filepath: The path to the JSON file where the state should be saved.
        """
        with open(filepath, 'w') as f:
            json.dump(DB, f)

    @staticmethod
    def load_state(filepath: str) -> None:
        """
        Loads the state of the in-memory database from a JSON file.

        Args:
            filepath: The path to the JSON file from which the state should be loaded.
        """
        global DB
        with open(filepath, 'r') as f:
            global DB
            DB = json.load(f)

# ---------------------------------------------------------------------------------------
# Helper Methods
# ---------------------------------------------------------------------------------------
def _ensure_user(userId: str) -> None:
    if userId not in DB['users']:
        raise ValueError(f"User '{userId}' does not exist.")



def _next_counter(counter_name: str) -> int:
    """
    Retrieves the next integer from the specified counter, increments it, and returns the new value.

    Args:
        counter_name: The name of the counter to increment.

    Returns:
        The incremented counter value.
    """
    current_val = DB['counters'].get(counter_name, 0)
    new_val = current_val + 1
    DB['counters'][counter_name] = new_val
    return new_val


# ---------------------------------------------------------------------------------------
# Resource: users
# ---------------------------------------------------------------------------------------
class Users:
    """
    users resource-level methods
    """

    @staticmethod
    def getProfile(userId: str = 'me') -> Dict[str, Any]:
        """
        Gets the current user's Gmail profile.

        Args:
            userId: The ID of the user whose profile is to be retrieved. Defaults to 'me' for the current user.

        Returns:
            A dictionary representing the user's profile.
        """
        _ensure_user(userId)
        return DB['users'][userId]['profile']

    @staticmethod
    def watch(userId: str = 'me', request: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sets up or updates a push notification watch on the given user mailbox.

        Args:
            userId: The ID of the user for whom to set up a watch. Defaults to 'me' for the current user.
            request: Optional dictionary containing the watch request parameters. Defaults to None.

        Returns:
            A dictionary representing the watch response.
        """
        _ensure_user(userId)
        if request is None:
            request = {}
        DB['users'][userId]['watch'] = request
        # Simulated response:
        resp = {
            'historyId': DB['users'][userId]['profile'].get('historyId', '1'),
            'expiration': '9999999999999'
        }
        return resp

    @staticmethod
    def stop(userId: str = 'me') -> Dict[str, Any]:
        """
        Stops receiving push notifications for the given user mailbox.

        Args:
            userId: The ID of the user for whom to stop notifications. Defaults to 'me' for the current user.

        Returns:
            An empty dictionary.
        """
        _ensure_user(userId)
        DB['users'][userId]['watch'] = {}
        return {}

    @staticmethod
    def exists(userId: str) -> bool:
        """
        Checks if the user exists in the database.

        Args:
            userId: The unique identifier for the user.

        Returns:
            True if the user exists, otherwise False.
        """
        return userId in DB['users']

    @staticmethod
    def createUser(userId: str, profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Creates a new user with the provided profile details.

        Args:
            userId: The unique identifier for the new user.
            profile: A dictionary containing profile information (must include a valid 'emailAddress').

        Returns:
            The newly created user record.
        """
        if profile is None or 'emailAddress' not in profile:
            raise ValueError("A valid 'emailAddress' must be provided in the profile.")
        DB['users'][userId] = {
            'profile': {
                'emailAddress': profile['emailAddress'],
                'messagesTotal': 0,
                'threadsTotal': 0,
                'historyId': '1'
            },
            'drafts': {},
            'messages': {},
            'threads': {},
            'labels': {},
            'settings': {
                'imap': {},
                'pop': {},
                'vacation': {'enableAutoReply': False},
                'language': {'displayLanguage': 'en'},
                'autoForwarding': {'enabled': False},
                'sendAs': {}
            },
            'history': [],
            'watch': {},
        }
        return DB['users'][userId]


    # -------------------------------------------------------------------------
    # users.drafts
    # -------------------------------------------------------------------------
    class Drafts:
        @staticmethod
        def create(userId: str = 'me',
                   draft: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            """
            Creates a new draft with a nested message object.

            Args:
                userId: The ID of the user creating the draft. Defaults to 'me'.
                draft: Optional dictionary containing the draft data. Defaults to None.

            Returns:
                A dictionary representing the created draft.
            """
            _ensure_user(userId)
            draft_id_num = _next_counter('draft')
            draft_id = f"draft-{draft_id_num}"
            if draft is None:
                draft = {}
            message_input = draft.get('message', {})
            message_obj = {
                'id': draft_id,
                'threadId': message_input.get('threadId', f"thread-{draft_id_num}"),
                'raw': message_input.get('raw', ''),
                'sender': message_input.get('sender', ''),
                'recipient': message_input.get('recipient', ''),
                'subject': message_input.get('subject', ''),
                'body': message_input.get('body', ''),
                'date': message_input.get('date', ''),
                'internalDate': message_input.get('internalDate', '234567890'),
                'isRead': message_input.get('isRead', False),
                'labelIds': message_input.get('labelIds', ['DRAFT'])
            }
            if 'DRAFT' not in [lbl.upper() for lbl in message_obj.get('labelIds', [])]:
                message_obj.setdefault('labelIds', []).append('DRAFT')
            draft_obj = {
                'id': draft_id,
                'message': message_obj
            }
            DB['users'][userId]['drafts'][draft_id] = draft_obj
            return draft_obj

        @staticmethod
        def list(userId: str = 'me',
                max_results: int = 100,
                page_token: str = '',
                q: str = '',
                include_spam_trash: bool = False) -> Dict[str, Any]:
            """
            Lists drafts with optional query filtering.
            """
            _ensure_user(userId)
            drafts_list = list(DB['users'][userId]['drafts'].values())
            if q:
                # Use shlex.split to correctly handle quoted strings
                tokens = shlex.split(q)
                for token in tokens:
                    token_lower = token.lower()
                    if token_lower.startswith("from:"):
                        target_email = token[5:].strip().lower()
                        drafts_list = [d for d in drafts_list if d.get('message', {}).get('sender', '').lower() == target_email]
                    elif token_lower.startswith("to:"):
                        target_email = token[3:].strip().lower()
                        drafts_list = [d for d in drafts_list if d.get('message', {}).get('recipient', '').lower() == target_email]
                    elif token_lower.startswith("subject:"):
                        subject_query = token[8:].strip().lower()
                        drafts_list = [d for d in drafts_list if subject_query in d.get('message', {}).get('subject', '').lower()]
                    elif token_lower.startswith("body:"):
                        body_query = token[5:].strip().lower()
                        drafts_list = [d for d in drafts_list if body_query in d.get('message', {}).get('body', '').lower()]
                    elif token_lower.startswith("label:"):
                        label_name = token[6:].strip().upper()
                        drafts_list = [d for d in drafts_list if label_name in [lbl.upper() for lbl in d.get('message', {}).get('labelIds', [])]]
                    else:
                        keyword = token_lower
                        drafts_list = [d for d in drafts_list if keyword in d.get('message', {}).get('subject', '').lower() or
                                      keyword in d.get('message', {}).get('body', '').lower() or
                                      keyword in d.get('message', {}).get('sender', '').lower() or
                                      keyword in d.get('message', {}).get('recipient', '').lower()]
            # This return statement must be outside the "if q:" block
            return {
                'drafts': drafts_list[:max_results],
                'nextPageToken': None
            }


        @staticmethod
        def update(userId: str = 'me',
                   id: str = '', draft: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
            """
            Updates an existing draft.

            Args:
                userId: The ID of the user whose draft is to be updated. Defaults to 'me'.
                id: The ID of the draft to update.
                draft: Optional dictionary containing the updated draft data. Defaults to None.

            Returns:
                The updated draft, or None if the draft does not exist.
            """
            _ensure_user(userId)
            if draft is None:
                draft = {}
            existing = DB['users'][userId]['drafts'].get(id)
            if not existing:
                return None
            existing_message = existing['message']
            message_update = draft.get('message', {})
            existing_message.update(message_update)
            if 'labelIds' in existing_message:
                if 'DRAFT' not in [lbl.upper() for lbl in existing_message['labelIds']]:
                    existing_message['labelIds'].append('DRAFT')
            else:
                existing_message['labelIds'] = ['DRAFT']
            return existing

        def delete(userId: str = 'me',
                   id: str = '') -> Optional[Dict[str, Any]]:
            """
            Deletes a draft.

            Args:
                userId: The ID of the user whose draft is to be deleted. Defaults to 'me'.
                id: The ID of the draft to delete.

            Returns:
                The deleted draft, or None if the draft does not exist.
            """
            _ensure_user(userId)
            return DB['users'][userId]['drafts'].pop(id, None)

        @staticmethod
        def get(userId: str = 'me',
                id: str = '',
                format: str = 'full') -> Optional[Dict[str, Any]]:
            """
            Retrieves a draft.

            Args:
                userId: The ID of the user whose draft is to be retrieved. Defaults to 'me'.
                id: The ID of the draft to retrieve.
                format: The format of the retrieved draft. Defaults to 'full'.

            Returns:
                The retrieved draft, or None if the draft does not exist.
            """
            _ensure_user(userId)
            return DB['users'][userId]['drafts'].get(id)

        @staticmethod
        def send(userId: str = 'me',
                 draft: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            """
            Sends a draft.

            Args:
                userId: The ID of the user sending the draft. Defaults to 'me'.
                draft: Optional dictionary containing the draft data. Defaults to None.

            Returns:
                The result of sending the draft.
            """
            _ensure_user(userId)
            if draft is None:
                draft = {}
            draft_id = draft.get('id')
            if draft_id and draft_id in DB['users'][userId]['drafts']:
                draft_obj = DB['users'][userId]['drafts'][draft_id]
                content = draft_obj.get('message', {}).get('raw', '')
                msg = Users.Messages.send(userId=userId, msg={'raw': content})
                DB['users'][userId]['drafts'].pop(draft_id, None)
                return msg
            else:
              # treat as new message
              content = draft.get('message', {}).get('raw', '')
              return Users.Messages.send(userId=userId, msg={'raw': content})

    # -------------------------------------------------------------------------
    # users.history
    # -------------------------------------------------------------------------
    class History:
        @staticmethod
        def list(userId: str = 'me',
                max_results: int = 100,
                page_token: str = '',
                start_history_id: str = '',
                label_id: str = '',
                history_types: Optional[List[str]] = None) -> Dict[str, Any]:
            """
            Lists the history of all changes to the mailbox (simulated).

            Args:
                userId: The ID of the user whose history is to be listed. Defaults to 'me'.
                max_results: The maximum number of history entries to return. Defaults to 100.
                page_token: A token to retrieve the next page of results. Defaults to ''.
                start_history_id: The ID of the history to start listing from. Defaults to ''.
                label_id: Only return history entries for messages with the specified label. Defaults to ''.
                history_types: Optional list of history types to return. Defaults to None.

            Returns:
                A dictionary containing the list of history entries, the next page token, and the current history ID.
            """
            _ensure_user(userId)
            history_data = DB['users'][userId]['history']
            return {
                'history': history_data[:max_results],
                'nextPageToken': None,
                'historyId': DB['users'][userId]['profile'].get('historyId', '1')
            }

    # -------------------------------------------------------------------------
    # users.messages
    # -------------------------------------------------------------------------
    class Messages:
        @staticmethod
        def trash(userId: str = 'me',
                  id: str = '') -> Optional[Dict[str, Any]]:
            """
            Moves a message to the trash.

            Args:
                userId: The ID of the user whose message is to be trashed. Defaults to 'me'.
                id: The ID of the message to trash.

            Returns:
                The modified message, or None if the message does not exist.
            """
            _ensure_user(userId)
            msg = DB['users'][userId]['messages'].get(id)
            if msg:
                labels = msg.get('labelIds',)
                if 'TRASH' not in labels:
                    labels.append('TRASH')
                msg['labelIds'] = labels
            return msg

        @staticmethod
        def untrash(userId: str = 'me',
                    id: str = '') -> Optional[Dict[str, Any]]:
            """
            Removes a message from the trash.

            Args:
                userId: The ID of the user whose message is to be untrashed. Defaults to 'me'.
                id: The ID of the message to untrash.

            Returns:
                The modified message, or None if the message does not exist.
            """
            _ensure_user(userId)
            msg = DB['users'][userId]['messages'].get(id)
            if msg:
                labels = msg.get('labelIds',)
                if 'TRASH' in labels:
                    labels.remove('TRASH')
                msg['labelIds'] = labels
            return msg

        @staticmethod
        def delete(userId: str = 'me',
                   id: str = '') -> Optional[Dict[str, Any]]:
            """
            Deletes a message permanently.

            Args:
                userId: The ID of the user whose message is to be deleted. Defaults to 'me'.
                id: The ID of the message to delete.

            Returns:
                The deleted message, or None if the message does not exist.
            """
            _ensure_user(userId)
            return DB['users'][userId]['messages'].pop(id, None)

        @staticmethod
        def batchDelete(userId: str = 'me',
                         ids: Optional[List[str]] = None) -> None:
            """
            Deletes multiple messages permanently.

            Args:
                userId: The ID of the user whose messages are to be deleted. Defaults to 'me'.
                ids: Optional list of message IDs to delete. Defaults to None.
            """
            _ensure_user(userId)
            if ids is None:
                ids = []
            for mid in ids:
                DB['users'][userId]['messages'].pop(mid, None)

        @staticmethod
        def import_(userId: str = 'me',
                     msg: Optional[Dict[str, Any]] = None,
                     internal_date_source: str = 'dateHeader',
                     never_mark_spam: bool = False,
                     process_for_calendar: bool = False,
                     deleted: bool = False) -> Dict[str, Any]:
            """
            Imports a message into the mailbox.

            Args:
                userId: The ID of the user to import the message for. Defaults to 'me'.
                msg: Optional dictionary containing the message data. Defaults to None.
                internal_date_source: The source of the message's internal date. Defaults to 'dateHeader'.
                never_mark_spam: Whether to never mark the message as spam. Defaults to False.
                process_for_calendar: Whether to process the message for calendar events. Defaults to False.
                deleted: Whether the message is deleted. Defaults to False.

            Returns:
                The imported message.
            """
            _ensure_user(userId)
            message_id_num = _next_counter('message')
            message_id = f"msg_{message_id_num}"
            new_msg = {
                'id': message_id,
                'raw': msg.get('raw', '') if msg else '',
                'labelIds': [],
                'internalDate': '123456789',
            }
            if deleted:
                new_msg['labelIds'].append('DELETED')
            DB['users'][userId]['messages'][message_id] = new_msg
            return new_msg

        @staticmethod
        def insert(userId: str = 'me',
                   msg: Optional[Dict[str, Any]] = None,
                   internal_date_source: str = 'receivedTime',
                   deleted: bool = False) -> Dict[str, Any]:
            """
            Inserts a message into the mailbox, bypassing normal scanning.

            Args:
                userId: The ID of the user to insert the message for. Defaults to 'me'.
                msg: Optional dictionary containing the message data. Defaults to None.
                internal_date_source: The source of the message's internal date. Defaults to 'receivedTime'.
                deleted: Whether the message is deleted. Defaults to False.

            Returns:
                The inserted message.
            """
            _ensure_user(userId)
            message_id_num = _next_counter('message')
            message_id = f"message-{message_id_num}"

            # Ensure msg is a dict to simplify get() calls.
            if msg is None:
                msg = {}

            # Use provided threadId if available; otherwise, default to a new thread id.
            thread_id = msg.get('threadId', f"thread-{message_id_num}")

            # Determine internalDate: if provided use that, otherwise (optionally) derive it.
            # Here we use the value from msg if available or a default placeholder.
            internal_date = msg.get('internalDate', '234567890')

            # Build the complete message entry.
            new_msg = {
                'id': message_id,
                'threadId': thread_id,
                'raw': msg.get('raw', ''),
                'sender': msg.get('sender', ''),
                'recipient': msg.get('recipient', ''),
                'subject': msg.get('subject', ''),
                'body': msg.get('body', ''),
                'date': msg.get('date', ''),
                'internalDate': internal_date,
                'isRead': msg.get('isRead', False),
                # Default labelIds mimic your DB example ("INBOX" and "UNREAD")
                'attachment': msg.get('attachment',[]),
                'labelIds': msg.get('labelIds', ['INBOX', 'UNREAD']),
            }

            # Append 'DELETED' if flagged.
            if deleted:
                new_msg['labelIds'].append('DELETED')

            DB['users'][userId]['messages'][message_id] = new_msg
            return new_msg

        @staticmethod
        def get(userId: str = 'me',
                id: str = '',
                format: str = 'full',
                metadata_headers: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
            """
            Gets the specified message.

            Args:
                userId: The ID of the user whose message is to be retrieved. Defaults to 'me'.
                id: The ID of the message to retrieve.
                format: The format of the message to retrieve. Defaults to 'full'.
                metadata_headers: Optional list of metadata headers to include in the response. Defaults to None.

            Returns:
                The retrieved message, or None if the message does not exist.
            """
            _ensure_user(userId)
            return DB['users'][userId]['messages'].get(id)

        @staticmethod
        def send(userId: str = 'me',
                msg: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            _ensure_user(userId)
            message_id_num = _next_counter('message')
            message_id = f"msg_{message_id_num}"
            # Ensure msg is a dict
            if msg is None:
                msg = {}
            new_msg = {
                'id': message_id,
                'threadId': msg.get('threadId', f"thread-{message_id_num}"),
                'raw': msg.get('raw', ''),
                'sender': msg.get('sender', ''),
                'recipient': msg.get('recipient', ''),
                'subject': msg.get('subject', ''),
                'body': msg.get('body', ''),
                'date': msg.get('date', ''),
                'internalDate': msg.get('internalDate', '345678901'),
                'isRead': msg.get('isRead', False),
                'attachment': msg.get('attachment', []),
                'labelIds': ['SENT'],  # Override labelIds for sent messages.
            }
            DB['users'][userId]['messages'][message_id] = new_msg
            return new_msg


        @staticmethod
        def list(userId: str = 'me',
                 max_results: int = 100,
                 page_token: str = '',
                 q: str = '',
                 labelIds: Optional[List[str]] = None,
                 include_spam_trash: bool = False) -> Dict[str, Any]:
            """
            Lists messages with optional query filtering.

            Args:
                userId: The ID of the user whose messages are to be listed. Defaults to 'me'.
                max_results: The maximum number of messages to return. Defaults to 100.
                page_token: A token to retrieve the next page of results. Defaults to ''.
                q: A query string to filter messages. Defaults to ''.
                labelIds: Optional list of label IDs to filter messages by. Defaults to None.
                include_spam_trash: Whether to include spam and trash messages. Defaults to False.

            Returns:
                A dictionary containing the list of messages and the next page token.
            """
            _ensure_user(userId)
            messages_list = DB['users'][userId]['messages'].values()

            # Start with everything; we will progressively narrow down
            filtered_messages = list(messages_list)

            # Initialize the attachment filter
            attachment_filter = None
            attachment_name = None

            # Naive tokenizer: split on whitespace
            tokens = q.split() if q else []

            for token in tokens:
                # Example: handle from:
                if token.lower().startswith("from:"):
                    # Extract the email after "from:"
                    target_email = token[5:].strip().lower()
                    filtered_messages = [
                        m for m in filtered_messages
                        if m.get("sender", "").lower() == target_email
                    ]

                # Example: handle to:
                elif token.lower().startswith("to:"):
                  target_email = token[3:].strip().lower()
                  if target_email:  # Only apply the filter if an email is provided.
                      filtered_messages = [
                          m for m in filtered_messages
                          if m.get("recipient", "").lower() == target_email
                      ]


                # Example: handle label:
                elif token.lower().startswith("label:"):
                    # Extract the label name after "label:"
                    label_name = token[6:].strip()
                    # We have two ways to do this:
                    # 1) If label_name is the *system* name we store directly (e.g. "INBOX"),
                    #   compare it to the actual system label (like "INBOX").
                    # 2) If label_name is an ID or user label name, you may need
                    #   to look up the label's internal ID in DB['users'][userId]['labels']
                    #   and then match it in each message's labelIds.
                    #
                    # For simplicity, suppose label_name is exactly the label *name*
                    # we store in the message labelIds (like "INBOX", "UNREAD", "IMPORTANT"):
                    filtered_messages = [
                        m for m in filtered_messages
                        if label_name.upper() in (m.get("labelIds") or [])
                        # or if label_name is user-level, check if it matches some DB label
                    ]

                # Example: handle subject:
                elif token.lower().startswith("subject:"):
                    # Extract the string after "subject:"
                    subject_query = token[8:].strip().lower()
                    filtered_messages = [
                        m for m in filtered_messages
                        if subject_query in m.get("subject", "").lower()
                    ]

                # Detect attachment search
                elif token.lower().startswith("attachment:"):
                    attachment_name = token[11:].strip().lower()
                    attachment_filter = True  # Mark that attachment filtering is needed

                # Example: handle a plain keyword (no explicit field prefix)
                else:
                    keyword = token.lower()
                    filtered_messages = [
                        m for m in filtered_messages
                        if keyword in m.get("subject", "").lower()
                        or keyword in m.get("body", "").lower()
                        or keyword in m.get("sender", "").lower()
                        or keyword in m.get("recipient", "").lower()
                    ]

            # Apply attachment filter separately after all other filters
            if attachment_filter:
                if attachment_name == "any":
                    # Keep only messages that have attachments
                    filtered_messages = [
                        m for m in filtered_messages
                        if m.get("attachments") and len(m["attachments"]) > 0
                    ]
                else:
                    # Keep only messages that contain a specific attachment filename
                    filtered_messages = [
                        m for m in filtered_messages
                        if any(
                            attachment_name in att.get("filename", "").lower()
                            for att in m.get("attachments",)
                        )
                    ]

            # If the caller explicitly passed labelIds in the method call, apply that filter, too.
            if labelIds:
                filtered_messages = [
                    m for m in filtered_messages
                    if set(labelIds).issubset(set(m.get("labelIds",)))
                ]

            # Trim to maxResults, ignoring pagination in this simple example
            return {
                "messages": filtered_messages[:max_results],
                "nextPageToken": None
            }

        @staticmethod
        def modify(userId: str = 'me',
                   id: str = '',
                   addLabelIds: Optional[List[str]] = None,
                   removeLabelIds: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
            """
            Modifies the labels of a message.

            Args:
                userId: The ID of the user whose message is to be modified. Defaults to 'me'.
                id: The ID of the message to modify.
                addLabelIds: Optional list of label IDs to add to the message. Defaults to None.
                removeLabelIds: Optional list of label IDs to remove from the message. Defaults to None.

            Returns:
                The modified message, or None if the message does not exist.
            """
            _ensure_user(userId)
            msg = DB['users'][userId]['messages'].get(id)
            if not msg:
                return None
            labels = msg.setdefault('labelIds',)
            if addLabelIds:
                for l in addLabelIds:
                    if l not in labels:
                        labels.append(l)
            if removeLabelIds:
                for l in removeLabelIds:
                    if l in labels:
                        labels.remove(l)
            msg['labelIds'] = labels
            return msg

        @staticmethod
        def batchModify(userId: str = 'me',
                         ids: Optional[List[str]] = None,
                         addLabelIds: Optional[List[str]] = None,
                         removeLabelIds: Optional[List[str]] = None) -> None:
            """
            Modifies the labels of multiple messages.

            Args:
                userId: The ID of the user whose messages are to be modified. Defaults to 'me'.
                ids: Optional list of message IDs to modify. Defaults to None.
                addLabelIds: Optional list of label IDs to add to the messages. Defaults to None.
                removeLabelIds: Optional list of label IDs to remove from the messages. Defaults to None.
            """
            _ensure_user(userId)
            if ids is None:
                ids = []
            for mid in ids:
                Users.Messages.modify(userId=userId, id=mid,
                                     addLabelIds=addLabelIds,
                                     removeLabelIds=removeLabelIds)

        class Attachments:
            @staticmethod
            def get(userId: str = 'me',
                    message_id: str = '',
                    id: str = '') -> Optional[Dict[str, Any]]:
                """
                Gets a message attachment.

                Args:
                    userId: The ID of the user whose message contains the attachment. Defaults to 'me'.
                    message_id: The ID of the message containing the attachment.
                    id: The ID of the attachment to retrieve.

                Returns:
                    The attachment data, or None if the message or attachment does not exist.
                """
                _ensure_user(userId)
                msg = DB['users'][userId]['messages'].get(message_id)
                if not msg:
                    return None
                # In a real scenario, attachments might be in the payload,
                # but we'll just simulate
                return {
                    'attachmentId': id,
                    'data': 'base64encoded=='
                }

    # -------------------------------------------------------------------------
    # users.labels
    # -------------------------------------------------------------------------
    class Labels:
        @staticmethod
        def create(userId: str = 'me',
                   label: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            """
            Creates a new label.

            Args:
                userId: The ID of the user creating the label. Defaults to 'me'.
                label: Optional dictionary containing the label data. Defaults to None.

            Returns:
                The created label.
            """
            _ensure_user(userId)
            label_id_num = _next_counter('label')
            label_id = f"Label_{label_id_num}"
            if label is None:
                label = {}
            new_label = {
                'id': label_id,
                'name': label.get('name', f'Label_{label_id_num}'),
                'labelListVisibility': label.get('labelListVisibility', 'labelShow'),
                'messageListVisibility': label.get('messageListVisibility', 'show'),
            }
            DB['users'][userId]['labels'][label_id] = new_label
            return new_label

        @staticmethod
        def delete(userId: str = 'me',
                   id: str = '') -> None:
            """
            Deletes a label.

            Args:
                userId: The ID of the user deleting the label. Defaults to 'me'.
                id: The ID of the label to delete.
            """
            _ensure_user(userId)
            DB['users'][userId]['labels'].pop(id, None)

        @staticmethod
        def get(userId: str = 'me',
                id: str = '') -> Optional[Dict[str, Any]]:
            """
            Retrieves a label.

            Args:
                userId: The ID of the user whose label is to be retrieved. Defaults to 'me'.
                id: The ID of the label to retrieve.

            Returns:
                The retrieved label, or None if the label does not exist.
            """
            _ensure_user(userId)
            return DB['users'][userId]['labels'].get(id)

        @staticmethod
        def list(userId: str = 'me') -> Dict[str, Any]:
            """
            Lists all labels for a user.

            Args:
                userId: The ID of the user whose labels are to be listed. Defaults to 'me'.

            Returns:
                A dictionary containing the list of labels.
            """
            _ensure_user(userId)
            labels = list(DB['users'][userId]['labels'].values())
            return {'labels': labels}

        @staticmethod
        def update(userId: str = 'me',
                   id: str = '',
                   label: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
            """
            Updates a label.

            Args:
                userId: The ID of the user whose label is to be updated. Defaults to 'me'.
                id: The ID of the label to update.
                label: Optional dictionary containing the updated label data. Defaults to None.

            Returns:
                The updated label, or None if the label does not exist.
            """
            _ensure_user(userId)
            if label is None:
                label = {}
            existing = DB['users'][userId]['labels'].get(id)
            if not existing:
                return None
            existing.update(label)
            return existing

        @staticmethod
        def patch(userId: str = 'me',
                  id: str = '',
                  label: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
            """
            Partially updates a label.

            Args:
                userId: The ID of the user whose label is to be patched. Defaults to 'me'.
                id: The ID of the label to patch.
                label: Optional dictionary containing the patched label data. Defaults to None.

            Returns:
                The patched label, or None if the label does not exist.
            """
            return Users.Labels.update(userId, id, label)

    # -------------------------------------------------------------------------
    # users.threads
    # -------------------------------------------------------------------------
    class Threads:
        @staticmethod
        def trash(userId: str = 'me',
                  id: str = '') -> Optional[Dict[str, Any]]:
            """
            Moves a thread and its messages to the trash.

            Args:
                userId: The ID of the user whose thread is to be trashed. Defaults to 'me'.
                id: The ID of the thread to trash.

            Returns:
                The trashed thread, or None if the thread does not exist.
            """
            _ensure_user(userId)
            thr = DB['users'][userId]['threads'].get(id)
            if thr:
                for mid in thr.get('messageIds', []):
                    Users.Messages.trash(userId, mid)
            return thr

        @staticmethod
        def untrash(userId: str = 'me',
                    id: str = '') -> Optional[Dict[str, Any]]:
            """
            Removes a thread and its messages from the trash.

            Args:
                userId: The ID of the user whose thread is to be untrashed. Defaults to 'me'.
                id: The ID of the thread to untrash.

            Returns:
                The untrashed thread, or None if the thread does not exist.
            """
            _ensure_user(userId)
            thr = DB['users'][userId]['threads'].get(id)
            if thr:
                for mid in thr.get('messageIds', []):
                    Users.Messages.untrash(userId, mid)
            return thr

        @staticmethod
        def delete(userId: str = 'me',
                   id: str = '') -> Optional[Dict[str, Any]]:
            """
            Deletes a thread and its messages permanently.

            Args:
                userId: The ID of the user whose thread is to be deleted. Defaults to 'me'.
                id: The ID of the thread to delete.

            Returns:
                The deleted thread, or None if the thread does not exist.
            """
            _ensure_user(userId)
            thr = DB['users'][userId]['threads'].pop(id, None)
            if thr:
                # also remove messages
                for mid in thr.get('messageIds', []):
                    DB['users'][userId]['messages'].pop(mid, None)
            return thr

        @staticmethod
        def get(userId: str = 'me',
                id: str = '',
                format: str = 'full',
                metadata_headers: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
            """
            Retrieves a thread.

            Args:
                userId: The ID of the user whose thread is to be retrieved. Defaults to 'me'.
                id: The ID of the thread to retrieve.
                format: The format of the thread to retrieve. Defaults to 'full'.
                metadata_headers: Optional list of metadata headers to include in the response. Defaults to None.

            Returns:
                The retrieved thread, or None if the thread does not exist.
            """
            _ensure_user(userId)
            return DB['users'][userId]['threads'].get(id)

        @staticmethod
        def list(userId: str = 'me',
                max_results: int = 100,
                page_token: str = '',
                q: str = '',
                labelIds: Optional[List[str]] = None,
                include_spam_trash: bool = False) -> Dict[str, Any]:
            """
            Lists threads.

            Args:
                userId: The ID of the user whose threads are to be listed. Defaults to 'me'.
                max_results: The maximum number of threads to return. Defaults to 100.
                page_token: A token to retrieve the next page of results. Defaults to ''.
                q: A query string to filter threads. Defaults to ''.
                labelIds: Optional list of label IDs to filter threads by. Defaults to None.
                include_spam_trash: Whether to include spam and trash threads. Defaults to False.

            Returns:
                A dictionary containing the list of threads and the next page token.
            """
            _ensure_user(userId)
            threads_list = list(DB['users'][userId]['threads'].values())
            return {
                'threads': [{'id': t['id']} for t in threads_list][:max_results],
                'nextPageToken': None
            }

        @staticmethod
        def modify(userId: str = 'me',
                   id: str = '',
                   addLabelIds: Optional[List[str]] = None,
                   removeLabelIds: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
            """
            Modifies the labels of a thread and its messages.

            Args:
                userId: The ID of the user whose thread is to be modified. Defaults to 'me'.
                id: The ID of the thread to modify.
                addLabelIds: Optional list of label IDs to add to the thread and its messages. Defaults to None.
                removeLabelIds: Optional list of label IDs to remove from the thread and its messages. Defaults to None.

            Returns:
                The modified thread, or None if the thread does not exist.
            """
            _ensure_user(userId)
            thr = DB['users'][userId]['threads'].get(id)
            if not thr:
                return None
            # apply label changes to all messages in the thread
            for mid in thr.get('messageIds', []):
                Users.Messages.modify(userId, mid, addLabelIds, removeLabelIds)
            return thr

    # -------------------------------------------------------------------------
    # users.settings
    # -------------------------------------------------------------------------
    class Settings:
        @staticmethod
        def getImap(userId: str = 'me') -> Dict[str, Any]:
            """
            Retrieves IMAP settings for a user.

            Args:
                userId: The ID of the user whose IMAP settings are to be retrieved. Defaults to 'me'.

            Returns:
                A dictionary containing the IMAP settings.
            """
            _ensure_user(userId)
            return DB['users'][userId]['settings']['imap']

        @staticmethod
        def updateImap(userId: str = 'me',
                        imap_settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            """
            Updates IMAP settings for a user.

            Args:
                userId: The ID of the user whose IMAP settings are to be updated. Defaults to 'me'.
                imap_settings: Optional dictionary containing the updated IMAP settings. Defaults to None.

            Returns:
                A dictionary containing the updated IMAP settings.
            """
            _ensure_user(userId)
            if imap_settings is None:
                imap_settings = {}
            DB['users'][userId]['settings']['imap'].update(imap_settings)
            return DB['users'][userId]['settings']['imap']

        @staticmethod
        def getPop(userId: str = 'me') -> Dict[str, Any]:
            """
            Retrieves POP settings for a user.

            Args:
                userId: The ID of the user whose POP settings are to be retrieved. Defaults to 'me'.

            Returns:
                A dictionary containing the POP settings.
            """
            _ensure_user(userId)
            return DB['users'][userId]['settings']['pop']

        @staticmethod
        def updatePop(userId: str = 'me',
                       pop_settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            """
            Updates POP settings for a user.

            Args:
                userId: The ID of the user whose POP settings are to be updated. Defaults to 'me'.
                pop_settings: Optional dictionary containing the updated POP settings. Defaults to None.

            Returns:
                A dictionary containing the updated POP settings.
            """
            _ensure_user(userId)
            if pop_settings is None:
                pop_settings = {}
            DB['users'][userId]['settings']['pop'].update(pop_settings)
            return DB['users'][userId]['settings']['pop']

        @staticmethod
        def getVacation(userId: str = 'me') -> Dict[str, Any]:
            """
            Retrieves vacation settings for a user.

            Args:
                userId: The ID of the user whose vacation settings are to be retrieved. Defaults to 'me'.

            Returns:
                A dictionary containing the vacation settings.
            """
            _ensure_user(userId)
            return DB['users'][userId]['settings']['vacation']

        @staticmethod
        def updateVacation(userId: str = 'me',
                            vacation_settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            """
            Updates vacation settings for a user.

            Args:
                userId: The ID of the user whose vacation settings are to be updated. Defaults to 'me'.
                vacation_settings: Optional dictionary containing the updated vacation settings. Defaults to None.

            Returns:
                A dictionary containing the updated vacation settings.
            """
            _ensure_user(userId)
            if vacation_settings is None:
                vacation_settings = {}
            DB['users'][userId]['settings']['vacation'].update(vacation_settings)
            return DB['users'][userId]['settings']['vacation']

        @staticmethod
        def getLanguage(userId: str = 'me') -> Dict[str, Any]:
            """
            Retrieves language settings for a user.

            Args:
                userId: The ID of the user whose language settings are to be retrieved. Defaults to 'me'.

            Returns:
                A dictionary containing the language settings.
            """
            _ensure_user(userId)
            return DB['users'][userId]['settings']['language']

        @staticmethod
        def updateLanguage(userId: str = 'me',
                            language_settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            """
            Updates language settings for a user.

            Args:
                userId: The ID of the user whose language settings are to be updated. Defaults to 'me'.
                language_settings: Optional dictionary containing the updated language settings. Defaults to None.

            Returns:
                A dictionary containing the updated language settings.
            """
            _ensure_user(userId)
            if language_settings is None:
                language_settings = {}
            # Attempt to store. If the requested language is not supported, we would handle that,
            # but in this simulation, we simply store it.
            DB['users'][userId]['settings']['language'].update(language_settings)
            return DB['users'][userId]['settings']['language']

        @staticmethod
        def getAutoForwarding(userId: str = 'me') -> Dict[str, Any]:
            """
            Retrieves auto-forwarding settings for a user.

            Args:
                userId: The ID of the user whose auto-forwarding settings are to be retrieved. Defaults to 'me'.

            Returns:
                A dictionary containing the auto-forwarding settings.
            """
            _ensure_user(userId)
            return DB['users'][userId]['settings']['autoForwarding']

        @staticmethod
        def updateAutoForwarding(userId: str = 'me',
                                   auto_forwarding_settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            """
            Updates auto-forwarding settings for a user.

            Args:
                userId: The ID of the user whose auto-forwarding settings are to be updated. Defaults to 'me'.
                auto_forwarding_settings: Optional dictionary containing the updated auto-forwarding settings. Defaults to None.

            Returns:
                A dictionary containing the updated auto-forwarding settings.
            """
            _ensure_user(userId)
            if auto_forwarding_settings is None:
                auto_forwarding_settings = {}
            DB['users'][userId]['settings']['autoForwarding'].update(auto_forwarding_settings)
            return DB['users'][userId]['settings']['autoForwarding']

        # -------------------------------------------------------------------------
        # users.settings.sendas
        # -------------------------------------------------------------------------

        class SendAs:
            @staticmethod
            def list(userId: str = 'me') -> Dict[str, Any]:
                """
                Lists send-as aliases for a user.

                Args:
                    userId: The ID of the user whose send-as aliases are to be listed. Defaults to 'me'.

                Returns:
                    A dictionary containing the list of send-as aliases.
                """
                _ensure_user(userId)
                sas = DB['users'][userId]['settings']['sendAs']
                return {
                    'sendAs': list(sas.values())
                }

            @staticmethod
            def get(userId: str = 'me',
                    send_as_email: str = '') -> Optional[Dict[str, Any]]:
                """
                Retrieves a send-as alias.

                Args:
                    userId: The ID of the user whose send-as alias is to be retrieved. Defaults to 'me'.
                    send_as_email: The email address of the send-as alias to retrieve.

                Returns:
                    The retrieved send-as alias, or None if it does not exist.
                """
                _ensure_user(userId)
                return DB['users'][userId]['settings']['sendAs'].get(send_as_email)

            @staticmethod
            def create(userId: str = 'me',
                       send_as: Dict[str, Any] = None) -> Dict[str, Any]:
                """
                Creates a new send-as alias.

                Args:
                    userId: The ID of the user creating the send-as alias. Defaults to 'me'.
                    send_as: Optional dictionary containing the send-as alias data. Defaults to None.

                Returns:
                    The created send-as alias.
                """
                _ensure_user(userId)
                if send_as is None:
                    send_as = {}
                # generate alias
                alias_count = len(DB['users'][userId]['settings']['sendAs']) + 1
                email = send_as.get('sendAsEmail', f"alias_{alias_count}@example.com")
                DB['users'][userId]['settings']['sendAs'][email] = {
                    'sendAsEmail': email,
                    'displayName': send_as.get('displayName', email),
                    'replyToAddress': send_as.get('replyToAddress', email),
                    'signature': send_as.get('signature', ''),
                    'verificationStatus': 'accepted',
                }
                return DB['users'][userId]['settings']['sendAs'][email]

            @staticmethod
            def update(userId: str = 'me',
                       send_as_email: str = '',
                       send_as: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
                """
                Updates a send-as alias.

                Args:
                    userId: The ID of the user whose send-as alias is to be updated. Defaults to 'me'.
                    send_as_email: The email address of the send-as alias to update.
                    send_as: Optional dictionary containing the updated send-as alias data. Defaults to None.

                Returns:
                    The updated send-as alias, or None if it does not exist.
                """
                _ensure_user(userId)
                if send_as is None:
                    send_as = {}
                existing = DB['users'][userId]['settings']['sendAs'].get(send_as_email)
                if not existing:
                    return None
                existing.update(send_as)
                return existing

            @staticmethod
            def patch(userId: str = 'me',
                      send_as_email: str = '',
                      send_as: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
                """
                Partially updates a send-as alias.

                Args:
                    userId: The ID of the user whose send-as alias is to be patched. Defaults to 'me'.
                    send_as_email: The email address of the send-as alias to patch.
                    send_as: Optional dictionary containing the patched send-as alias data. Defaults to None.

                Returns:
                    The patched send-as alias, or None if it does not exist.
                """
                return Users.Settings.SendAs.update(userId, send_as_email, send_as)

            @staticmethod
            def delete(userId: str = 'me',
                       send_as_email: str = '') -> None:
                """
                Deletes a send-as alias.

                Args:
                    userId: The ID of the user whose send-as alias is to be deleted. Defaults to 'me'.
                    send_as_email: The email address of the send-as alias to delete.
                """
                _ensure_user(userId)
                DB['users'][userId]['settings']['sendAs'].pop(send_as_email, None)

            @staticmethod
            def verify(userId: str = 'me',
                       send_as_email: str = '') -> Optional[Dict[str, Any]]:
                """
                Verifies a send-as alias.

                Args:
                    userId: The ID of the user whose send-as alias is to be verified. Defaults to 'me'.
                    send_as_email: The email address of the send-as alias to verify.

                Returns:
                    The verified send-as alias, or None if it does not exist or is already verified.
                """
                _ensure_user(userId)
                existing = DB['users'][userId]['settings']['sendAs'].get(send_as_email)
                if existing and existing.get('verificationStatus') == 'pending':
                    existing['verificationStatus'] = 'accepted'
                return existing

            # -------------------------------------------------------------------------
            # users.settings.SendAs.SmimeInfo
            # -------------------------------------------------------------------------

            class SmimeInfo:
                @staticmethod
                def list(userId: str = 'me',
                         send_as_email: str = '') -> Dict[str, Any]:
                    """
                    Lists S/MIME info for a send-as alias.

                    Args:
                        userId: The ID of the user whose S/MIME info is to be listed. Defaults to 'me'.
                        send_as_email: The email address of the send-as alias.

                    Returns:
                        A dictionary containing the list of S/MIME info.
                    """
                    _ensure_user(userId)
                    send_as_entry = DB['users'][userId]['settings']['sendAs'].get(send_as_email)
                    if send_as_entry is None:
                        return {'smimeInfo': []}
                    smime_info_dict = send_as_entry.setdefault('smimeInfo', {})
                    return {'smimeInfo': list(smime_info_dict.values())}


                @staticmethod
                def get(userId: str = 'me',
                        send_as_email: str = '',
                        smime_id: str = '') -> Optional[Dict[str, Any]]:
                    """
                    Retrieves S/MIME info for a send-as alias.

                    Args:
                        userId: The ID of the user whose S/MIME info is to be retrieved. Defaults to 'me'.
                        send_as_email: The email address of the send-as alias.
                        smime_id: The ID of the S/MIME info to retrieve.

                    Returns:
                        The retrieved S/MIME info, or None if it does not exist.
                    """
                    _ensure_user(userId)
                    send_as_entry = DB['users'][userId]['settings']['sendAs'].get(send_as_email)
                    if not send_as_entry:
                        return None
                    return send_as_entry.setdefault('smimeInfo', {}).get(smime_id)

                @staticmethod
                def insert(userId: str = 'me',
                           send_as_email: str = '',
                           smime: Dict[str, Any] = None) -> Dict[str, Any]:
                    """
                    Inserts S/MIME info for a send-as alias.

                    Args:
                        userId: The ID of the user whose S/MIME info is to be inserted. Defaults to 'me'.
                        send_as_email: The email address of the send-as alias.
                        smime: Optional dictionary containing the S/MIME info to insert. Defaults to None.

                    Returns:
                        The inserted S/MIME info.
                    """
                    _ensure_user(userId)
                    if smime is None:
                        smime = {}
                    send_as_entry = DB['users'][userId]['settings']['sendAs'].setdefault(send_as_email, {})
                    smime_dict = send_as_entry.setdefault('smimeInfo', {})
                    sid_num = _next_counter('smime')
                    sid = f"smime_{sid_num}"
                    new_smime = {
                        'id': sid,
                        'encryptedKey': smime.get('encryptedKey', ''),
                    }
                    smime_dict[sid] = new_smime
                    return new_smime

                @staticmethod
                def update(userId: str = 'me',
                           send_as_email: str = '',
                           id: str = '',
                           smime: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
                    """
                    Updates S/MIME info for a send-as alias.

                    Args:
                        userId: The ID of the user whose S/MIME info is to be updated. Defaults to 'me'.
                        send_as_email: The email address of the send-as alias.
                        id: The ID of the S/MIME info to update.
                        smime: Optional dictionary containing the S/MIME info to update. Defaults to None.

                    Returns:
                        The updated S/MIME info, or None if it does not exist.
                    """
                    _ensure_user(userId)
                    if smime is None:
                        smime = {}
                    send_as_entry = DB['users'][userId]['settings']['sendAs'].get(send_as_email)
                    if not send_as_entry:
                        return None
                    smime_dict = send_as_entry.setdefault('smimeInfo', {})
                    existing = smime_dict.get(id)
                    if not existing:
                        return None
                    existing.update(smime)
                    return existing

                @staticmethod
                def patch(userId: str = 'me',
                          send_as_email: str = '',
                          id: str = '',
                          smime: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
                    """
                    Partially updates S/MIME info for a send-as alias.

                    Args:
                        userId: The ID of the user whose S/MIME info is to be patched. Defaults to 'me'.
                        send_as_email: The email address of the send-as alias.
                        id: The ID of the S/MIME info to patch.
                        smime: Optional dictionary containing the S/MIME info to patch. Defaults to None.

                    Returns:
                        The patched S/MIME info, or None if it does not exist.
                    """
                    return Users.Settings.SendAs.SmimeInfo.update(userId, send_as_email, id, smime)

                @staticmethod
                def delete(userId: str = 'me',
                           send_as_email: str = '', id: str = '') -> None:
                    """
                    Deletes S/MIME info for a send-as alias.

                    Args:
                        userId: The ID of the user whose S/MIME info is to be deleted. Defaults to 'me'.
                        send_as_email: The email address of the send-as alias.
                        id: The ID of the S/MIME info to delete.
                    """
                    _ensure_user(userId)
                    send_as_entry = DB['users'][userId]['settings']['sendAs'].get(send_as_email)
                    if send_as_entry:
                        smime_dict = send_as_entry.setdefault('smimeInfo', {})
                        smime_dict.pop(id, None)

                @staticmethod
                def setDefault(userId: str = 'me',
                                send_as_email: str = '',
                                id: str = '') -> Optional[Dict[str, Any]]:
                    """
                    Sets default S/MIME info for a send-as alias.

                    Args:
                        userId: The ID of the user whose S/MIME info is to be set as default. Defaults to 'me'.
                        send_as_email: The email address of the send-as alias.
                        id: The ID of the S/MIME info to set as default.

                    Returns:
                        The S/MIME info set as default, or None if it does not exist.
                    """
                    _ensure_user(userId)
                    send_as_entry = DB['users'][userId]['settings']['sendAs'].get(send_as_email)
                    if not send_as_entry:
                        return None
                    smime_dict = send_as_entry.setdefault('smimeInfo', {})
                    existing = smime_dict.get(id)
                    if not existing:
                        return None
                    # set a field 'default' = True, un-set from others
                    for _, val in smime_dict.items():
                        val.pop('default', None)
                    existing['default'] = True
                    return existing
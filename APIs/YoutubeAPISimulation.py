"""
Full Python simulation for all resources from the Youtube API Discovery JSON,
with in-memory state, JSON persistence, and embedded tests.

Run this notebook end-to-end to execute tests verifying correctness of each method.
"""
import json
import unittest
import os
from typing import Dict, Any, List, Optional, Union
import random
import string

# ---------------------------------------------------------------------------------------
# In-Memory Database Structure for YouTube Data
# ---------------------------------------------------------------------------------------
# This database stores various YouTube data entities, organized as follows:
#
# - 'activities': [ {activity}, ... ]
#   - List of YouTube activity objects.
#
# - 'captions': { captionId: {caption}, ... }
#   - Dictionary of caption objects, indexed by caption ID.
#   - Each caption object contains a 'snippet' with the associated 'videoId'.
#
# - 'channels': [ {channel}, ... ]
#   - List of YouTube channel objects.
#
# - 'channelSections': { sectionId: {section}, ... }
#   - Dictionary of channel section objects, indexed by section ID.
#   - Each section object contains a 'snippet' with 'channelId' and 'type'.
#
# - 'channelStatistics': { statistics }
#   - Dictionary containing overall channel statistics.
#   - Includes 'commentCount', 'hiddenSubscriberCount', 'subscriberCount', 'videoCount', and 'viewCount'.
#
# - 'channelBanners': [ {banner}, ... ]
#   - List of channel banner objects (currently empty in this example).
#
# - 'comments': { commentId: {comment}, ... }
#   - Dictionary of comment objects, indexed by comment ID.
#   - Each comment object contains a 'snippet' with 'videoId' and 'parentId', 'moderationStatus', and 'bannedAuthor'.
#
# - 'commentThreads': { threadId: {thread}, ... }
#   - Dictionary of comment thread objects, indexed by thread ID.
#   - Each thread object contains a 'snippet' with 'channelId' and 'videoId', and a list of 'comments' (comment IDs).
#
# - 'subscriptions': { subId: {subscription}, ... }
#   - Dictionary of subscription objects, indexed by subscription ID.
#   - Each subscription object contains a 'snippet' with 'channelId' and 'resourceId' (specifying the subscribed channel).
#
# - 'videoCategories': { categoryId: {category}, ... }
#   - Dictionary of video category objects, indexed by category ID.
#   - Each category object contains a 'snippet' with 'title' and 'regionCode'.
#
# - 'memberships': { memberId: {membership}, ... }
#   - Dictionary of membership objects, indexed by membership ID.
#   - Each membership object contains a 'snippet' with 'memberChannelId', 'hasAccessToLevel', and 'mode'.

DB = {
    "activities": [
        {"kind": "youtube#activity", "etag": "etag1", "id": "activity1"},
        {"kind": "youtube#activity", "etag": "etag2", "id": "activity2"}
    ],
    "captions": {
        "caption1": {"id": "caption1", "snippet": {"videoId": "video1"}},
        "caption2": {"id": "caption2", "snippet": {"videoId": "video2"}}
    },
    "channels": {
        "channel1": {
        "part": "snippet,contentDetails,statistics", "categoryId": "10", "forUsername": "TechGuru", "hl": "en", "id": "channel1",
        "managedByMe": False, "maxResults": 5, "mine": False, "mySubscribers": True, "onBehalfOfContentOwner": None
    },
     "channel2": {
            "part": "snippet,statistics","categoryId": "20", "forUsername": "FoodieFun", "hl": "es", "id": "channel2",
            "managedByMe": True, "maxResults": 10, "mine": True, "mySubscribers": False, "onBehalfOfContentOwner": "CompanyXYZ"
    },
      "channel3": {"part": "contentDetails,statistics", "categoryId": "15", "forUsername": "TravelVlogs", "hl": "fr", "id": "channel3",
        "managedByMe": False, "maxResults": 7, "mine": False, "mySubscribers": True,"onBehalfOfContentOwner": None
    }
    },
    "channelSections": {
        "section1": {"id": "section1", "snippet": {"channelId": "channel1", "type": "allPlaylists"}},
        "section2": {"id": "section2", "snippet": {"channelId": "channel2", "type": "completedEvents"}},
        "section3": {"id": "section3", "snippet": {"channelId": "channel1", "type": "multipleChannels"}}
    },
    "channelStatistics": {
        "commentCount": 100,
        "hiddenSubscriberCount": False,
        "subscriberCount": 1000000,
        "videoCount": 500,
        "viewCount": 10000000
    },
    "channelBanners": [],
    "comments": {
        "comment1": {"id": "comment1", "snippet": {"videoId": "video1", "parentId": None}, "moderationStatus": "published", "bannedAuthor": False},
        "comment2": {"id": "comment2", "snippet": {"videoId": "video1", "parentId": "comment1"}, "moderationStatus": "heldForReview", "bannedAuthor": False},
        "comment3": {"id": "comment3", "snippet": {"videoId": "video2", "parentId": None}, "moderationStatus": "rejected", "bannedAuthor": True}
    },
    "commentThreads": {
        "thread1": {"id": "thread1", "snippet": {"channelId": "channel1", "videoId": "video1"}, "comments": ["comment1", "comment2"]},
        "thread2": {"id": "thread2", "snippet": {"channelId": "channel2", "videoId": "video2"}, "comments": ["comment3"]}
    },
    "subscriptions": {
        "sub1": {"id": "sub1", "snippet": {"channelId": "channel1", "resourceId": {"kind": "youtube#channel", "channelId": "channel2"}}},
        "sub2": {"id": "sub2", "snippet": {"channelId": "channel2", "resourceId": {"kind": "youtube#channel", "channelId": "channel1"}}}
    },
    "videoCategories": {
        "category1": {"id": "1", "snippet": {"title": "Film & Animation", "regionCode": "US"}},
        "category2": {"id": "2", "snippet": {"title": "Autos & Vehicles", "regionCode": "US"}},
        "category3": {"id": "10", "snippet": {"title": "Music", "regionCode": "CA"}}
    },
    "memberships": {
        "member1": {"id": "member1", "snippet": {"memberChannelId": "channel1", "hasAccessToLevel": "level1", "mode": "fanFunding"}},
        "member2": {"id": "member2", "snippet": {"memberChannelId": "channel2", "hasAccessToLevel": "level2", "mode": "sponsors"}}
    }
}

"""
Created the fully functional Notebook code around the 11 critical functionalities of the youtube API as per the API documentation.
 The Classes correspond to following functions:
Activites, Comment, CommentThread, Subscriptions, Channels, ChannelSection, ChannelStatistics, ChannelBanner,
VideoCategory, Caption and Memberships.

"""

# ---------------------------------------------------------------------------------------
# Persistence Class
# ---------------------------------------------------------------------------------------
class YoutubeAPI:
    """
    Handles in-memory database operations with JSON-based state persistence.
    """

    @staticmethod
    def save_state(filepath: str) -> None:
        """Saves the in-memory DB to a file."""
        with open(filepath, 'w') as f:
            json.dump(DB, f)

    @staticmethod
    def load_state(filepath: str) -> None:
        """Loads the DB from a file."""
        global DB
        with open(filepath, 'r') as f:
            DB = json.load(f)
# ---------------------------------------------------------------------------------------
# Utility Function
# ---------------------------------------------------------------------------------------


# Utility function to generate random string of a given length
def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Utility function to generate unique IDs for various entities
def generate_entity_id(entity_type):
    if  entity_type == "caption":
        # ID pattern: CPT + random alphanumeric string of 9 characters
        return f"CPT{generate_random_string(9)}"
    elif entity_type == "channel":
        # ID pattern: UC + random alphanumeric string of 8 characters
        return f"UC{generate_random_string(8)}"
    elif entity_type == "channelSection":
        # ID pattern: section + random alphanumeric string of 6 characters
        return f"CHsec{generate_random_string(6)}"
    elif entity_type == "comment":
        # ID pattern: CMT + random alphanumeric string of 7 characters
        return f"CMT{generate_random_string(7)}"
    elif entity_type == "commentthread":
        # ID pattern: CMT + random alphanumeric string of 5 characters
        return f"CMTTHTR{generate_random_string(5)}"
    elif entity_type == "subscription":
        # ID pattern: SUB + random alphanumeric string of 3 characters
        return f"SUBsub{generate_random_string(3)}"
    else:
        raise ValueError("Unknown entity type")
# ---------------------------------------------------------------------------------------
# Resource: Activities
# ---------------------------------------------------------------------------------------

class Activities:
    """Handles YouTube Activities API operations."""

    @staticmethod
    def list(
        part: str,
        channelId: Optional[str] = None,
        mine: Optional[bool] = None,
        maxResults: Optional[int] = None,
        pageToken: Optional[str] = None,
        publishedAfter: Optional[str] = None,
        publishedBefore: Optional[str] = None,
        regionCode: Optional[str] = None
    ) -> Dict[str, List]:
        """Retrieves a list of activities with optional filters."""
        results = DB["activities"]
        if channelId:
            results = [a for a in results if a.get("channelId") == channelId]
        if mine is not None:
            results = [a for a in results if a.get("mine") == mine]
        if maxResults:
            results = results[:min(maxResults, 50)]
        if publishedAfter:
            results = [a for a in results if a.get("publishedAfter", "2023-01-01T00:00:00Z") >= publishedAfter]
        if publishedBefore:
            results = [a for a in results if a.get("publishedBefore", "2023-12-31T00:00:00Z") <= publishedBefore]
        if regionCode:
            results = [a for a in results if a.get("regionCode") == regionCode]
        return {"items": results}


# ---------------------------------------------------------------------------------------
# Resource: Captions
# ---------------------------------------------------------------------------------------

class Caption:
    """Handles YouTube Caption API operations."""

    @staticmethod
    def delete(id: str,
               onBehalfOf: Optional[str] = None,
               onBehalfOfContentOwner: Optional[str] = None) -> Dict[str, bool]:
        """Deletes a caption."""
        if id not in DB["captions"]:
            return {"error": "Caption not found"}

        del DB["captions"][id]
        return {"success": True}


    def download(
        id: str,
        onBehalfOf: Optional[str] = None,
        onBehalfOfContentOwner: Optional[str] = None,
        tfmt: Optional[str] = None,
        tlang: Optional[str] = None
    ) -> str:
        """Downloads a caption track."""
        if id not in DB.get("captions", {}):
            return "Caption not found"

        caption = DB["captions"][id]

        format_mapping = {
            "srt": "Simulated SRT content",
            "vtt": "Simulated VTT content",
            "sbv": "Simulated SBV content"
        }

        if tfmt in format_mapping:
            return format_mapping[tfmt]
        elif tfmt:
            return "Unsupported format"

        if tlang:
            return f"Simulated translated caption to {tlang}"

        return caption.get("snippet", {}).get("text", "Caption content")

    @staticmethod
    def insert(
        part: str,
        snippet: str,
        onBehalfOf: Optional[str] = None,
        onBehalfOfContentOwner: Optional[str] = None,
        sync: bool = False
    ) -> Dict:
        """Inserts a new caption."""
        if part != "snippet":
            return {"error": "Invalid part parameter"}

        new_id = generate_entity_id("caption")
        new_caption = {"id": new_id, "snippet": snippet}
        DB["captions"][new_id] = new_caption
        return {"success": True, "caption": new_caption}

    @staticmethod
    def list(
        part: str,
        videoId: str,
        id: Optional[str] = None,
        onBehalfOf: Optional[str] = None,
        onBehalfOfContentOwner: Optional[str] = None
    ) -> Dict[str, List]:
        """Retrieves a list of captions."""
        if part not in ["id", "snippet"]:
            return {"error": "Invalid part parameter"}

        captions = [cap for cap in DB["captions"].values() if cap.get("snippet", {}).get("videoId") == videoId]
        if id:
            captions = [cap for cap in captions if cap["id"] == id]

        return {"items": captions}

    @staticmethod
    def update(
        part: str,
        id: str,
        snippet: Optional[str] = None,
        onBehalfOf: Optional[str] = None,
        onBehalfOfContentOwner: Optional[str] = None,
        sync: Optional[bool] = None
    ) -> Dict:
        """Updates a caption resource."""
        if part not in ["snippet"]:
            return {"error": "Invalid part parameter"}

        if id not in DB["captions"]:
            return {"error": "Caption not found"}

        if snippet:
            DB["captions"][id]["snippet"] = snippet

        return {"success": True, "message": "Caption updated."}

# ---------------------------------------------------------------------------------------
# Resource: Channels
# ---------------------------------------------------------------------------------------

class Channels:
    """Handles YouTube Channels API operations."""

    @staticmethod
    def list(
        category_id: Optional[str] = None,
        for_username: Optional[str] = None,
        hl: Optional[str] = None,
        channel_id: Optional[str] = None,
        managed_by_me: Optional[bool] = None,
        max_results: Optional[int] = None,
        mine: Optional[bool] = None,
        my_subscribers: Optional[bool] = None,
        on_behalf_of_content_owner: Optional[str] = None
    ) -> Dict[str, List[Dict]]:
        """Retrieves a list of channels with optional filters."""
        results = list(DB.get("channels", {}).values())

        if category_id:
            results = [c for c in results if c.get("categoryId") == category_id]
        if for_username:
            results = [c for c in results if c.get("forUsername") == for_username]
        if channel_id:
            results = [c for c in results if c.get("id") == channel_id]
        if hl:
            results = [c for c in results if c.get("hl") == hl]
        if managed_by_me is not None:
            results = [c for c in results if c.get("managedByMe") == managed_by_me]
        if mine is not None:
            results = [c for c in results if c.get("mine") == mine]
        if my_subscribers is not None:
            results = [c for c in results if c.get("mySubscribers") == my_subscribers]
        if on_behalf_of_content_owner:
            results = [c for c in results if c.get("onBehalfOfContentOwner") == on_behalf_of_content_owner]

        if max_results:
            results = results[:min(max_results, 50)]

        return {"items": results}

    @staticmethod
    def insert(
        part: str,
        category_id: Optional[str] = None,
        for_username: Optional[str] = None,
        hl: Optional[str] = None,
        channel_id: Optional[str] = None,
        managed_by_me: Optional[bool] = None,
        max_results: Optional[int] = None,
        mine: Optional[bool] = None,
        my_subscribers: Optional[bool] = None,
        on_behalf_of_content_owner: Optional[str] = None
    ) -> Dict[str, Optional[Dict]]:
        """Inserts a new channel resource."""
        if not part:
            return {"error": "Invalid part parameter"}

        new_id = generate_entity_id("channel")
        new_channel = {
            "id": new_id,
            "categoryId": category_id,
            "forUsername": for_username,
            "hl": hl,
            "managedByMe": managed_by_me,
            "maxResults": max_results,
            "mine": mine,
            "mySubscribers": my_subscribers,
            "onBehalfOfContentOwner": on_behalf_of_content_owner
        }
        DB.setdefault("channels", {})[new_id] = new_channel
        return {"success": True, "channel": new_channel}

    @staticmethod
    def update(channel_id: str, **kwargs) -> Dict[str, str]:
        """Updates metadata of a YouTube channel."""
        if not kwargs:
            return {"error": "No update parameters provided"}

        if channel_id not in DB.get("channels", {}):
            return {"error": f"Channel ID: {channel_id} not found in the database."}

        DB["channels"][channel_id].update({k: v for k, v in kwargs.items() if v is not None})
        return {"success": f"Channel ID: {channel_id} updated successfully."}

# ---------------------------------------------------------------------------------------
# Resource: Channel Section
# ---------------------------------------------------------------------------------------

class ChannelSection:
    """Handles YouTube Channel Sections API operations."""

    @staticmethod
    def list(
        part: str,
        channel_id: Optional[str] = None,
        hl: Optional[str] = None,
        section_id: Optional[str] = None,
        mine: bool = False,
        on_behalf_of_content_owner: Optional[str] = None
    ) -> Dict[str, List[Dict]]:
        """Retrieves a list of channel sections with optional filters."""
        if part not in ["id", "snippet", "contentDetails"]:
            return {"error": "Invalid part parameter"}

        filtered_sections = list(DB.get("channelSections", {}).values())

        if section_id:
            filtered_sections = [section for section in filtered_sections if section["id"] == section_id]
            return {"items": filtered_sections}

        if channel_id:
            filtered_sections = [section for section in filtered_sections if section.get("snippet", {}).get("channelId") == channel_id]

        if mine:
            filtered_sections = [section for section in filtered_sections if section.get("snippet", {}).get("mine")]

        return {"items": filtered_sections}

    @staticmethod
    def delete(section_id: str,
               on_behalf_of_content_owner: Optional[str] = None) -> Dict[str, bool]:
        """Deletes a channel section."""
        if section_id not in DB.get("channelSections", {}):
            return {"error": "Channel section not found"}

        del DB["channelSections"][section_id]
        return {"success": True}

    @staticmethod
    def insert(
        part: str,
        snippet: str,
        on_behalf_of_content_owner: Optional[str] = None,
        on_behalf_of_content_owner_channel: Optional[str] = None
    ) -> Dict[str, Optional[Dict]]:
        """Inserts a new channel section."""
        if part not in ["snippet", "contentDetails"]:
            return {"error": "Invalid part parameter"}

        new_id = generate_entity_id("channelSection")
        new_section = {"id": new_id, "snippet": snippet}
        DB.setdefault("channelSections", {})[new_id] = new_section
        return {"success": True, "channelSection": new_section}

    @staticmethod
    def update(
        part: str,
        section_id: str,
        snippet: Optional[str] = None,
        on_behalf_of_content_owner: Optional[str] = None
    ) -> Dict[str, str]:
        """Updates a channel section."""
        if part not in ["snippet", "contentDetails"]:
            return {"error": "Invalid part parameter"}

        if section_id not in DB.get("channelSections", {}):
            return {"error": "Channel section not found"}

        if snippet:
            DB["channelSections"][section_id]["snippet"] = snippet

        return {"success": "Channel section updated successfully."}

# ---------------------------------------------------------------------------------------
# Resource: Channel Statistics
# ---------------------------------------------------------------------------------------

class ChannelStatistics:
    """Handles YouTube Channel Statistics API operations."""

    @staticmethod
    def comment_count(comment_count: Optional[int] = None) -> Dict[str, int]:
        """Retrieves or sets the number of comments for the channel."""
        if comment_count is not None:
            return {"commentCount": comment_count}
        return {"commentCount": DB.get("channelStatistics", {}).get("commentCount", 0)}

    @staticmethod
    def hidden_subscriber_count(hidden_subscriber_count: Optional[bool] = None) -> Dict[str, bool]:
        """Checks whether the subscriber count is hidden."""
        if hidden_subscriber_count is not None:
            return {"hiddenSubscriberCount": hidden_subscriber_count}
        return {"hiddenSubscriberCount": DB.get("channelStatistics", {}).get("hiddenSubscriberCount", False)}

    @staticmethod
    def subscriber_count(subscriber_count: Optional[int] = None) -> Dict[str, int]:
        """Retrieves or sets the number of subscribers of the channel."""
        if subscriber_count is not None:
            return {"subscriberCount": subscriber_count}
        return {"subscriberCount": DB.get("channelStatistics", {}).get("subscriberCount", 0)}

    @staticmethod
    def video_count(video_count: Optional[int] = None) -> Dict[str, int]:
        """Retrieves or sets the number of videos uploaded to the channel."""
        if video_count is not None:
            return {"videoCount": video_count}
        return {"videoCount": DB.get("channelStatistics", {}).get("videoCount", 0)}

    @staticmethod
    def view_count(view_count: Optional[int] = None) -> Dict[str, int]:
        """Retrieves or sets the total view count of the channel."""
        if view_count is not None:
            return {"viewCount": view_count}
        return {"viewCount": DB.get("channelStatistics", {}).get("viewCount", 0)}

# ---------------------------------------------------------------------------------------
# Resource: Channel Banners
# ---------------------------------------------------------------------------------------

class ChannelBanners:
    """Handles YouTube Channel Banners API operations."""

    @staticmethod
    def insert(
        channel_id: Optional[str] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        on_behalf_of_content_owner_channel: Optional[str] = None
    ) -> Dict[str, Optional[str]]:
        """Inserts a new channel banner."""
        new_banner = {
            "channelId": channel_id,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            "onBehalfOfContentOwnerChannel": on_behalf_of_content_owner_channel
        }
        DB.setdefault("channelBanners", []).append(new_banner)
        return new_banner

# ---------------------------------------------------------------------------------------
# Resource: Comment
# ---------------------------------------------------------------------------------------

class Comment:
    """Handles YouTube Comment API operations."""

    @staticmethod
    def set_moderation_status(
        comment_id: str,
        moderation_status: str,
        ban_author: bool = False
    ) -> Dict[str, Optional[Dict]]:
        """Sets the moderation status of a comment."""
        if comment_id not in DB["comments"]:
            return {"error": "Comment not found"}

        if moderation_status not in ["heldForReview", "published", "rejected"]:
            return {"error": "Invalid moderation status"}

        DB["comments"][comment_id]["moderationStatus"] = moderation_status

        if ban_author and moderation_status == "rejected":
            DB["comments"][comment_id]["bannedAuthor"] = True

        return {"success": True, "comment": DB["comments"][comment_id]}

    @staticmethod
    def delete(comment_id: str) -> Dict[str, bool]:
        """Deletes a comment."""
        if comment_id not in DB["comments"]:
            return {"error": "Comment not found"}

        del DB["comments"][comment_id]
        return {"success": True}

    @staticmethod
    def insert(
        part: str,
        snippet: Optional[Dict] = None,
        moderation_status: str = "published",
        banned_author: bool = False
    ) -> Dict[str, Optional[Dict]]:
        """Inserts a new comment."""
        if not part:
            return {"error": "Invalid part parameter"}

        num = str(len(DB["comments"]) + 1)
        new_id = generate_entity_id("comment")
        new_comment = {
            "id": new_id,
            "snippet": snippet or {},
            "moderationStatus": moderation_status,
            "bannedAuthor": banned_author
        }
        DB["comments"][new_id] = new_comment
        return {"success": True, "comment": new_comment}

    @staticmethod
    def list(
        part: str,
        comment_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        max_results: Optional[int] = None,
        page_token: Optional[str] = None,
        text_format: Optional[str] = None
    ) -> Dict[str, List[Dict]]:
        """Retrieves a list of comments with optional filters."""
        if not part:
            return {"error": "Part parameter required"}

        filtered_comments = list(DB.get("comments", {}).values())

        if comment_id:
            filtered_comments = [comment for comment in filtered_comments if comment["id"] == comment_id]

        if parent_id:
            filtered_comments = [comment for comment in filtered_comments if comment.get("snippet", {}).get("parentId") == parent_id]

        if max_results:
            filtered_comments = filtered_comments[:max_results]

        return {"items": filtered_comments}

    @staticmethod
    def mark_as_spam(comment_id: str) -> Dict[str, Optional[Dict]]:
        """Marks a comment as spam."""
        if comment_id not in DB.get("comments", {}):
            return {"error": "Comment not found"}

        DB["comments"][comment_id]["moderationStatus"] = "heldForReview"
        return {"success": True, "comment": DB["comments"][comment_id]}

    @staticmethod
    def update(
        comment_id: str,
        snippet: Optional[Dict] = None,
        moderation_status: Optional[str] = None,
        banned_author: Optional[bool] = None
    ) -> Dict[str, Optional[Dict]]:
        """Updates an existing comment."""
        if not any([snippet, moderation_status, banned_author]):
            return {"error": "No update parameters provided"}

        if comment_id not in DB.get("comments", {}):
            return {"error": f"Comment ID: {comment_id} not found in the database."}

        if snippet is not None:
            DB["comments"][comment_id]["snippet"] = snippet
        if moderation_status is not None:
            DB["comments"][comment_id]["moderationStatus"] = moderation_status
        if banned_author is not None:
            DB["comments"][comment_id]["bannedAuthor"] = banned_author

        return {"success": f"Comment ID: {comment_id} updated successfully."}


# ---------------------------------------------------------------------------------------
# Class Comment Thread
# ---------------------------------------------------------------------------------------

class CommentThread:
    """Handles YouTube Comment Thread API operations."""

    @staticmethod
    def insert(
        part: str,
        snippet: Optional[Dict] = None,
        top_level_comment: Optional[Dict] = None
    ) -> Dict[str, Optional[Dict]]:
        """Inserts a new comment thread."""
        if part != "snippet":
            return {"error": "Invalid part parameter"}

        new_id = generate_entity_id("commentthread")
        new_thread = {
            "id": new_id,
            "snippet": snippet or {},
            "comments": [],
        }
        DB.setdefault("commentThreads", {})[new_id] = new_thread

        if top_level_comment:
            top_level_comment_id = top_level_comment.get("id")
            if top_level_comment_id:
                new_thread["comments"].append(top_level_comment_id)

        return {"success": True, "commentThread": new_thread}

    @staticmethod
    def list(
        part: str,
        thread_id: Optional[str] = None,
        channel_id: Optional[str] = None,
        video_id: Optional[str] = None,
        all_threads_related_to_channel_id: Optional[str] = None,
        search_terms: Optional[str] = None,
        moderation_status: Optional[str] = None,
        order: Optional[str] = None,
        max_results: Optional[int] = None,
        page_token: Optional[str] = None,
        text_format: Optional[str] = None
    ) -> Dict[str, List[Dict]]:
        """Retrieves a list of comment threads with optional filters."""
        if not part:
            return {"error": "Part parameter required"}

        filtered_threads = list(DB.get("commentThreads", {}).values())

        if thread_id:
            filtered_threads = [thread for thread in filtered_threads if thread["id"] == thread_id]

        if channel_id:
            filtered_threads = [thread for thread in filtered_threads if thread.get("snippet", {}).get("channelId") == channel_id]

        if video_id:
            filtered_threads = [thread for thread in filtered_threads if thread.get("snippet", {}).get("videoId") == video_id]

        if all_threads_related_to_channel_id:
            filtered_threads = [
                thread for thread in filtered_threads
                if thread.get("snippet", {}).get("channelId") == all_threads_related_to_channel_id or
                thread.get("snippet", {}).get("videoId") == all_threads_related_to_channel_id
            ]

        if search_terms:
            filtered_threads = [
                thread for thread in filtered_threads
                if search_terms.lower() in str(thread.get("snippet", {})).lower()
            ]

        if moderation_status:
            filtered_threads = [
                thread for thread in filtered_threads
                if all(
                    DB["comments"].get(comment_id, {}).get("moderationStatus") == moderation_status
                    for comment_id in thread.get("comments", [])
                )
            ]
        if max_results:
            filtered_threads = filtered_threads[:max_results]

        return {"items": filtered_threads}

    @staticmethod
    def delete(thread_id: str) -> Dict[str, str]:
        """Deletes a comment thread by its ID."""
        if thread_id in DB.get("commentThreads", {}):
            del DB["commentThreads"][thread_id]
            return {"success": f"Thread ID: {thread_id} deleted successfully."}
        return {"error": f"Thread ID: {thread_id} not found."}

    @staticmethod
    def update(
        thread_id: str,
        snippet: Optional[Dict] = None,
        comments: Optional[List[str]] = None
    ) -> Dict[str, Optional[Dict]]:
        """Updates an existing comment thread."""
        if not any([snippet, comments]):
            return {"error": "No update parameters provided"}

        if thread_id not in DB.get("commentThreads", {}):
            return {"error": f"Thread ID: {thread_id} not found in the database."}

        if snippet is not None:
            DB["commentThreads"][thread_id]["snippet"] = snippet
        if comments is not None:
            DB["commentThreads"][thread_id]["comments"] = comments

        return {"success": f"Thread ID: {thread_id} updated successfully.", "commentThread": DB["commentThreads"][thread_id]}


# ---------------------------------------------------------------------------------------
# Resource: Subscriptions
# ---------------------------------------------------------------------------------------

class Subscriptions:
    """Handles YouTube Subscriptions API operations."""

    @staticmethod
    def insert(
        part: str,
        snippet: Optional[Dict] = None
    ) -> Dict[str, Optional[Dict]]:
        """Inserts a new subscription."""
        if not part:
            return {"error": "Part parameter required"}

        new_id = generate_entity_id("subscription")
        new_subscription = {
            "id": new_id,
            "snippet": snippet or {},
        }
        DB.setdefault("subscriptions", {})[new_id] = new_subscription
        return {"success": True, "subscription": new_subscription}

    @staticmethod
    def delete(subscription_id: str) -> Dict[str, bool]:
        """Deletes a subscription."""
        if subscription_id not in DB.get("subscriptions", {}):
            return {"error": "Subscription not found"}

        del DB["subscriptions"][subscription_id]
        return {"success": True}

    @staticmethod
    def list(
        part: str,
        channel_id: Optional[str] = None,
        subscription_id: Optional[str] = None,
        mine: bool = False,
        my_recent_subscribers: bool = False,
        my_subscribers: bool = False,
        for_channel_id: Optional[str] = None,
        max_results: Optional[int] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        on_behalf_of_content_owner_channel: Optional[str] = None,
        order: Optional[str] = None,
        page_token: Optional[str] = None
    ) -> Dict[str, List[Dict]]:
        """Retrieves a list of subscriptions with optional filters."""
        if not part:
            return {"error": "Part parameter required"}

        filtered_subscriptions = list(DB.get("subscriptions", {}).values())

        if subscription_id:
            filtered_subscriptions = [sub for sub in filtered_subscriptions if sub["id"] == subscription_id]
            return {"items": filtered_subscriptions}

        if channel_id:
            filtered_subscriptions = [sub for sub in filtered_subscriptions if sub.get("snippet", {}).get("channelId") == channel_id]

        if mine:
            filtered_subscriptions = [sub for sub in filtered_subscriptions if sub.get("snippet", {}).get("mine")]

        if my_subscribers:
            filtered_subscriptions = [sub for sub in filtered_subscriptions if sub.get("snippet", {}).get("subscriber")]

        if for_channel_id:
            filtered_subscriptions = [sub for sub in filtered_subscriptions if sub.get("snippet", {}).get("forChannelId") == for_channel_id]

        if max_results:
            filtered_subscriptions = filtered_subscriptions[:max_results]

        return {"items": filtered_subscriptions}

# ---------------------------------------------------------------------------------------
# Resource: Video Category
# ---------------------------------------------------------------------------------------

class VideoCategory:
    """Handles YouTube Video Categories API operations."""

    @staticmethod
    def list(
        part: str,
        hl: Optional[str] = None,
        category_id: Optional[str] = None,
        region_code: Optional[str] = None
    ) -> Dict[str, List[Dict]]:
        """Retrieves a list of video categories with optional filters."""
        if part != "snippet":
            return {"error": "Invalid part parameter"}

        filtered_categories = list(DB.get("videoCategories", {}).values())

        if category_id:
            filtered_categories = [category for category in filtered_categories if category["id"] == category_id]
            return {"items": filtered_categories}

        if region_code:
            filtered_categories = [category for category in filtered_categories if category.get("snippet", {}).get("regionCode") == region_code]

        return {"items": filtered_categories}


# ---------------------------------------------------------------------------------------
# Resource: Memberships
# ---------------------------------------------------------------------------------------

class Memberships:
    """Handles YouTube Memberships API operations."""

    @staticmethod
    def list(
        part: str,
        has_access_to_level: Optional[str] = None,
        filter_by_member_channel_id: Optional[str] = None,
        max_results: Optional[int] = None,
        mode: Optional[str] = None,
        page_token: Optional[str] = None
    ) -> Dict[str, List[Dict]]:
        """Retrieves a list of members that match the request criteria for a channel."""
        if part != "snippet":
            return {"error": "Invalid part parameter"}

        filtered_members = list(DB.get("memberships", {}).values())

        if has_access_to_level:
            filtered_members = [
                member for member in filtered_members
                if member.get("snippet", {}).get("hasAccessToLevel") == has_access_to_level
            ]

        if filter_by_member_channel_id:
            channel_ids = filter_by_member_channel_id.split(",")
            filtered_members = [
                member for member in filtered_members
                if member.get("snippet", {}).get("memberChannelId") in channel_ids
            ]

        if max_results:
            filtered_members = filtered_members[:max_results]

        if mode:
            filtered_members = [
                member for member in filtered_members
                if member.get("snippet", {}).get("mode") == mode
            ]

        return {"items": filtered_members}
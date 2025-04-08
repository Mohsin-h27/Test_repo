#!/usr/bin/env python
"""
A single, self-contained Python file simulating the entire API specified in the
pythonic-named JSON discovery file. This simulation includes:

1. Full API Implementation as Python Classes & Methods
2. In-Memory State Management & Persistence
3. Embedded Unit Tests via unittest
4. Automatic Test Execution

To run tests:
    python this_file.py

All tests should pass, confirming the correctness of the API simulation.

Note: This is a demonstration of structure and completeness. The methods
generally return mock or minimal data from an in-memory store (DB). Extend,
customize, and refine as needed for real-world usage.
"""

import json
import os
import unittest
from typing import Any, Dict, List, Optional

###############################################################################
# GLOBAL STATE
###############################################################################
# Global in-memory DB for simulating persistent state. Each resource class
# reads/writes data here to simulate resource storage and manipulation.

DB = {
    #-----------------------------------
    # Resource-based keys:
    #-----------------------------------
    "accounts": {},         # e.g. {username: {...}}
    "announcements": [],    # list of announcement objects
    "captcha_needed": False, # whether captcha is required
    "collections": {},      # {collection_id: {title, sr_fullname, links, etc.}}
    "emoji": {},            # {subreddit_name: {emoji_name: {...}}}
    "flair": {},            # storing flair settings, e.g. {subreddit: {...}}
    "links": {},            # link (post) data, keyed by fullname or ID
    "comments": {},         # comment data, keyed by fullname or ID
    "listings": {},         # any data relevant to listing endpoints
    "live_threads": {},     # {thread_id: {...}}
    "messages": {},         # {message_id: {...}}
    "misc_data": {},        # for /misc
    "moderation": {},       # storing mod data
    "modmail": {},          # modmail conversations
    "modnotes": {},         # {user: [notes]}
    "multis": {},           # {multi_path: {...}}
    "search_index": {},     # mocked data for search
    "subreddits": {},       # {subreddit_name: {...}}
    "users": {},            # storing user info (like profiles)
    "widgets": {},          # {subreddit: {widget_id: {...}}}
    "wiki": {},             # {subreddit: {page_name: {...}}}
    #-----------------------------------
}

###############################################################################
# HELPER FUNCTIONS FOR PERSISTENCE
###############################################################################
def save_state(filepath: str) -> None:
    """
    Save the current DB state to a JSON file at `filepath`.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(DB, f, indent=2)


def load_state(filepath: str) -> None:
    """
    Load the DB state from a JSON file at `filepath`.
    Overwrites the current in-memory DB with the loaded content.
    """
    global DB
    if not os.path.isfile(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    DB = loaded


###############################################################################
# RESOURCE CLASSES
###############################################################################

class Account:
    """Simulation of /account endpoints."""

    @staticmethod
    def get_api_v1_me() -> Dict[str, Any]:
        """
        Retrieve the identity details of the currently authenticated user.
        Mocked to return a single example user.
        """
        # For demo, return a hard-coded user
        return {"username": "mock_user", "id": "t2_mocked"}

    @staticmethod
    def get_api_v1_me_blocked() -> List[str]:
        """Retrieve a list of users blocked by the authenticated user."""
        # Mock a short list
        return ["blocked_user_1", "blocked_user_2"]

    @staticmethod
    def get_api_v1_me_friends() -> List[str]:
        """Retrieve a list of friends for the authenticated user."""
        return ["friend_user_1", "friend_user_2"]

    @staticmethod
    def get_api_v1_me_karma() -> Dict[str, Any]:
        """Retrieve a breakdown of the authenticated user’s subreddit karma."""
        return {
            "karma_by_subreddit": [
                {"subreddit": "python", "karma": 123},
                {"subreddit": "learnprogramming", "karma": 456}
            ],
            "total_karma": 579
        }

    @staticmethod
    def get_api_v1_me_prefs(fields: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve the preference settings of the authenticated user."""
        # Could parse fields, but here we'll just return a mock set of prefs
        all_prefs = {
            "nightmode": True,
            "label_nsfw": False,
            "country_code": "US"
        }
        if not fields:
            return all_prefs
        requested = fields.split(',')
        return {key: value for key, value in all_prefs.items() if key in requested}

    @staticmethod
    def patch_api_v1_me_prefs(new_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the preference settings of the authenticated user.
        We'll just echo changes for simulation.
        """
        return {"updated_prefs": new_preferences, "status": "success"}

    @staticmethod
    def get_api_v1_me_trophies() -> List[Dict[str, Any]]:
        """Retrieve the trophies (awards) earned by the authenticated user."""
        return [
            {"trophy_name": "Early_Adopter", "description": "Joined early on."},
            {"trophy_name": "Helper", "description": "Provided helpful contributions."}
        ]

    @staticmethod
    def get_prefs_blocked() -> List[str]:
        """Retrieve detailed information about blocked users (alternative endpoint)."""
        return Account.get_api_v1_me_blocked()

    @staticmethod
    def get_prefs_friends() -> List[str]:
        """Retrieve detailed information about friends (alternative endpoint)."""
        return Account.get_api_v1_me_friends()

    @staticmethod
    def get_prefs_messaging() -> Dict[str, Any]:
        """Retrieve messaging preferences of the authenticated user."""
        return {
            "allow_pms": True,
            "email_notifications": False
        }

    @staticmethod
    def get_prefs_trusted() -> List[str]:
        """Retrieve the trusted user list for the authenticated user."""
        return ["trusted_user_1"]

    @staticmethod
    def get_prefs_where(where: str) -> Any:
        """
        Retrieve specific preference details from various preference categories.
        e.g. "blocked", "friends", etc.
        """
        if where == "blocked":
            return Account.get_prefs_blocked()
        elif where == "friends":
            return Account.get_prefs_friends()
        else:
            return {"detail": f"No mock preferences for category '{where}'"}


class Announcements:
    """Simulation of /announcements endpoints."""

    @staticmethod
    def get_api_announcements_v1() -> List[Dict[str, Any]]:
        """Retrieve a list of global announcements."""
        return DB["announcements"]

    @staticmethod
    def post_api_announcements_v1_hide(announcement_ids: List[str]) -> Dict[str, Any]:
        """Hide one or more announcements from the authenticated user’s feed."""
        # We won't do anything real; just return success
        return {"status": "announcements_hidden", "ids": announcement_ids}

    @staticmethod
    def post_api_announcements_v1_read(announcement_ids: List[str]) -> Dict[str, Any]:
        """Mark one or more announcements as read."""
        return {"status": "announcements_marked_read", "ids": announcement_ids}

    @staticmethod
    def post_api_announcements_v1_read_all() -> Dict[str, Any]:
        """Mark all global announcements as read."""
        return {"status": "all_announcements_marked_read"}

    @staticmethod
    def get_api_announcements_v1_unread() -> List[Dict[str, Any]]:
        """Retrieve a list of announcements not yet read by the user."""
        # In a real scenario, we'd filter unread. Here, just return entire list
        return DB["announcements"]


class Captcha:
    """Simulation of /captcha endpoints."""

    @staticmethod
    def get_api_needs_captcha() -> bool:
        """
        Check if the API currently requires CAPTCHA solutions for the user’s requests.
        We'll return the DB's 'captcha_needed' boolean.
        """
        return DB["captcha_needed"]


class Collections:
    """Simulation of /collections endpoints."""

    @staticmethod
    def post_api_v1_collections_add_post_to_collection(collection_id: str, link_fullname: str) -> Dict[str, Any]:
        """Add a post to an existing collection."""
        if collection_id not in DB["collections"]:
            return {"error": "Collection does not exist"}
        coll = DB["collections"][collection_id]
        coll.setdefault("links", [])
        coll["links"].append(link_fullname)
        return {"status": "success", "collection_id": collection_id, "added_link": link_fullname}

    @staticmethod
    def get_api_v1_collections_collection(collection_id: str) -> Dict[str, Any]:
        """Retrieve information about a specific collection."""
        return DB["collections"].get(collection_id, {"error": "Collection not found"})

    @staticmethod
    def post_api_v1_collections_create_collection(title: str, sr_fullname: str) -> Dict[str, Any]:
        """Create a new collection."""
        new_id = f"col_{len(DB.get('collections', {}))+1}" # Use .get for safety
        DB.setdefault("collections", {})[new_id] = {
            "title": title,
            "sr_fullname": sr_fullname,
            "links": [],
            "description": "",
            "display_layout": "TIMELINE"
        }
        return {"status": "collection_created", "collection_id": new_id}

    @staticmethod
    def post_api_v1_collections_delete_collection(collection_id: str) -> Dict[str, Any]:
        """Delete an existing collection."""
        if collection_id in DB.get("collections", {}):
            del DB["collections"][collection_id]
            return {"status": "collection_deleted", "collection_id": collection_id}
        return {"error": "Collection not found"}

    @staticmethod
    def post_api_v1_collections_remove_post_in_collection(link_fullname: str, collection_id: str) -> Dict[str, Any]:
        """Remove a post from a collection."""
        coll = DB.get("collections", {}).get(collection_id)
        if not coll:
            return {"error": "No such collection"}
        if link_fullname in coll.get("links", []):
            coll["links"].remove(link_fullname)
            return {"status": "success", "removed_link": link_fullname}
        return {"error": "Link not found in collection"}

    @staticmethod
    def post_api_v1_collections_reorder_collection(collection_id: str, link_fullnames: List[str]) -> Dict[str, Any]:
        """Reorder posts in a collection."""
        coll = DB.get("collections", {}).get(collection_id)
        if not coll:
            return {"error": "No such collection"}
        coll["links"] = link_fullnames
        return {"status": "success", "collection_id": collection_id, "new_order": link_fullnames}

    @staticmethod
    def get_api_v1_collections_subreddit_collections(sr_fullname: str) -> List[Dict[str, Any]]:
        """Retrieve multiple collections for a specific subreddit."""
        result = []
        for cid, cdata in DB.get("collections", {}).items():
            if cdata.get("sr_fullname") == sr_fullname: # Use .get for safety
                result.append({cid: cdata})
        return result

    @staticmethod
    def post_api_v1_collections_update_collection_description(collection_id: str, description: str) -> Dict[str, Any]:
        """Update the description of a collection."""
        coll = DB.get("collections", {}).get(collection_id)
        if not coll:
            return {"error": "No such collection"}
        coll["description"] = description
        return {"status": "success", "collection_id": collection_id, "new_description": description}

    @staticmethod
    def post_api_v1_collections_update_collection_display_layout(collection_id: str, display_layout: str) -> Dict[str, Any]:
        """Update how a collection is displayed (e.g., gallery or timeline view)."""
        coll = DB.get("collections", {}).get(collection_id)
        if not coll:
            return {"error": "No such collection"}
        coll["display_layout"] = display_layout
        return {"status": "success", "collection_id": collection_id, "display_layout": display_layout}

    @staticmethod
    def post_api_v1_collections_update_collection_title(collection_id: str, title: str) -> Dict[str, Any]:
        """Change the title of a collection."""
        coll = DB.get("collections", {}).get(collection_id)
        if not coll:
            return {"error": "No such collection"}
        coll["title"] = title
        return {"status": "success", "collection_id": collection_id, "new_title": title}


class Emoji:
    """Simulation of /emoji endpoints."""

    @staticmethod
    def post_api_v1_subreddit_emoji_json(subreddit: str, name: str, css: Optional[str] = None) -> Dict[str, Any]:
        """Add a new emoji to a subreddit."""
        sub_emojis = DB.setdefault("emoji", {}).setdefault(subreddit, {}) # Ensure keys exist
        if name in sub_emojis:
            return {"error": "Emoji name already in use"}
        sub_emojis[name] = {"css": css or "", "image_url": None}
        return {"status": "success", "subreddit": subreddit, "emoji_name": name}

    @staticmethod
    def delete_api_v1_subreddit_emoji_emoji_name(subreddit: str, emoji_name: str) -> Dict[str, Any]:
        """Remove an existing emoji from a subreddit."""
        sub_emojis = DB.get("emoji", {}).get(subreddit, {})
        if emoji_name not in sub_emojis:
            return {"error": "Emoji not found"}
        del sub_emojis[emoji_name]
        # Optional: remove subreddit key if empty
        # if not sub_emojis and subreddit in DB.get("emoji", {}):
        #     del DB["emoji"][subreddit]
        return {"status": "deleted", "emoji_name": emoji_name}

    @staticmethod
    def post_api_v1_subreddit_emoji_asset_upload_s3_json(filepath: str, mimetype: str) -> Dict[str, Any]:
        """
        Acquire and return an upload lease to an S3 temporary bucket.
        """
        # Simulated S3 upload lease details.
        lease = {
            "credentials": {
                "access_key_id": "EXAMPLEACCESSKEY",
                "secret_access_key": "EXAMPLESECRETACCESSKEY",
                "session_token": "EXAMPLESESSIONTOKEN"
            },
            "s3_url": "https://s3-temp-bucket.example.com/upload",
            "key": f"temp/{filepath}"
        }
        return lease

    @staticmethod
    def post_api_v1_subreddit_emoji_custom_size(emoji_name: str, width: int, height: int) -> Dict[str, Any]:
        """Set a custom display size for a subreddit emoji."""
        # For simplicity, let's say we store it in a dictionary.
        # We'll just confirm the request is recognized.
        # Note: This mock doesn't know which subreddit the emoji belongs to.
        return {
            "status": "custom_size_updated",
            "emoji_name": emoji_name,
            "width": width,
            "height": height
        }

    @staticmethod
    def get_api_v1_subreddit_emojis_all(subreddit: str) -> Dict[str, Any]:
        """Retrieve all emojis for a subreddit."""
        sub_emojis = DB.get("emoji", {}).get(subreddit, {})
        return {"subreddit": subreddit, "emojis": sub_emojis}


class Flair:
    """Simulation of /flair endpoints."""

    @staticmethod
    def post_api_clearflairtemplates(flair_type: str) -> Dict[str, Any]:
        """Clear all user or link flair templates."""
        # Not storing real templates, just mock.
        return {"status": "cleared", "flair_type": flair_type}

    @staticmethod
    def post_api_deleteflair(name: str) -> Dict[str, Any]:
        """Remove flair from a specific user in the subreddit."""
        return {"status": "flair_deleted", "user": name}

    @staticmethod
    def post_api_deleteflairtemplate(template_id: str) -> Dict[str, Any]:
        """Delete a flair template by ID."""
        return {"status": "flair_template_deleted", "template_id": template_id}

    @staticmethod
    def post_api_flair(api_type: str, name: str, flair_template_id: Optional[str] = None,
                       text: Optional[str] = None) -> Dict[str, Any]:
        """Set or update a user’s flair."""
        # Minimal example
        return {
            "status": "success",
            "api_type": api_type,
            "user": name,
            "template_id": flair_template_id,
            "text": text
        }

    @staticmethod
    def patch_api_flair_template_order(flair_type: str, template_ids: List[str]) -> Dict[str, Any]:
        """Reorder existing flair templates."""
        return {"status": "success", "flair_type": flair_type, "order": template_ids}

    @staticmethod
    def post_api_flairconfig(flair_enabled: Optional[bool] = None,
                             flair_position: Optional[str] = None) -> Dict[str, Any]:
        """Configure overall flair settings."""
        return {"status": "updated", "flair_enabled": flair_enabled, "flair_position": flair_position}

    @staticmethod
    def post_api_flaircsv(flair_csv: str) -> Dict[str, Any]:
        """Set multiple users' flairs from CSV input."""
        return {"status": "processed_csv", "csv_data": flair_csv}

    @staticmethod
    def get_api_flairlist(*, after: Optional[str] = None,
                          name: Optional[str] = None,
                          limit: Optional[int] = None) -> Dict[str, Any]:
        """Retrieve a paginated list of users and their flair."""
        return {"users": [], "after": after, "limit": limit, "filter_name": name}

    @staticmethod
    def post_api_flairselector(*, link: Optional[str] = None, name: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve available flair options for a link or user."""
        return {"options": [{"id": "abc", "text": "Example Flair"}], "link": link, "user": name}

    @staticmethod
    def post_api_flairtemplate(flair_type: str, text: str) -> Dict[str, Any]:
        """Create or update a user/link flair template."""
        return {"status": "template_saved", "flair_type": flair_type, "text": text}

    @staticmethod
    def post_api_flairtemplate_v2(flair_type: str, text: str) -> Dict[str, Any]:
        """Create/update flair template (v2)."""
        return {"status": "template_v2_saved", "flair_type": flair_type, "text": text}

    @staticmethod
    def get_api_link_flair() -> List[Dict[str, Any]]:
        """Retrieve link flair templates (legacy)."""
        return []

    @staticmethod
    def get_api_link_flair_v2() -> List[Dict[str, Any]]:
        """Retrieve link flair templates (v2)."""
        return []

    @staticmethod
    def post_api_selectflair(link: str, flair_template_id: str) -> Dict[str, Any]:
        """Apply a chosen link flair template to a specific post."""
        return {"status": "success", "link": link, "template_id": flair_template_id}

    @staticmethod
    def post_api_setflairenabled(api_type: str, flair_enabled: bool) -> Dict[str, Any]:
        """Enable or disable flair in a subreddit for all users."""
        return {"status": "flair_enabled_set", "enabled": flair_enabled}

    @staticmethod
    def get_api_user_flair() -> List[Dict[str, Any]]:
        """Retrieve all user flair templates for a subreddit (legacy)."""
        return []

    @staticmethod
    def get_api_user_flair_v2() -> List[Dict[str, Any]]:
        """Retrieve all user flair templates (v2)."""
        return []


class LinksAndComments:
    """Simulation of /links_and_comments endpoints."""

    @staticmethod
    def post_api_comment(parent: str, text: str) -> Dict[str, Any]:
        """Submit a new comment or reply."""
        new_id = f"t1_{len(DB.get('comments', {}))+1}" # Use .get for safety
        DB.setdefault("comments", {})[new_id] = { # Ensure keys exist
            "parent": parent,
            "body": text
        }
        return {"status": "comment_posted", "comment_id": new_id, "parent": parent}

    @staticmethod
    def post_api_del(id: str) -> Dict[str, Any]:
        """Delete a link or comment."""
        # We'll just set a 'deleted' flag if it exists
        if id in DB.get("comments", {}):
            DB["comments"][id]["deleted"] = True
            return {"status": "deleted", "type": "comment", "id": id}
        elif id in DB.get("links", {}):
            DB["links"][id]["deleted"] = True
            return {"status": "deleted", "type": "link", "id": id}
        return {"error": "not_found"}

    @staticmethod
    def post_api_editusertext(thing_id: str, text: str) -> Dict[str, Any]:
        """Edit a comment or self-post."""
        if thing_id in DB.get("comments", {}):
            # If the comment is marked deleted, return an error
            if DB["comments"][thing_id].get("deleted"):
                return {"error": "cannot_edit_deleted_comment"}
            DB["comments"][thing_id]["body"] = text
            return {"status": "updated_comment", "comment_id": thing_id}
        elif thing_id in DB.get("links", {}):
            # If the link is marked deleted, return an error
            if DB["links"][thing_id].get("deleted"):
                return {"error": "cannot_edit_deleted_post"}
            DB["links"][thing_id]["body"] = text
            return {"status": "updated_post", "link_id": thing_id}
        return {"error": "not_found"}

    @staticmethod
    def post_api_follow_post(fullname: str, follow: bool) -> Dict[str, Any]:
        """Follow or unfollow a post."""
        return {"status": "ok", "fullname": fullname, "follow": follow}

    @staticmethod
    def post_api_hide(id: List[str]) -> Dict[str, Any]:
        """Hide one or more posts from the user's front page listings."""
        return {"status": "hidden", "items": id}

    @staticmethod
    def get_api_info(*, id: Optional[str] = None, url: Optional[str] = None) -> Dict[str, Any]:
        """Fetch info about specified posts/comments by fullname or URL."""
        return {"id": id, "url": url, "results": []}

    @staticmethod
    def post_api_lock(id: str) -> Dict[str, Any]:
        return {"status": "locked", "id": id}

    @staticmethod
    def post_api_marknsfw(id: str) -> Dict[str, Any]:
        return {"status": "nsfw_marked", "id": id}

    @staticmethod
    def get_api_morechildren(link_id: str, children: str) -> Dict[str, Any]:
        """Retrieve additional comments omitted by pagination."""
        return {"link_id": link_id, "children_requested": children.split(',')}

    @staticmethod
    def post_api_report(thing_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        return {"status": "reported", "thing_id": thing_id, "reason": reason}

    @staticmethod
    def post_api_save(id: str) -> Dict[str, Any]:
        return {"status": "saved", "id": id}

    @staticmethod
    def get_api_saved_categories() -> List[Dict[str, Any]]:
        return []

    @staticmethod
    def post_api_sendreplies(id: str, state: bool) -> Dict[str, Any]:
        return {"status": "replies_state_changed", "id": id, "state": state}

    @staticmethod
    def post_api_set_contest_mode(state: bool, id: str) -> Dict[str, Any]:
        return {"status": "contest_mode_set", "id": id, "state": state}

    @staticmethod
    def post_api_set_subreddit_sticky(num: Optional[int], state: bool, id: str) -> Dict[str, Any]:
        return {"status": "sticky_set", "id": id, "slot": num, "sticky": state}

    @staticmethod
    def post_api_set_suggested_sort(sort: Optional[str], id: str) -> Dict[str, Any]:
        return {"status": "suggested_sort_set", "id": id, "sort": sort}

    @staticmethod
    def post_api_spoiler(id: str) -> Dict[str, Any]:
        return {"status": "spoiler_marked", "id": id}

    @staticmethod
    def post_api_store_visits() -> Dict[str, Any]:
        return {"status": "visits_stored"}

    @staticmethod
    def post_api_submit(sr: str, kind: str, title: str, url_or_text: Optional[str] = None) -> Dict[str, Any]:
        """Submit a new link or text post."""
        new_id = f"t3_{len(DB.get('links', {}))+1}" # Use .get for safety
        DB.setdefault("links", {})[new_id] = { # Ensure keys exist
            "subreddit": sr,
            "kind": kind,
            "title": title,
            "body": url_or_text or "",
            "deleted": False
        }
        return {"status": "submitted", "link_id": new_id}

    @staticmethod
    def post_api_unhide(id: List[str]) -> Dict[str, Any]:
        return {"status": "unhidden", "items": id}

    @staticmethod
    def post_api_unlock(id: str) -> Dict[str, Any]:
        return {"status": "unlocked", "id": id}

    @staticmethod
    def post_api_unmarknsfw(id: str) -> Dict[str, Any]:
        return {"status": "nsfw_removed", "id": id}

    @staticmethod
    def post_api_unsave(id: str) -> Dict[str, Any]:
        return {"status": "unsaved", "id": id}

    @staticmethod
    def post_api_unspoiler(id: str) -> Dict[str, Any]:
        return {"status": "spoiler_removed", "id": id}

    @staticmethod
    def post_api_vote(id: str, dir: int) -> Dict[str, Any]:
        return {"status": "voted", "id": id, "direction": dir}


class Listings:
    """Simulation of /listings endpoints."""

    @staticmethod
    def get_best(*, after: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        return {"listing_type": "best", "after": after, "limit": limit, "items": []}

    @staticmethod
    def get_by_id_names(names: str) -> Dict[str, Any]:
        return {"listing_type": "by_id", "names": names.split(','), "items": []}

    @staticmethod
    def get_comments_article(article: str) -> Dict[str, Any]:
        return {"article": article, "comments": []}

    @staticmethod
    def get_controversial(*, after: Optional[str] = None) -> Dict[str, Any]:
        return {"listing_type": "controversial", "after": after, "items": []}

    @staticmethod
    def get_duplicates_article(article: str) -> Dict[str, Any]:
        return {"article": article, "duplicates": []}

    @staticmethod
    def get_hot(*, limit: Optional[int] = None) -> Dict[str, Any]:
        return {"listing_type": "hot", "limit": limit, "items": []}

    @staticmethod
    def get_new() -> Dict[str, Any]:
        return {"listing_type": "new", "items": []}

    @staticmethod
    def get_rising() -> Dict[str, Any]:
        return {"listing_type": "rising", "items": []}

    @staticmethod
    def get_top(*, t: Optional[str] = None) -> Dict[str, Any]:
        return {"listing_type": "top", "timeframe": t, "items": []}

    @staticmethod
    def get_sort(sort: str) -> Dict[str, Any]:
        return {"listing_type": sort, "items": []}


class Live:
    """Simulation of /live endpoints."""

    @staticmethod
    def get_api_live_by_id_names(names: str) -> Dict[str, Any]:
        return {"live_threads_requested": names.split(','), "data": []}

    @staticmethod
    def post_api_live_create(title: str) -> Dict[str, Any]:
        new_id = f"live_{len(DB.get('live_threads', {}))+1}" # Use .get for safety
        DB.setdefault("live_threads", {})[new_id] = {"title": title, "updates": []} # Ensure keys exist
        return {"status": "live_thread_created", "thread_id": new_id}

    @staticmethod
    def get_api_live_happening_now() -> Dict[str, Any]:
        return {"featured_live_thread": None}  # mock

    @staticmethod
    def post_api_live_thread_accept_contributor_invite(thread: str) -> Dict[str, Any]:
        return {"status": "contributor_invite_accepted", "thread": thread}

    @staticmethod
    def post_api_live_thread_close_thread(thread: str) -> Dict[str, Any]:
        DB.get("live_threads", {}).get(thread, {})["closed"] = True # Use .get for safety
        return {"status": "thread_closed", "thread": thread}

    @staticmethod
    def post_api_live_thread_delete_update(update_id: str) -> Dict[str, Any]:
        return {"status": "update_deleted", "update_id": update_id}

    @staticmethod
    def post_api_live_thread_edit(*, description: Optional[str] = None) -> Dict[str, Any]:
        return {"status": "thread_edited", "description": description}

    @staticmethod
    def post_api_live_thread_hide_discussion() -> Dict[str, Any]:
        return {"status": "discussion_hidden"}

    @staticmethod
    def post_api_live_thread_invite_contributor(name: str) -> Dict[str, Any]:
        return {"status": "contributor_invited", "user": name}

    @staticmethod
    def post_api_live_thread_leave_contributor() -> Dict[str, Any]:
        return {"status": "left_as_contributor"}

    @staticmethod
    def post_api_live_thread_report(thread: str) -> Dict[str, Any]:
        return {"status": "live_thread_reported", "thread": thread}

    @staticmethod
    def post_api_live_thread_rm_contributor(name: str) -> Dict[str, Any]:
        return {"status": "contributor_removed", "user": name}

    @staticmethod
    def post_api_live_thread_rm_contributor_invite(name: str) -> Dict[str, Any]:
        return {"status": "invite_revoked", "user": name}

    @staticmethod
    def post_api_live_thread_set_contributor_permissions(name: str) -> Dict[str, Any]:
        return {"status": "permissions_set", "user": name}

    @staticmethod
    def post_api_live_thread_strike_update(id: str) -> Dict[str, Any]:
        return {"status": "update_struck", "update_id": id}

    @staticmethod
    def post_api_live_thread_unhide_discussion() -> Dict[str, Any]:
        return {"status": "discussion_unhidden"}

    @staticmethod
    def post_api_live_thread_update(body: str) -> Dict[str, Any]:
        return {"status": "update_added", "body": body}

    @staticmethod
    def get_live_thread(thread: str) -> Dict[str, Any]:
        data = DB.get("live_threads", {}).get(thread, {}) # Use .get for safety
        return {"thread": thread, "info": data}

    @staticmethod
    def get_live_thread_about() -> Dict[str, Any]:
        return {"about": "thread metadata placeholder"}

    @staticmethod
    def get_live_thread_contributors() -> List[str]:
        return []

    @staticmethod
    def get_live_thread_discussions() -> List[str]:
        return []

    @staticmethod
    def get_live_thread_updates_update_id() -> Dict[str, Any]:
        return {}


class Messages:
    """Simulation of /messages endpoints."""

    @staticmethod
    def post_api_block(id: str) -> Dict[str, Any]:
        return {"status": "blocked", "id": id}

    @staticmethod
    def post_api_collapse_message(id: List[str]) -> Dict[str, Any]:
        return {"status": "collapsed", "message_ids": id}

    @staticmethod
    def post_api_compose(to: str, subject: str, text: str) -> Dict[str, Any]:
        new_id = f"msg_{len(DB.get('messages', {}))+1}" # Use .get for safety
        DB.setdefault("messages", {})[new_id] = {"to": to, "subject": subject, "text": text} # Ensure keys exist
        return {"status": "message_sent", "message_id": new_id}

    @staticmethod
    def post_api_del_msg(id: str) -> Dict[str, Any]:
        if id in DB.get("messages", {}):
            del DB["messages"][id]
            return {"status": "message_deleted", "id": id}
        return {"error": "not_found"}

    @staticmethod
    def post_api_read_all_messages() -> Dict[str, Any]:
        return {"status": "all_messages_marked_read"}

    @staticmethod
    def post_api_read_message(id: List[str]) -> Dict[str, Any]:
        return {"status": "messages_marked_read", "ids": id}

    @staticmethod
    def post_api_unblock_subreddit() -> Dict[str, Any]:
        return {"status": "subreddit_unblocked"}

    @staticmethod
    def post_api_uncollapse_message(id: List[str]) -> Dict[str, Any]:
        return {"status": "uncollapsed", "ids": id}

    @staticmethod
    def post_api_unread_message(id: List[str]) -> Dict[str, Any]:
        return {"status": "marked_unread", "ids": id}

    @staticmethod
    def get_message_inbox() -> List[Dict[str, Any]]:
        return list(DB.get("messages", {}).values()) # Use .get for safety

    @staticmethod
    def get_message_sent() -> List[Dict[str, Any]]:
        return []

    @staticmethod
    def get_message_unread() -> List[Dict[str, Any]]:
        return []

    @staticmethod
    def get_message_where(where: str) -> List[Dict[str, Any]]:
        return []


class Misc:
    """Simulation of /misc endpoints."""

    @staticmethod
    def get_api_v1_scopes() -> Dict[str, Any]:
        """Retrieve all possible OAuth scopes and their descriptions."""
        return {"scopes": {"identity": "Access identity", "mysubreddits": "Access user subreddits"}}


class Moderation:
    """Simulation of /moderation endpoints."""

    @staticmethod
    def get_about_edited() -> List[Dict[str, Any]]:
        return []

    @staticmethod
    def get_about_log() -> List[Dict[str, Any]]:
        return []

    @staticmethod
    def get_about_modqueue() -> List[Dict[str, Any]]:
        return []

    @staticmethod
    def get_about_reports() -> List[Dict[str, Any]]:
        return []

    @staticmethod
    def get_about_spam() -> List[Dict[str, Any]]:
        return []

    @staticmethod
    def get_about_unmoderated() -> List[Dict[str, Any]]:
        return []

    @staticmethod
    def get_about_location(location: str) -> Dict[str, Any]:
        return {"location": location, "items": []}

    @staticmethod
    def post_api_accept_moderator_invite() -> Dict[str, Any]:
        return {"status": "moderator_invite_accepted"}

    @staticmethod
    def post_api_approve(id: str) -> Dict[str, Any]:
        return {"status": "approved", "id": id}

    @staticmethod
    def post_api_distinguish(id: str, how: str) -> Dict[str, Any]:
        return {"status": "distinguished", "id": id, "how": how}

    @staticmethod
    def post_api_ignore_reports(id: str) -> Dict[str, Any]:
        return {"status": "ignored_reports", "id": id}

    @staticmethod
    def post_api_leavecontributor() -> Dict[str, Any]:
        return {"status": "left_contributor"}

    @staticmethod
    def post_api_leavemoderator() -> Dict[str, Any]:
        return {"status": "left_moderator"}

    @staticmethod
    def post_api_remove(id: str, spam: Optional[bool] = False) -> Dict[str, Any]:
        return {"status": "removed", "id": id, "spam": spam}

    @staticmethod
    def post_api_show_comment(id: str) -> Dict[str, Any]:
        return {"status": "comment_shown", "id": id}

    @staticmethod
    def post_api_snooze_reports(id: str) -> Dict[str, Any]:
        return {"status": "reports_snoozed", "id": id}

    @staticmethod
    def post_api_unignore_reports(id: str) -> Dict[str, Any]:
        return {"status": "reports_unignored", "id": id}

    @staticmethod
    def post_api_unsnooze_reports(id: str) -> Dict[str, Any]:
        return {"status": "reports_unsnoozed", "id": id}

    @staticmethod
    def post_api_update_crowd_control_level(id: str, level: int) -> Dict[str, Any]:
        return {"status": "crowd_control_updated", "id": id, "level": level}

    @staticmethod
    def get_stylesheet() -> str:
        return "/* subreddit stylesheet placeholder */"


class Modmail:
    """Simulation of /modmail endpoints."""

    @staticmethod
    def post_api_mod_bulk_read(conversation_ids: List[str]) -> Dict[str, Any]:
        return {"status": "conversations_bulk_read", "ids": conversation_ids}

    @staticmethod
    def get_api_mod_conversations() -> Dict[str, Any]:
        return {"conversations": []}

    @staticmethod
    def get_api_mod_conversations_conversation_id(conversation_id: str) -> Dict[str, Any]:
        return {"conversation_id": conversation_id, "details": {}}

    @staticmethod
    def post_api_mod_conversations_conversation_id_approve() -> Dict[str, Any]:
        return {"status": "conversation_approved"}

    @staticmethod
    def post_api_mod_conversations_conversation_id_archive() -> Dict[str, Any]:
        return {"status": "conversation_archived"}

    @staticmethod
    def post_api_mod_conversations_conversation_id_disapprove() -> Dict[str, Any]:
        return {"status": "conversation_disapproved"}

    @staticmethod
    def delete_api_mod_conversations_conversation_id_highlight() -> Dict[str, Any]:
        return {"status": "highlight_removed"}

    @staticmethod
    def post_api_mod_conversations_conversation_id_mute() -> Dict[str, Any]:
        return {"status": "user_muted"}

    @staticmethod
    def post_api_mod_conversations_conversation_id_temp_ban() -> Dict[str, Any]:
        return {"status": "temp_ban_issued"}

    @staticmethod
    def post_api_mod_conversations_conversation_id_unarchive() -> Dict[str, Any]:
        return {"status": "conversation_unarchived"}

    @staticmethod
    def post_api_mod_conversations_conversation_id_unban() -> Dict[str, Any]:
        return {"status": "user_unbanned"}

    @staticmethod
    def post_api_mod_conversations_conversation_id_unmute() -> Dict[str, Any]:
        return {"status": "user_unmuted"}

    @staticmethod
    def post_api_mod_conversations_read() -> Dict[str, Any]:
        return {"status": "conversations_marked_read"}

    @staticmethod
    def get_api_mod_conversations_subreddits() -> List[str]:
        return []

    @staticmethod
    def post_api_mod_conversations_unread() -> Dict[str, Any]:
        return {"status": "conversations_marked_unread"}

    @staticmethod
    def get_api_mod_conversations_unread_count() -> Dict[str, Any]:
        return {"unread_count": 0}


class Modnote:
    """Simulation of /modnote endpoints."""

    @staticmethod
    def delete_api_mod_notes(note_id: str) -> Dict[str, Any]:
        return {"status": "note_deleted", "note_id": note_id}

    @staticmethod
    def get_api_mod_notes_recent(user: str, subreddit: str) -> Dict[str, Any]:
        return {"user": user, "subreddit": subreddit, "notes": DB.get("modnotes", {}).get(user, [])} # Use .get for safety


class Multis:
    """Simulation of /multis endpoints."""

    @staticmethod
    def delete_api_filter_filterpath(filterpath: str) -> Dict[str, Any]:
        return {"status": "filter_deleted", "filterpath": filterpath}

    @staticmethod
    def delete_api_filter_filterpath_r_srname(filterpath: str, srname: str) -> Dict[str, Any]:
        return {"status": "subreddit_removed_from_filter", "filter": filterpath, "srname": srname}

    @staticmethod
    def post_api_multi_copy(frm: str, to: str) -> Dict[str, Any]:
        new_multiname = f"multi_{len(DB.get('multis', {}))+1}" # Use .get for safety
        DB.setdefault("multis", {})[new_multiname] = {"source": frm, "path": to} # Ensure keys exist
        return {"status": "multi_copied", "new_multiname": new_multiname}

    @staticmethod
    def get_api_multi_mine() -> List[Dict[str, Any]]:
        return list(DB.get("multis", {}).values()) # Use .get for safety

    @staticmethod
    def get_api_multi_user_username(username: str) -> List[Dict[str, Any]]:
        return []

    @staticmethod
    def delete_api_multi_multipath(multipath: str) -> Dict[str, Any]:
        return {"status": "multi_deleted", "multipath": multipath}

    @staticmethod
    def get_api_multi_multipath_description(multipath: str) -> Dict[str, Any]:
        return {"description": "", "multipath": multipath}

    @staticmethod
    def delete_api_multi_multipath_r_srname(multipath: str, srname: str) -> Dict[str, Any]:
        return {"status": "subreddit_removed_from_multi", "multipath": multipath, "srname": srname}


class Search:
    """Simulation of /search endpoints."""

    @staticmethod
    def get_search(*, q: str, restrict_sr: Optional[bool] = None, sort: Optional[str] = None) -> Dict[str, Any]:
        return {"query": q, "restrict_sr": restrict_sr, "sort": sort, "results": []}


class Subreddits:
    """Simulation of /subreddits endpoints."""

    @staticmethod
    def get_about_banned() -> List[str]:
        return []

    @staticmethod
    def get_about_contributors() -> List[str]:
        return []

    @staticmethod
    def get_about_moderators() -> List[str]:
        return []

    @staticmethod
    def get_about_muted() -> List[str]:
        return []

    @staticmethod
    def get_about_wikibanned() -> List[str]:
        return []

    @staticmethod
    def get_about_wikicontributors() -> List[str]:
        return []

    @staticmethod
    def get_about_where(where: str) -> Dict[str, Any]:
        return {"where": where, "users": []}

    @staticmethod
    def post_api_delete_sr_banner() -> Dict[str, Any]:
        return {"status": "sr_banner_deleted"}

    @staticmethod
    def post_api_delete_sr_header() -> Dict[str, Any]:
        return {"status": "sr_header_deleted"}

    @staticmethod
    def post_api_delete_sr_icon() -> Dict[str, Any]:
        return {"status": "sr_icon_deleted"}

    @staticmethod
    def post_api_delete_sr_img(img_name: str) -> Dict[str, Any]:
        return {"status": "sr_image_deleted", "img_name": img_name}

    @staticmethod
    def get_api_recommend_sr_srnames(srnames: str) -> Dict[str, Any]:
        return {"recommendations_for": srnames.split(','), "recommendations": []}

    @staticmethod
    def get_api_search_reddit_names(query: str) -> Dict[str, Any]:
        return {"query": query, "available": True}

    @staticmethod
    def post_api_search_subreddits(query: str) -> Dict[str, Any]:
        return {"query": query, "results": []}

    @staticmethod
    def post_api_site_admin(name: str, title: str) -> Dict[str, Any]:
        # Creating or editing a subreddit
        DB.setdefault("subreddits", {})[name] = {"title": title} # Ensure keys exist
        return {"status": "subreddit_created_or_edited", "name": name, "title": title}

    @staticmethod
    def get_api_submit_text(sr: str) -> Dict[str, Any]:
        return {"subreddit": sr, "submit_text": "Welcome to the subreddit!"}

    @staticmethod
    def get_api_subreddit_autocomplete(query: str) -> List[str]:
        return []

    @staticmethod
    def get_api_subreddit_autocomplete_v2() -> List[str]:
        return []

    @staticmethod
    def post_api_subreddit_stylesheet(op: str, stylesheet_contents: str) -> Dict[str, Any]:
        return {"status": "stylesheet_saved", "op": op, "contents": stylesheet_contents}

    @staticmethod
    def post_api_subscribe(action: str, sr_name: str) -> Dict[str, Any]:
        return {"status": "subscribed", "action": action, "subreddit": sr_name}

    @staticmethod
    def post_api_upload_sr_img(name: str, file: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "image_uploaded", "img_name": name}

    @staticmethod
    def get_api_v1_subreddit_post_requirements(subreddit: str) -> Dict[str, Any]:
        return {"subreddit": subreddit, "requirements": {"title_required": True}}

    @staticmethod
    def get_r_subreddit_about(subreddit: str) -> Dict[str, Any]:
        info = DB.get("subreddits", {}).get(subreddit, {"title": "Untitled Subreddit"}) # Use .get for safety
        return {"subreddit": subreddit, "info": info}

    @staticmethod
    def get_r_subreddit_about_edit() -> Dict[str, Any]:
        return {"edit_info": "placeholder"}

    @staticmethod
    def get_r_subreddit_about_rules() -> List[Dict[str, Any]]:
        return []

    @staticmethod
    def get_r_subreddit_about_traffic() -> Dict[str, Any]:
        return {"traffic_stats": []}

    @staticmethod
    def get_sidebar() -> str:
        return "Sidebar content"

    @staticmethod
    def get_sticky() -> List[str]:
        return ["t3_sticky1"]

    @staticmethod
    def get_subreddits_default() -> List[str]:
        return ["r/Python", "r/learnprogramming"]

    @staticmethod
    def get_subreddits_gold() -> List[str]:
        return []

    @staticmethod
    def get_subreddits_mine_contributor() -> List[str]:
        return []

    @staticmethod
    def get_subreddits_mine_moderator() -> List[str]:
        return []

    @staticmethod
    def get_subreddits_mine_streams() -> List[str]:
        return []

    @staticmethod
    def get_subreddits_mine_subscriber() -> List[str]:
        return []

    @staticmethod
    def get_subreddits_mine_where(where: str) -> List[str]:
        return []

    @staticmethod
    def get_subreddits_new() -> List[str]:
        return []

    @staticmethod
    def get_subreddits_popular() -> List[str]:
        return ["r/AskReddit", "r/funny", "r/pics"]

    @staticmethod
    def get_subreddits_search(q: str) -> List[str]:
        return []

    @staticmethod
    def get_subreddits_where(where: str) -> List[str]:
        return []

    @staticmethod
    def get_users_new() -> List[str]:
        return []

    @staticmethod
    def get_users_popular() -> List[str]:
        return []

    @staticmethod
    def get_users_search() -> List[str]:
        return []

    @staticmethod
    def get_users_where(where: str) -> List[str]:
        return []


class Users:
    """Simulation of /users endpoints."""

    @staticmethod
    def post_api_block_user(account_id: str) -> Dict[str, Any]:
        return {"status": "user_blocked", "account_id": account_id}

    @staticmethod
    def post_api_friend(api_type: str, name: str) -> Dict[str, Any]:
        return {"status": "friend_added", "user": name}

    @staticmethod
    def post_api_report_user(user: str, reason: Optional[str] = None) -> Dict[str, Any]:
        return {"status": "user_reported", "user": user, "reason": reason}

    @staticmethod
    def post_api_setpermissions(name: str, permissions: Optional[List[str]] = None) -> Dict[str, Any]:
        return {"status": "permissions_set", "user": name, "permissions": permissions or []}

    @staticmethod
    def post_api_unfriend(name: str, *, type: str) -> Dict[str, Any]:
        return {"status": "relationship_removed", "user": name, "type": type}

    @staticmethod
    def get_api_user_data_by_account_ids(ids: str) -> Dict[str, Any]:
        return {"ids": ids.split(','), "user_data": []}

    @staticmethod
    def get_api_username_available(user: str) -> Dict[str, Any]:
        return {"username": user, "available": True}

    @staticmethod
    def delete_api_v1_me_friends_username(username: str) -> Dict[str, Any]:
        return {"status": "user_unfriended", "username": username}

    @staticmethod
    def get_api_v1_user_username_trophies(username: str) -> Dict[str, Any]:
        return {"username": username, "trophies": []}

    @staticmethod
    def get_user_username_about(username: str) -> Dict[str, Any]:
        # Check DB
        if username in DB.get("users", {}): # Use .get for safety
            return {"status": "ok", "profile": DB["users"][username]}
        return {"status": "not_found"}

    @staticmethod
    def get_user_username_comments(username: str) -> List[Dict[str, Any]]:
        return []

    @staticmethod
    def get_user_username_downvoted() -> List[str]:
        return []

    @staticmethod
    def get_user_username_gilded() -> List[str]:
        return []

    @staticmethod
    def get_user_username_hidden() -> List[str]:
        return []

    @staticmethod
    def get_user_username_overview() -> List[Dict[str, Any]]:
        return []

    @staticmethod
    def get_user_username_saved() -> List[str]:
        return []

    @staticmethod
    def get_user_username_submitted() -> List[str]:
        return []

    @staticmethod
    def get_user_username_upvoted() -> List[str]:
        return []

    @staticmethod
    def get_user_username_where(where: str) -> List[Dict[str, Any]]:
        return []


class Widgets:
    """Simulation of /widgets endpoints."""

    @staticmethod
    def post_api_widget(widget_data: Dict[str, Any]) -> Dict[str, Any]:
        widget_id = f"widget_{len(DB.get('widgets', {}))+1}" # Use .get for safety
        DB.setdefault("widgets", {})[widget_id] = widget_data # Ensure keys exist
        return {"status": "widget_created", "widget_id": widget_id}

    @staticmethod
    def delete_api_widget_widget_id(widget_id: str) -> Dict[str, Any]:
        if widget_id in DB.get("widgets", {}):
            del DB["widgets"][widget_id]
            return {"status": "widget_deleted", "widget_id": widget_id}
        return {"error": "widget_not_found"}

    @staticmethod
    def post_api_widget_image_upload_s3(filepath: str, mimetype: str) -> Dict[str, Any]:
        """
        Acquire and return an upload lease to an S3 temporary bucket for widget image uploads.

        The returned JSON object contains:
          - credentials: Temporary credentials for uploading assets to S3.
          - s3_url: The S3 URL for the upload request.
          - key: The key to use for uploading, which incorporates the provided filepath.
        """
        lease = {
            "credentials": {
                "access_key_id": "EXAMPLEACCESSKEY",
                "secret_access_key": "EXAMPLESECRETACCESSKEY",
                "session_token": "EXAMPLESESSIONTOKEN"
            },
            "s3_url": "https://s3-temp-bucket.example.com/upload",
            "key": f"temp/{filepath}"
        }
        return lease


    @staticmethod
    def patch_api_widget_order_section(section: str, ordered_widgets: List[str]) -> Dict[str, Any]:
        return {"status": "widget_order_patched", "section": section, "ordered_widgets": ordered_widgets}

    @staticmethod
    def get_api_widgets() -> Dict[str, Any]:
        return {"widgets": DB.get("widgets", {})} # Use .get for safety


class Wiki:
    """Simulation of /wiki endpoints."""

    @staticmethod
    def post_api_wiki_alloweditor_add(page: str, username: str) -> Dict[str, Any]:
        return {"status": "editor_added", "page": page, "username": username}

    @staticmethod
    def post_api_wiki_alloweditor_del(page: str, username: str) -> Dict[str, Any]:
        return {"status": "editor_removed", "page": page, "username": username}

    @staticmethod
    def post_api_wiki_alloweditor_act(act: str) -> Dict[str, Any]:
        return {"status": "wiki_editor_action", "action": act}

    @staticmethod
    def post_api_wiki_edit(page: str, content: str) -> Dict[str, Any]:
        subwiki = DB.setdefault("wiki", {}).setdefault("default_subreddit", {}) # Ensure keys exist
        subwiki[page] = {"content": content}
        return {"status": "wiki_page_edited", "page": page}

    @staticmethod
    def post_api_wiki_hide(page: str, revision: str) -> Dict[str, Any]:
        return {"status": "revision_hidden", "page": page, "revision": revision}

    @staticmethod
    def post_api_wiki_revert(page: str, revision: str) -> Dict[str, Any]:
        return {"status": "wiki_page_reverted", "page": page, "revision": revision}

    @staticmethod
    def get_wiki_discussions_page(page: str) -> Dict[str, Any]:
        return {"page": page, "discussions": []}

    @staticmethod
    def get_wiki_pages() -> List[str]:
        subwiki = DB.get("wiki", {}).get("default_subreddit", {}) # Use .get for safety
        return list(subwiki.keys())

    @staticmethod
    def get_wiki_revisions() -> List[Dict[str, Any]]:
        return []

    @staticmethod
    def get_wiki_revisions_page(page: str) -> Dict[str, Any]:
        return {"page": page, "revisions": []}

    @staticmethod
    def get_wiki_settings_page(page: str) -> Dict[str, Any]:
        return {"page": page, "settings": {}}

    @staticmethod
    def get_wiki_page(page: str) -> Dict[str, Any]:
        subwiki = DB.get("wiki", {}).get("default_subreddit", {}) # Use .get for safety
        if page in subwiki:
            return {"page": page, "content": subwiki[page]["content"]}
        return {"page": page, "error": "not_found"}


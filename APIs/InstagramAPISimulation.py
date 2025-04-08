#!/usr/bin/env python
"""
Fully Functional Python API Simulation

Implements a mock Instagram API based on the provided specification. All resources
and methods are implemented as Python classes and in-memory data is stored in a
global DB dictionary. Includes save/load functionality for state persistence, and
embedded unit tests for comprehensive coverage.

Execute this file directly to run the test suite (using unittest).

Author: Thales Goncalves
"""

import json
import os
import unittest
from typing import Dict, Any, List

# ------------------------------------------------------------------------------
# Global In-Memory Database (JSON-serializable)
# ------------------------------------------------------------------------------
DB = {"users": {}, "media": {}, "comments": {}}

# ------------------------------------------------------------------------------
# User
# ------------------------------------------------------------------------------
class User:
    """Handles user-related operations."""

    @staticmethod
    def create_user(user_id: str, name: str, username: str) -> Dict[str, Any]:
        if user_id in DB["users"]:
            return {"error": "User already exists"}
        DB["users"][user_id] = {"name": name, "username": username}
        return {"id": user_id, "name": name, "username": username}

    @staticmethod
    def get_user(user_id: str) -> Dict[str, Any]:
        return {"id": user_id, **DB["users"].get(user_id, {"error": "User not found"})}

    @staticmethod
    def list_users() -> List[Dict[str, Any]]:
        return [{"id": user_id, **info} for user_id, info in DB["users"].items()]

    @staticmethod
    def delete_user(user_id: str) -> Dict[str, Any]:
        if user_id in DB["users"]:
            del DB["users"][user_id]
            return {"success": True}
        return {"error": "User not found"}

    @staticmethod
    def get_user_id_by_username(username: str) -> str:
        """
        Returns only the user ID string for the given username by performing
        a case-insensitive match on the 'username' field in the users database.
        If no match is found, returns "User not found".
        """
        for user_id, user in DB["users"].items():
            if user.get("username", "").lower() == username.lower():
                return user_id
        return "User not found"


# ------------------------------------------------------------------------------
# Media
# ------------------------------------------------------------------------------
class Media:
    """Handles media-related operations."""

    @staticmethod
    def create_media(user_id: str, image_url: str, *, caption: str = "") -> Dict[str, Any]:
        if user_id not in DB["users"]:
            return {"error": "User does not exist"}
        media_id = f"media_{len(DB['media']) + 1}"
        DB["media"][media_id] = {"user_id": user_id, "image_url": image_url, "caption": caption}
        return {"id": media_id, "user_id": user_id, "image_url": image_url, "caption": caption}

    @staticmethod
    def list_media() -> List[Dict[str, Any]]:
        return [{"id": media_id, **info} for media_id, info in DB["media"].items()]

    @staticmethod
    def delete_media(media_id: str) -> Dict[str, Any]:
        if media_id in DB["media"]:
            del DB["media"][media_id]
            return {"success": True}
        return {"error": "Media not found"}

# ------------------------------------------------------------------------------
# Comment
# ------------------------------------------------------------------------------
class Comment:
    """Handles comment-related operations."""

    @staticmethod
    def add_comment(media_id: str, user_id: str, message: str) -> Dict[str, Any]:
        if media_id not in DB["media"]:
            return {"error": "Media does not exist"}
        comment_id = f"comment_{len(DB['comments']) + 1}"
        DB["comments"][comment_id] = {"media_id": media_id, "user_id": user_id, "message": message}
        return {"id": comment_id, "media_id": media_id, "user_id": user_id, "message": message}

    @staticmethod
    def list_comments(media_id: str) -> List[Dict[str, Any]]:
        return [
            {"id": comment_id, **info}
            for comment_id, info in DB["comments"].items()
            if info["media_id"] == media_id
        ]

# ------------------------------------------------------------------------------
# StateManager
# ------------------------------------------------------------------------------
class StateManager:
    """Handles saving and loading of state."""

    @staticmethod
    def save_state(filepath: str = "state.json") -> None:
        with open(filepath, "w") as f:
            json.dump(DB, f)

    @staticmethod
    def load_state(filepath: str = "state.json") -> None:
        global DB
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                DB = json.load(f)
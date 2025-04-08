"""
Full Python simulation for all resources from the Google Docs API Discovery JSON,
with in-memory state, JSON persistence, and embedded tests.

Run this notebook end-to-end to execute tests verifying correctness of each method.
"""

import json
import unittest
import os
from typing import Dict, Any, List, Optional, Union


# ---------------------------------------------------------------------------------------
# In-Memory Docs Database Structure
# ---------------------------------------------------------------------------------------
# All user data is organized under DOCS_DB['users'][userId], which is itself a dictionary storing:
#
#   - 'documents': { documentId: {...}, ... }
#     Contains documents owned or accessible by the user. Each document may include structured content, text elements, styles, lists, and collaborative editing history.
#
#
# Additionally, DOCS_DB['counters'] holds numeric counters used for generating unique IDs for:
#   - 'document': Unique identifiers for documents stored in 'documents'.


DOCS_DB = {
    'users': {
        'me': {
            'documents': {},
        }
    },
    'counters': {
        'document': 0,
    }
}

import json
import uuid
from typing import List, Dict, Any

# ---------------------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------------------
# DB = {
#     "users": {
#         "me": {
#             "about": {
#                 "user": {
#                     "displayName": "John Doe",
#                     "kind": "drive#user",
#                     "me": True,
#                     "permissionId": "user-1234",
#                     "emailAddress": "jdoe@example.com"
#                 }
#             },
#             "files": {},
#             "drives": {},
#             "comments": {},
#             "replies": {},
#             "labels": {},
#             "accessproposals": {},
#             "counters": {
#                 "file": 0,
#                 "drive": 0,
#                 "comment": 0,
#                 "reply": 0,
#                 "label": 0,
#                 "accessproposal": 0,
#                 "revision": 0
#             }
#         }
#     }
# }

# ---------------------------------------------------------------------------------------
# Save and Load DB
# ---------------------------------------------------------------------------------------

# it is expected that the GDriveAPISimulation.py file will be imported in the same environment
from GDriveAPISimulation import DriveAPI, DB as DRIVE_DB

DB = DRIVE_DB  # Ensure shared reference

def save_state(filepath: str):
    """Save the current DB state using DriveAPI."""
    DriveAPI.save_state(filepath)

def load_state(filepath: str):
    """Load the DB state using DriveAPI."""

    DriveAPI.load_state(filepath)

# ---------------------------------------------------------------------------------------
# Helper Methods
# ---------------------------------------------------------------------------------------

def _ensure_user(userId: str = "me") -> None:
    """Ensure that the user entry exists in DB, creating if necessary."""
    if userId not in DB['users']:
        DB['users'][userId] = {
            'about': {
                'user': {
                    'emailAddress': f'{userId}@example.com',
                    'displayName': f'User {userId}'
                },
                'storageQuota': {
                    'limit': '10000000000',
                    'usage': '0'
                }
            },
            'files': {},
            'drives': {},
            'comments': {},
            'replies': {},
            'labels': {},
            'accessproposals': {},
            'counters': {
                'file': 0,
                'drive': 0,
                'comment': 0,
                'reply': 0,
                'label': 0,
                'accessproposal': 0,
                'revision': 0
            }
        }

def _ensure_file(fileId, userId: str = "me"):
    """Ensure file exists in the user's files."""
    _ensure_user(userId)

    if fileId not in DB['users'][userId]['files']:
        DB['users'][userId]['files'][fileId] = {}

    # Ensure global collections exist
    for collection in ['comments', 'replies', 'labels', 'accessproposals']:
        if collection not in DB['users'][userId]:
            DB['users'][userId][collection] = {}

def _next_counter(counter_name: str, userId: str = "me") -> int:
    """Retrieve the next counter value from DB['users'][userId]['counters'][counter_name]."""
    current_val = DB['users'][userId]['counters'].get(counter_name, 0)
    new_val = current_val + 1
    DB['users'][userId]['counters'][counter_name] = new_val
    return new_val

# ---------------------------------------------------------------------------------------
# Document Class (CRUD)
# ---------------------------------------------------------------------------------------

class Documents:
    """Represents a Google Docs document."""

    @staticmethod
    def get(documentId: str, suggestionsViewMode: str = None, includeTabsContent: bool = False, userId: str = "me") -> dict:
        """Gets the latest version of the specified document."""
        if documentId not in DB['users'][userId]['files']:
            return {"error": "Document not found"}, 404

        document = DB['users'][userId]['files'][documentId].copy()

        if suggestionsViewMode:
            document["suggestionsViewMode"] = suggestionsViewMode

        if includeTabsContent:
            document["includeTabsContent"] = includeTabsContent

        # Attach comments, replies, labels, accessproposals related to this doc
        document["comments"] = {
            cid: c for cid, c in DB['users'][userId]['comments'].items() if c["fileId"] == documentId
        }
        document["replies"] = {
            rid: r for rid, r in DB['users'][userId]['replies'].items() if r["fileId"] == documentId
        }
        document["labels"] = {
            lid: l for lid, l in DB['users'][userId]['labels'].items() if l["fileId"] == documentId
        }
        document["accessproposals"] = {
            pid: p for pid, p in DB['users'][userId]['accessproposals'].items() if p["fileId"] == documentId
        }

        return document, 200

    @staticmethod
    def create(title: str = "Untitled Document", userId: str = "me") -> dict:
        """Creates a blank document."""
        _ensure_user(userId)

        documentId = str(uuid.uuid4())
        userId = "me"
        user_data = DB['users'][userId]
        user_email = user_data['about']['user']['emailAddress']

        document = {
            "id": documentId,
            "driveId": "",
            "name": title,
            "mimeType": "application/vnd.google-apps.document",
            "createdTime": "2025-03-11T09:00:00Z",
            "modifiedTime": "2025-03-11T09:00:00Z",
            "parents": [],
            "owners": [user_email],
            "suggestionsViewMode": "DEFAULT",
            "includeTabsContent": False,
            "content": [],
            "tabs": [],
            "permissions": [{
              "role": "owner",
              "type": "user",
              "emailAddress": user_email
            }]
        }

        DB['users'][userId]['files'][documentId] = document
        _next_counter('file', userId)

        return document, 200

    @staticmethod
    def batchUpdate(documentId: str, requests: list, userId: str = "me") -> dict:
        """Applies one or more updates to the document."""
        if documentId not in DB['users'][userId]['files']:
            return {"error": "Document not found"}, 404

        document = DB['users'][userId]['files'][documentId]
        responses = []

        for request in requests:
            if "insertText" in request:
                insert_text = request["insertText"]
                text = insert_text["text"]
                location = insert_text["location"]["index"]

                document["content"].insert(location, {"textRun": {"content": text}})
                responses.append({"insertText": {}})

            elif "updateDocumentStyle" in request:
                update_style = request["updateDocumentStyle"]
                document["documentStyle"] = update_style["documentStyle"]
                responses.append({"updateDocumentStyle": {}})
            else:
                responses.append({"error": "Unsupported request type"})

        DB['users'][userId]['files'][documentId] = document
        return {"documentId": documentId, "replies": responses}, 200

"""
Full Python simulation for all resources from the Google Drive API Discovery JSON,
with in-memory state, JSON persistence, and embedded tests.

Run this notebook end-to-end to execute tests verifying correctness of each method.
"""

import json
import unittest
import os
from typing import Dict, Any, List, Optional, Union

# ---------------------------------------------------------------------------------------
# In-Memory Drive Database Structure
# ---------------------------------------------------------------------------------------
# All user data is organized under DRIVE_DB['users'][userId], which is itself a dictionary storing:
#
#   - 'about': dict
#     Contains metadata and general information about the user's Drive account, including:
#       - 'kind': Resource type identifier (e.g., 'drive#about').
#       - 'storageQuota': Details about storage limits and usage (total limit, usage, usage in Drive and Trash).
#       - 'driveThemes': Available themes for shared drives.
#       - 'canCreateDrives': Boolean indicating if the user can create shared drives.
#       - 'importFormats': Supported import formats.
#       - 'exportFormats': Supported export formats.
#       - 'appInstalled': Whether the Drive app is installed.
#       - 'user': Basic information about the user (display name, permission ID, email, etc.).
#       - 'folderColorPalette': Available folder color options.
#       - 'maxImportSizes': Maximum import file sizes for specific formats.
#       - 'maxUploadSize': Maximum upload size allowed.
#
#   - 'files': { fileId: {...}, ... }
#     Contains metadata and content of individual files owned or accessible by the user.
#
#   - 'drives': { driveId: {...}, ... }
#     Contains shared drive (team drive) information the user can access or manage.
#
#   - 'comments': { commentId: {...}, ... }
#     Contains comments made on files, including discussions and annotations.
#
#   - 'replies': { replyId: {...}, ... }
#     Contains replies to comments on files.
#
#   - 'labels': { labelId: {...}, ... }
#     Contains metadata labels that can be applied to files and folders.
#
#   - 'accessproposals': { proposalId: {...}, ... }
#     Contains proposals related to file access permissions, typically used for requesting or granting access.
#
#
# Additionally, DRIVE_DB['counters'] holds numeric counters used for generating unique IDs for:
#   - 'file': Files stored in 'files'.
#   - 'drive': Shared drives in 'drives'.
#   - 'comment': Comments on files.
#   - 'reply': Replies to comments.
#   - 'label': Metadata labels.
#   - 'accessproposal': Access proposals.
#   - 'revision': File revisions (if implemented).


DB = {
    'users': {
        'me': {
            'about': {
                'kind': 'drive#about',
                'storageQuota': {
                    'limit': '107374182400',  # Example: 100 GB
                    'usageInDrive': '0',
                    'usageInDriveTrash': '0',
                    'usage': '0'
                },
                'driveThemes': False,
                'canCreateDrives': True,
                'importFormats': {},
                'exportFormats': {},
                'appInstalled': False,
                'user': {
                    'displayName': 'Example User',
                    'kind': 'drive#user',
                    'me': True,
                    'permissionId': '1234567890',
                    'emailAddress': 'me@example.com'
                },
                'folderColorPalette':"",
                'maxImportSizes': {},
                'maxUploadSize': '52428800'  # Example: 50 MB
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
    },

}

import json
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from dateutil import parser

# ---------------------------------------------------------------------------------------
# Persistence Class
# ---------------------------------------------------------------------------------------
class DriveAPI:
    """
    The top-level class that handles the in-memory DB and provides
    save/load functionality for JSON-based state persistence.
    """

    @staticmethod
    def save_state(filepath: str) -> None:
        with open(filepath, 'w') as f:
            json.dump(DB, f)

    # staticmethod
    # def load_state(filepath: str) -> None:
    #     global DB
    #     with open(filepath, 'r') as f:
    #         DB = json.load(f)
    @staticmethod
    def load_state(filepath: str) -> None:
        global DB
        with open(filepath, 'r') as f:
            new_data = json.load(f)
            DB.clear()
            DB.update(new_data)

# ---------------------------------------------------------------------------------------
# Helper Methods
# ---------------------------------------------------------------------------------------
def _ensure_user(userId: str) -> None:
    """
    Ensure that the user entry exists in DB, creating if necessary.
    """
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
            'changes': {},
            'drives': {},
            'permissions': {},
            'comments': {},
            'replies': {},
            'apps': {},
            'channels': {},
            'counters': {}
        }


def _ensure_file(userId, fileId):
    # Ensure the user has files
    if 'files' not in DB['users'][userId]:
        DB['users'][userId]['files'] = {}

    # Ensure the file exists
    if fileId not in DB['users'][userId]['files']:
        DB['users'][userId]['files'][fileId] = {}

    # Ensure the permissions list exists
    if 'permissions' not in DB['users'][userId]['files'][fileId]:
        DB['users'][userId]['files'][fileId]['permissions'] = []




def _next_counter(counter_name: str) -> int:
    """
    Retrieve the next integer from DB['counters'][counter_name], increment, and return.
    """
    userId = 'me'
    current_val = DB['users'][userId]['counters'].get(counter_name, 0)
    new_val = current_val + 1
    DB['users'][userId]['counters'][counter_name] = new_val
    return new_val

def _parse_query(q: str) -> List[List[Dict[str, Any]]]:
    """
    Parses a compound query string into a list of condition groups.
    Supports both 'AND' and 'OR' conditions.
    Flexible parsing for spaces.
    """
    operators = [' contains ', '!=', '=', '<', '<=', '>', '>=', ' in ']

    # Split by 'or' first
    raw_or_conditions = [cond.strip() for cond in q.split(' or ')]

    parsed_groups = []
    for or_group in raw_or_conditions:
        raw_and_conditions = [cond.strip() for cond in or_group.split(' and ')]
        parsed_conditions = []

        for cond in raw_and_conditions:
            parsed = None
            for op in operators:
                if op.strip() in cond:
                    parts = cond.split(op.strip())
                    if len(parts) != 2:
                        raise ValueError(f"Invalid condition format: '{cond}'")
                    query_term, value = parts
                    parsed = {
                        'query_term': query_term.strip(),
                        'operator': op.strip(),
                        'value': value.strip().strip("'\"")
                    }
                    break

            if not parsed:
                raise ValueError(f"Unsupported condition or bad format: '{cond}'")

            parsed_conditions.append(parsed)

        parsed_groups.append(parsed_conditions)

    return parsed_groups


def _apply_query_filter(files: List[Dict[str, Any]], condition_groups: List[List[Dict[str, str]]]) -> List[Dict[str, Any]]:
    """
    Filters files based on groups of conditions.
    Each group represents conditions joined by 'AND'.
    Groups are joined by 'OR'.
    """
    if not condition_groups:
        return files

    filtered_files = []
    for file in files:
        # If file matches any of the OR groups, include it
        for group in condition_groups:
            if _matches_all_conditions(file, group):
                filtered_files.append(file)
                break  # No need to check other OR groups

    return filtered_files


def _matches_all_conditions(file: Dict[str, Any], conditions: List[Dict[str, str]]) -> bool:
    """
    Checks if a file satisfies all conditions in a group (AND logic).
    """
    for cond in conditions:

        query_term = cond['query_term']
        operator = cond['operator']
        value = cond['value']

        file_value = file.get(query_term)

        if cond['operator'] == 'in':
            file_value = file.get(value)
            value = query_term.strip("'\"")


        # print(f'file_value:{file_value}')
        # print(f'value: {value}')
        # print(f'qt: {query_term}')
        # print(f'op: {operator}')

        # Handle boolean conversion
        if isinstance(file_value, bool):
            value = value.lower() == 'true'

        if file_value is None:
            return False

        # Convert datetime fields
        if query_term in ['modifiedTime', 'createdTime']:
            file_value = parser.parse(file_value)
            value = parser.parse(value)

        # Operator comparisons
        if operator == '=' and not (file_value == value):
            return False
        elif operator == '!=' and not (file_value != value):
            return False
        elif operator == 'contains' and value not in str(file_value):
            return False
        elif operator == 'in' and str(value) not in file_value:
            return False
        elif operator == '<' and not (file_value < value):
            return False
        elif operator == '<=' and not (file_value <= value):
            return False
        elif operator == '>' and not (file_value > value):
            return False
        elif operator == '>=' and not (file_value >= value):
            return False

    return True

def _delete_descendants(userId: str, user_email: str, parent_id: str):
    """
    Recursively deletes all child files/folders owned by the user.
    """
    all_files = DB['users'][userId]['files']
    children = [
        f_id for f_id, f in all_files.items()
        if parent_id in f.get('parents', []) and user_email in f.get('owners', [])
    ]

    for child_id in children:
        child = all_files.get(child_id)
        if child:
            if child.get('mimeType') == 'application/vnd.google-apps.folder':
                _delete_descendants(userId, user_email, child_id)

            file_size = int(child.get('size', 0))
            all_files.pop(child_id, None)
            Files._update_user_usage(userId, -file_size)


def _has_drive_role(user_email: str, folder: dict, required_role: str = 'organizer') -> bool:
    """
    Checks if the user has the required role in a folder's permissions.
    """
    for perm in folder.get('permissions', []):
        if perm.get('emailAddress') == user_email and perm.get('role') == required_role:
            return True
    return False


# ---------------------------------------------------------------------------------------
# Resource: about
# ---------------------------------------------------------------------------------------
class About:
    """
    about resource-level methods
    """

    @staticmethod
    def get(fields: str = '*') -> Dict[str, Any]:
        """
        Gets information about the user, the user's Drive, and system capabilities.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        return DB['users'][userId]['about']


# ---------------------------------------------------------------------------------------
# Resource: apps
# ---------------------------------------------------------------------------------------
class Apps:
    """
    apps resource-level methods
    """

    @staticmethod
    def get(appId: str) -> Optional[Dict[str, Any]]:
        """
        Gets a specific app.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        return DB['users'][userId]['apps'].get(appId)

    @staticmethod
    def list(appFilterExtensions: str = '',
             appFilterMimeTypes: str = '',
             languageCode: str = '',
             ) -> Dict[str, Any]:
        """
        Lists a user's installed apps.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        # In a real implementation, filtering would be applied here
        apps_list = list(DB['users'][userId]['apps'].values())
        return {
            'kind': 'drive#appList',
            'items': apps_list
        }


# ---------------------------------------------------------------------------------------
# Resource: changes
# ---------------------------------------------------------------------------------------
class Changes:
    """
    changes resource-level methods
    """

    @staticmethod
    def getStartPageToken(driveId: str = '',
                          supportsAllDrives: bool = False,
                          supportsTeamDrives: bool = False,
                          teamDriveId: str = ''
                          ) -> Dict[str, Any]:
        """
        Gets the starting pageToken for listing future changes.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        # In a real implementation, the token would be fetched/generated
        start_page_token = DB['users'][userId]['changes'].get('startPageToken')
        if not start_page_token:
            start_page_token = _next_counter('change_token')
            DB['users'][userId]['changes']['startPageToken'] = start_page_token
        return {
            'kind': 'drive#startPageToken',
            'startPageToken': start_page_token
        }

    @staticmethod
    def list(pageToken: str,
             driveId: str = '',
             includeCorpusRemovals: bool = False,
             includeItemsFromAllDrives: bool = False,
             includeRemoved: bool = True,
             includeTeamDriveItems: bool = False,
             pageSize: int = 100,
             restrictToMyDrive: bool = False,
             spaces: str = 'drive',
             supportsAllDrives: bool = False,
             supportsTeamDrives: bool = False,
             teamDriveId: str = '',
             includePermissionsForView: str = '',
             includeLabels: str = ''
             ) -> Dict[str, Any]:
        """
        Lists the changes for a user or shared drive.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        # In a real implementation, changes would be fetched and filtered
        changes_list = list(DB['users'][userId]['changes'].get('changes',))
        return {
            'kind': 'drive#changeList',
            'nextPageToken': None,
            'changes': changes_list[:pageSize]
        }

    @staticmethod
    def watch(pageToken: str,
              resource: Optional[Dict[str, Any]] = None,
              driveId: str = '',
              includeCorpusRemovals: bool = False,
              includeItemsFromAllDrives: bool = False,
              includeRemoved: bool = True,
              includeTeamDriveItems: bool = False,
              pageSize: int = 100,
              restrictToMyDrive: bool = False,
              spaces: str = 'drive',
              supportsAllDrives: bool = False,
              supportsTeamDrives: bool = False,
              teamDriveId: str = '',
              includePermissionsForView: str = '',
              includeLabels: str = ''
              ) -> Dict[str, Any]:
        """
        Subscribes to changes for a user.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        if resource is None:
            resource = {}
        # In a real implementation, a watch would be set up
        DB['users'][userId]['channels'][resource.get('id')] = resource
        return resource


# ---------------------------------------------------------------------------------------
# Resource: channels
# ---------------------------------------------------------------------------------------
class Channels:
    """
    channels resource-level methods
    """

    @staticmethod
    def stop(resource: Optional[Dict[str, Any]] = None) -> None:
        """
        Stops watching resources through this channel.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        if resource is None:
            resource = {}
        DB['users'][userId]['channels'].pop(resource.get('id'), None)


# ---------------------------------------------------------------------------------------
# Resource: comments
# ---------------------------------------------------------------------------------------
class Comments:
    """
    Comments resource-level methods.
    """

    @staticmethod
    def create(fileId: str,
               body: Optional[Dict[str, Any]] = None,
               fields: str = '*') -> Dict[str, Any]:
        """
        Creates a comment on a file.
        """
        userId = 'me'
        _ensure_user(userId)
        comment_id_num = _next_counter('comment')
        comment_id = f"comment_{comment_id_num}"

        if body is None:
            body = {}

        new_comment = {
            'kind': 'drive#comment',
            'id': comment_id,
            'fileId': fileId,
            'content': body.get('content', ''),
            'createdTime': '2023-10-27T12:00:00.000Z',  # Simulated timestamp
            'modifiedTime': '2023-10-27T12:00:00.000Z'
        }

        DB['users'][userId]['comments'][comment_id] = new_comment
        return new_comment

    @staticmethod
    def get(fileId: str,
            commentId: str,
            fields: str = '*') -> Optional[Dict[str, Any]]:
        """
        Retrieves a comment by ID.
        """
        userId = 'me'
        _ensure_user(userId)
        comment = DB['users'][userId]['comments'].get(commentId)

        if comment and comment['fileId'] == fileId:
            return comment
        return None

    @staticmethod
    def list(fileId: str,
             includeDeleted: bool = False,
             pageSize: int = 20,
             pageToken: str = '',
             startModifiedTime: str = '',
             fields: str = '*') -> Dict[str, Any]:
        """
        Lists comments for a file.
        """
        userId = 'me'
        _ensure_user(userId)

        comments_list = [
            comment for comment in DB['users'][userId]['comments'].values()
            if comment['fileId'] == fileId
        ]

        return {
            'kind': 'drive#commentList',
            'comments': comments_list[:pageSize],
            'nextPageToken': None
        }

    @staticmethod
    def update(fileId: str,
               commentId: str,
               body: Optional[Dict[str, Any]] = None,
               fields: str = '*') -> Optional[Dict[str, Any]]:
        """
        Updates a comment by ID.
        """
        userId = 'me'
        _ensure_user(userId)

        if body is None:
            body = {}

        comment = DB['users'][userId]['comments'].get(commentId)

        if not comment or comment['fileId'] != fileId:
            return None

        comment.update(body)
        comment['modifiedTime'] = '2023-10-27T12:00:01.000Z'  # Updated time
        return comment

    @staticmethod
    def delete(fileId: str,
               commentId: str) -> None:
        """
        Deletes a comment by ID.
        """
        userId = 'me'
        _ensure_user(userId)

        comment = DB['users'][userId]['comments'].get(commentId)

        if comment and comment['fileId'] == fileId:
            DB['users'][userId]['comments'].pop(commentId, None)


# ---------------------------------------------------------------------------------------
# Resource: permissions
# ---------------------------------------------------------------------------------------
class Permissions:
    """
    permissions resource-level methods
    """

    @staticmethod
    def create(fileId: str,
               body: Optional[Dict[str, Any]] = None,
               emailMessage: str = '',
               sendNotificationEmail: bool = True,
               supportsAllDrives: bool = False,
               supportsTeamDrives: bool = False,
               transferOwnership: bool = False,
               useDomainAdminAccess: bool = False,
               ) -> Dict[str, Any]:
        """
        Creates a permission for a file or shared drive.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        _ensure_file(userId, fileId)

        permission_id_num = len(DB['users'][userId]['files'][fileId]['permissions'])+1
        permission_id = f"permission-{permission_id_num}"

        if body is None:
            body = {}

        new_permission = {
            'id': permission_id,
            'role': body.get('role', 'reader'),
            'type': body.get('type', 'user'),
            'emailAddress': body.get('emailAddress', f"user_{permission_id_num}@example.com")
        }

        DB['users'][userId]['files'][fileId]['permissions'].append(new_permission)
        return new_permission

    @staticmethod
    def delete(fileId: str,
               permissionId: str,
               supportsAllDrives: bool = False,
               supportsTeamDrives: bool = False,
               useDomainAdminAccess: bool = False) -> None:
        """
        Deletes a permission.
        """
        userId = 'me'
        _ensure_user(userId)
        _ensure_file(userId, fileId)

        permissions = DB['users'][userId]['files'][fileId]['permissions']
        # Filter out the permission with matching id
        DB['users'][userId]['files'][fileId]['permissions'] = [
            p for p in permissions if p.get('id') != permissionId
        ]

    @staticmethod
    def get(fileId: str,
            permissionId: str,
            supportsAllDrives: bool = False,
            supportsTeamDrives: bool = False,
            useDomainAdminAccess: bool = False,
            ) -> Optional[Dict[str, Any]]:
        """
        Gets a permission by ID.
        """
        userId = 'me'
        _ensure_user(userId)
        _ensure_file(userId, fileId)

        permissions = DB['users'][userId]['files'][fileId]['permissions']
        for permission in permissions:
            if permission.get('id') == permissionId:
                return permission

        return None

    @staticmethod
    def list(fileId: str,
             supportsAllDrives: bool = False,
             supportsTeamDrives: bool = False,
             useDomainAdminAccess: bool = False,
             ) -> Dict[str, Any]:
        """
        Lists a file's or shared drive's permissions.
        """
        userId = 'me'
        _ensure_user(userId)
        _ensure_file(userId, fileId)

        permissions_list = DB['users'][userId]['files'][fileId]['permissions']

        return {
            'kind': 'drive#permissionList',
            'permissions': permissions_list
        }

    @staticmethod
    def update(fileId: str,
           permissionId: str,
           body=None,
           removeExpiration: bool = False,
           supportsAllDrives: bool = False,
           supportsTeamDrives: bool = False,
           transferOwnership: bool = False,
           useDomainAdminAccess: bool = False,
           ):

        userId = 'me'
        _ensure_user(userId)
        _ensure_file(userId, fileId)

        if body is None:
            body = {}

        file_entry = DB['users'][userId]['files'][fileId]
        permissions = file_entry['permissions']

        # Get new owner's email from body
        new_owner_email = body.get('emailAddress')

        if transferOwnership:
            if not new_owner_email:
                print("No emailAddress provided in body.")
                return None

            # Search for an existing permission with this email
            new_owner_permission = next((perm for perm in permissions if perm['emailAddress'] == new_owner_email), None)

            # If no permission exists, create one
            if not new_owner_permission:

                new_owner_permission = {
                    'role': 'owner',
                    'type': 'user',
                    'emailAddress': new_owner_email
                }
                new_permission_ = Permissions.create(fileId, body=new_owner_permission)

                # permissions.append(new_owner_permission)
                # print(f"Created new permission for {new_owner_email} with id {new_permission_id}")

            # Demote all existing owners
            for perm in permissions:
                if perm['role'] == 'owner' and perm['emailAddress'] != new_owner_email:
                    # print(f"Demoting {perm['emailAddress']} from owner to writer")
                    perm['role'] = 'writer'

            # Promote the new owner
            # print(f"Promoting {new_owner_email} to owner")
            # new_owner_permission['role'] = 'owner'

            # Update the owners list
            file_entry['owners'] = [new_owner_email]
            # print(f"Updated owners list: {file_entry['owners']}")

            # Return the new owner's permission
            return new_owner_permission, file_entry

        # If it's not a transferOwnership call, update by permissionId
        permission = next((perm for perm in permissions if perm['id'] == permissionId), None)

        if permission:
            permission.update(body)
            return permission

        return None





# ---------------------------------------------------------------------------------------
# Resource: replies
# ---------------------------------------------------------------------------------------
class Replies:
    """
    replies resource-level methods
    """
    @staticmethod
    def create(fileId: str,
               commentId: str,
               body: Optional[Dict[str, Any]] = None,
               ) -> Dict[str, Any]:
        """
        Creates a reply to a comment.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        reply_id_num = _next_counter('reply')
        reply_id = f"reply_{reply_id_num}"
        if body is None:
            body = {}
        new_reply = {
            'kind': 'drive#reply',
            'id': reply_id,
            'fileId': fileId,
            'commentId': commentId,
            'content': body.get('content', ''),
            'createdTime': '2023-10-27T12:00:00.000Z',  # Simulate time
            'modifiedTime': '2023-10-27T12:00:00.000Z'
        }
        DB['users'][userId]['replies'][reply_id] = new_reply
        return new_reply



    @staticmethod
    def delete(fileId: str, commentId: str, replyId: str, ) -> None:
        """
        Deletes a reply.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        DB['users'][userId]['replies'].pop(replyId, None)

    @staticmethod
    def get(fileId: str, commentId: str, replyId: str, includeDeleted: bool = False, ) -> Optional[Dict[str, Any]]:
        """
        Gets a reply.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        reply = DB['users'][userId]['replies'].get(replyId)
        if reply and reply.get('deleted') and not includeDeleted:
            return None
        return reply

    @staticmethod
    def list(fileId: str,
            commentId: str,
            includeDeleted: bool = False,
            pageSize: int = 20,
            pageToken: str = '',
            ) -> Dict[str, Any]:
        """
        Lists a comment's replies, filtered by fileId and commentId.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)

        # Fetch all replies for the user
        all_replies = DB['users'][userId]['replies'].values()

        # Filter replies by fileId and commentId
        filtered_replies = [
            reply for reply in all_replies
            if reply['fileId'] == fileId and reply['commentId'] == commentId
        ]

        # Implement basic pagination (no real token-based pagination for simplicity)
        paginated_replies = filtered_replies[:pageSize]

        return {
            'kind': 'drive#replyList',
            'replies': paginated_replies,
            'nextPageToken': None  # Implement token logic if needed later
        }


    @staticmethod
    def update(fileId: str,
               commentId: str,
               replyId: str,
               body: Optional[Dict[str, Any]] = None,
               ) -> Optional[Dict[str, Any]]:
        """
        Updates a reply with patch semantics.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        if body is None:
            body = {}
        existing = DB['users'][userId]['replies'].get(replyId)
        if not existing:
            return None
        existing.update(body)
        return existing

# ---------------------------------------------------------------------------------------
# Resource: drives
# ---------------------------------------------------------------------------------------
class Drives:
    """
    drives resource-level methods
    """

    @staticmethod
    def create(requestId: str,
               body: Optional[Dict[str, Any]] = None,
               ) -> Dict[str, Any]:
        """
        Creates a shared drive.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        drive_id_num = _next_counter('drive')
        drive_id = f"drive_{drive_id_num}"
        if body is None:
            body = {}
        new_drive = {
            'kind': 'drive#drive',
            'id': drive_id,
            'name': body.get('name', f'Drive_{drive_id_num}')
        }
        DB['users'][userId]['drives'][drive_id] = new_drive
        return new_drive

    @staticmethod
    def delete(driveId: str,
               useDomainAdminAccess: bool = False,
               allowItemDeletion: bool = False) -> None:
        """
        Permanently deletes a shared drive for which the user is an organizer.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        DB['users'][userId]['drives'].pop(driveId, None)

    @staticmethod
    def get(driveId: str, useDomainAdminAccess: bool = False, ) -> Optional[Dict[str, Any]]:
        """
        Gets a shared drive's metadata by ID.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        return DB['users'][userId]['drives'].get(driveId)

    @staticmethod
    def hide(driveId: str, ) -> Optional[Dict[str, Any]]:
        """
        Hides a shared drive from the default view.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        drive = DB['users'][userId]['drives'].get(driveId)
        if drive:
            drive['hidden'] = True
        return drive


    @staticmethod
    def list(pageSize: int = 10,
         pageToken: str = '',
         q: str = '',
         useDomainAdminAccess: bool = False,
         ) -> Dict[str, Any]:
         """
         Lists the user's shared drives.

         """
         userId = 'me'
         _ensure_user(userId)

         # Get all drives for the user
         drives_list = list(DB['users'][userId]['drives'].values())

         # Apply query filtering if q is provided
         if q:
            conditions = _parse_query(q)  # This returns a list of condition groups
            drives_list = _apply_query_filter(drives_list, conditions)

         return {
             'kind': 'drive#driveList',
             'nextPageToken': None,
             'drives': drives_list[:pageSize]
         }


    @staticmethod
    def unhide(driveId: str, ) -> Optional[Dict[str, Any]]:
        """
        Restores a shared drive to the default view.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        drive = DB['users'][userId]['drives'].get(driveId)
        if drive and drive.get('hidden'):
            drive['hidden'] = False
        return drive

    @staticmethod
    def update(driveId: str,
               body: Optional[Dict[str, Any]] = None,
               useDomainAdminAccess: bool = False,
               ) -> Optional[Dict[str, Any]]:
        """
        Updates the metadata for a shared drive.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        if body is None:
            body = {}
        existing = DB['users'][userId]['drives'].get(driveId)
        if not existing:
            return None
        existing.update(body)
        return existing

# ---------------------------------------------------------------------------------------
# Resource: files
# ---------------------------------------------------------------------------------------
class Files:
    """
    files resource-level methods with quota enforcement
    """

    @staticmethod
    def _get_user_quota(userId: str) -> Dict[str, int]:
        """Helper to fetch user quota info."""
        quota = DB['users'][userId]['about']['storageQuota']
        return {
            'limit': int(quota['limit']),
            'usage': int(quota['usage'])
        }

    @staticmethod
    def _update_user_usage(userId: str, size_diff: int):
        """Helper to update user quota usage."""
        quota = DB['users'][userId]['about']['storageQuota']
        quota['usage'] = str(int(quota['usage']) + size_diff)

    @staticmethod
    def copy(fileId: str,
             body: Optional[Dict[str, Any]] = None,
             enforceSingleParent: bool = False,
             ignoreDefaultVisibility: bool = False,
             keepRevisionForever: bool = False,
             ocrLanguage: str = '',
             supportsAllDrives: bool = False,
             supportsTeamDrives: bool = False,
             includePermissionsForView: str = '',
             includeLabels: str = '',
             ) -> Dict[str, Any]:
        """
        Creates a copy of a file if quota allows.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)

        original_file = DB['users'][userId]['files'].get(fileId)
        if not original_file:
            return {}

        file_size = int(original_file.get('size', 0))
        quota = Files._get_user_quota(userId)

        # Quota check before copying
        if quota['usage'] + file_size > quota['limit']:
            return {
                    "error": {
                        "code": 403,
                        "message": "Quota exceeded. Cannot copy the file."
                    }
                }

        file_id_num = _next_counter('file')
        file_id = f"file_{file_id_num}"

        if body is None:
            body = {}

        # Manually deep copy the original_file
        new_file = {}
        for key, value in original_file.items():
            if isinstance(value, list):
                new_file[key] = value.copy()
            elif isinstance(value, dict):
                new_file[key] = {k: v for k, v in value.items()}  # simple shallow copy of inner dict
            else:
                new_file[key] = value

        new_file['id'] = file_id
        new_file['name'] = body.get('name', f"Copy of {original_file['name']}")

        # Save the copied file
        DB['users'][userId]['files'][file_id] = new_file

        # Update quota usage
        Files._update_user_usage(userId, file_size)


        return new_file



    @staticmethod
    def create(body: Optional[Dict[str, Any]] = None,
              media_body: Optional[Any] = None,
              enforceSingleParent: bool = False,
              ignoreDefaultVisibility: bool = False,
              keepRevisionForever: bool = False,
              ocrLanguage: str = '',
              supportsAllDrives: bool = False,
              supportsTeamDrives: bool = False,
              useContentAsIndexableText: bool = False,
              includePermissionsForView: str = '',
              includeLabels: str = '',
              ) -> Dict[str, Any]:
        """
        Creates a new file with permissions if quota allows.
        If permissions are provided, they replace any existing ones.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)

        if body is None:
            body = {}

        file_size = int(body.get('size', '0'))
        quota = Files._get_user_quota(userId)

        # Update file metadata from media_body if provided
        if media_body:
            body['size'] = str(getattr(media_body, 'size', file_size))
            body['md5Checksum'] = getattr(media_body, 'md5Checksum', '')
            body['sha1Checksum'] = getattr(media_body, 'sha1Checksum', '')
            body['sha256Checksum'] = getattr(media_body, 'sha256Checksum', '')
            body['mimeType'] = getattr(media_body, 'mimeType', body.get('mimeType', 'application/octet-stream'))
            body['imageMediaMetadata'] = getattr(media_body, 'imageMediaMetadata', {})
            body['videoMediaMetadata'] = getattr(media_body, 'videoMediaMetadata', {})

            file_size = int(body['size'])

        # Quota check before creating
        if quota['usage'] + file_size > quota['limit']:
            return {
                "error": {
                    "code": 403,
                    "message": "Quota exceeded. Cannot create the file."
                }
            }

        file_id_num = _next_counter('file')
        file_id = f"file_{file_id_num}"

        user_email = DB['users'][userId]['about'].get('user', {}).get('emailAddress', 'user@example.com')

        # Create base file structure with additional parameters
        new_file = {
            'kind': 'drive#file',
            'id': file_id,
            'driveId': '',
            'name': body.get('name', f'File_{file_id_num}'),
            'mimeType': body.get('mimeType', 'application/octet-stream'),
            'parents': body.get('parents', []),
            'createdTime': body.get('createdTime', '2025-03-14T00:00:00Z'),
            'modifiedTime': body.get('modifiedTime', '2025-03-14T00:00:00Z'),
            'trashed': False,
            'starred': body.get('starred', False),
            'owners': [user_email],
            'size': str(file_size),
            'md5Checksum': body.get('md5Checksum', ''),
            'sha1Checksum': body.get('sha1Checksum', ''),
            'sha256Checksum': body.get('sha256Checksum', ''),
            'imageMediaMetadata': body.get('imageMediaMetadata', {}),
            'videoMediaMetadata': body.get('videoMediaMetadata', {}),
            'permissions': [],
            # Additional parameters
            'enforceSingleParent': enforceSingleParent,
            'ignoreDefaultVisibility': ignoreDefaultVisibility,
            'keepRevisionForever': keepRevisionForever,
            'ocrLanguage': ocrLanguage,
            'supportsAllDrives': supportsAllDrives,
            'supportsTeamDrives': supportsTeamDrives,
            'useContentAsIndexableText': useContentAsIndexableText,
            'includePermissionsForView': includePermissionsForView,
            'includeLabels': includeLabels
        }

        # Handle permissions override logic
        if 'permissions' in body:
            new_file['permissions'] = []
            additional_permissions = body.get('permissions', [])

            for permission in additional_permissions:
                if not all(k in permission for k in ['id', 'role', 'type']):
                    continue
                if permission['type'] == 'user' and 'emailAddress' not in permission:
                    continue
                new_file['permissions'].append(permission)
        else:
            # Default permission (only owner)
            new_file['permissions'].append({
                'id': 'permission_' + file_id,
                'role': 'owner',
                'type': 'user',
                'emailAddress': user_email
            })

        # Save to DB
        DB['users'][userId]['files'][file_id] = new_file

        # Update quota usage
        Files._update_user_usage(userId, file_size)

        return new_file




    @staticmethod
    def delete(fileId: str,
              enforceSingleParent: bool = False,
              supportsAllDrives: bool = False,
              supportsTeamDrives: bool = False) -> None:
        """
        Permanently deletes a file owned by the user without moving it to trash.
        If the file is in a shared drive, the user must be an organizer on the parent folder.
        If the target is a folder, all descendants owned by the user are also deleted.
        """
        userId = 'me'
        _ensure_user(userId)
        user_data = DB['users'][userId]
        user_email = user_data['about']['user']['emailAddress']

        file = user_data['files'].get(fileId)
        if not file:
            raise FileNotFoundError(f"File with ID '{fileId}' not found.")

        # Ownership check
        if user_email not in file.get('owners', []):
            raise PermissionError(f"User '{user_email}' does not own file '{fileId}'.")

        # Shared Drive handling
        if file.get('driveId'):
            parent_ids = file.get('parents', [])
            parent_checked = False

            for parent_id in parent_ids:
                # Try to get parent as a folder (from files)
                parent = user_data['files'].get(parent_id)
                if parent:
                    if not _has_drive_role(user_email, parent, 'organizer'):
                        raise PermissionError(f"User must be an organizer on folder '{parent_id}' to delete items from shared drive.")
                    parent_checked = True
                    break

            # If no folder parent found, fall back to checking drive ownership
            if not parent_checked:
                drive = user_data['drives'].get(file['driveId'])
                if not drive:
                    raise PermissionError(f"Drive '{file['driveId']}' not found.")
                # Optional: Assume user can delete if they created the drive (no roles in schema)
                # Or skip this block entirely if not simulating drive-level roles

        # Recursive delete if folder
        if file.get('mimeType') == 'application/vnd.google-apps.folder':
            _delete_descendants(userId, user_email, fileId)

        # Delete the file itself
        file_size = int(file.get('size', 0))
        user_data['files'].pop(fileId, None)
        Files._update_user_usage(userId, -file_size)



    @staticmethod
    def emptyTrash(driveId: str = '',
                   enforceSingleParent: bool = False,
                   supportsAllDrives: bool = False,
                   supportsTeamDrives: bool = False) -> None:
        """
        Permanently deletes all of the trashed files owned by the user.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        # In a real implementation, trash would be tracked and emptied
        pass

    @staticmethod
    def export(fileId: str,
               mimeType: str,
               ) -> Dict[str, Any]:
        """
        Exports a Google Doc to the requested MIME type and returns the binary content.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        # In a real implementation, conversion and export would be handled
        return {
            'kind': 'drive#export',
            'fileId': fileId,
            'mimeType': mimeType,
            'content': b'Exported content'
        }

    @staticmethod
    def generateIds(count: int = 1,
                    space: str = 'file',
                    ) -> Dict[str, Any]:
        """
        Generates a set of file IDs.
        """
        ids = []
        for _ in range(count):
            file_id_num = _next_counter('file')
            ids.append(f"file_{file_id_num}")
        return {
            'kind': 'drive#generatedIds',
            'ids': ids
        }

    @staticmethod
    def get(fileId: str,
            acknowledgeAbuse: bool = False,
            supportsAllDrives: bool = False,
            supportsTeamDrives: bool = False,
            includePermissionsForView: str = '',
            includeLabels: str = '',
            ) -> Optional[Dict[str, Any]]:
        """
        Gets a file's metadata or content by ID.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        return DB['users'][userId]['files'].get(fileId)



    @staticmethod
    def list(corpora: str = 'user',
            driveId: str = '',
            includeItemsFromAllDrives: bool = False,
            includeTeamDriveItems: bool = False,
            orderBy: str = 'folder,modifiedTime desc,name',
            pageSize: int = 10,
            pageToken: str = '',
            q: str = '',
            spaces: str = 'drive',
            supportsAllDrives: bool = False,
            supportsTeamDrives: bool = False,
            teamDriveId: str = '',
            includePermissionsForView: str = '',
            includeLabels: str = '',
            ) -> Dict[str, Any]:
        """
        Lists the user's files with support for Shared Drives, ordering, and pagination.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)

        # Get all files for this user
        files_list = list(DB['users'][userId]['files'].values())

        # Filter by driveId (Shared Drive)
        if driveId:
            files_list = [f for f in files_list if f.get('driveId') == driveId or driveId in f.get('parents', [])]
        else:
            if not includeItemsFromAllDrives:
                files_list = [f for f in files_list if not f.get('driveId')]

        # Apply custom query filters (if any)
        if q:
            conditions = _parse_query(q)
            files_list = _apply_query_filter(files_list, conditions)

        return {
            'kind': 'drive#fileList',
            'nextPageToken': None,
            'files': files_list[:pageSize]
        }


    @staticmethod
    def update(fileId: str,
              body: Optional[Dict[str, Any]] = None,
              media_body: Optional[Any] = None,
              acknowledgeAbuse: bool = False,
              addParents: str = '',
              enforceSingleParent: bool = False,
              ignoreDefaultVisibility: bool = False,
              keepRevisionForever: bool = False,
              ocrLanguage: str = '',
              removeParents: str = '',
              supportsAllDrives: bool = False,
              supportsTeamDrives: bool = False,
              useContentAsIndexableText: bool = False,
              includePermissionsForView: str = '',
              includeLabels: str = '',
              ) -> Optional[Dict[str, Any]]:
        """
        Updates a file's metadata or content with patch semantics.
        Can also add or remove parents.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)

        if body is None:
            body = {}

        # Get the file to update
        existing = DB['users'][userId]['files'].get(fileId)
        if not existing:
            return None

        # Ensure 'parents' exists as a list
        if 'parents' not in existing or not isinstance(existing['parents'], list):
            existing['parents'] = []

        # Handle addParents (comma-separated string of parent IDs)
        if addParents:
            add_parents_list = [p.strip() for p in addParents.split(',') if p.strip()]
            for parent in add_parents_list:
                if parent not in existing['parents']:
                    existing['parents'].append(parent)

        # Handle removeParents (comma-separated string of parent IDs)
        if removeParents:
            remove_parents_list = [p.strip() for p in removeParents.split(',') if p.strip()]
            existing['parents'] = [p for p in existing['parents'] if p not in remove_parents_list]

        # If enforceSingleParent is True, only keep the last parent
        if enforceSingleParent and existing['parents']:
            existing['parents'] = [existing['parents'][-1]]

        # Apply the patch update from body
        existing.update(body)

        return existing


    @staticmethod
    def watch(fileId: str,
              body: Optional[Dict[str, Any]] = None,
              acknowledgeAbuse: bool = False,
              ignoreDefaultVisibility: bool = False,
              supportsAllDrives: bool = False,
              supportsTeamDrives: bool = False,
              includePermissionsForView: str = '',
              includeLabels: str = '',
              ) -> Dict[str, Any]:
        """
        Subscribes to changes to a file.
        """
        userId = 'me'  # Assuming 'me' for now
        _ensure_user(userId)
        if body is None:
            body = {}
        # In a real implementation, a watch would be set up
        DB['users'][userId]['channels'][body.get('id')] = body
        return body

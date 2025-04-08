import json
import os
import unittest
from typing import Dict, Any, List, Optional, Union

# In-memory database
# DB = {
#     'users': {},
#     'counters': {}
# }

# it is expected that the GDriveAPISimulation file will be imported in the same environment
from GDriveAPISimulation import DriveAPI, DB as DRIVE_DB

DB = DRIVE_DB

# ---------------------------------------------------------------------------------------
# Persistence Class
# ---------------------------------------------------------------------------------------
class SheetsAPI:
    """
    Handles the in-memory DB and provides save/load functionality.
    """

    @staticmethod
    def save_state(filepath: str):
        """Save the current DB state using DriveAPI."""
        DriveAPI.save_state(filepath)

    @staticmethod
    def load_state(filepath: str):
        """Load the DB state using DriveAPI."""
        DriveAPI.load_state(filepath)



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



def _next_counter(counter_name: str, userId: str) -> int:
    """
    Retrieve the next integer from DB['counters'][counter_name], increment, and return.
    """
    current_val = DB["users"][userId]["counters"].get(counter_name, 0)
    new_val = current_val + 1
    DB["users"][userId]["counters"][counter_name] = new_val
    return new_val



# ---------------------------------------------------------------------------------------
# Spreadsheet Class
# ---------------------------------------------------------------------------------------
class Spreadsheet:
    """Represents a spreadsheet resource."""

    def __init__(self, spreadsheet_id: str, properties: dict = None, sheets: list = None):
        self.id = spreadsheet_id
        self.properties = properties or {}
        self.sheets = sheets or []
        self.data = {}  # In-memory grid data

    def to_dict(self):
        """Convert the spreadsheet object to a dictionary representation."""
        userId = "me"
        user_data = DB['users'][userId]
        user_email = user_data['about']['user']['emailAddress']

        return {
            "id": self.id,
            "name": self.properties.get("title", "Untitled Spreadsheet"),
            "mimeType": "application/vnd.google-apps.spreadsheet",
            "properties": self.properties,
            "sheets": self.sheets,
            "data": self.data,
            "owners": [self.properties.get("owner", user_email)],
            "permissions": self.properties.get("permissions", []),
            "parents": self.properties.get("parents", []),
            "size": self.properties.get("size", 0),
        }


    @staticmethod
    def from_dict(obj: dict):
        spreadsheet = Spreadsheet(
            spreadsheet_id=obj["id"],
            properties=obj.get("properties", {}),
            sheets=obj.get("sheets", [])
        )
        spreadsheet.data = obj.get("data", {})
        return spreadsheet


# ---------------------------------------------------------------------------------------
# Spreadsheets API Class
# ---------------------------------------------------------------------------------------
class Spreadsheets:
    """Handles spreadsheet operations."""

    @staticmethod
    def create(spreadsheet: dict) -> dict:
        spreadsheet_id = spreadsheet.get("id")
        new_spreadsheet = Spreadsheet(
            spreadsheet_id,
            spreadsheet.get("properties", {}),
            spreadsheet.get("sheets", [])
        )
        userId = "me"
        DB['users'][userId]['files'][spreadsheet_id] = new_spreadsheet.to_dict()
        # return {
        #     "id": spreadsheet_id,
        #     "properties": new_spreadsheet.properties,
        #     "sheets": new_spreadsheet.sheets
        # }
        return new_spreadsheet.to_dict()

    @staticmethod
    def get(spreadsheet_id: str, ranges: list = None, includeGridData: bool = False) -> dict:
        userId = "me"
        if spreadsheet_id not in DB['users'][userId]['files']:
            raise ValueError("Spreadsheet not found")
        spreadsheet = DB['users'][userId]['files'][spreadsheet_id]
        response = {
            "id": spreadsheet.get('id'),
            "properties": spreadsheet.get('properties'),
            "sheets": spreadsheet.get('sheets')
        }
        if includeGridData and ranges:
            grid_data = {}
            for r in ranges:
                grid_data[r] = spreadsheet['data'].get(r, [])
            response["data"] = grid_data
        return response

    @staticmethod
    def getByDataFilter(spreadsheet_id: str, includeGridData: bool = False, dataFilters: list = None) -> dict:
        userId = "me"
        if spreadsheet_id not in DB['users'][userId]['files']:
            raise ValueError("Spreadsheet not found")

        userId = "me"
        spreadsheet = DB['users'][userId]['files'][spreadsheet_id]
        response = {
            "id": spreadsheet.get('id'),
            "properties": spreadsheet.get('properties'),
            "sheets": spreadsheet.get('sheets')
        }
        if includeGridData and dataFilters:
            response["data"] = spreadsheet['data']
        return response


    @staticmethod
    def batchUpdate(
        spreadsheet_id: str,
        requests: list,
        include_spreadsheet_in_response: bool = False,
        response_ranges: list = None,
        response_include_grid_data: bool = False
    ) -> dict:

        userId = "me"
        if spreadsheet_id not in DB['users'][userId]['files']:
            raise ValueError("Spreadsheet not found")

        spreadsheet = DB['users'][userId]['files'][spreadsheet_id]
        response = {"id": spreadsheet_id}

        # Process the batch requests
        responses = []
        for req in requests:
            # if 'addSheetRequest' in req:
            #     properties = req['addSheetRequest'].get('properties', {})
            #     sheet_id = properties.get('sheetId')

            #     if sheet_id is None:
            #         raise ValueError("addSheetRequest must include a 'sheetId' in 'properties'")

            #     if sheet_id in spreadsheet.sheets:
            #         raise ValueError(f"Sheet with sheetId {sheet_id} already exists")

            #     spreadsheet.sheets.append({
            #         "properties": {
            #             "sheetId": sheet_id,
            #             **properties
            #         }
            #     })

            #     responses.append({
            #         "addSheetResponse": {
            #             "properties": spreadsheet.sheets[-1]
            #         }
            #     })

            if 'addSheetRequest' in req:
                properties = req['addSheetRequest'].get('properties', {})
                sheet_id = properties.get('sheetId')

                if sheet_id is None:
                    raise ValueError("addSheetRequest must include a 'sheetId' in 'properties'")

                # Check if sheetId already exists in the list
                existing_ids = [s['properties']['sheetId'] for s in spreadsheet['sheets']]
                if sheet_id in existing_ids:
                    raise ValueError(f"Sheet with sheetId {sheet_id} already exists")

                new_sheet = {
                    "properties": {
                        "sheetId": sheet_id,
                        **properties
                    }
                }
                spreadsheet['sheets'].append(new_sheet)

                responses.append({
                    "addSheetResponse": {
                        "properties": new_sheet
                    }
                })



            elif 'deleteSheetRequest' in req:
                sheet_id = req['deleteSheetRequest'].get('sheetId')

                if sheet_id is None:
                    raise ValueError("deleteSheetRequest must include a 'sheetId'")

                sheets = spreadsheet['sheets']

                sheet_exists = any(sheet['properties']['sheetId'] == sheet_id for sheet in sheets)

                if not sheet_exists:
                    raise ValueError(f"Sheet with sheetId {sheet_id} does not exist")

                updated_sheets = [sheet for sheet in sheets if sheet['properties']['sheetId'] != sheet_id]

                spreadsheet['sheets'] = updated_sheets

                responses.append({
                    "deleteSheetResponse": {
                        "sheetId": sheet_id
                    }
                })

            elif 'updateSheetPropertiesRequest' in req:
                properties_update = req['updateSheetPropertiesRequest'].get('properties')
                fields = req['updateSheetPropertiesRequest'].get('fields')

                if not properties_update or not fields:
                    raise ValueError("updateSheetPropertiesRequest must include 'properties' and 'fields'")

                sheet_id = properties_update.get('sheetId')

                if sheet_id is None:
                    raise ValueError("updateSheetPropertiesRequest must include a 'sheetId' in 'properties'")

                updated = False
                for sheet in spreadsheet['sheets']:
                    if sheet['properties']['sheetId'] == sheet_id:
                        for field in fields.split(','):
                            field = field.strip()
                            if field in properties_update:
                                sheet['properties'][field] = properties_update[field]
                        updated = True
                        responses.append({
                            "updateSheetPropertiesResponse": {
                                "properties": sheet['properties']
                            }
                        })
                        break

                if not updated:
                    raise ValueError(f"Sheet with sheetId {sheet_id} does not exist")

            elif "updateCells" in req:
                update = req["updateCells"]
                range_ = (
                    f"{update['range']['sheetId']}!"
                    f"{update['range']['startRowIndex']}:{update['range']['endRowIndex']}"
                    f"{update['range']['startColumnIndex']}:{update['range']['endColumnIndex']}"
                )
                spreadsheet['data'][range_] = update["rows"]
                responses.append({"updateCells": {"updatedRange": range_}})

            else:
                raise ValueError(f"Unsupported request type: {list(req.keys())[0]}")

        response["responses"] = responses

        if include_spreadsheet_in_response:
            updated_spreadsheet = {
                "id": spreadsheet_id,
                "sheets": spreadsheet['sheets']
            }

            if response_ranges:
                updated_spreadsheet["responseRanges"] = response_ranges

            if response_include_grid_data:
                updated_spreadsheet["responseIncludeGridData"] = True

            response["updatedSpreadsheet"] = updated_spreadsheet

        return response




# ---------------------------------------------------------------------------------------
# Spreadsheet Values API Class
# ---------------------------------------------------------------------------------------
class SpreadsheetValues:
    """Handles spreadsheet values operations."""

    @staticmethod
    def get(spreadsheet_id: str, range: str, majorDimension: str = None, valueRenderOption: str = None, dateTimeRenderOption: str = None) -> dict:

        userId = "me"

        if spreadsheet_id not in DB['users'][userId]['files']:
            raise ValueError("Spreadsheet not found")

        spreadsheet = DB['users'][userId]['files'][spreadsheet_id]
        values = spreadsheet['data'].get(range, [[""]])
        return {
            "range": range,
            "majorDimension": majorDimension,
            "values": values
        }

    @staticmethod
    def update(spreadsheet_id: str, range: str, valueInputOption: str, values: list, includeValuesInResponse: bool = False, responseValueRenderOption: str = None, responseDateTimeRenderOption: str = None) -> dict:

        userId = "me"
        if spreadsheet_id not in DB['users'][userId]['files']:
            raise ValueError("Spreadsheet not found")


        spreadsheet = DB['users'][userId]['files'][spreadsheet_id]
        spreadsheet['data'][range] = values
        response = {
            "id": spreadsheet_id,
            "updatedRange": range,
            "updatedRows": len(values),
            "updatedColumns": len(values[0]) if values else 0
        }
        if includeValuesInResponse:
            response["values"] = values
        return response

    @staticmethod
    def append(spreadsheet_id: str, range: str, valueInputOption: str, values: list, insertDataOption: str = None, includeValuesInResponse: bool = False, responseValueRenderOption: str = None, responseDateTimeRenderOption: str = None) -> dict:

        userId = "me"
        if spreadsheet_id not in DB['users'][userId]['files']:
            raise ValueError("Spreadsheet not found")


        spreadsheet = DB['users'][userId]['files'][spreadsheet_id]
        if range in spreadsheet['data']:
            spreadsheet['data'][range].extend(values)
        else:
            spreadsheet['data'][range] = values
        response = {
            "id": spreadsheet_id,
            "updatedRange": range,
            "updatedRows": len(values),
            "updatedColumns": len(values[0]) if values else 0
        }
        if includeValuesInResponse:
            response["values"] = values
        return response

    @staticmethod
    def clear(spreadsheet_id: str, range: str) -> dict:
        userId = "me"
        if spreadsheet_id not in DB['users'][userId]['files']:
            raise ValueError("Spreadsheet not found")


        spreadsheet = DB['users'][userId]['files'][spreadsheet_id]
        if range in spreadsheet['data']:
            del spreadsheet['data'][range]
        return {"id": spreadsheet_id, "clearedRange": range}

    @staticmethod
    def batchGet(spreadsheet_id: str, ranges: list, majorDimension: str = None, valueRenderOption: str = None, dateTimeRenderOption: str = None) -> dict:
        userId = "me"
        if spreadsheet_id not in DB['users'][userId]['files']:
            raise ValueError("Spreadsheet not found")


        spreadsheet = DB['users'][userId]['files'][spreadsheet_id]
        value_ranges = []
        for range_ in ranges:
            values = spreadsheet['data'].get(range_, [[""]])
            value_ranges.append({
                "range": range_,
                "majorDimension": majorDimension,
                "values": values
            })
        return {"id": spreadsheet_id, "valueRanges": value_ranges}

    @staticmethod
    def batchUpdate(spreadsheet_id: str, valueInputOption: str, data: list, includeValuesInResponse: bool = False, responseValueRenderOption: str = None, responseDateTimeRenderOption: str = None) -> dict:
        userId = "me"
        if spreadsheet_id not in DB['users'][userId]['files']:
            raise ValueError("Spreadsheet not found")

        spreadsheet = DB['users'][userId]['files'][spreadsheet_id]
        updated_data = []
        for value_range in data:
            range_ = value_range["range"]
            values = value_range["values"]
            spreadsheet['data'][range_] = values
            updated_data.append({"range": range_, "values": values})
        response = {"id": spreadsheet_id, "updatedData": updated_data}
        if includeValuesInResponse:
            response["updatedData"] = updated_data
        return response

    @staticmethod
    def batchClear(spreadsheet_id: str, ranges: list) -> dict:
        userId = "me"
        if spreadsheet_id not in DB['users'][userId]['files']:
            raise ValueError("Spreadsheet not found")


        spreadsheet = DB['users'][userId]['files'][spreadsheet_id]
        cleared_ranges = []
        for range_ in ranges:
            if range_ in spreadsheet['data']:
                del spreadsheet['data'][range_]
            cleared_ranges.append({"clearedRange": range_})
        return {"id": spreadsheet_id, "clearedRanges": cleared_ranges}

    @staticmethod
    def batchGetByDataFilter(spreadsheet_id: str, dataFilters: list, majorDimension: str = None, valueRenderOption: str = None, dateTimeRenderOption: str = None) -> dict:
        userId = "me"
        if spreadsheet_id not in DB['users'][userId]['files']:
            raise ValueError("Spreadsheet not found")

        spreadsheet = DB['users'][userId]['files'][spreadsheet_id]
        value_ranges = []
        for range_, values in spreadsheet['data'].items():
            value_ranges.append({
                "range": range_,
                "majorDimension": majorDimension,
                "values": values
            })
        return {"id": spreadsheet_id, "valueRanges": value_ranges}

    @staticmethod
    def batchUpdateByDataFilter(spreadsheet_id: str, valueInputOption: str, data: list, includeValuesInResponse: bool = False, responseValueRenderOption: str = None, responseDateTimeRenderOption: str = None) -> dict:
        userId = "me"
        if spreadsheet_id not in DB['users'][userId]['files']:
            raise ValueError("Spreadsheet not found")

        spreadsheet = DB['users'][userId]['files'][spreadsheet_id]
        updated_data = []
        for data_filter_value_range in data:
            range_ = data_filter_value_range["range"]
            values = data_filter_value_range["values"]
            spreadsheet['data'][range_] = values
            updated_data.append({"range": range_, "values": values})
        response = {"id": spreadsheet_id, "updatedData": updated_data}
        if includeValuesInResponse:
            response["updatedData"] = updated_data
        return response
"""
Full Python simulation for all resources from the Google Drive API Discovery JSON,
with in-memory state, JSON persistence, and embedded tests.

Run this notebook end-to-end to execute tests verifying correctness of each method.

"""

# ---------------------------------------------------------------------------------------
# In-Memory Spreadsheet Database Structure
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


# DRIVE_DB = {
#     'users': {
#         'me': {
#             'about': {
#                 'kind': 'drive#about',
#                 'storageQuota': {
#                     'limit': '107374182400',  # Example: 100 GB
#                     'usageInDrive': '0',
#                     'usageInDriveTrash': '0',
#                     'usage': '0'
#                 },
#                 'driveThemes': False,
#                 'canCreateDrives': True,
#                 'importFormats': {},
#                 'exportFormats': {},
#                 'appInstalled': False,
#                 'user': {
#                     'displayName': 'Example User',
#                     'kind': 'drive#user',
#                     'me': True,
#                     'permissionId': '1234567890',
#                     'emailAddress': 'me@example.com'
#                 },
#                 'folderColorPalette':"",
#                 'maxImportSizes': {},
#                 'maxUploadSize': '52428800'  # Example: 50 MB
#             },
#             'files': {},
#             'drives': {},
#             'comments': {},
#             'replies': {},
#             'labels': {},
#             'accessproposals': {}
#         }
#     },
#     'counters': {
#         'file': 0,
#         'drive': 0,
#         'comment': 0,
#         'reply': 0,
#         'label': 0,
#         'accessproposal': 0,
#         'revision': 0
#     }
# }
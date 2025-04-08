import json
from datetime import datetime
import re

CURRENT_USER_ID = 'users/user123'
DB = {
  "media": [
    {
      "resourceName": ""
    }
  ],
  "User": [
    {
      "name": "users/user123",
      "displayName": "abc",
      "domainId": "",
      "type": "HUMAN",
      "isAnonymous": False
    }
  ],
  "Space": [
    {
      "name": "spaces/AAAAAAAAA",
      "type": "ROOM",
      "spaceType": "SPACE",
      "singleUserBotDm": False,
      "threaded": False,
      "displayName": "My Space Name",
      "externalUserAllowed": True,
      "spaceThreadingState": "UNTHREADED_MESSAGES",
      "spaceDetails": {
        "description": "Description of the space.",
        "guidelines": "Guidelines for the space."
      },
      "spaceHistoryState": "HISTORY_ON",
      "importMode": False,
      "createTime": "2023-10-27T12:00:00.000Z",
      "lastActiveTime": "2023-10-27T13:00:00.000Z",
      "adminInstalled": False,
      "membershipCount": {
        "joinedDirectHumanUserCount": 0,
        "joinedGroupCount": 0
      },
      "accessSettings": {
        "accessState": "PRIVATE",
        "audience": "audiences/default"
      },
      "spaceUri": "https://example.com/spaces/AAAAAAAAA",
      "predefinedPermissionSettings": "COLLABORATION_SPACE",
       "permissionSettings": {
        "manageMembersAndGroups": {},
        "modifySpaceDetails": {},
        "toggleHistory": {},
        "useAtMentionAll": {},
        "manageApps": {},
        "manageWebhooks": {},
        "postMessages": {},
        "replyMessages": {}
     },
      "importModeExpireTime": "2023-10-28T12:00:00.000Z"
    }
  ],
  "Message": [
    {
      "name": "",
      "sender": {
        "name": "",
        "displayName": "",
        "domainId": "",
        "type": "",
        "isAnonymous": False
      },
      "createTime": "",
      "lastUpdateTime": "",
      "deleteTime": "",
      "text": "",
      "formattedText": "",
      "cards": [],
      "cardsV2": [],
      "annotations": [],
      "thread": {
        "name": "",
        "threadKey": ""
      },
      "space": {
        "name": "",
        "type": "",
        "spaceType": ""
      },
      "fallbackText": "",
      "actionResponse": {},
      "argumentText": "",
      "slashCommand": {},
      "attachment": [
        {
          "name": "",
          "contentName": "",
          "contentType": "",
          "attachmentDataRef": {},
          "driveDataRef": {},
          "thumbnailUri": "",
          "downloadUri": "",
          "source": ""
        }
      ],
      "matchedUrl": {},
      "threadReply": False,
      "clientAssignedMessageId": "",
      "emojiReactionSummaries": [],
      "privateMessageViewer": {
        "name": "",
        "displayName": "",
        "domainId": "",
        "type": "",
        "isAnonymous": False
      },
      "deletionMetadata": {},
      "quotedMessageMetadata": {},
      "attachedGifs": [],
      "accessoryWidgets": []
    }
  ],
  "Membership": [
    {
      "name": "spaces/AAAAAAA/members/USER123",
      "state": "JOINED",
      "role": "ROLE_MEMBER",
      "member": {
        "name": "USER123",
        "displayName": "John Doe",
        "domainId": "example.com",
        "type": "HUMAN",
        "isAnonymous": False
      },
      "groupMember": {},
      "createTime": "",
      "deleteTime": ""
    }
  ],
  "Reaction": [
    {
      "name": "",
      "user": {
        "name": "",
        "displayName": "",
        "domainId": "",
        "type": "",
        "isAnonymous": False
      },
      "emoji": {
        "unicode": "🙂"
      }
    }
  ],
  "SpaceNotificationSetting": [
    {
      "name": "",
      "notificationSetting": "",
      "muteSetting": ""
    }
  ],
  "SpaceReadState": [
    {
      "name": "users/{user}/spaces/{space}/spaceReadState",
      "lastReadTime": ""
    }
  ],
  "ThreadReadState": [
    {
      "name": "users/{user}/spaces/{space}/threads/{thread}/threadReadState",
      "lastReadTime": ""
    }
  ],
  "SpaceEvent": [
    {
      "name": "spaces/{space}/spaceEvents/{spaceEvent}",
      "eventTime": "",
      "eventType": "",
      "messageCreatedEventData": {},
      "messageUpdatedEventData": {},
      "messageDeletedEventData": {},
      "messageBatchCreatedEventData": {},
      "messageBatchUpdatedEventData": {},
      "messageBatchDeletedEventData": {},
      "spaceUpdatedEventData": {},
      "spaceBatchUpdatedEventData": {},
      "membershipCreatedEventData": {},
      "membershipUpdatedEventData": {},
      "membershipDeletedEventData": {},
      "membershipBatchCreatedEventData": {},
      "membershipBatchUpdatedEventData": {},
      "membershipBatchDeletedEventData": {},
      "reactionCreatedEventData": {},
      "reactionDeletedEventData": {},
      "reactionBatchCreatedEventData": {},
      "reactionBatchDeletedEventData": {}
    }
  ],
  "Attachment": [
      {
        "name": "",
        "contentName": "",
        "contentType": "",
        "attachmentDataRef": {},
        "driveDataRef": {},
        "thumbnailUri": "https://drive.google.com/thumbnail?id=agenda",
        "downloadUri": "https://drive.google.com/download?id=agenda",
        "source": "UPLOADED_CONTENT"
      }
    ]

}


import json

class GoogleChatAPI:
    """
    The top-level class that handles the in-memory DB for the Google Chat API and provides
    save/load functionality for JSON-based state persistence.
    """

    @staticmethod
    def save_state(filepath: str) -> None:
        """Saves the current in-memory DB state to a JSON file."""
        with open(filepath, 'w') as f:
            json.dump(DB, f, indent=2)
        print(f"State saved to {filepath}")

    @staticmethod
    def load_state(filepath: str) -> None:
        """Loads the in-memory DB state from a JSON file."""
        global DB
        with open(filepath, 'r') as f:
            DB = json.load(f)
        print(f"State loaded from {filepath}")



# ---------------------------------------------------------------------------------------
# Resource: Media
# ---------------------------------------------------------------------------------------
class Media:
    """Handles media-related operations."""
    @staticmethod
    def download(resourceName: str) -> None:
        """Download media from the given resource name."""
        print(f"Downloading media with resource name: {resourceName}")

    @staticmethod
    def upload(parent: str, attachment_request: dict) -> dict:
        """
        Uploads an attachment to the specified Chat space.

        Parameters:
          - parent (str): The resource name of the Chat space (e.g. "spaces/AAA").
          - attachment_request (dict): The request body for the upload, e.g.:
                {
                  "contentName": "file.pdf",
                  "contentType": "application/pdf"
                }

        Behavior:
          - Generates a new attachment resource name in the format:
                "spaces/{space}/attachments/{attachmentId}"
          - Adds a new record to DB["Attachment"] with the provided file details and
            sets "source" to "UPLOADED_CONTENT".
          - Returns the created attachment record.
        """
        # Generate a new attachment ID based on the current count in DB["Attachment"]
        new_id = str(len(DB.get("Attachment", [])) + 1)
        resource_name = f"{parent}/attachments/{new_id}"

        # Build the new attachment object based on the schema.
        attachment = {
            "name": resource_name,
            "contentName": attachment_request.get("contentName", "unknown"),
            "contentType": attachment_request.get("contentType", "application/octet-stream"),
            "attachmentDataRef": {},
            "driveDataRef": {},
            "thumbnailUri": "",
            "downloadUri": "",
            "source": "UPLOADED_CONTENT"
        }

        # Ensure DB["Attachment"] exists.
        if "Attachment" not in DB:
            DB["Attachment"] = []
        DB["Attachment"].append(attachment)
        print(f"Uploaded attachment: {resource_name}")
        return attachment


# ---------------------------------------------------------------------------------------
# Resource: Spaces
# ---------------------------------------------------------------------------------------

class Spaces:
    """Handles operations under /spaces."""

    @staticmethod
    def list(pageSize: int = None, pageToken: str = None, filter: str = None) -> None:
        """
        Lists spaces the CURRENT_USER_ID is a member of.
        - pageSize (int): Max number of spaces to return (default 100, max 1000).
        - pageToken (str): A naive offset for pagination. We'll parse it as an int.
        - filter (str): e.g. 'spaceType = "SPACE"' or 'spaceType = "GROUP_CHAT" OR spaceType = "DIRECT_MESSAGE"'
        Returns:
          {
            "spaces": [...],
            "nextPageToken": "..."
          }
        """

        def parse_space_type_filter(filter: str):

          ALLOWED_SPACE_TYPES = {"SPACE", "GROUP_CHAT", "DIRECT_MESSAGE"}
          # Normalize by removing spaces around = and operators
          normalized = filter.replace("=", " = ").replace("OR", " OR ")
          # Reject if 'AND' is used
          if re.search(r'\bAND\b', filter, re.IGNORECASE):
              return {"error": "'AND' operator is not supported. Use 'OR' instead."}
          # Regex to find all spaceType = "VALUE" or space_type = "VALUE"
          pattern = re.compile(r'(spaceType|space_type)\s*=\s*"([^"]+)"')
          matches = pattern.findall(normalized)
          valid = []
          if not matches:
              return {"error":"No valid expressions found."}

          for _, value in matches:
              if value in ALLOWED_SPACE_TYPES:
                  valid.append(value)
              else:
                  return {"error":f"Invalid space type: '{value}'"}

          return {'space_types' : valid}

        user_spaces = []
        for sp in DB["Space"]:
            # Check membership by forming "spaces/AAA/members/CURRENT_USER_ID"
            membership_name = f"{sp.get('name')}/members/{CURRENT_USER_ID}"
            found_membership = False
            for mem in DB["Membership"]:
                if mem.get("name") == membership_name:
                    found_membership = True
                    break
            if found_membership:
                user_spaces.append(sp)

        if filter:
          parsed_filter = parse_space_type_filter(filter)
          if "error" in parsed_filter:
            return {"error": parsed_filter["error"]}
          space_types = parsed_filter["space_types"]
          user_spaces = [sp for sp in user_spaces if sp["spaceType"] in space_types]


        # Build the response
        response = {
            "spaces": user_spaces
        }
        next_token = ''
        response["nextPageToken"] = next_token

        return response

    @staticmethod
    def search(useAdminAccess: bool,
        pageSize: int = None,
        pageToken: str = None,
        query: str = None,
        orderBy: str = None) -> dict:
        """
        Returns a list of spaces in a Google Workspace organization based on an administrator's search.

        Parameters:
          - useAdminAccess (bool): Must be True.
          - pageSize (int, optional): Maximum number of spaces to return. Default is 100; maximum is 1000.
          - pageToken (str, optional): A token received from a previous search, interpreted as an integer offset.
          - query (str): Required. A search query using parameters:
                - create_time
                - customer (must be "customers/my_customer")
                - display_name (uses the HAS (:) operator)
                - external_user_allowed
                - last_active_time
                - space_history_state
                - space_type (must be "SPACE")
          - orderBy (str, optional): How the spaces are ordered.
                Supported values include:
                  • membership_count.joined_direct_human_user_count ASC|DESC
                  • last_active_time ASC|DESC
                  • create_time ASC|DESC
                Default ordering is create_time ascending.

        Returns:
          dict: A SearchSpacesResponse containing:
                {
                  "spaces": [ ... list of matching space objects ... ],
                  "nextPageToken": "..."  // if there are more spaces available
                }
        """

        print(f"search called with useAdminAccess={useAdminAccess}, pageSize={pageSize}, pageToken={pageToken}, query={query}, orderBy={orderBy}")

        def parse_page_token(token: str) -> int:
            try:
                off = int(token)
                return max(off, 0)
            except (ValueError, TypeError):
                return 0

        def default_page_size(ps: int) -> int:
            if ps is None:
                return 100
            if ps < 0:
                return 100
            return min(ps, 1000)

        def matches_field(space: dict, field: str, operator: str, value: str) -> bool:
            # For simplicity, assume fields are stored as in our DB:
            # - "display_name" maps to space["displayName"] (case-insensitive substring match)
            # - "external_user_allowed" maps to space["externalUserAllowed"] (boolean)
            # - "space_history_state" maps to space["spaceHistoryState"]
            # - "create_time" maps to space["createTime"]
            # - "last_active_time" maps to space["lastActiveTime"]
            field = field.strip().lower()
            if field == "display_name":
                # Use HAS operator: value should be a substring (case-insensitive)
                return value.lower() in space.get("displayName", "").lower()
            elif field == "external_user_allowed":
                # Compare boolean (value will be "true" or "false")
                bool_val = True if value.lower() == "true" else False
                return space.get("externalUserAllowed") == bool_val
            elif field in ("create_time", "last_active_time"):
                # Use string comparison (assuming ISO8601 format)
                space_val = space.get("createTime") if field == "create_time" else space.get("lastActiveTime")
                if operator == "=":
                    return space_val == value
                elif operator == ">":
                    return space_val > value
                elif operator == "<":
                    return space_val < value
                elif operator == ">=":
                    return space_val >= value
                elif operator == "<=":
                    return space_val <= value
                else:
                    return False
            elif field == "space_history_state":
                return space.get("spaceHistoryState") == value
            # For unknown fields, assume no match.
            return True

        def parse_filter(query_str: str) -> list:
            # Split query on "AND"
            segments = [seg.strip() for seg in query_str.split("AND")]
            expressions = []
            for seg in segments:
                # We support two types:
                #   display_name:"text"
                #   external_user_allowed = "true"/"false"
                #   space_history_state = "HISTORY_ON" or "HISTORY_OFF"
                #   create_time, last_active_time comparisons: operator can be one of >, <, >=, <=, =
                # We'll detect operator by checking for one of these symbols.
                for op in [">=", "<=", ">", "<", "="]:
                    if op in seg:
                        # Split only once.
                        parts_seg = seg.split(op, 1)
                        field = parts_seg[0].strip().replace("display_name", "display_name")  # alias as needed
                        value = parts_seg[1].strip().strip("\"")
                        expressions.append((field, op, value))
                        break
                else:
                    # Special case: display_name:"text" where operator is actually ':'
                    if "display_name:" in seg:
                        parts_seg = seg.split("display_name:", 1)
                        field = "display_name"
                        value = parts_seg[1].strip().strip("\"")
                        # For display_name, operator is implicitly HAS.
                        expressions.append((field, "HAS", value))
            return expressions

        def apply_filters(spaces: list, expressions: list) -> list:
            filtered = []
            for sp in spaces:
                match_all = True
                for (field, op, value) in expressions:
                    # Skip expressions for required fields that we've already enforced.
                    if field in ("customer", "space_type"):
                        continue
                    # For HAS operator, treat it like display_name.
                    if op == "HAS":
                        if not matches_field(sp, field, op, value):
                            match_all = False
                            break
                    else:
                        if not matches_field(sp, field, op, value):
                            match_all = False
                            break
                if match_all:
                    filtered.append(sp)
            return filtered

        # --- Main body of search() ---
        if useAdminAccess is not True:
            print("Error: Only admin access is supported (useAdminAccess must be true).")
            return {}

        # Validate required query: must include customer = "customers/my_customer" AND space_type = "SPACE"
        query_lower = query.lower() if query else ""
        if 'customer =' not in query_lower or 'customers/my_customer' not in query_lower:
            print("Error: query must include customer = \"customers/my_customer\".")
            return {}
        if 'space_type' not in query_lower or '"space"' not in query_lower:
            print("Error: query must include space_type = \"SPACE\".")
            return {}

        # Set pageSize and pageToken.
        ps = default_page_size(pageSize)
        offset = parse_page_token(pageToken)

        # 1) Filter DB["Space"] by required fields.
        candidate_spaces = []
        for sp in DB["Space"]:
            if sp.get("customer", "").lower() != "customers/my_customer":
                continue
            if sp.get("spaceType") != "SPACE":
                continue
            candidate_spaces.append(sp)

        # 2) Parse additional filters from query.
        expressions = parse_filter(query)
        candidate_spaces = apply_filters(candidate_spaces, expressions)

        # 3) Ordering.
        # Default order: create_time ASC. Otherwise, orderBy string is parsed.
        if orderBy:
            parts_order = orderBy.split()
            sort_field = parts_order[0].strip().lower()
            sort_order = "ASC"
            if len(parts_order) > 1 and parts_order[1].upper() == "DESC":
                sort_order = "DESC"
        else:
            sort_field = "create_time"
            sort_order = "ASC"

        def sort_key(sp):
            if sort_field == "membership_count.joined_direct_human_user_count":
                return sp.get("membershipCount", {}).get("joined_direct_human_user_count", 0)
            elif sort_field == "last_active_time":
                return sp.get("lastActiveTime", "")
            elif sort_field == "create_time":
                return sp.get("createTime", "")
            return ""
        candidate_spaces.sort(key=sort_key, reverse=(sort_order == "DESC"))

        # 4) Pagination: slice the list.
        total = len(candidate_spaces)
        end = offset + ps
        page_items = candidate_spaces[offset:end]
        nextPageToken = str(end) if end < total else None

        result = {"spaces": page_items}
        if nextPageToken:
            result["nextPageToken"] = nextPageToken

        print(f"SearchSpacesResponse: {result}")
        return result



    @staticmethod
    def get(name: str, useAdminAccess: bool = None) -> None:
        """
        Returns details about a space:
          - name: e.g. "spaces/AAAA"
          - useAdminAccess: if True, the caller is an admin and can view any space.
                          if False or None, the user must be a member to see it.

        For simplicity, returns {} if the space is not found or the user lacks permission.
        In production, you'd return a proper 403 or 404 error.
        """

        # 1) Find the space in DB["Space"]
        found_space = {}
        for sp in DB["Space"]:
            if sp.get("name") == name:
                found_space = sp
                break

        # 3) If admin privileges are used, return the space directly
        if useAdminAccess:
            return found_space

        # 4) Otherwise, check if the CURRENT_USER_ID is a member of the space
        membership_name = f"{name}/members/{CURRENT_USER_ID}"
        is_member = False
        for mem in DB["Membership"]:
            if mem.get("name") == membership_name:
                is_member = True
                break

        # 5) Return the space if user is a member; otherwise, empty
        if is_member:
            return found_space
        else:
            return {}

    @staticmethod
    def create(requestId: str = None, space: dict = {}) -> dict:
        """
        Creates a space.

        Parameters (as per documentation):
          - requestId (str, optional): A unique identifier for this request.
          - The request body is a Space resource (passed in the `space` parameter):
          {
            "spaceType": "SPACE",
            "displayName": "My New Space",
            "spaceDetails": {
                "description": "A space for discussing project X.",
                "guidelines": "Be respectful and stay on topic."
            },
            "externalUserAllowed": true
            }

        Returns:
          dict: The created Space resource, or {} on error.
        """
        if space is None:
            space = {}

        # 1. Validate spaceType and displayName
        space_type = space.get("spaceType")
        display_name = space.get("displayName", "").strip()

        if not space_type:
            print("Error: spaceType is required.")
            return {}

        if space_type == "SPACE" and not display_name:
             print("Error: displayName is required when spaceType is SPACE")
             return{}

        # 2. Check for duplicate displayName
        if space_type == "SPACE" and display_name:
          for sp in DB["Space"]:
              if sp.get("displayName", "").strip().lower() == display_name.lower():
                  print(f"Error: A space with displayName '{display_name}' already exists.")
                  return {}

        # 3. Generate space name if not provided
        space_id = f"SPACE_{len(DB['Space']) + 1}"
        space["name"] = f"spaces/{space_id}"

        # 4. Prepare the new space object
        new_space = space.copy()
        new_space.setdefault("singleUserBotDm", False)
        new_space.setdefault("externalUserAllowed", False)
        new_space.setdefault("importMode", False)
        new_space["createTime"] = datetime.utcnow().isoformat() + "Z"


        # 6. Save the space
        DB["Space"].append(new_space)
        print(f"Space created: {new_space['name']}")


        # 7. Create membership for the calling user (if not importMode)
        if not new_space.get("importMode") and (space_type != "DIRECT_MESSAGE" or not space.get("singleUserBotDm")):
            membership_name = f"{new_space['name']}/members/{CURRENT_USER_ID}"
            membership = {
                "name": membership_name,
                "state": "JOINED",
                "role": "ROLE_MANAGER",
                "member": {
                    "name": CURRENT_USER_ID,
                     #Look for user in DB
                    "displayName": next((user["displayName"] for user in DB["User"] if user["name"] == CURRENT_USER_ID), None),
                    "type": "HUMAN",
                },
                "createTime": datetime.utcnow().isoformat() + "Z"
            }
            DB["Membership"].append(membership)
            print(f"Membership created for calling user: {membership_name}")

        return new_space



    @staticmethod
    def setup(setup_body: dict) -> dict:
        """
        Sets up a space with initial members.

        Request Body (SetUpSpaceRequest) example:
          {
            "space": {
                "spaceType": "SPACE",
                "displayName": "My New Space",
                "spaceDetails": {
                    "description": "A space for discussing project X.",
                    "guidelines": "Be respectful and stay on topic."
                },
                "externalUserAllowed": true
            },
            "memberships": [
              {
                "member": {
                  "name": "users/otheruser@example.com",
                  "type": "HUMAN",
                  "displayName": "Other User"
                },
                "role": "ROLE_MEMBER"
              },
              ... additional memberships ...
            ]
          }

        Behavior:
          - Creates a new space using the details in setup_body["space"].
          - If a space with the same displayName already exists, it returns {} (simulating ALREADY_EXISTS).
          - Generates a resource name if not provided (format: "spaces/SPACE_N").
          - If importMode is false, automatically adds the calling user (CURRENT_USER_ID) as a member.
          - Processes additional memberships provided in setup_body["memberships"].
            Any membership that targets the calling user is ignored.

        Returns:
          dict: The newly created Space resource, or {} on error.
        """
        print(f"setup_space called with setup_body={setup_body}")

        # Extract space details and memberships from the request body.
        space_req = setup_body.get("space", {})
        memberships_req = setup_body.get("memberships", [])

        new_space = Spaces.create(space=space_req)

        # Remove any membership targeting the calling user.
        for mem in memberships_req:
            mem_member = mem.get("member", {}).get("name", "").strip()
            if mem_member.lower() == CURRENT_USER_ID.lower():
                print("Skipping membership for the calling user (already added).")
                continue

            # Build membership resource name: must be in the format "spaces/{space}/members/{member}"
            membership_name = f"{new_space['name']}/members/{mem_member}"
            mem["name"] = membership_name
            mem.setdefault("role", "ROLE_MEMBER")
            mem.setdefault("state", "INVITED")
            mem.setdefault("createTime", datetime.utcnow().isoformat() + "Z")
            DB["Membership"].append(mem)
            print(f"Added membership: {membership_name}")

        return new_space

    @staticmethod
    def patch(name: str, updateMask: str, space_updates: dict, useAdminAccess: bool = False) -> dict:
        """
        Updates a space.

        Parameters:
          - name (str): Required. Resource name of the space (e.g., "spaces/AAA").
          - updateMask (str): Required. A comma-separated list of field paths to update (or "*" to update all supported fields).
            Supported field paths:
              • space_details              (updates the description inside spaceDetails)
              • display_name               (only for spaces with spaceType "SPACE")
              • space_type                 (only supports changing GROUP_CHAT to SPACE; if provided, display_name must be non-empty)
              • space_history_state        (updates the space history state; must be the only field updated)
              • access_settings.audience   (updates the audience in accessSettings; only for spaces of type "SPACE")
              • permission_settings        (replaces the entire permissionSettings object)
          - space_updates (dict): Request body, a Space resource with the updated field values.
          - useAdminAccess (bool, optional): If true, the method runs with admin privileges. Some field masks are not supported when using admin access.

        Returns:
          dict: The updated Space resource, or {} if not found or error.
        """
        print(f"patch_space called with name={name}, updateMask={updateMask}, useAdminAccess={useAdminAccess}, space_updates={space_updates}")

        # 1) Locate the space in DB by matching the name exactly.
        target_space = None
        for sp in DB["Space"]:
            if sp.get("name") == name:
                target_space = sp
                break
        if not target_space:
            print("Space not found.")
            return {}

        # 2) Parse the updateMask.
        if updateMask.strip() == "*":
            # Update all supported fields.
            masks = [
                "space_details", "display_name", "space_type",
                "space_history_state", "access_settings.audience", "permission_settings"
            ]
        else:
            masks = [m.strip() for m in updateMask.split(",")]

        # 3) Update each supported field.
        for mask in masks:
            if mask == "space_details":
                # Update the description inside spaceDetails.
                # Check if "spaceDetails" exists in the request body and contains "description".
                if "spaceDetails" in space_updates and "description" in space_updates["spaceDetails"]:
                    new_desc = space_updates["spaceDetails"]["description"]
                    # Limit description to 150 characters.
                    target_space.setdefault("spaceDetails", {})["description"] = new_desc[:150]
                else:
                    print("No spaceDetails.description provided; skipping.")
            elif mask == "display_name":
                # Update displayName if the current spaceType is "SPACE".
                if target_space.get("spaceType") == "SPACE":
                    if "displayName" in space_updates:
                        target_space["displayName"] = space_updates["displayName"]
                    else:
                        print("displayName not provided in updates; skipping.")
                else:
                    print("displayName update is only supported for spaces of type SPACE; skipping.")
            elif mask == "space_type":
                # Allowed only if current spaceType is GROUP_CHAT and new value is SPACE.
                current_type = target_space.get("spaceType")
                new_type = space_updates.get("spaceType")
                if current_type == "GROUP_CHAT" and new_type == "SPACE":
                    # Additionally, if updating displayName along with space_type, ensure it's non-empty.
                    if "displayName" in space_updates and space_updates["displayName"].strip() != "":
                        target_space["spaceType"] = "SPACE"
                    else:
                        print("Invalid update: displayName must be non-empty when changing space_type.")
                        return {}
                else:
                    print("Invalid space_type update: Only GROUP_CHAT -> SPACE is supported; skipping.")
            elif mask == "space_history_state":
                # Updates the space history state. Per doc, this must be updated alone.
                # (Here, we do not enforce the "alone" requirement.)
                if "spaceHistoryState" in space_updates:
                    target_space["spaceHistoryState"] = space_updates["spaceHistoryState"]
                else:
                    print("spaceHistoryState not provided; skipping.")
            elif mask == "access_settings.audience":
                # Updates accessSettings.audience. Supported only for spaces with type SPACE.
                if target_space.get("spaceType") == "SPACE":
                    if "accessSettings" in space_updates and "audience" in space_updates["accessSettings"]:
                        target_space.setdefault("accessSettings", {})["audience"] = space_updates["accessSettings"]["audience"]
                    else:
                        print("access_settings.audience not provided; skipping.")
                else:
                    print("access_settings.audience update is supported only for spaces of type SPACE; skipping.")
            elif mask == "permission_settings":
                # Replaces the entire permissionSettings object.
                if "permissionSettings" in space_updates:
                    target_space["permissionSettings"] = space_updates["permissionSettings"]
                else:
                    print("permission_settings not provided; skipping.")
            else:
                print(f"Unsupported update mask field: {mask}; skipping.")

        print(f"Updated space: {target_space}")
        return target_space

    @staticmethod
    def delete(name: str, useAdminAccess: bool = None) -> None:
        """
        Deletes the specified space (cascading remove of child resources),
        returning an empty dict if not found or unauthorized.

        Args:
          name (str): Resource name of the space to delete, e.g. "spaces/SPACE_1"
          useAdminAccess (bool): If True, no membership check is required.
          CURRENT_USER_ID_ID (str): The ID of the user calling this method.

        """
        print(f"Deleting space: {name}, useAdminAccess={useAdminAccess}, CURRENT_USER_ID={CURRENT_USER_ID}")

        # 1) Find the space
        target_space = None
        for sp in DB["Space"]:
            if sp.get("name") == name:
                target_space = sp
                break

        # 2) If space not found, return {}
        if not target_space:
            print(f"No space found with name={name}")
            return {}

        # 3) If not admin, user must be a member
        if not useAdminAccess and CURRENT_USER_ID:
            # Check membership
            membership_name = f"{name}/members/{CURRENT_USER_ID}"
            is_member = False
            for mem in DB["Membership"]:
                if mem.get("name") == membership_name:
                    is_member = True
                    break
            if not is_member:
                print(f"User {CURRENT_USER_ID} is not a member of {name} => unauthorized.")
                return {}

        # 4) Remove space from DB
        DB["Space"].remove(target_space)
        print(f"Space '{name}' removed from DB.")

        # 5) Remove all child resources referencing this space
        #    We'll do it by checking membership, message, reaction names that start with "spaces/SPACE_ID"
        to_remove_memberships = []
        for m in DB["Membership"]:
            if m.get("name", "").startswith(name + "/"):
                to_remove_memberships.append(m)
        for m in to_remove_memberships:
            DB["Membership"].remove(m)
            print(f"Removed membership: {m['name']}")

        to_remove_messages = []
        for msg in DB["Message"]:
            if msg.get("name", "").startswith(name + "/"):
                to_remove_messages.append(msg)
        for msg in to_remove_messages:
            DB["Message"].remove(msg)
            print(f"Removed message: {msg['name']}")

        # If there are Reaction or Attachment resources, we do similarly
        to_remove_reactions = []
        if "Reaction" in DB:
            for r in DB["Reaction"]:
                if r.get("name", "").startswith(name + "/"):
                    to_remove_reactions.append(r)
            for r in to_remove_reactions:
                DB["Reaction"].remove(r)
                print(f"Removed reaction: {r['name']}")

        # 6) Return empty response to indicate success
        print(f"Space '{name}' and all child resources deleted.")
        return {}
    # ---------------------------------------------------------------------------------------
    # Resource: Spaces.Messages
    # ---------------------------------------------------------------------------------------
    class Messages:
        """Handles operations under /spaces/.../messages."""

        @staticmethod
        def create(parent: str, requestId: str = None,
                   messageReplyOption: str = 'MESSAGE_REPLY_OPTION_UNSPECIFIED', messageId: str = None, message_body: dict = None) -> None:

              """
              Creates a message in a space. The space is identified by `parent`, e.g. "spaces/AAA".
              We require that the caller (CURRENT_USER_ID) is a member of "spaces/{parent}/members/{CURRENT_USER_ID}".

              Args:
                parent (str): The full space name, e.g. "spaces/AAA".
                requestId (str): Optional unique request ID for idempotency. If re-used by same user => same message, else conflict => {}.
                messageReplyOption (str): e.g. "REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD".
                messageId (str): Optional. Must start with "client-" if provided. Becomes part of the message's name.
                message_body (dict): The message resource from the request body (text is required) as shown below:

                {
                    "text": "This is a message with all optional fields.",
                    "clientAssignedMessageId": "my-custom-message-id",
                    "thread": {
                        "name": "spaces/space123/threads/threadABC"
                    },
                    "messageReplyOption": "REPLY_MESSAGE_FAIL_IF_NOT_FOUND",
                    "attachment": [
                        {
                            "name": "attachment_id"
                        }
                    ],
                    "fallbackText": "Fallback text for the card.",
                    "accessoryWidgets": [
                        {
                        "decoratedText": {
                            "text": "some text",
                            "startIcon": {
                                "iconUrl": "www.example.com"
                            }
                        }
                        }
                    ],
                        "privateMessageViewer": {
                            "name": "users/someuser"
                        }
                }

              Returns:
                dict: The created (or existing) message object, or {} if conflict/error.
              """

              if not message_body:
                  print('no message body is provided')
                  return {}

              # 1) Verify membership => name = "spaces/{parent}/members/{CURRENT_USER_ID}"
              membership_name = f"{parent}/members/{CURRENT_USER_ID}"
              is_member = any(m.get("name") == membership_name for m in DB["Membership"])
              if not is_member:
                  print(f"Error: user {CURRENT_USER_ID} is not a member of {parent}.")
                  return {}

              if messageId:
                  if not messageId.startswith("client-"):
                      print("Error: messageId must start with 'client-'.")
                      return {}
                  new_msg_name = f"{parent}/messages/{messageId}"
              else:
                  # generate a numeric ID
                  new_msg_name = f"{parent}/messages/{len(DB['Message']) + 1}"

              # 4) Build the new message object
              new_message = {
                  "name": new_msg_name,
                  "text": message_body.get("text", ""),
                  "attachment": message_body.get("attachment", []),
                  "createTime": datetime.now().isoformat() + "Z",
                  "thread": message_body.get("thread", {}),
                  # The sender is set from the user ID (in reality, the server would do this, but we'll store it here)
                  "sender": {
                      "name": CURRENT_USER_ID,
                      "type": "HUMAN"
                  }
              }

              # If messageReplyOption is set, store it
              if messageReplyOption:
                  pass

              # If messageId is set, store it as clientAssignedMessageId
              if messageId:
                  new_message["clientAssignedMessageId"] = messageId

              # 5) Insert into DB
              DB["Message"].append(new_message)
              print(f"Message {new_msg_name} created successfully.")


              return new_message


        @staticmethod
        def list(parent: str, pageSize: int = None, pageToken: str = None,
                 filter: str = None, orderBy: str = None, showDeleted: bool = None) -> None:
                """
                Lists messages in a space (parent='spaces/AAA') where the caller is a member.

                Args:
                  parent (str): Required. Resource name of the space, e.g. "spaces/AAA".
                  pageSize (int): Optional max number of messages (default 25, max 1000).
                  pageToken (str): Optional page offset (naive integer).
                  filter (str): Optional. e.g. create_time > "2023-01-01T00:00:00Z" AND thread.name=spaces/AAA/threads/THREAD1
                  orderBy (str): Optional. e.g. "ASC" or "DESC" (defaults to create_time ASC)
                  showDeleted (bool): If False, skip messages with deleteTime != ""
                  CURRENT_USER_ID (str): The user calling this method.

                Returns:
                  dict: "ListMessagesResponse" with:
                    {
                      "messages": [...],
                      "nextPageToken": "...",
                    }
                  If no messages, "messages" is an empty list or omitted nextPageToken.
                """
                print(f"Listing messages in {parent} with pageSize={pageSize}, pageToken={pageToken}, "
                      f"filter={filter}, orderBy={orderBy}, showDeleted={showDeleted}, CURRENT_USER_ID={CURRENT_USER_ID}")

                # 1) Check membership
                #    The user must have a membership named "spaces/AAA/members/{CURRENT_USER_ID}" in DB["Membership"]
                membership_name = f"{parent}/members/{CURRENT_USER_ID}"
                user_is_member = any(mem.get("name") == membership_name for mem in DB["Membership"])
                if not user_is_member:
                    print("Caller is not a member of this space => no access.")
                    # In real usage, you'd raise an error (403). We'll return empty for demonstration.
                    return {"messages": []}

                # 2) Default pageSize => 25, must not exceed 1000, must not be negative
                if pageSize is None:
                    pageSize = 25
                if pageSize < 0:
                    raise ValueError("pageSize cannot be negative.")
                if pageSize > 1000:
                    pageSize = 1000

                # 3) Convert pageToken to offset
                offset = 0
                if pageToken:
                    try:
                        offset_val = int(pageToken)
                        if offset_val >= 0:
                            offset = offset_val
                    except ValueError:
                        pass  # ignore invalid => offset=0

                # 4) Gather messages that belong to 'parent'
                #    Typically, "name" is "spaces/AAA/messages/MSGID"
                #    We'll keep only those that start with parent + "/messages/"
                all_msgs = []
                for msg in DB["Message"]:
                    if msg.get("name", "").startswith(parent + "/messages/"):
                        all_msgs.append(msg)

                # 5) If showDeleted != True, skip messages that have a non-empty deleteTime
                if not showDeleted:
                    filtered_msgs = []
                    for m in all_msgs:
                        if not m.get("deleteTime"):
                            filtered_msgs.append(m)
                    all_msgs = filtered_msgs

                # 6) Filter parse: e.g. "create_time > "2023-01-01T00:00:00Z" AND thread.name=spaces/AAA/threads/123"
                #    We'll do a naive approach by splitting on "AND" and checking each condition.
                if filter:
                    segments = filter.split("AND")
                    def matches_filter(msg_obj):
                        for seg in segments:
                            seg_str = seg.strip()
                            seg_lower = seg_str.lower()

                            # thread.name = spaces/AAA/threads/XYZ
                            if "thread.name" in seg_lower:
                                # parse out the right side
                                if "=" not in seg_str:
                                    return False
                                lhs, rhs = seg_str.split("=", 1)
                                rhs_val = rhs.strip()
                                # e.g. "spaces/AAA/threads/THREAD1"
                                if msg_obj.get("thread", {}).get("name", "") != rhs_val:
                                    return False

                            # create_time > "2023-01-01T00:00:00Z"
                            # create_time < "2023-02-01T00:00:00Z"
                            if "create_time" in seg_lower:
                                # find operator >, <, ...
                                possible_ops = [">", "<", ">=", "<="]
                                chosen_op = None
                                for op in possible_ops:
                                    if op in seg_str:
                                        chosen_op = op
                                        break
                                if not chosen_op:
                                    return False

                                lhs, rhs = seg_str.split(chosen_op, 1)
                                compare_time = rhs.strip().strip('"')
                                msg_time = msg_obj.get("createTime", "")

                                # Very naive string compare. Real code should parse RFC-3339 as datetime objects.
                                if chosen_op == ">":
                                    if not (msg_time > compare_time):
                                        return False
                                elif chosen_op == "<":
                                    if not (msg_time < compare_time):
                                        return False
                                elif chosen_op == ">=":
                                    if not (msg_time >= compare_time):
                                        return False
                                elif chosen_op == "<=":
                                    if not (msg_time <= compare_time):
                                        return False

                        return True

                    # apply matches_filter
                    filtered_msgs = [m for m in all_msgs if matches_filter(m)]
                    all_msgs = filtered_msgs

                # # 7) Order by create_time (default ASC, or "DESC")
                # sort_desc = (orderBy and orderBy.upper() == "DESC")
                # # default to ascending if no orderBy provided
                # print(all_msgs)
                # all_msgs.sort(key=lambda x: x.get("createTime", ""), reverse=sort_desc)

                # 8) Apply offset + pageSize
                total = len(all_msgs)
                page_end = offset + pageSize
                page_items = all_msgs[offset:page_end]
                next_token = None
                if page_end < total:
                    next_token = str(page_end)

                # 9) Build the response (ListMessagesResponse)
                response = {
                    "messages": page_items
                }
                if next_token:
                    response["nextPageToken"] = next_token

                return response

        @staticmethod
        def get(name: str) -> None:
              """
              Returns details about a message by name:
                name format: "spaces/{space}/messages/{message}"

              1) Parse out the {space} portion from the path to check membership.
              2) If the caller isn't a member of that space, return {} (or raise error).
              3) Find the message in DB["Message"] by 'name'.
              4) Return the found message or {} if not found.

              Args:
                name (str): Required. e.g. "spaces/AAA/messages/123" or "spaces/AAA/messages/client-custom-id"
                CURRENT_USER_ID (str): The ID of the user requesting this message.

              Returns:
                dict: The message resource or {} if not found / no permission.
              """
              print(f"get_message called with name={name}, CURRENT_USER_ID={CURRENT_USER_ID}")

              # 1) Parse out the space portion from name => "spaces/AAA" is the first 2 segments
              parts = name.split("/")
              if len(parts) < 4:
                  print("Error: invalid message name format.")
                  return {}
              # expected: ["spaces", "AAA", "messages", "MESSAGE_ID"]
              # so the space name is e.g. "spaces/AAA" from the first 2 elements
              space_name = "/".join(parts[:2])  # => "spaces/AAA"

              # 2) Check membership => "spaces/AAA/members/{CURRENT_USER_ID}"
              membership_name = f"{space_name}/members/{CURRENT_USER_ID}"
              is_member = any(m.get("name") == membership_name for m in DB["Membership"])
              if not is_member:
                  print(f"Caller {CURRENT_USER_ID} is not a member of {space_name} => no permission.")
                  return {}

              # 3) Find the message
              found_msg = None
              for msg in DB["Message"]:
                  if msg.get("name") == name:
                      found_msg = msg
                      break

              # 4) Return the message or {}
              if not found_msg:
                  print(f"No message found with name={name}")
                  return {}

              print(f"Found message: {found_msg}")
              return found_msg

        def update(name: str, updateMask: str, allowMissing: bool, body: dict) -> dict:
              """
              PUT /v1/{+name}?updateMask=&allowMissing=

              - name (str): e.g. "spaces/AAA/messages/1" or "spaces/AAA/messages/client-custom-id".
              - updateMask (str): Comma-separated field paths or "*" for everything.
                                Valid fields per docs:
                                "text", "attachment", "cards", "cards_v2", "accessory_widgets".
              - allowMissing (bool): If true and message doesn't exist, create it,
                                    but only if the ID is client-assigned (starts with "client-").
              - body (dict): The request body, a `Message` resource with fields:
                  {
                    "text": "...",
                    "attachment": [...],
                    "cards": [...],
                    "cardsV2": [...],
                    "accessoryWidgets": [...]
                  }
                The doc says these are the fields you can update.
                If absent from `updateMask`, they're ignored.

              Returns:
                dict: The updated (or newly created) message. Or {} if error.

              Exactly matches the doc's parameters:
                - Path param: name
                - Query params: updateMask, allowMissing
                - Request body: Message
              """

              print(f"update_message called: name={name}, updateMask={updateMask}, allowMissing={allowMissing}")

              # 1) Look for existing message
              existing = None
              for msg in DB["Message"]:
                  if msg["name"] == name:
                      existing = msg
                      break

              # 2) If not found => maybe create if allowMissing and client-assigned ID
              if not existing:
                  if allowMissing:
                      # The doc: "If `true` and the message isn't found, a new message is created and `updateMask` is ignored.
                      #           The specified message ID must be client-assigned or the request fails."
                      # So we check if the last path segment starts with "client-"
                      parts = name.split("/")
                      if len(parts) < 4 or parts[2] != "messages":
                          print("Invalid name format.")
                          return {}
                      msg_id = parts[3]  # e.g. "client-xyz"

                      if not msg_id.startswith("client-"):
                          print("Not found, allowMissing=True but ID isn't client- => fail.")
                          return {}

                      print("Message not found => create new with client ID.")
                      # create minimal new message
                      existing = {
                          "name": name,
                          "text": "",
                          "attachment": [],
                      }
                      DB["Message"].append(existing)
                  else:
                      print("Message not found, allowMissing=False => can't update.")
                      return {}

              # 3) Parse updateMask
              valid_fields = ["text", "attachment", "cards", "cards_v2", "accessory_widgets"]
              if updateMask.strip() == "*":
                  fields_to_update = valid_fields
              else:
                  fields_to_update = [f.strip() for f in updateMask.split(",")]

              # 4) Apply updates from request body
              for field in fields_to_update:
                  if field not in valid_fields:
                      print(f"Skipping unknown or unsupported field '{field}'.")
                      continue

                  # Note: doc says "cards_v2", but in code we might store it as "cardsV2".
                  # We'll unify the naming so that "cards_v2" from doc => "cardsV2" in DB.
                  if field == "cards_v2":
                      internal_field = "cardsV2"
                  else:
                      internal_field = field

                  # If the body has that field, update. If not, skip it.
                  if field in body or internal_field in body:
                      # If body uses "cards_v2", we do body.get(field) or body.get(internal_field).
                      new_val = body.get(field, body.get(internal_field))
                      existing[internal_field] = new_val

              print(f"Updated message => {existing}")
              return existing



        @staticmethod
        def patch(name: str, updateMask: str, allowMissing: bool = None, message: dict = None) -> None:
            """Update a message (PATCH)."""
            print(f"Patching message {name} with updateMask={updateMask}, "
                  f"allowMissing={allowMissing}, message={message}")

        @staticmethod
        def delete(name: str, force: bool = None) -> None:
            """
            Deletes a message.

            Args:
              name (str): Required path param. e.g. "spaces/AAA/messages/123"
              force (bool): Optional query param. If true, also deletes threaded replies.
                            If false and the message has replies => fail.

            Returns:
              dict: an empty dict (simulating an empty response) if success or if fails, the same.
                    In a real app, you'd return a 404/403 or some other error code.

            Behavior:
              1) Find the message in DB["Message"] by 'name'.
              2) Check if the message has any threaded replies in DB. If found and force=false => fail.
              3) If force=true, remove the message and its replies.
              4) If force=false and no replies, remove the message.
              5) Return {} to simulate an Empty response.
            """

            print(f"delete_message called with name={name}, force={force}")

            # 1) Locate the message
            target_msg = None
            for m in DB["Message"]:
                if m.get("name") == name:
                    target_msg = m
                    break

            if not target_msg:
                print("Message not found => returning empty.")
                return {}

            # 2) Check for threaded replies. We'll say a "reply" is any message whose
            #    thread references target_msg["name"] as "thread.parent"
            message_threads = target_msg.get("thread", {}).get('name','')
            replies = []
            for m in DB["Message"]:
                thread = m.get("thread", {})
                if thread.get("name") == message_threads:
                    replies.append(m)

            if replies:
                # We have threaded replies
                if not force:
                    # fail => can't delete this parent
                    print(f"Message {name} has replies => need force=true => fail.")
                    return {}
                else:
                    # force=true => remove the replies too
                    for r in replies:
                        DB["Message"].remove(r)
                        print(f"Deleted reply => {r['name']}")

            # 3) Remove the target message
            DB["Message"].remove(target_msg)
            print(f"Message {name} deleted.")
            return {}  # simulating an Empty response



        # ---------------------------------------------------------------------------------------
        # Resource: Spaces.Messages.Attachments
        # ---------------------------------------------------------------------------------------

        class Attachments:
            """Handles operations under /spaces/.../messages/.../attachments."""

            @staticmethod
            def get(name: str) -> dict:
                """
                Retrieves attachment metadata by its resource name.
                Name format: "spaces/{space}/messages/{message}/attachments/{attachment}"

                Steps:
                  1) Parse out the parent message => "spaces/AAA/messages/123".
                  2) Find that message in DB.
                  3) Look in message["attachment"] for an item whose "name" == name.
                  4) Return the attachment (dict) if found, else {}.
                """
                print(f"Attachments.get called with name={name}")

                # 1) Extract the parent portion => "spaces/AAA/messages/123"
                parts = name.split("/")
                if len(parts) < 5 or parts[0] != "spaces" or parts[2] != "messages" or parts[4] != "attachments":
                    print("Invalid attachment name format.")
                    return {}

                # Rejoin the first 4 segments => "spaces/AAA/messages/123"
                parent_message_name = "/".join(parts[:4])  # e.g. "spaces/AAA/messages/123"
                attachment_id = parts[4]  # Should be "attachments", but we already check above
                # Actually the real attachment ID is parts[5], if it exists
                if len(parts) < 6:
                    print("Attachment ID is missing.")
                    return {}

                attachment_res_id = parts[5]  # e.g. "ATT1"

                # So the full name is "spaces/AAA/messages/123/attachments/ATT1"
                # But we already have that in 'name'. We'll just confirm if it matches.

                # 2) Find the message in DB
                found_message = None
                for msg in DB["Message"]:
                    if msg.get("name") == parent_message_name:
                        found_message = msg
                        break

                if not found_message:
                    print(f"Parent message not found: {parent_message_name}")
                    return {}

                # 3) Search the message's "attachment" list for one with "name" == full 'name'
                for att in found_message.get("attachment", []):
                    if att.get("name") == name:
                        print(f"Found attachment => {att}")
                        return att

                # Not found
                print(f"No attachment found with name={name}")
                return {}

        # ---------------------------------------------------------------------------------------
        # Resource: Spaces.Messages.Reactions
        # ---------------------------------------------------------------------------------------

        class Reactions:
            """Handles operations under /spaces/.../messages/.../reactions."""

            @staticmethod
            def create(parent: str, reaction: dict) -> None:
                """
                Creates a reaction and adds it to a message.

                Args:
                  parent (str): e.g. "spaces/AAA/messages/111"
                  reaction_body (dict): The Reaction resource from the request body, e.g.
                    {
                      "emoji": {
                        "unicode": "🙂"
                        // or "custom_emoji": { "uid": "XYZ" }
                      },
                      "user": {
                        "name": "users/USER123"
                        // possibly other user fields
                      }
                    }

                Returns:
                  dict: The created Reaction resource, or {} if error.

                Steps:
                  1) Validate parent format => "spaces/{space}/messages/{message}".
                  2) Generate a new name => parent + "/reactions/{ID}".
                  3) Insert into DB["Reaction"] and return it.
                """
                print(f"Reactions.create called with parent={parent}, reaction_body={reaction}")

                # 1) Validate parent format
                parts = parent.split("/")
                if len(parts) < 4 or parts[0] != "spaces" or parts[2] != "messages":
                    print("Invalid parent format.")
                    return {}

                # 2) Generate a reaction name
                new_id = str(len(DB["Reaction"]) + 1)
                reaction_name = f"{parent}/reactions/{new_id}"

                # 3) Build the reaction object
                new_reaction = {
                    "name": reaction_name,
                    "emoji": reaction.get("emoji", {}),
                    "user": reaction.get("user", {})
                }

                # Insert into DB
                DB["Reaction"].append(new_reaction)
                print(f"Created reaction => {new_reaction}")
                return new_reaction

            @staticmethod
            def list(parent: str, pageSize: int = None, pageToken: str = None, filter: str = None) -> None:
                """
                Lists reactions to a message.

                Args:
                  parent (str): e.g. "spaces/AAA/messages/111"
                  pageSize (int, optional): max # of reactions to return (default 25, max 200).
                  pageToken (str, optional): naive page offset as an integer string.
                  filter (str, optional): e.g. "emoji.unicode = \"🙂\" OR emoji.unicode = \"👍\" AND user.name = \"users/USER123\""

                Returns:
                  dict: In the shape of:
                    {
                      "reactions": [...],
                      "nextPageToken": "...",
                    }
                  If no more data, nextPageToken is omitted.

                Steps:
                  1) Gather all reactions whose name starts with {parent}.
                  2) Optionally parse filter => naive approach for 'emoji.unicode', 'emoji.custom_emoji.uid', 'user.name'.
                  3) Paginate with pageSize, pageToken.
                """
                print(f"Reactions.list called with parent={parent}, pageSize={pageSize}, pageToken={pageToken}, filter={filter}")

                # Default pageSize
                if pageSize is None:
                    pageSize = 25
                if pageSize > 200:
                    pageSize = 200
                if pageSize < 0:
                    pageSize = 25  # or error

                # parse pageToken => offset
                offset = 0
                if pageToken:
                    try:
                        off = int(pageToken)
                        if off >= 0:
                            offset = off
                    except ValueError:
                        pass  # ignore

                # 1) collect all reactions for parent
                all_rxns = []
                for r in DB["Reaction"]:
                    if r["name"].startswith(parent + "/reactions/"):
                        all_rxns.append(r)

                # 2) apply filter if provided
                # The doc says we can do expressions like:
                #   user.name = "users/USERA" OR user.name = "users/USERB"
                #   emoji.unicode = "🙂" OR emoji.custom_emoji.uid = "XYZ"
                #   AND between user and emoji
                # We'll do a minimal approach:
                def _reaction_matches_filter(rxn: dict, tokens: list) -> bool:
                    """
                    A minimal parse for filter tokens. For example:
                      tokens = ["emoji.unicode", "=", "\"🙂\"", "AND", "user.name", "=", "\"users/USER111\""]
                    We'll find expressions of the form [field, "=", quoted_value] and keep track of OR or AND.

                    The doc says valid queries:
                      user.name = "users/AAAAAA"
                      emoji.unicode = "🙂"
                      emoji.custom_emoji.uid = "UID"
                    We can have OR among the same field type, AND between user and emoji, etc.
                    We'll do something extremely naive:
                      - We group the tokens into expressions and operators.
                      - If an expression is "field = \"value\"", we test rxn's field.

                    This won't fully cover parentheses or advanced combos, but demonstrates the concept.
                    """
                    # We'll parse out expressions of the form (field, "=", value) plus "AND"/"OR" in between.
                    expressions = []
                    operators = []
                    i = 0
                    while i < len(tokens):
                        t = tokens[i]
                        if t.upper() in ("AND", "OR"):
                            operators.append(t.upper())
                            i += 1
                        else:
                            # expect something like "field", "=", "\"value\""
                            if i + 2 < len(tokens) and tokens[i+1] == "=":
                                field = tokens[i]
                                val = tokens[i+2].strip('"')
                                expressions.append((field, val))
                                i += 3
                            else:
                                # invalid parse => skip
                                return False

                    # We then interpret them in a naive way:
                    # - For each expression, check if rxn satisfies it.
                    # - If we see "AND", we require both. If we see "OR", we require either. The doc has constraints about grouping.
                    # We'll do a simplistic approach:
                    if not expressions:
                        return True

                    # We'll handle them in sequence: expression1 (operator) expression2 (operator) expression3 ...
                    # For the doc: "OR" can appear among the same field type, "AND" can appear between different field types
                    # We'll apply a partial approach: if any "OR", we treat them as "field matches any of these" if same field, or fail if different.

                    # We'll group expressions by field to handle the doc's constraints (only OR within the same field).
                    # Then AND across different fields. This is still simplistic but closer to the doc's rules.
                    # e.g. user.name = "users/USER111" OR user.name = "users/USER222"
                    # AND emoji.unicode = "🙂" OR emoji.unicode = "👍"

                    # We'll transform expressions + operators into groups.
                    # Example: [("emoji.unicode", "🙂"), OR, ("emoji.unicode", "👍"), AND, ("user.name", "users/USER111")]

                    # We'll do a single pass to group by AND:
                    groups = []  # each group is a list of expressions that are OR'ed together
                    current_group = [expressions[0]]  # start
                    for idx, op in enumerate(operators):
                        expr = expressions[idx+1]
                        if op == "OR":
                            # add to current group
                            current_group.append(expr)
                        elif op == "AND":
                            # finish the current group, start a new group
                            groups.append(current_group)
                            current_group = [expr]
                        else:
                            # unknown => skip
                            return False
                    # add last group
                    groups.append(current_group)

                    # Now we have groups of OR expressions, we require each group to match (AND).
                    # e.g. group1 => [("emoji.unicode","🙂"),("emoji.unicode","👍")] => means rxn must have emoji.unicode that is either "🙂" or "👍"
                    # group2 => [("user.name","users/USER111")] => must match as well
                    for group in groups:
                        # They all share the same field or doc says "OR with same field"? We'll allow them to share the same field or be different, but doc focuses on same field for OR. We'll do an "OR" check among them.
                        matched_this_group = False
                        for (field, val) in group:
                            if _matches_expression(rxn, field, val):
                                matched_this_group = True
                                break
                        if not matched_this_group:
                            return False

                    return True


                def _matches_expression(rxn: dict, field: str, val: str) -> bool:
                    """
                    Check if a single reaction satisfies e.g. user.name = "users/USER111"
                    or emoji.unicode = "🙂", or emoji.custom_emoji.uid = "ABC".
                    """
                    if field == "user.name":
                        # check rxn["user"]["name"] == val
                        return rxn.get("user", {}).get("name") == val
                    elif field == "emoji.unicode":
                        return rxn.get("emoji", {}).get("unicode") == val
                    elif field == "emoji.custom_emoji.uid":
                        # rxn["emoji"]["custom_emoji"]["uid"] == val
                        return rxn.get("emoji", {}).get("custom_emoji", {}).get("uid") == val
                    else:
                        # unknown
                        return False

                if filter:
                    # We'll parse a few patterns for demonstration.
                    # Real logic would fully parse parentheses and multiple AND/OR expressions.
                    # e.g. "emoji.unicode = \"🙂\" AND user.name = \"users/USER111\""
                    # We'll handle basic ( X = "val" ) statements with AND or OR, ignoring parentheses.
                    tokens = filter.split()
                    # e.g. tokens => ["emoji.unicode", "=", "\"🙂\"", "AND", "user.name", "=", "\"users/USER111\""]
                    # We'll do a naive pass
                    filtered = []
                    for rxn in all_rxns:
                        if _reaction_matches_filter(rxn, tokens):
                            filtered.append(rxn)
                    all_rxns = filtered

                # 3) pagination
                total = len(all_rxns)
                end = offset + pageSize
                page_items = all_rxns[offset:end]
                next_token = None
                if end < total:
                    next_token = str(end)

                # Build result
                result = {"reactions": page_items}
                if next_token:
                    result["nextPageToken"] = next_token
                return result

            @staticmethod
            def delete(name: str) -> None:
                """
                Deletes a reaction by name: "spaces/AAA/messages/111/reactions/123"

                Returns empty dict to simulate an Empty response.
                """
                # Find and remove from DB
                for r in DB["Reaction"]:
                    if r.get("name") == name:
                        DB["Reaction"].remove(r)
                        print(f"Deleted reaction => {r}")
                        return {}
                print("Reaction not found => returning {}")
                return {}

    # ---------------------------------------------------------------------------------------
    # Resource: Spaces.Members
    # ---------------------------------------------------------------------------------------

    class Members:
        """Handles operations for space memberships under '/spaces/{space}/members'."""
        @staticmethod
        def list(parent: str,
                pageSize: int = None,
                pageToken: str = None,
                filter: str = None,
                showGroups: bool = None,
                showInvited: bool = None,
                useAdminAccess: bool = None) -> dict:
            """
            Lists memberships in a space.

            Parameters:
              - parent (str): Required. Resource name of the space, e.g. "spaces/AAA".
              - pageSize (int, optional): Maximum number of memberships to return.
                  If unspecified, at most 100 are returned; the maximum value is 1000.
              - pageToken (str, optional): A page token from a previous call (interpreted as an integer offset).
              - filter (str, optional): A query filter. You can filter memberships by role (e.g.
                  role = "ROLE_MEMBER" or role = "ROLE_MANAGER") and member type (e.g. member.type = "HUMAN"
                  or member.type != "BOT"). When using admin access, either member.type = "HUMAN" or
                  member.type != "BOT" is required.
              - showGroups (bool, optional): When true, also returns memberships associated with a Google Group.
              - showInvited (bool, optional): When true, also returns memberships in the INVITED state.
              - useAdminAccess (bool, optional): When true, the method runs with administrator privileges.

            Returns:
              dict: A ListMembershipsResponse containing:
                    {
                      "memberships": [ list of membership objects ],
                      "nextPageToken": "..."  // if more results are available
                    }
            """

            print(f"Members.list called with parent={parent}, pageSize={pageSize}, pageToken={pageToken}, filter={filter}, showGroups={showGroups}, showInvited={showInvited}, useAdminAccess={useAdminAccess}")

            # --- Helper functions defined inside the method ---
            def parse_page_token(token: str) -> int:
                try:
                    return max(int(token), 0)
                except (ValueError, TypeError):
                    return 0

            def default_page_size(ps: int) -> int:
                if ps is None:
                    return 100
                if ps < 0:
                    return 100
                return min(ps, 1000)

            def apply_filter(membership: dict, expressions: list) -> bool:
                """
                Given a membership and a list of expressions, returns True if the membership matches.
                Each expression is a tuple: (field, operator, value)
                Supported fields: "role" and "member.type".
                Supported operators: "=" and "!=".
                """
                for field, op, value in expressions:
                    # Normalize field names:
                    if field == "role":
                        field_val = membership.get("role", "")
                    elif field == "member.type":
                        field_val = membership.get("member", {}).get("type", "")
                    else:
                        continue

                    if op == "=":
                        if field_val != value:
                            return False
                    elif op == "!=":
                        if field_val == value:
                            return False
                return True

            def parse_filter(filter_str: str) -> list:
                """
                Very naive parser for filter.
                Splits on 'AND' and 'OR' is not supported across different fields.
                Returns a list of tuples (field, operator, value).
                For example:
                  'role = "ROLE_MANAGER" OR role = "ROLE_MEMBER"' -> we can split into multiple expressions
                  but for simplicity, we treat OR as multiple acceptable values for the same field,
                  and for filters with AND, all conditions must match.
                Here, we assume conditions are separated by 'AND' (case-insensitive).
                """
                expressions = []
                segments = [seg.strip() for seg in filter_str.split("AND")]
                for seg in segments:
                    # Look for "=" or "!=" in the segment.
                    if "!=" in seg:
                        parts = seg.split("!=")
                        operator = "!="
                    elif "=" in seg:
                        parts = seg.split("=")
                        operator = "="
                    else:
                        continue
                    if len(parts) < 2:
                        continue
                    field = parts[0].strip()
                    value = parts[1].strip().strip("\"")
                    expressions.append((field, operator, value))
                return expressions

            # --- End of helper functions ---

            # 1) Validate that parent is in the correct format: "spaces/{space}"
            if not parent.startswith("spaces/"):
                print("Invalid parent format. Expected 'spaces/{space}'.")
                return {}

            # 2) Start with memberships whose resource name begins with f"{parent}/members/"
            all_memberships = []
            for mem in DB["Membership"]:
                if mem.get("name", "").startswith(f"{parent}/members/"):
                    all_memberships.append(mem)

            # 3) If useAdminAccess is true, filter out app memberships.
            if useAdminAccess:
                all_memberships = [m for m in all_memberships if not m.get("name", "").endswith("/members/app")]
                # Also, per documentation, ensure that the filter includes a condition on member.type.
                # (We do not enforce it strictly here, but note that unsupported filters might be rejected.)

            # 4) Apply the query filter if provided.
            if filter:
                exprs = parse_filter(filter)
                # If useAdminAccess is true, ensure that at least one expression filters member.type to "HUMAN" or != "BOT"
                if useAdminAccess:
                    type_expr_ok = any((field == "member.type" and ((op == "=" and value.upper() == "HUMAN") or (op == "!=" and value.upper() == "BOT"))) for field, op, value in exprs)
                    if not type_expr_ok:
                        print("Error: When using admin access, filter must include member.type = \"HUMAN\" or member.type != \"BOT\".")
                        return {}
                all_memberships = [m for m in all_memberships if apply_filter(m, exprs)]

            # 5) Filter by showGroups and showInvited.
            if showGroups is not None and not showGroups:
                # Exclude memberships that are associated with a Google Group.
                # We'll assume a membership is for a Google Group if its member.name starts with "groups/".
                all_memberships = [m for m in all_memberships if not m.get("member", {}).get("name", "").startswith("groups/")]
            if showInvited is not None and not showInvited:
                # Exclude memberships in INVITED state.
                all_memberships = [m for m in all_memberships if m.get("state", "").upper() != "INVITED"]

            # 6) Set pageSize and pageToken.
            ps = default_page_size(pageSize)
            offset = parse_page_token(pageToken)

            # 7) Apply pagination.
            total = len(all_memberships)
            end = offset + ps
            page_items = all_memberships[offset:end]
            nextPageToken = str(end) if end < total else None

            response = {"memberships": page_items}
            if nextPageToken:
                response["nextPageToken"] = nextPageToken

            print(f"ListMembershipsResponse: {response}")
            return response

        @staticmethod
        def get(name: str, useAdminAccess: bool = None) -> dict:
            """
            Returns details about a membership.

            Args:
              name (str): Required. The membership resource name, e.g.
                          "spaces/{space}/members/{userID}" or "spaces/{space}/members/app".
              useAdminAccess (bool, optional): If True, method runs using the user's
                                              Google Workspace admin privileges.

            Behavior:
              1) Look up the membership in DB["Membership"].
              2) If found:
                - If it's "spaces/.../members/app" and useAdminAccess == True,
                  doc says it's not supported => return {}.
                - Otherwise, return the membership.
              3) If not found, return {}.
            """
            print(f"Members.get called with name={name}, useAdminAccess={useAdminAccess}")

            # 1) Locate the membership in DB
            found = None
            for mem in DB["Membership"]:
                if mem.get("name") == name:
                    found = mem
                    break

            # 2) If not found, return {}
            if not found:
                print("Membership not found => {}")
                return {}

            # Check if membership is "app" and useAdminAccess == True
            # The doc says: "Getting app memberships in a space isn't supported when using admin access."
            # So we skip returning details in that scenario
            if useAdminAccess:
                # If the membership name ends with "/members/app", it's the app membership
                if name.endswith("/members/app"):
                    print("Admin access used for app membership => not supported => {}")
                    return {}

            print(f"Found membership => {found}")
            return found
            print(f"Getting membership '{name}' with useAdminAccess={useAdminAccess}")

        @staticmethod
        def create(
            parent: str,
            membership: dict,
            useAdminAccess: bool = None
        ) -> None:
            """
            Creates a membership for a user or group in the specified 'parent' space.

            Args:
              parent (str): e.g. "spaces/AAA"
              membership (dict): The request body representing a 'Membership' resource.
                Example:
                  {
                    "member": {
                      "name": "users/USER999",  # MUST start with 'users/'
                      "type": "HUMAN",
                    },
                    "role": "ROLE_MEMBER",
                    "state": "INVITED"
                  }
              useAdminAccess (bool, optional): If True, method runs using admin privileges
                with certain constraints.
            """

            parts = parent.split("/")
            if len(parts) != 2 or parts[0] != "spaces":
                print("Invalid parent format. Expected 'spaces/{space}'. => returning {}.")
                return {}

            # 2) Validate membership["member"]["name"] => must match "users/{something}"
            if "member" not in membership or "name" not in membership["member"]:
                print("member not provided correctly")
                return {}

            mem_name = membership["member"]["name"]  # e.g. "users/USER999"
            if not mem_name.startswith("users/"):
                print("member name must start with 'users/'.")
                return {}

            membership_name = f"{parent}/members/{mem_name}"  # e.g. "spaces/AAA/members/users/USER999"
            membership["name"] = membership_name

            # We'll do a minimal check: if membership["member"]["type"] == "BOT", skip
            if useAdminAccess:
                if membership["member"].get("type") == "BOT":
                    print("Admin access => not supported to create membership for a Chat app => returning {}.")
                    return {}

            # 5) Check for existing membership
            for m in DB["Membership"]:
                if m.get("name") == membership_name:
                    print("Membership already exists => returning existing.")
                    return m

            membership.setdefault("role", "ROLE_MEMBER")
            membership.setdefault("state", "INVITED")
            membership.setdefault("createTime", datetime.now().isoformat() + "Z")

            DB["Membership"].append(membership)
            print(f"Membership created => {membership}")
            return membership

        @staticmethod
        def patch(
            name: str,
            updateMask: str,
            membership: dict,
            useAdminAccess: bool = None
        ) -> None:
            """
            Updates a membership.

            Args:
                name (str): Required. Resource name of the membership (e.g., 'spaces/AAA/members/BBB').
                updateMask (str): Required. Field paths to update (e.g., 'role').
                membership (dict): The updated Membership object.
                useAdminAccess (bool, optional): Use the caller's Google Workspace admin privileges.
            """
            print(f"Patching membership '{name}' with updateMask={updateMask}, membership={membership}, "
                  f"useAdminAccess={useAdminAccess}")

        @staticmethod
        def delete(name: str, useAdminAccess: bool = False) -> dict:
            """
            Deletes a membership given its resource name.

            Args:
              name (str): Required. Resource name of the membership to delete.
                          Must be in the format "spaces/{space}/members/{member}".
                          For example, "spaces/AAA/members/users/example@gmail.com" or "spaces/AAA/members/app".
              useAdminAccess (bool): Optional. If true, the method runs using admin privileges.
                                    Note: Deleting app memberships using admin access is not supported.

            Returns:
              dict: The deleted membership resource if deletion is successful, otherwise {}.

            Behavior:
              1) Look up the membership in DB["Membership"] by matching the name exactly.
              2) If not found, return {}.
              3) If useAdminAccess is true and the membership is for an app (i.e. its name ends with "/members/app"),
                deletion is not supported—return {}.
              4) Otherwise, delete the membership from DB and return it.
            """
            # 1) Find the membership in the database.
            target = None
            for m in DB["Membership"]:
                if m.get("name") == name:
                    target = m
                    break

            if not target:
                print("Membership not found.")
                return {}

            # 2) If useAdminAccess is true, then deleting an app membership is not supported.
            if useAdminAccess and name.endswith("/members/app"):
                print("Deleting app memberships using admin access is not supported.")
                return {}

            # 3) Remove the membership from DB
            DB["Membership"].remove(target)
            print(f"Deleted membership: {target}")
            return target


    # ---------------------------------------------------------------------------------------
    # Resource: Spaces.SpaceEvents
    # ---------------------------------------------------------------------------------------

    class SpaceEvents:
        """Handles space events operations."""

        @staticmethod
        def get(name: str) -> None:
            """
            Retrieves an event from a Google Chat space.

            Args:
                name (str): Resource name of the event. Format: 'spaces/{space}/spaceEvents/{spaceEvent}'.
            """
            print(f"Getting space event: {name}")

        @staticmethod
        def list(parent: str, pageSize: int = None, pageToken: str = None, filter: str = None) -> None:
            """
            Lists events from a Google Chat space.

            Args:
                parent (str): Resource name of the space. Format: 'spaces/{space}'.
                pageSize (int, optional): Max number of space events to return.
                pageToken (str, optional): Token from a previous list call for pagination.
                filter (str, required): Query filter that includes event types and optional time ranges.
            """
            print(f"Listing space events in {parent} with pageSize={pageSize}, pageToken={pageToken}, filter={filter}")



# ---------------------------------------------------------------------------------------
# Resource: users
# ---------------------------------------------------------------------------------------

class Users:
    """Top-level class for user-related operations."""
    @staticmethod
    def _create_user(display_name: str,type: str = None):
          """
          Creates a user.
          """
          print(f"create_user called with display_name={display_name}, type={type}")
          user = {
              "name": f"users/user{len(DB['User']) + 1}",
              "displayName": display_name,
              "type": type if type else "HUMAN",
              "createTime": datetime.utcnow().isoformat() + "Z"
          }
          DB["User"].append(user)
          return user

    def _change_user(user_id: str) -> None:
        """
        Changes the caller to the specified user.
        """
        global CURRENT_USER_ID
        CURRENT_USER_ID = user_id
        print(f"User changed to {CURRENT_USER_ID}")


    # ---------------------------------------------------------------------------------------
    # Resource: Users.Spaces
    # ---------------------------------------------------------------------------------------


    class Spaces:
        """Sub-resource under users: spaces read state and notifications."""

        @staticmethod
        def getSpaceReadState(name: str) -> dict:
            """
            Returns details about a user's read state within a space.
            Expected name format: users/{user}/spaces/{space}/spaceReadState
            """
            print(f"getSpaceReadState called with name={name}")
            for state in DB["SpaceReadState"]:
                if state.get("name") == name:
                    return state
            print("SpaceReadState not found.")
            return {}

        @staticmethod
        def updateSpaceReadState(name: str, updateMask: str, requestBody: dict) -> dict:
            """
            Updates a user's space read state.
            - name: users/{user}/spaces/{space}/spaceReadState
            - updateMask: a comma-separated list; currently supported: "last_read_time"
            - requestBody: a SpaceReadState resource containing the new "last_read_time" value.
            """
            print(f"updateSpaceReadState called with name={name}, updateMask={updateMask}, requestBody={requestBody}")
            # Find the state resource
            state_obj = None
            for state in DB["SpaceReadState"]:
                if state.get("name") == name:
                    state_obj = state
                    break
            if not state_obj:
                print("SpaceReadState not found.")
                return {}

            # Parse updateMask; only "last_read_time" is supported.
            masks = [m.strip() for m in updateMask.split(",")]
            if "last_read_time" in masks or "*" in masks:
                if "last_read_time" in requestBody:
                    # The new value is coerced to be later than the latest message's create time (not enforced here).
                    state_obj["last_read_time"] = requestBody["last_read_time"]
                else:
                    print("last_read_time not provided in requestBody.")
            else:
                print("No supported field in updateMask.")
            return state_obj

        # ---------------------------------------------------------------------------------------
        # Resource: Users.Spaces.Threads
        # ---------------------------------------------------------------------------------------

        class Threads:
            """Sub-resource for threads read state within a space."""
            @staticmethod
            def getThreadReadState(name: str) -> dict:
                """
                Returns details about a user's read state within a thread.
                Expected name format: users/{user}/spaces/{space}/threads/{thread}/threadReadState
                """
                print(f"getThreadReadState called with name={name}")
                for state in DB["ThreadReadState"]:
                    if state.get("name") == name:
                        return state
                print("ThreadReadState not found.")
                return {}

        # ---------------------------------------------------------------------------------------
        # Resource: Users.Spaces.SpaceNotificationSetting
        # ---------------------------------------------------------------------------------------

        class SpaceNotificationSetting:
            """Sub-resource for space notification settings."""

            @staticmethod
            def get(name: str) -> dict:
                """
                Gets the space notification setting.
                Expected name format: users/{user}/spaces/{space}/spaceNotificationSetting
                """
                print(f"SpaceNotificationSetting.get called with name={name}")
                for setting in DB["SpaceNotificationSetting"]:
                    if setting.get("name") == name:
                        return setting
                print("SpaceNotificationSetting not found.")
                return {}

            @staticmethod
            def patch(name: str, updateMask: str, requestBody: dict) -> dict:
                """
                Updates the space notification setting.
                - name: users/{user}/spaces/{space}/spaceNotificationSetting
                - updateMask: comma-separated list; supported: "notification_setting", "mute_setting"
                - requestBody: a SpaceNotificationSetting resource with new values.
                """
                print(f"SpaceNotificationSetting.patch called with name={name}, updateMask={updateMask}, requestBody={requestBody}")
                target = None
                for setting in DB["SpaceNotificationSetting"]:
                    if setting.get("name") == name:
                        target = setting
                        break
                if not target:
                    print("SpaceNotificationSetting not found.")
                    return {}

                masks = [m.strip() for m in updateMask.split(",")]
                if "notification_setting" in masks or "*" in masks:
                    if "notification_setting" in requestBody:
                        target["notification_setting"] = requestBody["notification_setting"]
                if "mute_setting" in masks or "*" in masks:
                    if "mute_setting" in requestBody:
                        target["mute_setting"] = requestBody["mute_setting"]

                return target

# -------------------------------
# Global in-memory "database" setup
# -------------------------------
def reset_db():
    global DB, REQUEST_ID_MAP
    DB = {
        "User":[],
        "Space": [],
        "Membership": [],
        "Message": [],
        "Reaction": [],
        "SpaceReadState": [],
        "ThreadReadState": [],
        "SpaceNotificationSetting": []
    }
    REQUEST_ID_MAP = {}

# Global caller identifiers
CURRENT_USER = "users/USER123"
CURRENT_USER_ID = CURRENT_USER  # for compatibility with code using CURRENT_USER_ID

# -------------------------------
# (Assume final code from above is defined here.)
# For brevity, only the test cases are shown.
# -------------------------------

# --- Test cases for Media ---
def test_media():
    print("\n--- test_media ---")
    media = Media()
    media.download("media/sample_image.png")
    attachment_request = {
        "contentName": "sample_file.pdf",
        "contentType": "application/pdf"
    }
    result = media.upload("spaces/AAA", attachment_request)
    print("Uploaded Attachment:", result)

# --- Test cases for Spaces.create ---
def test_spaces_create():
    print("\n--- test_spaces_create ---")
    reset_db()
    space_request = {
        "displayName": "Test Space",
        "spaceType": "SPACE",
        "importMode": False,
    }
    created = Spaces.create(space=space_request)
    assert created.get("name", "").startswith("spaces/"), "Space name not generated correctly."
    # Check that the calling user was added as a membership.
    expected_membership = f"{created['name']}/members/{CURRENT_USER_ID}"
    memberships = [m for m in DB["Membership"] if m.get("name") == expected_membership]
    assert memberships, "Calling user membership not created."
    print("Spaces.create test passed.")

# --- Test cases for Spaces.setup ---
def test_spaces_setup():
    print("\n--- test_spaces_setup ---")
    reset_db()
    setup_request = {
        "space": {
            "displayName": "Setup Space",
            "spaceType": "SPACE",
            "importMode": False,
            "customer": "customers/my_customer"
        },
        "memberships": [
            {
                "member": {
                    "name": "users/otheruser@example.com",
                    "type": "HUMAN",
                    "displayName": "Other User"
                },
                "role": "ROLE_MEMBER"
            },
            {
                "member": {
                    "name": "users/USER123",  # Should be skipped (calling user)
                    "type": "HUMAN",
                    "displayName": "User One Twenty-Three"
                },
                "role": "ROLE_MEMBER"
            }
        ]
    }
    created_space = Spaces.setup(setup_request)
    # Expect caller membership exists and one extra membership from request.
    caller_mem = f"{created_space['name']}/members/{CURRENT_USER_ID}"
    other_mem = f"{created_space['name']}/members/users/otheruser@example.com"
    mem_names = [m["name"] for m in DB["Membership"]]
    assert caller_mem in mem_names, "Caller membership missing in setup."
    assert other_mem in mem_names, "Other membership missing in setup."
    print("Spaces.setup test passed.")

# --- Test cases for Spaces.patch ---
def test_spaces_patch():
    print("\n--- test_spaces_patch ---")
    reset_db()
    # First, create a space.
    space_request = {
        "displayName": "Patch Space",
        "spaceType": "SPACE",
        "importMode": False,
        "customer": "customers/my_customer",
        "spaceDetails": {"description": "Old description"}
    }
    space_obj = Spaces.create(requestId="req-101", space=space_request)
    # Now, patch the space.
    patch_updates = {
        "spaceDetails": {"description": "New description updated via patch"},
        "displayName": "Patch Space Updated",
        "spaceHistoryState": "HISTORY_ON",
        "accessSettings": {"audience": "SPECIFIC_USERS"},
        "permissionSettings": {"manageMembersAndGroups": True}
    }
    updated = Spaces.patch(
        name=space_obj["name"],
        updateMask="space_details,display_name,space_history_state,access_settings.audience,permission_settings",
        space_updates=patch_updates,
        useAdminAccess=False
    )
    assert updated.get("displayName") == "Patch Space Updated", "displayName not updated correctly."
    assert updated.get("spaceHistoryState") == "HISTORY_ON", "spaceHistoryState not updated."
    new_desc = updated.get("spaceDetails", {}).get("description", "")
    assert new_desc.startswith("New description"), "spaceDetails.description not updated."
    print("Spaces.patch test passed.")

# --- Test cases for Spaces.search ---
def test_spaces_search():
    print("\n--- test_spaces_search ---")
    reset_db()
    # Prepopulate DB["Space"]
    DB["Space"].extend([
        {
            "name": "spaces/AAA",
            "displayName": "Team Chat Room",
            "spaceType": "SPACE",
            "customer": "customers/my_customer",
            "externalUserAllowed": True,
            "spaceHistoryState": "HISTORY_ON",
            "membershipCount": {"joined_direct_human_user_count": 10},
            "createTime": "2022-05-01T10:00:00Z",
            "lastActiveTime": "2023-05-01T12:00:00Z",
            "accessSettings": {"audience": "OPEN"},
            "permissionSettings": {}
        },
        {
            "name": "spaces/BBB",
            "displayName": "Fun Event",
            "spaceType": "SPACE",
            "customer": "customers/my_customer",
            "externalUserAllowed": False,
            "spaceHistoryState": "HISTORY_OFF",
            "membershipCount": {"joined_direct_human_user_count": 25},
            "createTime": "2021-12-15T09:30:00Z",
            "lastActiveTime": "2023-04-20T16:00:00Z",
            "accessSettings": {"audience": "RESTRICTED"},
            "permissionSettings": {}
        },
        {
            "name": "spaces/CCC",
            "displayName": "DM Room",
            "spaceType": "DIRECT_MESSAGE",
            "customer": "customers/my_customer",
            "externalUserAllowed": True,
            "spaceHistoryState": "HISTORY_ON",
            "membershipCount": {"joined_direct_human_user_count": 2},
            "createTime": "2023-01-10T08:00:00Z",
            "lastActiveTime": "2023-03-01T14:00:00Z",
            "accessSettings": {},
            "permissionSettings": {}
        }
    ])
    # Sample query: must include required parts
    sample_query = ('customer = "customers/my_customer" AND space_type = "SPACE" '
                    'AND display_name:"Team" AND last_active_time > "2022-01-01T00:00:00Z"')
    result = Spaces.search(
        useAdminAccess=True,
        pageSize=2,
        pageToken="0",
        query=sample_query,
        orderBy="create_time ASC"
    )
    assert "spaces" in result, "No spaces key in search result."
    print("Spaces.search test passed.")

# --- Test cases for Spaces.get ---
def test_spaces_get():
    print("\n--- test_spaces.get ---")
    reset_db()
    # Create a space and a membership for CURRENT_USER
    space_request = {
        "displayName": "Get Space Test",
        "spaceType": "SPACE",
        "importMode": False,
        "customer": "customers/my_customer"
    }
    created = Spaces.create(requestId="req-201", space=space_request)
    # Test get with admin access (should return space regardless)
    got_space = Spaces.get(name=created["name"], useAdminAccess=True)
    assert got_space, "Space not returned with admin access."
    # Test get with user auth: CURRENT_USER is a member so it should return the space.
    got_space2 = Spaces.get(name=created["name"], useAdminAccess=False)
    print(got_space2)
    assert got_space2, "Space not returned for member."
    # Test get for a non-member (simulate by using a wrong CURRENT_USER_ID)
    global CURRENT_USER_ID
    CURRENT_USER_ID = "users/OTHER"
    got_space3 = Spaces.get(name=created["name"], useAdminAccess=False)
    assert got_space3 == {}, "Non-member should not retrieve space."
    # Reset CURRENT_USER_ID
    CURRENT_USER_ID = CURRENT_USER
    print("Spaces.get test passed.")

# --- Test cases for Spaces.delete ---
def test_spaces_delete():
    print("\n--- test_spaces.delete ---")
    reset_db()
    # Create a space to delete.
    space_request = {
        "displayName": "Delete Space Test",
        "spaceType": "SPACE",
        "importMode": False,
        "customer": "customers/my_customer"
    }
    created = Spaces.create(requestId="req-301", space=space_request)
    # Add an extra membership and message
    membership = {
        "name": f"{created['name']}/members/users/extra@example.com",
        "state": "JOINED",
        "role": "ROLE_MEMBER",
        "member": {
            "name": "users/extra@example.com",
            "displayName": "Extra User",
            "domainId": "example.com",
            "type": "HUMAN",
            "isAnonymous": False
        },
        "groupMember": {},
        "createTime": datetime.utcnow().isoformat() + "Z",
        "deleteTime": ""
    }
    DB["Membership"].append(membership)
    message = {
        "name": f"{created['name']}/messages/1",
        "text": "Message to delete",
        "createTime": datetime.utcnow().isoformat() + "Z",
        "thread": {},
        "sender": {"name": CURRENT_USER, "type": "HUMAN"}
    }
    DB["Message"].append(message)
    # Delete the space using non-admin access (user must be a member)
    deleted = Spaces.delete(name=created["name"], useAdminAccess=False)
    assert deleted == {}, "delete should return an empty dict on success."
    # Ensure space is removed
    remaining_spaces = [sp for sp in DB["Space"] if sp.get("name") == created["name"]]
    assert not remaining_spaces, "Space was not removed from DB."
    # Ensure related memberships and messages are removed.
    remaining_memberships = [m for m in DB["Membership"] if m.get("name", "").startswith(created["name"])]
    remaining_messages = [m for m in DB["Message"] if m.get("name", "").startswith(created["name"])]
    assert not remaining_memberships, "Child memberships not removed."
    assert not remaining_messages, "Child messages not removed."
    print("Spaces.delete test passed.")

# --- Test cases for Spaces.Messages.create, list, get, update, delete ---
def test_messages():
    print("\n--- test_spaces.messages tests ---")
    reset_db()
    # First, add a membership for CURRENT_USER in space "spaces/AAA"
    space_obj = {
        "name": "spaces/AAA",
        "displayName": "Messages Test Space",
        "spaceType": "SPACE",
        "customer": "customers/my_customer",
        "importMode": False
    }
    DB["Space"].append(space_obj)
    caller_membership = {
        "name": f"{space_obj['name']}/members/{CURRENT_USER_ID}",
        "state": "JOINED",
        "role": "ROLE_MEMBER",
        "member": {"name": CURRENT_USER_ID, "type": "HUMAN"},
        "groupMember": {},
        "createTime": datetime.utcnow().isoformat() + "Z",
        "deleteTime": ""
    }
    DB["Membership"].append(caller_membership)
    # Test creating a message.
    msg_body = {"text": "Hello, world!"}
    created_msg = Spaces.Messages.create(parent="spaces/AAA", requestId="msg-req-001",
                                           messageReplyOption="REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD",
                                           messageId="client-001", message_body=msg_body)
    print(created_msg)
    assert created_msg.get("name", "").endswith("client-001"), "Message name not set correctly."
    # Test listing messages.
    list_result = Spaces.Messages.list(parent="spaces/AAA", pageSize=10, pageToken="0", filter=None, orderBy="ASC", showDeleted=False)
    assert "messages" in list_result, "List response missing messages key."
    # Test getting the message.
    got_msg = Spaces.Messages.get(name=created_msg["name"])
    assert got_msg.get("text") == "Hello, world!", "Message text mismatch."
    # Test updating the message (PUT).
    update_body = {"text": "Hello, updated world!", "attachment": []}
    updated_msg = Spaces.Messages.update(name=created_msg["name"], updateMask="text", allowMissing=False, body=update_body)
    assert updated_msg.get("text") == "Hello, updated world!", "Message update failed."
    # Test deleting the message.
    delete_result = Spaces.Messages.delete(name=created_msg["name"], force=False)
    # After deletion, message should no longer exist.
    got_after_delete = Spaces.Messages.get(name=created_msg["name"])
    assert got_after_delete == {}, "Message was not deleted."
    print("Spaces.Messages tests passed.")

# --- Test cases for Spaces.Messages.Attachments.get ---
def test_attachments():
    print("\n--- test_spaces.messages.attachments tests ---")
    reset_db()
    # Prepopulate a message with attachments.
    space_obj = {"name": "spaces/AAA", "displayName": "Attachment Test Space", "spaceType": "SPACE", "customer": "customers/my_customer"}
    DB["Space"].append(space_obj)
    message_obj = {
        "name": "spaces/AAA/messages/1",
        "text": "Message with attachment",
        "thread": {},
        "createTime": datetime.utcnow().isoformat() + "Z"
    }
    # Add an attachment to the message.
    attachment = {
        "name": "spaces/AAA/messages/1/attachments/ATT1",
        "contentName": "file.png",
        "contentType": "image/png"
    }
    message_obj["attachment"] = [attachment]
    DB["Message"].append(message_obj)
    # Test attachment get.
    att = Spaces.Messages.Attachments.get("spaces/AAA/messages/1/attachments/ATT1")
    assert att.get("contentName") == "file.png", "Attachment retrieval failed."
    print("Attachments.get test passed.")

# --- Test cases for Spaces.Messages.Reactions ---
def test_reactions():
    print("\n--- test_spaces.messages.reactions tests ---")
    reset_db()
    # Prepopulate a message.
    space_obj = {"name": "spaces/AAA", "displayName": "Reaction Test Space", "spaceType": "SPACE", "customer": "customers/my_customer"}
    DB["Space"].append(space_obj)
    message_obj = {
        "name": "spaces/AAA/messages/1",
        "text": "Message for reactions",
        "thread": {},
        "createTime": datetime.utcnow().isoformat() + "Z"
    }
    DB["Message"].append(message_obj)
    # Test creating a reaction.
    reaction_body = {
        "emoji": {"unicode": "🙂"},
        "user": {"name": "users/USER123"}
    }
    created_rxn = Spaces.Messages.Reactions.create(parent="spaces/AAA/messages/1", reaction=reaction_body)
    assert created_rxn.get("emoji", {}).get("unicode") == "🙂", "Reaction creation failed."
    # Test listing reactions.
    rxn_list = Spaces.Messages.Reactions.list(parent="spaces/AAA/messages/1", pageSize=10, pageToken="0", filter='emoji.unicode = "🙂"')
    assert "reactions" in rxn_list and len(rxn_list["reactions"]) >= 1, "Reaction listing failed."
    # Test deleting a reaction.
    del_result = Spaces.Messages.Reactions.delete(created_rxn.get("name"))
    # After deletion, listing should return zero reactions.
    rxn_list_after = Spaces.Messages.Reactions.list(parent="spaces/AAA/messages/1", pageSize=10, pageToken="0", filter=None)
    assert len(rxn_list_after.get("reactions", [])) == 0, "Reaction deletion failed."
    print("Reactions tests passed.")

# --- Test cases for Users.Spaces (read state and notification settings) ---
def test_user_space_resources():
    print("\n--- test_users.spaces tests ---")
    reset_db()
    # Prepopulate SpaceReadState
    DB["SpaceReadState"].append({
        "name": "users/me/spaces/AAA/spaceReadState",
        "last_read_time": "2023-05-01T12:00:00Z"
    })
    # Test getSpaceReadState
    state = Users.Spaces.getSpaceReadState("users/me/spaces/AAA/spaceReadState")
    assert state.get("last_read_time") == "2023-05-01T12:00:00Z", "getSpaceReadState failed."
    # Test updateSpaceReadState
    updated_state = Users.Spaces.updateSpaceReadState("users/me/spaces/AAA/spaceReadState", updateMask="last_read_time", requestBody={"last_read_time": "2023-06-01T15:00:00Z"})
    assert updated_state.get("last_read_time") == "2023-06-01T15:00:00Z", "updateSpaceReadState failed."

    # Prepopulate ThreadReadState
    DB["ThreadReadState"].append({
        "name": "users/me/spaces/AAA/threads/THREAD1/threadReadState",
        "last_read_time": "2023-05-01T12:00:00Z"
    })
    thread_state = Users.Spaces.Threads.getThreadReadState("users/me/spaces/AAA/threads/THREAD1/threadReadState")
    assert thread_state.get("last_read_time") == "2023-05-01T12:00:00Z", "getThreadReadState failed."

    # Prepopulate SpaceNotificationSetting
    DB["SpaceNotificationSetting"].append({
        "name": "users/me/spaces/AAA/spaceNotificationSetting",
        "notification_setting": "ALL_MESSAGES",
        "mute_setting": "NOT_MUTED"
    })
    notif = Users.Spaces.SpaceNotificationSetting.get("users/me/spaces/AAA/spaceNotificationSetting")
    assert notif.get("notification_setting") == "ALL_MESSAGES", "SpaceNotificationSetting.get failed."
    patched_notif = Users.Spaces.SpaceNotificationSetting.patch("users/me/spaces/AAA/spaceNotificationSetting", updateMask="notification_setting, mute_setting", requestBody={"notification_setting": "MUTED", "mute_setting": "ALL"})
    assert patched_notif.get("notification_setting") == "MUTED", "SpaceNotificationSetting.patch failed."
    print("Users.Spaces tests passed.")


# -------------------------------
# Run all tests
# -------------------------------
def run_tests():
    test_media()
    test_spaces_create()
    test_spaces_setup()
    test_spaces_patch()
    test_spaces_search()
    test_spaces_get()
    test_spaces_delete()
    test_messages()
    test_attachments()
    test_reactions()
    test_user_space_resources()
    print("\nAll tests passed successfully.")


if __name__ == "__main__":
    run_tests()


setup_request = {
        "space": {
            "displayName": "Setup Space",
            "spaceType": "SPACE",
            "importMode": False,
        },
        "memberships": [
            {
                "member": {
                    "name": "users/otheruser@example.com",
                    "type": "HUMAN",
                    "displayName": "Other User"
                },
                "role": "ROLE_MEMBER"
            }
        ]
    }
created_space = Spaces.setup(setup_request)
# Expect caller membership exists and one extra membership from request.
caller_mem = f"{created_space['name']}/members/{CURRENT_USER_ID}"
other_mem = f"{created_space['name']}/members/users/otheruser@example.com"
mem_names = [m["name"] for m in DB["Membership"]]

Spaces.Messages.create(parent = created_space.get('name'), message_body={'text' : 'hi'})

Spaces.Messages.list(parent = created_space.get('name'))
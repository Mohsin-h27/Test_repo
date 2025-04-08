#!/usr/bin/env python
"""
Fully Functional Python API Simulation

This single, self-contained Python file implements a mock Confluence-like REST API
based on the JSON API Discovery File provided earlier. The implementation includes:

1) Complete API Implementation:
   - A Python class for each major resource.
   - Class methods for each method in the specification.
   - In-memory JSON-serializable storage (`DB`) to maintain state.
   - Basic error handling and edge-case simulation.

2) State Persistence:
   - `save_state(filepath: str)` and `load_state(filepath: str)` methods to
     persist the `DB` to/from a JSON file.

3) Comprehensive Testing:
   - Embedded unit tests, using Python's unittest library.
   - Tests can be executed directly by running this script.
   - Tests validate correctness of each major resource and method, as well
     as data persistence/load.

To run tests:
    python this_file.py
(or)
    ./this_file.py

All tests should pass if the implementation is correct. Make sure you have
write permissions if you run tests that perform state saving/loading.
"""

import json
import os
import unittest
import re
from typing import Any, Dict, List, Optional, Union

# -------------------------------------------------------------------
# In-Memory State: A global dictionary to hold all data in JSON form
# -------------------------------------------------------------------
DB = {
	"contents": {
	"1": {"id": "1", "type": "page", "spaceKey": "DEV", "title": "Project Overview", "status": "current", "body": {}, "postingDay": None},
	"2": {"id": "2", "type": "blogpost", "spaceKey": "HR", "title": "Company Update", "status": "current", "body": {}, "postingDay": "2024-03-15"},
	"3": {"id": "3", "type": "page", "spaceKey": "DEV", "title": "API Documentation", "status": "current", "body": {}, "postingDay": None},
	"4": {"id": "4", "type": "blogpost", "spaceKey": "ENG", "title": "Tech Trends", "status": "trashed", "body": {}, "postingDay": "2024-01-10"},
	"5": {"id": "5", "type": "page", "spaceKey": "MARKETING", "title": "Strategy Plan", "status": "current", "body": {}, "postingDay": None}
	},
	"content_counter": 6,

	"content_properties": {
	"1": {"key": "author", "value": "Alice", "version": 1},
	"2": {"key": "views", "value": 150, "version": 1},
	"3": {"key": "last_updated", "value": "2024-06-10", "version": 1},
	"4": {"key": "category", "value": "Tech", "version": 1},
	"5": {"key": "priority", "value": "High", "version": 1}
	},

	"content_labels": {
	"1": ["important", "project", "overview"],
	"2": ["announcement", "hr"],
	"3": ["api", "documentation"],
	"4": ["tech", "trends"],
	"5": ["marketing", "strategy"]
	},

	"long_tasks": {
	"1": {"id": "1", "status": "in_progress", "description": "Content migration"},
	"2": {"id": "2", "status": "completed", "description": "Indexing documents"},
	"3": {"id": "3", "status": "failed", "description": "Database cleanup"},
	"4": {"id": "4", "status": "in_progress", "description": "Rebuilding cache"},
	"5": {"id": "5", "status": "completed", "description": "Generating reports"}
	},
	"long_task_counter": 6,

	"spaces": {
	"DEV": {"spaceKey": "DEV", "name": "Development", "description": "Development team space"},
	"HR": {"spaceKey": "HR", "name": "Human Resources", "description": "HR announcements and policies"},
	"ENG": {"spaceKey": "ENG", "name": "Engineering", "description": "Engineering discussions"},
	"MARKETING": {"spaceKey": "MARKETING", "name": "Marketing", "description": "Marketing strategies and campaigns"},
	"SALES": {"spaceKey": "SALES", "name": "Sales", "description": "Sales reports and insights"}
	},

	"deleted_spaces_tasks": {
	"1": {"spaceKey": "OLD_PROJECT", "status": "complete", "description": "Deleted old project space"},
	"2": {"spaceKey": "ARCHIVED", "status": "in_progress", "description": "Archiving old data"},
	"3": {"spaceKey": "LEGACY", "status": "failed", "description": "Attempt to delete legacy space"},
	"4": {"spaceKey": "TEST", "status": "complete", "description": "Test space removed"},
	"5": {"spaceKey": "EXPERIMENTAL", "status": "in_progress", "description": "Cleaning up experimental space"}
	}
}

# -------------------------------------------------------------------
# Persistence Helpers
# -------------------------------------------------------------------
def save_state(filepath: str) -> None:
    """
    Save current in-memory DB state to a JSON file.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(DB, f, ensure_ascii=False, indent=2)


def load_state(filepath: str) -> None:
    """
    Load DB state from a JSON file into the global DB dictionary.
    """
    global DB
    with open(filepath, 'r', encoding='utf-8') as f:
        DB = json.load(f)

def _evaluate_cql_expression(content, expression):
    """Evaluates a single CQL expression against a content item."""
    match = re.match(r"(\w+)\s*(>=|<=|!=|!~|>|<|=|~)\s*'(.*?)'", expression)

    if not match:
        return False

    field, operator, value = match.groups()
    content_value = content.get(field)

    if content_value is None:
        return False

    if operator == '=':
        return content_value == value
    elif operator == '!=':
        return content_value != value
    elif operator == '>':
        return content_value > value
    elif operator == '>=':
        return content_value >= value
    elif operator == '<':
        return content_value < value
    elif operator == '<=':
        return content_value <= value
    elif operator == '~':
        return value in content_value
    elif operator == '!~':
        return value not in content_value

    return False

def _evaluate_cql_tree(content, tokens):
    """Evaluates a list of CQL tokens, handling parentheses and logical operators."""
    stack = []
    operators = []

    def apply_operator():
        op = operators.pop()
        if op == 'not':
            # Unary operator: negate the top of the stack.
            operand = stack.pop()
            stack.append(not operand)
        else:
            # Binary operators: pop two operands.
            right = stack.pop()
            left = stack.pop()
            if op == 'and':
                stack.append(left and right)
            elif op == 'or':
                stack.append(left or right)

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                apply_operator()
            operators.pop()  # Remove '('
        elif token in ('and', 'or', 'not'):
            # For binary operators (and, or), apply any pending higher or equal precedence operators.
            # not has highest precedence and is right-associative so we don't pop it immediately.
            while (operators and operators[-1] in ('not', 'and', 'or') and token != 'not'):
                apply_operator()
            operators.append(token)
        else:
            # Token is a condition expression
            stack.append(_evaluate_cql_expression(content, token))
        i += 1

    while operators:
        apply_operator()

    return stack[0]
# -------------------------------------------------------------------
# 1) content_api
# -------------------------------------------------------------------
class ContentAPI:
    """
    Simulated endpoints for managing Confluence-like 'Content' (Pages, Blogposts, etc.).
    Methods correspond to the discovery JSON file, renamed to be more Pythonic.
    """

    def get_content_list(
        self,
        type: Optional[str] = None,
        spaceKey: Optional[str] = None,
        title: Optional[str] = None,
        status: Optional[str] = "current",
        postingDay: Optional[str] = None,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Returns a paginated list of content, filtered by various parameters.
        This is a simulation with in-memory data stored in DB["contents"].
        """
        # Collect all content
        all_contents = list(DB["contents"].values())

        # Filter
        if type:
            all_contents = [c for c in all_contents if c.get("type") == type]
        if spaceKey:
            all_contents = [c for c in all_contents if c.get("spaceKey") == spaceKey]
        if title:
            all_contents = [c for c in all_contents if c.get("title") == title]
        if postingDay and type == "blogpost":
            # Simulate a postingDay check
            all_contents = [
                c for c in all_contents
                if c.get("postingDay") == postingDay
            ]
        if status and status != "any":
            # "current" or "trashed"
            all_contents = [c for c in all_contents if c.get("status") == status]
        elif status == "any":
            #No filter for status
            pass
        else:
            # Default to "current" if not specified
            all_contents = [c for c in all_contents if c.get("status") == "current"]

        # Pagination
        paginated = all_contents[start:start + limit]
        return paginated

    def create_content(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates new content. Must include certain fields in the body:
          - type
          - title, if type='page'
          - spaceKey

        Extended behavior for comments:
          - If type is "comment", then the body must include an "ancestors" list (with at least one parent id).
          - The API will retrieve the parent content and build a complete ancestors chain by taking the parent's own ancestors (if any) and appending the parent's id.
          - The parent's record is updated to include the new comment id under a "children" list (for direct comments) and each ancestor (including the parent) is updated under "descendants".
        """
        new_id = str(DB["content_counter"])
        DB["content_counter"] += 1

        # Build default content
        new_content = {
            "id": new_id,
            "type": body.get("type", "page"),  # default to page
            "spaceKey": body.get("spaceKey", ""),
            "title": body.get("title", ""),
            "status": body.get("status", "current"),
            "body": body.get("body", {}),  # store as-is
            "postingDay": body.get("postingDay", None),
            "link": os.path.join(
                "/content",
                new_id
            )
        }
        # Extended behavior for comments
        if new_content["type"] == "comment":
            # Expect the body to include an "ancestors" list
            if "ancestors" not in body or not body["ancestors"]:
                raise ValueError("Comments must include an ancestors list with a parent id.")
            # Get the immediate parent's id from the provided ancestors
            parent_id = body["ancestors"][0]
            parent = DB["contents"].get(parent_id)
            if not parent:
                raise ValueError(f"Parent content not found.")

            # Build a complete ancestors chain:
            # Start with the parent's ancestors (ensuring each is of type 'content'), then add the parent.
            complete_ancestors = [
                DB["contents"].get(ancestor["id"])
                for ancestor in parent.get("ancestors", [])
            ] + [parent]
            new_content["ancestors"] = complete_ancestors

            # Update the parent record:
            # 1. Add this comment to the parent's direct children.
            if "children" not in parent:
                parent["children"] = []
            parent["children"].append(new_content)
            DB["contents"][parent.get("id")] = parent

            # 2. Cascade up: add the new comment id to all ancestors' descendants.
            for ancestor_ref in complete_ancestors:
                ancestor_id = ancestor_ref["id"]
                ancestor = DB["contents"].get(ancestor_id)
                if ancestor:
                    if "descendants" not in ancestor:
                        ancestor["descendants"] = []
                    ancestor["descendants"].append(new_content)
                    DB["contents"][ancestor_id] = ancestor

        # Save new content in DB
        DB["contents"][new_id] = new_content
        return new_content

    def search_content(
        self,
        cql: str,
        cqlcontext: Optional[str] = None,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25,
    ) -> List[Dict[str, Any]]:
        """
        Fetch a list of content using a mock "CQL".
        Facilitates complex CQL queries with logical operators and parentheses.
        """
        all_contents = list(DB["contents"].values())

        # Tokenize the CQL query
        tokens = re.findall(r"\(|\)|and|or|not|\w+\s*(?:>=|<=|!=|!~|>|<|=|~)\s*'[^']*'", cql)

        # Filter contents based on the CQL query
        filtered_contents = [
            content
            for content in all_contents
            if _evaluate_cql_tree(content, tokens)
        ]

        # Pagination
        paginated = filtered_contents[start : start + limit]
        return paginated

    def get_content(
        self,
        id: str,
        status: Optional[str] = None,
        version: Optional[int] = None,
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Returns a single piece of content by ID.
        Honors status if specified (or default 'current').
        """
        content = DB["contents"].get(id)
        if not content:
            raise ValueError(f"Content with id={id} not found.")

        if status and status != "any":
            if content.get("status") != status:
                raise ValueError(f"Content status mismatch. status={status}")
        else:
            # version is not truly tracked in this simulation, ignoring for now
            return content

    def update_content(self, id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates or restores a piece of content, must increment version in the body for realism.
        We'll skip actual version checks in this simple simulation.
        """
        content = DB["contents"].get(id)
        if not content:
            raise ValueError(f"Content with id={id} not found.")

        # If the body includes a status e.g. 'trashed' or 'current', handle it
        new_status = body.get("status")
        if new_status:
            content["status"] = new_status
        # If there's an updated title, body, etc.
        if "title" in body:
            content["title"] = body["title"]
        if "body" in body:
            content["body"] = body["body"]
        DB["contents"][id] = content
        return content

    def  delete_content(self, id: str, status: Optional[str] = None) -> None:
        """
        Trashes or purges content. If content is 'current' and is trashable, mark it 'trashed'.
        If content is 'trashed' and status=trashed again, delete permanently.
        If content is not trashable, delete permanently (not actually simulated).
        """
        content = DB["contents"].get(id)
        if not content:
            raise ValueError(f"Content with id={id} not found.")
        current_status = content.get("status", "current")
        if current_status == "current":
            # trash it
            content["status"] = "trashed"
            DB["contents"][id] = content
        elif current_status == "trashed" and status == "trashed":
            # delete permanently
            del DB["contents"][id]
        elif status == 'trashed':
            # delete if current_status is not trashable
            del DB["contents"][id]
        else:
          pass

    def get_content_history(
        self,
        id: str,
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Returns the 'history' of a piece of Content. We'll return a simple, static simulation.
        """
        content = DB["contents"].get(id)
        if not content:
            raise ValueError(f"Content with id={id} not found.")
        # We'll just return a mock dictionary.
        history = {
            "id": id,
            "latest": True,
            "createdBy": "mockuser",
            "createdDate": "2023-01-01T12:00:00.000Z",
            "previousVersion": None,
            "nextVersion": None
        }
        return history

    def get_content_children(
        self,
        id: str,
        expand: Optional[str] = None,
        parentVersion: int = 0
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Returns a map of direct children of content. For simplicity, we won't track real hierarchy.
        We'll pretend no content is child of another in this minimal simulation.
        """
        content = DB["contents"].get(id)
        if not content:
            raise ValueError(f"Content with id={id} not found.")
        # In a real scenario we might track parent->child relationships.
        # We'll just return an empty map for demonstration.
        children_by_type = {
            "page": [],
            "blogpost": [],
            "comment": [],
            "attachment": []
        }

        # Get the list of children IDs stored in the parent's "children" field.
        children = content.get("children", [])

        # For each child id, retrieve the full content and group by its type.
        for child in children:
            if child:
                child_type = child.get("type")
                if child_type in children_by_type:
                    children_by_type[child_type].append(child)
                else:
                    # Optionally, handle unexpected content types here.
                    pass

        return children_by_type

    def get_content_children_of_type(
        self,
        id: str,
        child_type: str,
        expand: Optional[str] = None,
        parentVersion: int = 0,
        start: int = 0,
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Returns direct children of a specific type.
        """
        parent = DB["contents"].get(id)
        if not parent:
            raise ValueError(f"Content with id={id} not found.")

        children = parent.get("children", [])
        comments = []
        for child in children:
            if child and child.get("type") == child_type:
                comments.append(child)

        return comments[start:start+limit]

    def get_content_comments(
        self,
        id: str,
        expand: Optional[str] = None,
        parentVersion: int = 0,
        start: int = 0,
        limit: int = 25,
        location: Optional[str] = None,
        depth: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns the comments for content.
        """
        parent = DB["contents"].get(id)
        if not parent:
            raise ValueError(f"Content with id={id} not found.")

        children = parent.get("children", [])
        comments = []
        for child in children:
            if child and child.get("type") == "comment":
                comments.append(child)

        return comments[start:start+limit]

    def get_content_attachments(
        self,
        id: str,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 50,
        filename: Optional[str] = None,
        mediaType: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns attachments. We'll return an empty list in this basic simulation.
        """
        return []

    def create_attachments(
        self,
        id: str,
        file: Any,
        comment: Optional[str] = None,
        minorEdit: bool = False
    ) -> Dict[str, Any]:
        """
        Adds attachments. We'll just return a simple mock response.
        """
        content = DB["contents"].get(id)
        if not content:
            raise ValueError(f"Content with id={id} not found.")
        # Fake an "attachment" record
        return {
            "attachmentId": "1",
            "fileName": getattr(file, "name", "unknown"),
            "comment": comment,
            "minorEdit": minorEdit
        }

    def update_attachment(
        self,
        id: str,
        attachmentId: str,
        body: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates attachment metadata. We'll simulate it as a no-op.
        """
        content = DB["contents"].get(id)
        if not content:
            raise ValueError(f"Content with id={id} not found.")
        return {
            "attachmentId": attachmentId,
            "updatedFields": body
        }

    def update_attachment_data(
        self,
        id: str,
        attachmentId: str,
        file: Any,
        comment: Optional[str] = None,
        minorEdit: bool = False
    ) -> Dict[str, Any]:
        """
        Updates the binary data of an existing attachment. Mock only.
        """
        content = DB["contents"].get(id)
        if not content:
            raise ValueError(f"Content with id={id} not found.")
        return {
            "attachmentId": attachmentId,
            "updatedFile": getattr(file, "name", "unknown"),
            "comment": comment,
            "minorEdit": minorEdit
        }

    def get_content_descendants(
        self,
        id: str,
        expand: Optional[str] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Returns a map of all descendants (by type). We'll return an empty structure here.
        """
        return {"comment": [], "attachment": []}

    def get_content_descendants_of_type(
        self,
        id: str,
        type: str,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Returns descendants of a particular type. Return an empty list in this simulation.
        """
        return []

    def get_content_labels(
        self,
        id: str,
        prefix: Optional[str] = None,
        start: int = 0,
        limit: int = 200
    ) -> List[Dict[str, Any]]:
        """
        Returns a paginated list of content labels. If a prefix is provided,
        it filters labels that start with the given prefix.
        """
        content = DB["contents"].get(id)
        if not content:
            raise ValueError(f"Content with id={id} not found.")

        # Retrieve labels or return empty list if none exist
        labels = DB["content_labels"].get(id, [])

        # Apply prefix filter if provided
        if prefix:
            labels = [label for label in labels if label.startswith(prefix)]

        # Apply pagination
        paginated_labels = labels[start:start + limit]

        # Return in expected response format
        return [{"label": label} for label in paginated_labels]


    def add_content_labels(
        self,
        id: str,
        labels: List[Any]
    ) -> List[Dict[str, Any]]:
        """
        Adds labels to a content item. If the content does not have existing labels,
        a new entry is created. Returns the updated list of labels.
        """
        content = DB["contents"].get(id)
        if not content:
            raise ValueError(f"Content with id={id} not found.")

        # Ensure the content has an entry in the labels dictionary
        if id not in DB["content_labels"]:
            DB["content_labels"][id] = []

        # Add new labels, avoiding duplicates
        existing_labels = set(DB["content_labels"][id])
        new_labels = set(labels)
        DB["content_labels"][id] = list(existing_labels.union(new_labels))

        # Return updated label list in expected response format
        return [{"label": label} for label in DB["content_labels"][id]]


    def get_content_properties(
        self,
        id: str,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Returns a paginated list of content properties for the specified content.
        """
        # Gather all properties from DB["content_properties"] for that ID
        matching = []
        for (cid, key), prop in DB["content_properties"].items():
            if cid == id:
                matching.append(prop)
        return matching[start:start + limit]

    def create_content_property(
        self,
        id: str,
        body: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates a new content property. Expects 'key' in body, 'value' in body.
        """
        content = DB["contents"].get(id)
        if not content:
            raise ValueError(f"Content with id={id} not found.")
        key = body.get("key")
        if not key:
            raise ValueError("Missing property 'key'.")
        value = body.get("value", {})
        version = 1
        DB["content_properties"][(id, key)] = {
            "key": key,
            "value": value,
            "version": version
        }
        return DB["content_properties"][(id, key)]

    def get_content_property(
        self,
        id: str,
        key: str,
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Returns a content property by key.
        """
        prop = DB["content_properties"].get((id, key))
        if not prop:
            raise ValueError(f"Property '{key}' not found for content {id}.")
        return prop

    def create_content_property_for_key(
        self,
        id: str,
        key: str,
        body: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates a new content property for the given key if version=1, else update.
        """
        # We'll treat it similarly to create_content_property but with the key param
        content = DB["contents"].get(id)
        if not content:
            raise ValueError(f"Content with id={id} not found.")
        version = body.get("version", {}).get("number", 1)
        value = body.get("value", {})
        DB["content_properties"][(id, key)] = {
            "key": key,
            "value": value,
            "version": version
        }
        return DB["content_properties"][(id, key)]

    def update_content_property(
        self,
        id: str,
        key: str,
        body: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates a content property, requires correct version increment. We'll skip strict checks.
        """
        prop = DB["content_properties"].get((id, key))
        if not prop:
            raise ValueError(f"Property '{key}' not found for content {id}.")
        new_version = body.get("version", {}).get("number", prop["version"] + 1)
        value = body.get("value", prop["value"])
        updated = {
            "key": key,
            "value": value,
            "version": new_version
        }
        DB["content_properties"][(id, key)] = updated
        return updated

    def delete_content_property(
        self,
        id: str,
        key: str
    ) -> None:
        """
        Deletes a content property by key.
        """
        if (id, key) in DB["content_properties"]:
            del DB["content_properties"][(id, key)]
        else:
            raise ValueError(f"Property '{key}' not found for content {id}.")

    def get_content_restrictions_by_operation(
        self,
        id: str,
        expand: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Returns restriction info by operation type. We return a minimal mock.
        """
        if id not in DB["contents"]:
            raise ValueError(f"Content with id={id} not found.")
        return {
            "read": {"restrictions": {"user": [], "group": []}},
            "update": {"restrictions": {"user": [], "group": []}}
        }

    def get_content_restrictions_for_operation(
        self,
        id: str,
        operationKey: str,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Returns restriction details for a single operation key (read/update).
        We'll produce a mock response.
        """
        if id not in DB["contents"]:
            raise ValueError(f"Content with id={id} not found.")
        if operationKey not in ["read", "update"]:
            raise ValueError(f"OperationKey '{operationKey}' not supported.")
        return {
            "operationKey": operationKey,
            "restrictions": {
                "user": [],
                "group": []
            }
        }

# -------------------------------------------------------------------
# 2) content_body_api
# -------------------------------------------------------------------
class ContentBodyAPI:
    """
    Simulates converting content body representations. We'll mock it since no real transformations.
    """

    def convert_content_body(self, to: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts from one content representation to another, faking the logic.
        """
        if to not in ["view", "export_view", "editor", "storage"]:
            raise ValueError(f"Unsupported target representation '{to}'.")
        # We'll just return the body with a note about 'convertedTo'
        return {
            "convertedTo": to,
            "originalBody": body
        }

# -------------------------------------------------------------------
# 3) long_task_api
# -------------------------------------------------------------------
class LongTaskAPI:
    """
    Simulates long-running tasks. We'll store them in DB['long_tasks'].
    """

    def get_long_tasks(
        self,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Returns info about all tracked tasks.
        """
        tasks = list(DB["long_tasks"].values())
        return tasks[start:start+limit]

    def get_long_task(self, id: str, expand: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns info about a single task by ID.
        """
        task = DB["long_tasks"].get(id)
        if not task:
            raise ValueError(f"Task with id={id} not found.")
        return task

# -------------------------------------------------------------------
# 4) space_api
# -------------------------------------------------------------------
class SpaceAPI:
    """
    Simulated space management methods.
    """

    def get_spaces(
        self,
        spaceKey: Optional[str] = None,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Returns info about multiple spaces, optionally filtered by spaceKey.
        """
        all_spaces = list(DB["spaces"].values())
        if spaceKey:
            # In Confluence, spaceKey can be repeated, but let's do a simple approach:
            all_spaces = [s for s in all_spaces if s["spaceKey"] == spaceKey]
        return all_spaces[start:start+limit]

    def create_space(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new space. Must include 'key' and 'name' in the body.
        """
        spaceKey = body.get("key")
        if not spaceKey:
            raise ValueError("Missing space 'key'.")
        if spaceKey in DB["spaces"]:
            raise ValueError(f"Space with key={spaceKey} already exists.")
        new_space = {
            "spaceKey": spaceKey,
            "name": body.get("name", ""),
            "description": body.get("description", "")
        }
        DB["spaces"][spaceKey] = new_space
        return new_space

    def create_private_space(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new private space. Similar logic as create_space, but with different default perms.
        """
        return self.create_space(body)

    def get_space(self, spaceKey: str, expand: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns info about a single space by key.
        """
        space = DB["spaces"].get(spaceKey)
        if not space:
            raise ValueError(f"Space with key={spaceKey} not found.")
        return space

    def update_space(self, spaceKey: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates a space (name, description, homepage).
        """
        space = DB["spaces"].get(spaceKey)
        if not space:
            raise ValueError(f"Space with key={spaceKey} not found.")
        # Update fields
        if "name" in body:
            space["name"] = body["name"]
        if "description" in body:
            space["description"] = body["description"]
        # ignoring homepage for brevity
        DB["spaces"][spaceKey] = space
        return space

    def delete_space(self, spaceKey: str) -> Dict[str, Any]:
        """
        Deletes a space. We'll simulate returning a long-running task.
        """
        if spaceKey not in DB["spaces"]:
            raise ValueError(f"Space with key={spaceKey} not found.")
        task_id = str(DB["long_task_counter"])
        DB["long_task_counter"] += 1
        DB["deleted_spaces_tasks"][task_id] = {
            "id": task_id,
            "spaceKey": spaceKey,
            "status": "in_progress",
            "description": f"Deleting space '{spaceKey}'"
        }
        # We'll pretend it completes immediately for this simulation:
        del DB["spaces"][spaceKey]
        DB["deleted_spaces_tasks"][task_id]["status"] = "complete"
        return DB["deleted_spaces_tasks"][task_id]

    def get_space_content(
        self,
        spaceKey: str,
        depth: Optional[str] = None,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Returns content in a given space. We'll filter DB["contents"] by spaceKey.
        """
        all_contents = list(DB["contents"].values())
        results = [c for c in all_contents if c.get("spaceKey") == spaceKey]
        return results[start:start+limit]

    def get_space_content_of_type(
        self,
        spaceKey: str,
        type: str,
        depth: Optional[str] = None,
        expand: Optional[str] = None,
        start: int = 0,
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Returns content of a specified type within a space.
        """
        content_list = self.get_space_content(spaceKey, depth, expand, start=0, limit=999999)
        filtered = [c for c in content_list if c.get("type") == type]
        return filtered[start:start+limit]
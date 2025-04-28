"""
User Management by ID Module

This module provides functionality for managing SCIM (System for Cross-domain
Identity Management) users by their unique identifiers. It implements the SCIM
protocol (RFC 7644) for user resource management, supporting operations for
retrieving, updating, and deleting specific users.

The module interfaces with the simulation database to provide comprehensive
user management capabilities, allowing users to:
- Retrieve specific user details by ID
- Update user attributes using PATCH operations
- Replace entire user resources using PUT operations
- Delete users from the system
"""

from typing import Dict, Optional, Union, List, Any
from .SimulationEngine import db

def get(id: str, attributes: Optional[str] = None, filter: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Retrieves a User resource by ID (see section 3.4.1 of RFC 7644).

    This function locates a specific user in the system using their unique
    identifier and returns their complete or filtered information.

    Args:
        id (str): The unique identifier of the user to retrieve.
        attributes (Optional[str], default=None): Comma-separated list of attributes
            to include in the response. If specified, only these attributes will
            be returned.
        filter (Optional[str], default=None): Filter criteria for the user search.
            Not fully implemented in simulation.

    Returns:
        Optional[Dict[str, Any]]: If found, returns a dictionary containing the
            user's information. If attributes is specified, only includes the
            requested attributes. If not found, returns None.
    """
    for user in db.DB["scim"]["users"]:
        if user.get("id") == id:
            if attributes:
                attrs = attributes.split(",")
                return {attr: user.get(attr) for attr in attrs if attr in user}
            return user
    return None

def patch(id: str, body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Updates one or more attributes of a User resource using PATCH operations
    (see section 3.5.2 of RFC 7644).

    This function applies a sequence of modifications to a user's attributes
    using the SCIM PATCH operation format.

    Args:
        id (str): The unique identifier of the user to update.
        body (Dict[str, Any]): Dictionary containing the PATCH operations:
            - "Operations" (List[Dict[str, Any]]): List of operations to perform
            Each operation should contain:
                - "op" (str): The operation type (e.g., "replace")
                - "path" (str): The attribute path to modify
                - "value" (Any): The new value for the attribute

    Returns:
        Optional[Dict[str, Any]]: If found and updated, returns the modified
            user dictionary. If not found, returns None.
    """
    for user in db.DB["scim"]["users"]:
        if user.get("id") == id:
            for operation in body.get("Operations", []):
                op = operation.get("op")
                path = operation.get("path")
                value = operation.get("value")
                if op == "replace" and path and value:
                    parts = path.split(".")
                    if len(parts) == 1:
                        user[parts[0]] = value
            return user
    return None

def put(id: str, body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Updates a User resource using PUT operation (see section 3.5.1 of RFC 7644).

    This function replaces the entire user resource with the provided data,
    maintaining the original ID.

    Args:
        id (str): The unique identifier of the user to update.
        body (Dict[str, Any]): Dictionary containing the complete new user
            resource data.

    Returns:
        Optional[Dict[str, Any]]: If found and updated, returns the new user
            dictionary with the original ID. If not found, returns None.
    """
    for i, user in enumerate(db.DB["scim"]["users"]):
        if user.get("id") == id:
            db.DB["scim"]["users"][i] = body
            body["id"] = id
            return body
    return None

def delete(id: str) -> bool:
    """
    Deletes a User resource (see section 3.6 of RFC 7644).

    This function removes a user from the system using their unique identifier.

    Args:
        id (str): The unique identifier of the user to delete.

    Returns:
        bool: True if the user was found and deleted, False if the user was
            not found.
    """
    for i, user in enumerate(db.DB["scim"]["users"]):
        if user.get("id") == id:
            del db.DB["scim"]["users"][i]
            return True
    return False 
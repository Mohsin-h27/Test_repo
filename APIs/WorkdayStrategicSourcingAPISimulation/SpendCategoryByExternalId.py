"""
Spend Category Management by External ID Module

This module provides functionality for managing spend categories using their external
identifiers in the Workday Strategic Sourcing system. It supports operations for
retrieving, updating, and deleting spend category details using external IDs.

The module interfaces with the simulation database to provide comprehensive spend
category management capabilities, allowing users to perform CRUD operations on spend
categories using their external IDs. This is particularly useful when integrating
with external systems that maintain their own spend category identifiers.

Functions:
    get: Retrieves spend category details by external ID
    patch: Updates spend category details by external ID
    delete: Deletes a spend category by external ID
"""

from typing import Dict, Any, Optional, List
from .SimulationEngine import db

def get(external_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves the details of a specific spend category using its external identifier.

    This function searches the database for a spend category with the specified
    external ID and returns all associated details if found.

    Args:
        external_id (str): The external identifier of the spend category to retrieve.
            This is the identifier used by external systems to reference the spend category.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the spend category details if found.
            The dictionary includes the following key-value pairs:
            - "id" (int): The internal unique identifier of the spend category
            - "name" (str): The display name of the spend category
            - "external_id" (str): The external identifier used to look up this category
            - "usages" (Optional[List[str]]): A list of usage contexts where this spend
                category is applicable
            Returns None if no spend category exists with the given external ID.
    """
    for category in db.DB["spend_categories"].values():
        if category.get("external_id") == external_id:
            return category
    return None

def patch(external_id: str, name: Optional[str] = None, new_external_id: Optional[str] = None, 
          usages: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
    """
    Updates the details of an existing spend category using its external identifier.

    This function allows partial updates to a spend category's details. Only the fields
    that are provided will be updated; unspecified fields will retain their current values.

    Args:
        external_id (str): The external identifier of the spend category to update.
            This is the current external ID used to locate the spend category.
        name (Optional[str], default=None): The new name for the spend category.
            If None, the current name will be retained.
        new_external_id (Optional[str], default=None): The new external identifier for the spend category.
            If None, the current external ID will be retained.
        usages (Optional[List[str]], default=None): The new list of usage contexts for the spend category.
            If None, the current usages will be retained.

    Returns:
        Optional[Dict[str, Any]]: The updated spend category details if successful.
            The dictionary includes the following key-value pairs:
            - "id" (int): The internal unique identifier of the spend category
            - "name" (str): The updated or current name of the spend category
            - "external_id" (str): The updated or current external identifier
            - "usages" (Optional[List[str]]): The updated or current list of usage contexts
            Returns None if no spend category exists with the given external ID.
    """
    for id, category in db.DB["spend_categories"].items():
        if category.get("external_id") == external_id:
            if name is not None:
                category["name"] = name
            if new_external_id is not None:
                category["external_id"] = new_external_id
            if usages is not None:
                category["usages"] = usages
            return category
    return None

def delete(external_id: str) -> bool:
    """
    Deletes a spend category using its external identifier.

    This function permanently removes a spend category from the system. The operation
    cannot be undone, and any references to the deleted category in other parts of
    the system may need to be updated.

    Args:
        external_id (str): The external identifier of the spend category to delete.
            This is the external ID used to locate the spend category to be deleted.

    Returns:
        bool: True if the spend category was successfully deleted,
              False if no spend category exists with the given external ID.
    """
    for id, category in db.DB["spend_categories"].items():
        if category.get("external_id") == external_id:
            del db.DB["spend_categories"][id]
            return True
    return False 
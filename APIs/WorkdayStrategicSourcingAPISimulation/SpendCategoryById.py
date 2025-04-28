"""
Spend Category Management by ID Module

This module provides functionality for managing spend categories using their unique
internal identifiers in the Workday Strategic Sourcing system. It supports operations
for retrieving, updating, and deleting spend category details.

The module interfaces with the simulation database to provide comprehensive spend
category management capabilities, allowing users to perform CRUD operations on spend
categories using their internal IDs.

Functions:
    get: Retrieves spend category details by ID
    patch: Updates spend category details by ID
    delete: Deletes a spend category by ID
"""

from typing import Dict, Any, Optional, List, Union
from .SimulationEngine import db

def get(id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieves the details of a specific spend category using its unique internal identifier.

    This function looks up a spend category in the database using its internal ID and
    returns all associated details if found.

    Args:
        id (int): The unique internal identifier of the spend category to retrieve.
            Must be a positive integer.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the spend category details if found.
            The dictionary includes the following key-value pairs:
            - "id" (int): The internal unique identifier of the spend category
            - "name" (str): The display name of the spend category
            - "external_id" (Optional[str]): An external identifier for the spend category,
                if one has been assigned
            - "usages" (Optional[List[str]]): A list of usage contexts where this spend
                category is applicable
            Returns None if no spend category exists with the given ID.
    """
    return db.DB["spend_categories"].get(id)

def patch(id: int, name: Optional[str] = None, external_id: Optional[str] = None, 
          usages: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
    """
    Updates the details of an existing spend category using its unique internal identifier.

    This function allows partial updates to a spend category's details. Only the fields
    that are provided will be updated; unspecified fields will retain their current values.

    Args:
        id (int): The unique internal identifier of the spend category to update.
            Must be a positive integer.
        name (Optional[str], default=None): The new name for the spend category.
            If None, the current name will be retained.
        external_id (Optional[str], default=None): The new external identifier for the spend category.
            If None, the current external ID will be retained.
        usages (Optional[List[str]], default=None): The new list of usage contexts for the spend category.
            If None, the current usages will be retained.

    Returns:
        Optional[Dict[str, Any]]: The updated spend category details if successful.
            The dictionary includes the following key-value pairs:
            - "id" (int): The internal unique identifier of the spend category
            - "name" (str): The updated or current name of the spend category
            - "external_id" (Optional[str]): The updated or current external identifier
            - "usages" (Optional[List[str]]): The updated or current list of usage contexts
            Returns None if no spend category exists with the given ID.
    """
    if id not in db.DB["spend_categories"]:
        return None
    category = db.DB["spend_categories"][id]
    if name is not None:
        category["name"] = name
    if external_id is not None:
        category["external_id"] = external_id
    if usages is not None:
        category["usages"] = usages
    return category

def delete(id: int) -> bool:
    """
    Deletes a spend category using its unique internal identifier.

    This function permanently removes a spend category from the system. The operation
    cannot be undone, and any references to the deleted category in other parts of
    the system may need to be updated.

    Args:
        id (int): The unique internal identifier of the spend category to delete.
            Must be a positive integer.

    Returns:
        bool: True if the spend category was successfully deleted,
              False if no spend category exists with the given ID.
    """
    if id in db.DB["spend_categories"]:
        del db.DB["spend_categories"][id]
        return True
    return False 
"""
Spend Categories Management Module

This module provides functionality for managing spend categories in the Workday Strategic
Sourcing system. It supports operations for retrieving all spend categories and creating
new spend category entries.

The module interfaces with the simulation database to maintain spend category data, which
is used to categorize and track spending across different areas of procurement and
supplier management.

Functions:
    get: Retrieves all spend categories
    post: Creates a new spend category
"""

from typing import List, Dict, Any, Optional
from .SimulationEngine import db

def get() -> List[Dict[str, Any]]:
    """
    Retrieves all spend categories from the database.

    This function returns a list of all spend categories currently defined in the system,
    including their internal IDs, names, external IDs, and usage contexts.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing spend category entries.
            Each dictionary contains the following key-value pairs:
            - "id" (int): The internal unique identifier of the spend category
            - "name" (str): The display name of the spend category
            - "external_id" (Optional[str]): An external identifier for the spend category,
                if one has been assigned
            - "usages" (Optional[List[str]]): A list of usage contexts where this spend
                category is applicable
    """
    return list(db.DB["spend_categories"].values())

def post(name: str, external_id: Optional[str] = None, usages: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Creates a new spend category with the specified parameters.

    This function creates a new spend category entry in the system with the provided
    parameters and assigns it a unique internal identifier.

    Args:
        name (str): The name of the spend category.
            This is a required field and cannot be empty.
        external_id (Optional[str], default=None): An external identifier for the spend category.
            This is an optional field that can be used to link the category to external systems.
        usages (Optional[List[str]], default=None): A list of usage contexts for the spend category.
            This is an optional field that specifies where the category can be used.

    Returns:
        Dict[str, Any]: A dictionary containing the newly created spend category details.
            The dictionary includes the following key-value pairs:
            - "id" (int): The automatically generated internal unique identifier
            - "name" (str): The provided name of the spend category
            - "external_id" (Optional[str]): The provided external identifier, if any
            - "usages" (Optional[List[str]]): The provided list of usage contexts, if any
    """
    new_id = len(db.DB["spend_categories"]) + 1
    new_category = {
        "id": new_id,
        "name": name,
        "external_id": external_id,
        "usages": usages,
    }
    db.DB["spend_categories"][new_id] = new_category
    return new_category 
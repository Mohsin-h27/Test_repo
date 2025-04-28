"""
Supplier Company Management by ID Module

This module provides functionality for managing individual supplier companies using
their unique internal identifiers in the Workday Strategic Sourcing system. It
supports operations for retrieving, updating, and deleting supplier company records.

The module interfaces with the simulation database to provide comprehensive supplier
company management capabilities, allowing users to:
- Retrieve detailed supplier company information
- Update existing supplier company records
- Delete supplier company entries
- Handle related resource inclusion where applicable

Functions:
    get: Retrieves supplier company details by ID
    patch: Updates supplier company details by ID
    delete: Deletes a supplier company by ID
"""

from typing import Dict, Any, Optional, Tuple, Union
from .SimulationEngine import db

def get(id: int, include: Optional[str] = None) -> Tuple[Union[Dict[str, Any], Dict[str, str]], int]:
    """
    Retrieves the details of a specific supplier company using its unique identifier.

    This function looks up a supplier company in the database using its internal ID
    and returns all associated details if found. It also supports including related
    resources in the response.

    Args:
        id (int): The unique identifier of the supplier company to retrieve.
            Must be a positive integer.
        include (Optional[str], default=None): Comma-separated list of related resources to include
            in the response. Not fully implemented in simulation.

    Returns:
        Tuple[Union[Dict[str, Any], Dict[str, str]], int]: A tuple containing:
            - Dict[str, Any]: The supplier company details if found, including:
                - "id" (int): The internal unique identifier
                - "external_id" (Optional[str]): The external identifier, if assigned
                - "name" (str): The company name
                - "status" (str): The company status
                - "address" (Dict[str, Any]): Company address details
                - "contacts" (List[Dict[str, Any]]): List of company contacts
                - "segmentation" (Dict[str, Any]): Company segmentation details
                - Other company-specific fields
            - int: HTTP status code (200 for success, 404 for not found)
            If company not found, returns:
            - Dict[str, str]: Error message with key "error"
            - int: 404 status code
    """
    company = db.DB["suppliers"]["supplier_companies"].get(id)
    if not company:
        return {"error": "Company not found"}, 404
    if include:
        # Simulate include logic (not fully implemented)
        pass
    return company, 200

def patch(id: int, include: Optional[str] = None, 
          body: Optional[Dict[str, Any]] = None) -> Tuple[Union[Dict[str, Any], Dict[str, str]], int]:
    """
    Updates the details of an existing supplier company.

    This function allows updating a supplier company's details. It supports partial
    updates and related resource inclusion.

    Args:
        id (int): The unique identifier of the supplier company to update.
            Must be a positive integer.
        include (Optional[str], default=None): Comma-separated list of related resources to include
            in the response. Not fully implemented in simulation.
        body (Optional[Dict[str, Any]], default=None): Dictionary containing the supplier company attributes
            to update. Required for successful update. May include:
            - "name" (str): New company name
            - "status" (str): New company status
            - "external_id" (str): New external identifier
            - "address" (Dict[str, Any]): New address details
            - Other updatable company fields

    Returns:
        Tuple[Union[Dict[str, Any], Dict[str, str]], int]: A tuple containing:
            - Dict[str, Any]: The updated supplier company details if successful
            - int: HTTP status code (200 for success, 404 for not found, 400 for bad request)
            If unsuccessful, returns:
            - Dict[str, str]: Error message with key "error"
            - int: Appropriate error status code (404 for not found, 400 for bad request)
    """
    company = db.DB["suppliers"]["supplier_companies"].get(id)
    if not company:
        return {"error": "Company not found"}, 404
    if not body:
        return {"error": "Body is required"}, 400
    company.update(body)
    if include:
        # Simulate include logic (not fully implemented)
        pass
    return company, 200

def delete(id: int) -> Tuple[Union[Dict[str, Any], Dict[str, str]], int]:
    """
    Deletes a supplier company using its unique identifier.

    This function permanently removes a supplier company from the system. The operation
    cannot be undone, and any references to the deleted company in other parts of
    the system may need to be updated.

    Args:
        id (int): The unique identifier of the supplier company to delete.
            Must be a positive integer.

    Returns:
        Tuple[Union[Dict[str, Any], Dict[str, str]], int]: A tuple containing:
            - Dict[str, Any]: Empty dictionary if successful
            - int: HTTP status code (204 for success, 404 for not found)
            If company not found, returns:
            - Dict[str, str]: Error message with key "error"
            - int: 404 status code
    """
    if id not in db.DB["suppliers"]["supplier_companies"]:
        return {"error": "Company not found"}, 404
    del db.DB["suppliers"]["supplier_companies"][id]
    return {}, 204 
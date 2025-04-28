"""
Supplier Company Management by External ID Module

This module provides functionality for managing supplier companies using their external
identifiers in the Workday Strategic Sourcing system. It supports operations for
retrieving, updating, and deleting supplier company records using external IDs.

The module interfaces with the simulation database to provide comprehensive supplier
company management capabilities, particularly useful when integrating with external
systems that maintain their own identifiers. It allows users to:
- Retrieve detailed supplier company information using external IDs
- Update existing supplier company records with external ID validation
- Delete supplier company entries by external ID
- Handle related resource inclusion where applicable

Functions:
    get: Retrieves supplier company details by external ID
    patch: Updates supplier company details by external ID
    delete: Deletes a supplier company by external ID
"""

from typing import Dict, Any, Optional, Tuple, Union
from .SimulationEngine import db

def get(external_id: str, include: Optional[str] = None) -> Tuple[Union[Dict[str, Any], Dict[str, str]], int]:
    """
    Retrieves the details of a specific supplier company using its external identifier.

    This function searches the database for a supplier company with the specified
    external ID and returns all associated details if found. It also supports
    including related resources in the response.

    Args:
        external_id (str): The external identifier of the supplier company to retrieve.
            This is the identifier used by external systems to reference the supplier company.
        include (Optional[str], default=None): Comma-separated list of related resources to include
            in the response. Not fully implemented in simulation.

    Returns:
        Tuple[Union[Dict[str, Any], Dict[str, str]], int]: A tuple containing:
            - Dict[str, Any]: The supplier company details if found, including:
                - "id" (int): The internal unique identifier
                - "external_id" (str): The external identifier
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
    for company in db.DB["suppliers"]["supplier_companies"].values():
        if company.get("external_id") == external_id:
            if include:
                #simulate include
                pass
            return company, 200
    return {"error": "Company not found"}, 404

def patch(external_id: str, include: Optional[str] = None, 
          body: Optional[Dict[str, Any]] = None) -> Tuple[Union[Dict[str, Any], Dict[str, str]], int]:
    """
    Updates the details of an existing supplier company using its external identifier.

    This function allows updating a supplier company's details while ensuring the
    external ID in the request body matches the one in the URL. It supports partial
    updates and related resource inclusion.

    Args:
        external_id (str): The external identifier of the supplier company to update.
            This is the current external ID used to locate the supplier company.
        include (Optional[str], default=None): Comma-separated list of related resources to include
            in the response. Not fully implemented in simulation.
        body (Optional[Dict[str, Any]], default=None): Dictionary containing the supplier company attributes
            to update. Required for successful update. The external_id in the body
            must match the one in the URL. May include:
            - "id" (str): Must match the external_id parameter
            - "name" (str): New company name
            - "status" (str): New company status
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
    for company_id, company in db.DB["suppliers"]["supplier_companies"].items():
        if company.get("external_id") == external_id:
            if not body:
                return {"error": "Body is required"}, 400
            if body.get("id") != external_id:
                return {"error": "External id in body must match url"}, 400

            company.update(body)
            if include:
                #simulate include
                pass
            return company, 200
    return {"error": "Company not found"}, 404

def delete(external_id: str) -> Tuple[Union[Dict[str, Any], Dict[str, str]], int]:
    """
    Deletes a supplier company using its external identifier.

    This function permanently removes a supplier company from the system. The operation
    cannot be undone, and any references to the deleted company in other parts of
    the system may need to be updated.

    Args:
        external_id (str): The external identifier of the supplier company to delete.
            This is the external ID used to locate the supplier company to be deleted.

    Returns:
        Tuple[Union[Dict[str, Any], Dict[str, str]], int]: A tuple containing:
            - Dict[str, Any]: Empty dictionary if successful
            - int: HTTP status code (204 for success, 404 for not found)
            If company not found, returns:
            - Dict[str, str]: Error message with key "error"
            - int: 404 status code
    """
    company_id_to_delete = None
    for company_id, company in db.DB["suppliers"]["supplier_companies"].items():
        if company.get("external_id") == external_id:
            company_id_to_delete = company_id
            break
    if company_id_to_delete is None:
        return {"error": "Company not found"}, 404
    del db.DB["suppliers"]["supplier_companies"][company_id_to_delete]
    return {}, 204 
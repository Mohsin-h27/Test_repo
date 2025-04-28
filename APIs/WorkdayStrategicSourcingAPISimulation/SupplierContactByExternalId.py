"""
Supplier Contact Management by External ID Module

This module provides functionality for managing supplier contacts using their external
identifiers in the Workday Strategic Sourcing system. It supports operations for
retrieving, updating, and deleting supplier contact records using external IDs.

The module interfaces with the simulation database to provide comprehensive supplier
contact management capabilities, particularly useful when integrating with external
systems that maintain their own identifiers. It allows users to:
- Retrieve detailed supplier contact information using external IDs
- Update existing supplier contact records with external ID validation
- Delete supplier contact entries by external ID
- Handle related resource inclusion where applicable

Functions:
    get: Retrieves supplier contact details by external ID
    patch: Updates supplier contact details by external ID
    delete: Deletes a supplier contact by external ID
"""

from .SimulationEngine import db

def get(external_id: str, include: str = None):
    """
    Retrieves the details of a specific supplier contact using its external identifier.

    Args:
        external_id (str): The external identifier of the supplier contact to retrieve.
        include (str, optional): Comma-separated list of related resources to include
            in the response. Not fully implemented in simulation.

    Returns:
        tuple: A tuple containing:
            - dict: The supplier contact details if found,
                   or an error message if contact not found
            - int: HTTP status code (200 for success, 404 for not found)
    """
    for contact in db.DB["suppliers"]["supplier_contacts"].values():
        if contact.get("external_id") == external_id:
            if include:
                # Simulate include logic (not fully implemented)
                pass
            return contact, 200
    return {"error": "Contact not found"}, 404

def patch(external_id: str, include: str = None, body: dict = None):
    """
    Updates the details of an existing supplier contact using its external identifier.

    Args:
        external_id (str): The external identifier of the supplier contact to update.
        include (str, optional): Comma-separated list of related resources to include
            in the response. Not fully implemented in simulation.
        body (dict, optional): Dictionary containing the supplier contact attributes
            to update. Required for successful update.

    Returns:
        tuple: A tuple containing:
            - dict: The updated supplier contact details if successful,
                   or an error message if contact not found or body missing
            - int: HTTP status code (200 for success, 404 for not found,
                  400 for bad request)
    """
    for contact_id, contact in db.DB["suppliers"]["supplier_contacts"].items():
        if contact.get("external_id") == external_id:
            if not body:
                return {"error": "Body is required"}, 400
            contact.update(body)
            if include:
                # Simulate include logic (not fully implemented)
                pass
            return contact, 200
    return {"error": "Contact not found"}, 404

def delete(external_id: str):
    """
    Deletes a supplier contact using its external identifier.

    Args:
        external_id (str): The external identifier of the supplier contact to delete.

    Returns:
        tuple: A tuple containing:
            - dict: Empty dictionary if successful,
                   or an error message if contact not found
            - int: HTTP status code (204 for success, 404 for not found)
    """
    contact_id_to_delete = None
    for contact_id, contact in db.DB["suppliers"]["supplier_contacts"].items():
        if contact.get("external_id") == external_id:
            contact_id_to_delete = contact_id
            break
    if contact_id_to_delete is None:
        return {"error": "Contact not found"}, 404
    del db.DB["suppliers"]["supplier_contacts"][contact_id_to_delete]
    return {}, 204 
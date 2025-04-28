"""
Supplier Contact Management by ID Module

This module provides functionality for managing individual supplier contacts using
their unique internal identifiers in the Workday Strategic Sourcing system. It
supports operations for retrieving, updating, and deleting supplier contact records.

The module interfaces with the simulation database to provide comprehensive supplier
contact management capabilities, allowing users to:
- Retrieve detailed supplier contact information
- Update existing supplier contact records
- Delete supplier contact entries
- Handle related resource inclusion where applicable

Functions:
    get: Retrieves supplier contact details by ID
    patch: Updates supplier contact details by ID
    delete: Deletes a supplier contact by ID
"""

from .SimulationEngine import db

def get(id: int, include: str = None):
    """
    Retrieves the details of a specific supplier contact using its unique identifier.

    Args:
        id (int): The unique identifier of the supplier contact to retrieve.
        include (str, optional): Comma-separated list of related resources to include
            in the response. Not fully implemented in simulation.

    Returns:
        tuple: A tuple containing:
            - dict: The supplier contact details if found,
                   or an error message if contact not found
            - int: HTTP status code (200 for success, 404 for not found)
    """
    contact = db.DB["suppliers"]["supplier_contacts"].get(id)
    if not contact:
        return {"error": "Contact not found"}, 404
    if include:
        # Simulate include logic (not fully implemented)
        pass
    return contact, 200

def patch(id: int, include: str = None, body: dict = None):
    """
    Updates the details of an existing supplier contact using its unique identifier.

    Args:
        id (int): The unique identifier of the supplier contact to update.
        include (str, optional): Comma-separated list of related resources to include
            in the response. Not fully implemented in simulation.
        body (dict, optional): Dictionary containing the supplier contact attributes
            to update. Required for successful update. The ID in the body must match
            the one in the URL.

    Returns:
        tuple: A tuple containing:
            - dict: The updated supplier contact details if successful,
                   or an error message if contact not found, body missing,
                   or ID mismatch
            - int: HTTP status code (200 for success, 404 for not found,
                  400 for bad request)
    """
    contact = db.DB["suppliers"]["supplier_contacts"].get(id)
    if not contact:
        return {"error": "Contact not found"}, 404
    if not body:
        return {"error": "Body is required"}, 400
    if body.get("id") != id:
        return {"error": "Id in body must match url"}, 400
    contact.update(body)
    if include:
        # Simulate include logic (not fully implemented)
        pass
    return contact, 200

def delete(id: int):
    """
    Deletes a supplier contact using its unique identifier.

    Args:
        id (int): The unique identifier of the supplier contact to delete.

    Returns:
        tuple: A tuple containing:
            - dict: Empty dictionary if successful,
                   or an error message if contact not found
            - int: HTTP status code (204 for success, 404 for not found)
    """
    if id not in db.DB["suppliers"]["supplier_contacts"]:
        return {"error": "Contact not found"}, 404
    del db.DB["suppliers"]["supplier_contacts"][id]
    return {}, 204 
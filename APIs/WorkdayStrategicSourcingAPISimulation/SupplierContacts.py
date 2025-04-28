"""
Supplier Contacts Management Module

This module provides functionality for managing supplier contacts in the Workday
Strategic Sourcing system. It supports operations for creating new supplier contact
records with custom attributes and relationships.

The module interfaces with the simulation database to provide supplier contact
management capabilities, allowing users to:
- Create new supplier contact records with custom attributes
- Support for related resource inclusion
- Maintain relationships with supplier companies
- Handle contact information and preferences

Functions:
    post: Creates a new supplier contact record
"""

from .SimulationEngine import db

def post(include: str = None, body: dict = None):
    """
    Creates a new supplier contact with specified attributes and relationships.

    This function allows for the creation of new supplier contact records in the
    system, with support for custom attributes and optional related resource
    inclusion.

    Args:
        include (str, optional): Comma-separated list of related resources to include
            in the response. Not fully implemented in simulation.
        body (dict, optional): Dictionary containing the supplier contact attributes
            and relationships to create. Required for successful creation.

    Returns:
        tuple: A tuple containing:
            - dict: The created supplier contact record if successful,
                   or an error message if body is missing
            - int: HTTP status code (201 for success, 400 for bad request)
    """
    if not body:
        return {"error": "Body is required"}, 400
    
    contact_id = len(db.DB["suppliers"]["supplier_contacts"]) + 1
    contact = {"id": contact_id, **body}
    db.DB["suppliers"]["supplier_contacts"][contact_id] = contact
    
    if include:
        # Simulate include logic (not fully implemented)
        pass
    return contact, 201 
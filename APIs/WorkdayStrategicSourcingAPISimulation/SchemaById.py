"""
SCIM Schema Management by ID Module

This module provides functionality for managing SCIM (System for Cross-domain Identity Management)
schemas using their unique URIs in the Workday Strategic Sourcing system. It supports operations
for retrieving detailed schema information.

The module interfaces with the simulation database to provide access to SCIM schema definitions,
which are essential for understanding the structure and attributes of identity resources in the
system.

Functions:
    get: Retrieves a specific SCIM schema by its URI
"""

from typing import Dict, Optional, Any
from .SimulationEngine import db

def get(uri: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves detailed information about a specific SCIM schema using its unique URI.

    This function searches the simulation database for a SCIM schema matching the provided URI.
    If found, it returns the complete schema definition including all attributes and metadata.

    Args:
        uri (str): The unique URI identifier of the SCIM schema to retrieve.
            Example: "urn:ietf:params:scim:schemas:core:2.0:User"

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the complete schema definition if found.
            The dictionary includes the following key-value pairs:
            - "uri" (str): The unique identifier of the schema
            - "name" (str): The display name of the schema
            - "description" (str): A human-readable description of the schema
            - "attributes" (List[Dict[str, Any]]): List of attribute definitions
            - Other metadata fields as defined in the SCIM specification
            Returns None if no schema exists with the given URI.
    """
    for schema in db.DB["scim"]["schemas"]:
        if schema.get("uri") == uri:
            return schema
    return None 
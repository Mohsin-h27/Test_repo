"""
SCIM Schema Management Module.

This module provides functionality for retrieving information about supported SCIM schemas
as defined in RFC 7644, section 3.4. It serves as a central point for schema information
used across the Workday Strategic Sourcing API simulation.

The module provides a single function to retrieve all available SCIM schemas, which are
essential for understanding the structure and attributes of identity resources in the system.
"""

from typing import List, Dict, Any
from .SimulationEngine import db

def get() -> List[Dict[str, Any]]:
    """
    Retrieve information about all supported SCIM schemas.

    This endpoint implements the SCIM schema discovery mechanism as specified in RFC 7644,
    section 3.4. It returns a list of all available schemas that can be used for
    validating and processing SCIM resources.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a SCIM schema.
            Each schema dictionary contains the following key-value pairs:
            - "id" (str): The schema's unique identifier
            - "name" (str): The schema's display name
            - "description" (str): A human-readable description of the schema
            - "attributes" (List[Dict[str, Any]]): List of attribute definitions, where each attribute
                contains:
                - "name" (str): The attribute name
                - "type" (str): The attribute data type
                - "multiValued" (bool): Whether the attribute can have multiple values
                - "description" (str): A human-readable description of the attribute
                - "required" (bool): Whether the attribute is required
                - "caseExact" (bool): Whether the attribute value is case-sensitive
                - "mutability" (str): The attribute's mutability (readOnly, readWrite, immutable, writeOnly)
                - "returned" (str): When the attribute is returned (always, never, default, request)
                - "uniqueness" (str): The attribute's uniqueness constraint (none, server, global)
            - "meta" (Dict[str, Any]): Schema metadata including:
                - "location" (str): The schema's URI
                - "resourceType" (str): The type of resource (Schema)
                - "created" (str): Creation timestamp
                - "lastModified" (str): Last modification timestamp
                - "version" (str): The schema version
    """
    return db.DB["scim"]["schemas"]
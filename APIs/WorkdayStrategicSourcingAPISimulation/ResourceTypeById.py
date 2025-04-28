"""
SCIM Resource Type Management by ID Module

This module provides functionality for managing SCIM (System for Cross-domain Identity
Management) resource types using their unique identifiers in the Workday Strategic
Sourcing system. It supports operations for retrieving detailed information about
specific resource types.

The module interfaces with the simulation database to provide access to SCIM resource
type definitions, which include endpoint configurations, supported schemas, and
extensions for different types of resources in the system.

Functions:
    get: Retrieves SCIM resource type details by resource name
"""

from typing import Dict, Optional
from .SimulationEngine import db

def get(resource: str) -> Optional[Dict]:
    """
    Retrieves detailed information about a specific SCIM resource type.

    Args:
        resource (str): The name of the SCIM resource type to retrieve.

    Returns:
        Optional[Dict]: A dictionary containing the resource type details if found,
                       including endpoint configurations, supported schemas, and extensions.
                       Returns None if no matching resource type exists.
    """
    for resource_type in db.DB["scim"]["resource_types"]:
        if resource_type.get("resource") == resource:
            return resource_type
    return None 
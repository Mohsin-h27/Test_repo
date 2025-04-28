"""
SCIM Resource Types Management Module

This module provides functionality for managing SCIM (System for Cross-domain Identity
Management) resource types in the Workday Strategic Sourcing system. It supports
operations for discovering available resource types and retrieving detailed information
about specific resource types.

The module interfaces with the simulation database to provide access to SCIM resource
type definitions, which include endpoint configurations, supported schemas, and
extensions for different types of resources in the system.

Functions:
    get: Retrieves a list of all available SCIM resource types
    get_by_resource: Retrieves details for a specific SCIM resource type
"""

from typing import List, Dict, Optional
from .SimulationEngine import db

def get() -> List[Dict]:
    """
    Retrieves a list of all available SCIM resource types in the system.

    Returns:
        List[Dict]: A list of dictionaries, where each dictionary contains the details
                   of a SCIM resource type, including its endpoint configurations,
                   supported schemas, and extensions.
    """
    return db.DB["scim"]["resource_types"]

def get_by_resource(resource: str) -> Optional[Dict]:
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
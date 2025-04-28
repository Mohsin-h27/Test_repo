"""
Project Type Management by ID Module

This module provides functionality for managing project types using their unique internal
identifiers in the Workday Strategic Sourcing system. It supports operations for retrieving
project type details.

The module interfaces with the simulation database to provide access to project type
definitions, which include configuration settings, default values, and metadata for
different types of projects in the system.

Functions:
    get: Retrieves project type details by ID
"""

from typing import Dict, Optional

from .SimulationEngine import db

def get(id: int) -> Optional[Dict]:
    """
    Retrieves the details of a specific project type using its unique internal identifier.

    Args:
        id (int): The unique internal identifier of the project type to retrieve.

    Returns:
        Optional[Dict]: A dictionary containing the project type details if found,
                       None if no project type exists with the given ID.
    """
    return db.DB["projects"]["project_types"].get(id) 
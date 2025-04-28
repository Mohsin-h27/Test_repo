"""
Project Types Management Module

This module provides functionality for managing project types in the Workday Strategic
Sourcing system. It supports operations for retrieving all available project types.

The module interfaces with the simulation database to provide access to project type
definitions, which include configuration settings, default values, and metadata for
different types of projects in the system.

Functions:
    get: Retrieves a list of all project types
"""

from typing import Dict, List

from .SimulationEngine import db

def get() -> List[Dict]:
    """
    Retrieves a list of all project types defined in the system.

    Returns:
        List[Dict]: A list of dictionaries, where each dictionary contains the details
                   of a project type, including its configuration settings, default values,
                   and metadata.
    """
    return list(db.DB["projects"]["project_types"].values()) 
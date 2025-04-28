"""
Project Milestone Reports Module

This module provides functionality for managing and retrieving project milestone reports
in the Workday Strategic Sourcing system. It supports operations for retrieving both the
report entries and the associated schema definitions.

The module interfaces with the simulation database to provide access to project milestone
report data, which includes comprehensive information about project milestones, their
status, completion dates, and associated metadata.

Functions:
    get_entries: Retrieves a list of all project milestone report entries
    get_schema: Retrieves the schema definition for project milestone reports
"""

from .SimulationEngine import db

def get_entries():
    """
    Retrieves all project milestone report entries from the database.

    Returns:
        list: A list of dictionaries containing project milestone report entries.
              Each entry contains detailed information about project milestones,
              including milestone status, completion dates, and associated project details.
    """
    return db.DB["reports"]["project_milestone_reports_entries"]

def get_schema():
    """
    Retrieves the schema definition for project milestone reports.

    Returns:
        dict: A dictionary containing the schema definition for project milestone reports.
              The schema includes field definitions, data types, and validation rules
              for project milestone report data.
    """
    return db.DB["reports"]["project_milestone_reports_schema"] 
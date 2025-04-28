"""
Project Reports Module

This module provides functionality for managing and retrieving project reports
in the Workday Strategic Sourcing system. It supports operations for retrieving
both individual project report entries and all project report entries, as well
as the associated schema definitions.

The module interfaces with the simulation database to provide access to project
report data, which includes comprehensive information about projects, their
status, milestones, and associated metadata.

Functions:
    get_project_report_entries: Retrieves entries for a specific project report
    get_entries: Retrieves all project report entries
    get_schema: Retrieves the schema definition for project reports
"""

from .SimulationEngine import db

def get_project_report_entries(project_report_id: int):
    """
    Retrieves entries for a specific project report using its unique identifier.

    Args:
        project_report_id (int): The unique identifier of the project report.

    Returns:
        list: A list of dictionaries containing project report entries for the specified report.
              Each entry contains detailed information about the project report.
              Returns an empty list if no entries are found for the specified report.
    """
    return db.DB["reports"].get(f'project_reports_{project_report_id}_entries', [])

def get_entries():
    """
    Retrieves all project report entries from the database.

    Returns:
        list: A list of dictionaries containing all project report entries.
              Each entry contains detailed information about a specific project report,
              including project status, milestones, and associated metadata.
    """
    return db.DB["reports"]["project_reports_entries"]

def get_schema():
    """
    Retrieves the schema definition for project reports.

    Returns:
        dict: A dictionary containing the schema definition for project reports.
              The schema includes field definitions, data types, and validation rules
              for project report data.
    """
    return db.DB["reports"]["project_reports_schema"] 
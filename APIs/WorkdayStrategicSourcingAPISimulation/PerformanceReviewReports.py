"""
Performance Review Reports Module

This module provides functionality for managing and retrieving performance review reports
in the Workday Strategic Sourcing system. It supports operations for retrieving both the
report entries and the associated schema definitions.

The module interfaces with the simulation database to provide access to performance review
report data, which includes comprehensive information about performance reviews, their
status, and associated metadata.

Functions:
    get_entries: Retrieves a list of all performance review report entries
    get_schema: Retrieves the schema definition for performance review reports
"""

from .SimulationEngine import db

def get_entries():
    """
    Retrieves all performance review report entries from the database.

    Returns:
        list: A list of dictionaries containing performance review report entries.
              Each entry contains detailed information about a specific performance review,
              including review status, participants, and evaluation criteria.
    """
    return db.DB["reports"]["performance_review_reports_entries"]

def get_schema():
    """
    Retrieves the schema definition for performance review reports.

    Returns:
        dict: A dictionary containing the schema definition for performance review reports.
              The schema includes field definitions, data types, and validation rules
              for performance review report data.
    """
    return db.DB["reports"]["performance_review_reports_schema"] 
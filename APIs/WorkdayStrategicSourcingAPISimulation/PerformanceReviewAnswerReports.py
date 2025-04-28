"""
Performance Review Answer Reports Module

This module provides functionality for managing and retrieving performance review answer reports
in the Workday Strategic Sourcing system. It supports operations for retrieving both the
report entries and the associated schema definitions.

The module interfaces with the simulation database to provide access to performance review
answer report data, which includes detailed information about answers provided in performance
reviews and their associated metadata.

Functions:
    get_entries: Retrieves a list of all performance review answer report entries
    get_schema: Retrieves the schema definition for performance review answer reports
"""

from .SimulationEngine import db

def get_entries():
    """
    Retrieves all performance review answer report entries from the database.

    Returns:
        list: A list of dictionaries containing performance review answer report entries.
              Each entry contains detailed information about a specific performance review answer.
              Returns an empty list if no entries are found.
    """
    return db.DB["reports"].get('performance_review_answer_reports_entries', [])

def get_schema():
    """
    Retrieves the schema definition for performance review answer reports.

    Returns:
        dict: A dictionary containing the schema definition for performance review answer reports.
              The schema includes field definitions, data types, and validation rules.
              Returns an empty dictionary if no schema is defined.
    """
    return db.DB["reports"].get('performance_review_answer_reports_schema', {}) 
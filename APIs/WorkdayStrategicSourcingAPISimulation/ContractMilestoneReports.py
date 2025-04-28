"""
Contract Milestone Reports Management Module for Workday Strategic Sourcing API Simulation.

This module provides functionality for managing and retrieving contract milestone
reports in the Workday Strategic Sourcing system. It supports operations for
accessing milestone report entries and their associated schema definitions. The
module enables comprehensive tracking and reporting of contract milestones and
their associated metrics.
"""

from typing import List, Dict
from .SimulationEngine import db

def get_entries() -> List[Dict]:
    """Retrieves a list of contract milestone report entries.

    This function returns all milestone report entries currently stored in the
    system, providing access to milestone tracking and reporting data. The entries
    include detailed information about contract milestones, their status, and
    associated metrics.

    Returns:
        List[Dict]: A list of dictionaries, where each dictionary represents a
            milestone report entry containing:
            - milestone_id (int): Unique identifier of the milestone
            - milestone_name (str): Name of the milestone
            - contract_id (int): ID of the associated contract
            - status (str): Current status of the milestone
            - due_date (str): Expected completion date
            - completed_date (str): Actual completion date
            - description (str): Detailed description of the milestone
            - created_at (str): Timestamp of milestone creation
            - updated_at (str): Timestamp of last update
            - metrics (Dict): Milestone-specific performance metrics

    Note:
        If no milestone report entries exist in the system, an empty list is
        returned. The returned data is read-only and should not be modified
        directly.
    """
    return db.DB["reports"].get('contract_milestone_reports_entries', [])

def get_schema() -> Dict:
    """Retrieves the schema definition for contract milestone reports.

    This function returns the complete schema definition that describes the
    structure and validation rules for contract milestone reports in the system.
    The schema defines the data model and constraints for milestone report
    creation and management.

    Returns:
        Dict: A dictionary containing the schema definition, including:
            - fields (Dict): Field definitions and types
            - validations (Dict): Validation rules and constraints
            - required_fields (List[str]): List of mandatory fields
            - relationships (Dict): Field relationships and dependencies
            - configurations (Dict): Report-specific settings and options

    Note:
        If no schema is defined in the system, an empty dictionary is returned.
        The schema is used for validation and documentation purposes and should
        not be modified directly.
    """
    return db.DB["reports"].get('contract_milestone_reports_schema', {}) 
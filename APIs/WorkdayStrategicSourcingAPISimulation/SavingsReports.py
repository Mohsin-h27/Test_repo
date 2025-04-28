"""
Savings Reports Management Module

This module provides functionality for managing savings reports in the Workday Strategic
Sourcing system. It supports operations for retrieving savings report entries and their
associated schema definitions.

The module interfaces with the simulation database to provide access to savings report
data, which includes detailed information about cost savings, financial metrics, and
related reporting information.

Functions:
    get_entries: Retrieves all savings report entries from the system
    get_schema: Retrieves the schema definition for savings reports
"""

from typing import List, Dict
from .SimulationEngine import db

def get_entries() -> List[Dict]:
    """
    Retrieves all savings report entries from the system.

    Returns:
        List[Dict]: A list of dictionaries, where each dictionary contains the details
                   of a savings report entry, including cost savings metrics, financial
                   data, and related reporting information. Returns an empty list if no
                   entries are found.
    """
    return db.DB["reports"].get('savings_reports_entries', [])

def get_schema() -> Dict:
    """
    Retrieves the schema definition for savings reports.

    Returns:
        Dict: A dictionary containing the schema definition for savings reports,
              including field names, data types, and validation rules. Returns an
              empty dictionary if no schema is defined.
    """
    return db.DB["reports"].get('savings_reports_schema', {}) 
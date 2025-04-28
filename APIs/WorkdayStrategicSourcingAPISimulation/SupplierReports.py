"""
Supplier Reports Management Module

This module provides functionality for managing supplier reports in the Workday
Strategic Sourcing system. It supports operations for retrieving supplier report
entries and their associated schema.

The module interfaces with the simulation database to provide comprehensive
report management capabilities, allowing users to:
- Retrieve all supplier report entries
- Access the supplier report schema definition
"""

from typing import List, Dict, Any
from .SimulationEngine import db

def get_entries() -> List[Dict[str, Any]]:
    """
    Retrieves all supplier report entries from the database.

    This function returns a list of all supplier report entries stored in the
    simulation database.

    Returns:
        List[Dict[str, Any]]: A list of supplier report entries, where each entry
            is a dictionary containing report-specific data fields.
    """
    return db.DB["reports"].get('supplier_reports_entries', [])

def get_schema() -> Dict[str, Any]:
    """
    Retrieves the schema definition for supplier reports.

    This function returns the schema that defines the structure and validation
    rules for supplier reports in the system.

    Returns:
        Dict[str, Any]: A dictionary containing the schema definition for
            supplier reports, including field definitions, types, and validation
            rules.
    """
    return db.DB["reports"].get('supplier_reports_schema', {}) 
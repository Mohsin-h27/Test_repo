"""
Supplier Review Reports Management Module

This module provides functionality for managing supplier review reports in the
Workday Strategic Sourcing system. It supports operations for retrieving supplier
review report entries and their associated schema.

The module interfaces with the simulation database to provide comprehensive
review report management capabilities, allowing users to:
- Retrieve all supplier review report entries
- Access the supplier review report schema definition
"""

from typing import List, Dict, Any
from .SimulationEngine import db

def get_entries() -> List[Dict[str, Any]]:
    """
    Retrieves all supplier review report entries from the database.

    This function returns a list of all supplier review report entries stored in
    the simulation database.

    Returns:
        List[Dict[str, Any]]: A list of supplier review report entries, where
            each entry is a dictionary containing review-specific data fields
            such as:
            - Review scores
            - Reviewer information
            - Review dates
            - Review comments
            - Other review-related metrics
    """
    return db.DB["reports"].get('supplier_review_reports_entries', [])

def get_schema() -> Dict[str, Any]:
    """
    Retrieves the schema definition for supplier review reports.

    This function returns the schema that defines the structure and validation
    rules for supplier review reports in the system.

    Returns:
        Dict[str, Any]: A dictionary containing the schema definition for
            supplier review reports, including:
            - Field definitions
            - Data types
            - Validation rules
            - Required fields
            - Field constraints
    """
    return db.DB["reports"].get('supplier_review_reports_schema', {}) 
"""
Suppliers Management Module

This module provides functionality for managing suppliers in the Workday Strategic
Sourcing system. It supports operations for retrieving supplier information,
including both bulk retrieval of all suppliers and individual supplier lookup.

The module interfaces with the simulation database to provide comprehensive
supplier management capabilities, allowing users to:
- Retrieve a list of all suppliers in the system
- Look up individual suppliers by their unique identifier
"""

from typing import List, Dict, Any, Optional
from .SimulationEngine import db

def get_suppliers() -> List[Dict[str, Any]]:
    """
    Retrieves a list of all suppliers from the database.

    This function returns all supplier entries stored in the simulation database.

    Returns:
        List[Dict[str, Any]]: A list of supplier dictionaries, where each
            dictionary contains supplier-specific data fields such as:
            - "id" (int): The unique identifier of the supplier
            - "name" (str): The name of the supplier
            - "status" (str): The current status of the supplier
            - Other supplier-specific fields
    """
    return db.DB["reports"].get('suppliers', [])

def get_supplier(supplier_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieves a specific supplier by their unique identifier.

    This function searches the database for a supplier matching the provided ID
    and returns their complete information if found.

    Args:
        supplier_id (int): The unique identifier of the supplier to retrieve.

    Returns:
        Optional[Dict[str, Any]]: If found, returns a dictionary containing the
            supplier's complete information. If not found, returns None.
    """
    suppliers = db.DB["reports"].get('suppliers', [])
    for supplier in suppliers:
        if supplier.get('id') == supplier_id:
            return supplier
    return None 
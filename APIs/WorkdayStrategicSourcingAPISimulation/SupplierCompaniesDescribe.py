"""
Supplier Company Field Description Module

This module provides functionality for describing the fields available in the
supplier company object. It allows users to retrieve a list of all available
fields that can be used when working with supplier company data.

The module interfaces with the simulation database to provide field information
for supplier company objects, enabling users to understand the structure and
available attributes of supplier company data.
"""

from typing import List, Tuple, Union
from .SimulationEngine import db

def get() -> Tuple[Union[List[str], List], int]:
    """
    Retrieves a list of fields available in the supplier company object.

    This function returns all field names that are present in the supplier company
    object structure. If no supplier companies exist in the database, it returns
    an empty list.

    Returns:
        Tuple[Union[List[str], List], int]: A tuple containing:
            - List[str]: List of field names available in the supplier company object,
              including but not limited to:
                - "id" (int): The unique identifier of the supplier company
                - "name" (str): The name of the supplier company
                - "status" (str): The current status of the supplier company
                - "external_id" (str): The external identifier of the supplier company
                - "address" (dict): The address information of the supplier company
                - "contacts" (list): List of contacts associated with the supplier company
                - Other supplier company-specific fields
            - int: HTTP status code (200 for success)
            If no supplier companies exist, returns:
            - List: Empty list
            - int: 200 status code
    """
    if not db.DB["suppliers"]["supplier_companies"]:
        return [], 200
    return list(db.DB["suppliers"]["supplier_companies"][list(db.DB["suppliers"]["supplier_companies"].keys())[0]].keys()), 200 
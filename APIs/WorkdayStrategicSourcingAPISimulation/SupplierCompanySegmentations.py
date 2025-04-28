"""
Supplier Company Segmentation Management Module

This module provides functionality for managing supplier company segmentations in the
Workday Strategic Sourcing system. It supports operations for retrieving existing
segmentations and creating new ones.

The module interfaces with the simulation database to provide comprehensive
segmentation management capabilities, allowing users to:
- Retrieve all existing supplier company segmentations
- Create new supplier company segmentations with custom parameters
"""

from typing import Dict, Any, List, Tuple, Union, Optional
from .SimulationEngine import db

def get() -> Tuple[List[Dict[str, Any]], int]:
    """
    Retrieves a list of all supplier company segmentations.

    This function returns all existing supplier company segmentations from the
    simulation database.

    Returns:
        Tuple[List[Dict[str, Any]], int]: A tuple containing:
            - List[Dict[str, Any]]: List of segmentation dictionaries, where each
              dictionary contains:
                - "id" (int): The unique identifier of the segmentation
                - Other segmentation-specific fields
            - int: HTTP status code (200 for success)
    """
    return list(db.DB["suppliers"]["supplier_company_segmentations"].values()), 200

def post(body: Optional[Dict[str, Any]] = None) -> Tuple[Union[Dict[str, Any], Dict[str, str]], int]:
    """
    Creates a new supplier company segmentation with the specified parameters.

    This function creates a new segmentation entry in the database with a unique
    identifier and the provided parameters.

    Args:
        body (Optional[Dict[str, Any]], default=None): Dictionary containing the
            segmentation parameters. Required fields:
            - At least one field to define the segmentation
            Optional fields:
            - Any segmentation-specific fields

    Returns:
        Tuple[Union[Dict[str, Any], Dict[str, str]], int]: A tuple containing:
            - Dict[str, Any]: The created segmentation dictionary including:
                - "id" (int): The newly assigned unique identifier
                - All provided segmentation fields
            - int: HTTP status code (201 for created)
            If request body is missing, returns:
            - Dict[str, str]: Error message with key "error"
            - int: 400 status code
    """
    if not body:
        return {"error": "Body is required"}, 400
    segmentation_id = len(db.DB["suppliers"]["supplier_company_segmentations"]) + 1
    segmentation = {"id": segmentation_id, **body}
    db.DB["suppliers"]["supplier_company_segmentations"][segmentation_id] = segmentation
    return segmentation, 201
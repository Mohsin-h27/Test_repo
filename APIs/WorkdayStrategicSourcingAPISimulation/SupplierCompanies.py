"""
Supplier Companies Management Module

This module provides functionality for managing supplier companies in the Workday
Strategic Sourcing system. It supports operations for retrieving and creating
supplier company records with various filtering, inclusion, and pagination options.

The module interfaces with the simulation database to provide comprehensive supplier
company management capabilities. It allows users to:
- Retrieve supplier companies with flexible filtering options
- Create new supplier company records with custom attributes
- Support for related resource inclusion and pagination
- Handle complex relationships and attributes

Functions:
    get: Retrieves supplier companies based on specified criteria
    post: Creates a new supplier company record
"""

from typing import Dict, Any, Optional, List, Tuple, Union
from .SimulationEngine import db

def get(filter: Optional[Dict[str, Any]] = None, include: Optional[str] = None, 
        page: Optional[Dict[str, Any]] = None) -> Tuple[List[Dict[str, Any]], int]:
    """
    Retrieves a list of supplier companies based on specified criteria.

    This function supports filtering, related resource inclusion, and pagination
    of supplier company records. It returns a list of companies matching the
    specified criteria.

    Args:
        filter (Optional[Dict[str, Any]], default=None): Dictionary of field-value pairs to filter supplier companies.
            Each key represents a field to match, and its value is the required value.
            Common filter fields include:
            - "name" (str): Company name
            - "status" (str): Company status
            - "external_id" (str): External identifier
            - Other company-specific fields
        include (Optional[str], default=None): Comma-separated list of related resources to include
            in the response. Not fully implemented in simulation.
        page (Optional[Dict[str, Any]], default=None): Pagination parameters for the response.
            Not fully implemented in simulation. Expected format:
            - "size" (int): Number of records per page
            - "number" (int): Page number (1-based)

    Returns:
        Tuple[List[Dict[str, Any]], int]: A tuple containing:
            - List[Dict[str, Any]]: List of supplier company dictionaries matching the criteria.
                Each dictionary includes:
                - "id" (int): The internal unique identifier
                - "external_id" (Optional[str]): The external identifier, if assigned
                - "name" (str): The company name
                - "status" (str): The company status
                - "address" (Dict[str, Any]): Company address details
                - "contacts" (List[Dict[str, Any]]): List of company contacts
                - "segmentation" (Dict[str, Any]): Company segmentation details
                - Other company-specific fields
            - int: HTTP status code (200 for success)
    """
    companies = list(db.DB["suppliers"]["supplier_companies"].values())
    if filter:
        filtered_companies = []
        for company in companies:
            match = True
            for key, value in filter.items():
                if company.get(key) != value:
                    match = False
                    break
            if match:
                filtered_companies.append(company)
        companies = filtered_companies
    if include:
        # Simulate include logic (not fully implemented)
        pass
    if page:
        # Simulate pagination logic (not fully implemented)
        pass
    return companies, 200

def post(include: Optional[str] = None, 
         body: Optional[Dict[str, Any]] = None) -> Tuple[Union[Dict[str, Any], Dict[str, str]], int]:
    """
    Creates a new supplier company with specified attributes and relationships.

    This function creates a new supplier company record with the provided attributes
    and assigns it a unique internal identifier.

    Args:
        include (Optional[str], default=None): Comma-separated list of related resources to include
            in the response. Not fully implemented in simulation.
        body (Optional[Dict[str, Any]], default=None): Dictionary containing the supplier company attributes
            and relationships to create. Required for successful creation. May include:
            - "name" (str): Company name (required)
            - "status" (str): Company status
            - "external_id" (str): External identifier
            - "address" (Dict[str, Any]): Company address details
            - "contacts" (List[Dict[str, Any]]): List of company contacts
            - "segmentation" (Dict[str, Any]): Company segmentation details
            - Other company-specific fields

    Returns:
        Tuple[Union[Dict[str, Any], Dict[str, str]], int]: A tuple containing:
            - Dict[str, Any]: The created supplier company record if successful, including:
                - "id" (int): The automatically generated internal unique identifier
                - All fields provided in the body
            - int: HTTP status code (201 for success, 400 for bad request)
            If body is missing, returns:
            - Dict[str, str]: Error message with key "error"
            - int: 400 status code
    """
    if not body:
        return {"error": "Body is required"}, 400
    company_id = len(db.DB["suppliers"]["supplier_companies"]) + 1
    company = {"id": company_id, **body}
    db.DB["suppliers"]["supplier_companies"][company_id] = company
    if include:
        # Simulate include logic (not fully implemented)
        pass
    return company, 201 
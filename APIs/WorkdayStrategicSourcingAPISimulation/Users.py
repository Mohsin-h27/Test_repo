
"""
SCIM Users Management Module

This module provides functionality for managing SCIM (System for Cross-domain
Identity Management) users in the Workday Strategic Sourcing system. It implements
the SCIM protocol (RFC 7644) for user resource management, supporting operations
for retrieving and creating users.

The module interfaces with the simulation database to provide comprehensive
user management capabilities, allowing users to:
- Retrieve lists of users with filtering, pagination, and sorting
- Create new users in the system
"""

from typing import List, Dict, Any, Optional
from .SimulationEngine import db

def get(attributes: Optional[str] = None, filter: Optional[str] = None,
        startIndex: Optional[int] = None, count: Optional[int] = None,
        sortBy: Optional[str] = None, sortOrder: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieves a list of users based on specified criteria (see section 3.4.2 of RFC 7644).

    This function supports filtering, pagination, and sorting of user resources.
    The pagination size is limited to 100 results per request.

    Args:
        attributes (Optional[str], default=None): Comma-separated list of attributes
            to include in the response. If specified, only these attributes will
            be returned for each user.
        filter (Optional[str], default=None): Filter criteria for the user search.
            Currently implements simple string matching.
        startIndex (Optional[int], default=None): The 1-based index of the first
            result in the current set of list results.
        count (Optional[int], default=None): The number of resources returned in
            a list response page.
        sortBy (Optional[str], default=None): The attribute whose value shall be
            used to order the returned responses.
        sortOrder (Optional[str], default=None): The order in which the sortBy
            parameter is applied. Allowed values are "ascending" or "descending".

    Returns:
        List[Dict[str, Any]]: A list of user dictionaries, where each dictionary
            contains the requested user attributes. If attributes is specified,
            only includes the requested attributes for each user.
    """
    users = db.DB["scim"]["users"]
    if filter:
        # Simple filter simulation
        filtered_users = []
        for user in users:
            if filter in str(user):
                filtered_users.append(user)
        users = filtered_users

    if startIndex and count:
        start = startIndex - 1
        end = start + count
        users = users[start:end]

    if sortBy:
        reverse = sortOrder == "descending"
        users.sort(key=lambda x: x.get(sortBy, ""), reverse=reverse)

    if attributes:
        attrs = attributes.split(",")
        result = []
        for user in users:
            filtered_user = {attr: user.get(attr) for attr in attrs if attr in user}
            result.append(filtered_user)
        return result
    return users

def post(body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a new User resource (see section 3.3 of RFC 7644).

    This function creates a new user in the system with the provided attributes
    and assigns a unique identifier.

    Args:
        body (Dict[str, Any]): Dictionary containing the user attributes:
            - Required fields as per SCIM schema
            - Optional fields as per SCIM schema

    Returns:
        Dict[str, Any]: The created user dictionary including:
            - "id" (str): The newly assigned unique identifier
            - All provided user attributes
    """
    user_id = str(len(db.DB["scim"]["users"]) + 1)
    body["id"] = user_id
    db.DB["scim"]["users"].append(body)
    return body 
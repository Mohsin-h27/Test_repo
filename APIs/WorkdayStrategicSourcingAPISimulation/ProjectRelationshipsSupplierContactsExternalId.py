"""
Project Supplier Contact Relationships by External ID Module

This module provides functionality for managing relationships between projects and supplier
contacts using external identifiers in the Workday Strategic Sourcing system. It supports
operations for adding and removing supplier contacts from projects using external IDs.

The module interfaces with the simulation database to maintain project-supplier contact
relationships, allowing for efficient management of supplier contact assignments to projects
using external identifiers. This is particularly useful when integrating with external
systems that maintain their own identifiers for projects and supplier contacts.

Functions:
    post: Adds supplier contacts to a project using external IDs
    delete: Removes supplier contacts from a project using external IDs
"""

from typing import Dict, List

from .SimulationEngine import db

def post(project_external_id: str, supplier_contact_external_ids: List[str]) -> bool:
    """
    Adds one or more supplier contacts to a project using external identifiers.

    Args:
        project_external_id (str): The external identifier of the project.
        supplier_contact_external_ids (List[str]): A list of supplier contact external IDs to add to the project.
                                                  For optimal performance, it's recommended to add 10 or fewer
                                                  supplier contacts in a single request.

    Returns:
        bool: True if the supplier contacts were successfully added to the project,
              False if the project doesn't exist.
    """
    for id, project in db.DB["projects"]["projects"].items():
        if project.get("external_id") == project_external_id:
            if "supplier_contacts" not in db.DB["projects"]["projects"][id]:
                db.DB["projects"]["projects"][id]["supplier_contacts"] = []
            db.DB["projects"]["projects"][id]["supplier_contacts"].extend(supplier_contact_external_ids)
            return True
    return False

def delete(project_external_id: str, supplier_contact_external_ids: List[str]) -> bool:
    """
    Removes one or more supplier contacts from a project using external identifiers.

    Args:
        project_external_id (str): The external identifier of the project.
        supplier_contact_external_ids (List[str]): A list of supplier contact external IDs to remove from the project.
                                                  For optimal performance, it's recommended to remove 10 or fewer
                                                  supplier contacts in a single request.

    Returns:
        bool: True if the supplier contacts were successfully removed from the project,
              False if the project doesn't exist or has no supplier contacts.
    """
    for id, project in db.DB["projects"]["projects"].items():
        if project.get("external_id") == project_external_id and "supplier_contacts" in db.DB["projects"]["projects"][id]:
            db.DB["projects"]["projects"][id]["supplier_contacts"] = [
                sid for sid in db.DB["projects"]["projects"][id]["supplier_contacts"] if sid not in supplier_contact_external_ids
            ]
            return True
    return False 
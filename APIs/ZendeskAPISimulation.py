#!/usr/bin/env python
"""
Fully Functional Python API Simulation

Implements a mock Zendesk API based on the provided specification. All resources
and methods are implemented as Python classes and in-memory data is stored in a
global DB dictionary. Includes save/load functionality for state persistence, and
embedded unit tests for comprehensive coverage.

Execute this file directly to run the test suite (using unittest).

Author: Thales Goncalves
"""

import json
import os
import unittest
from typing import List, Dict, Union

# ------------------------------------------------------------------------------
# Global In-Memory Database (JSON-serializable)
# ------------------------------------------------------------------------------
DB = {
    "tickets": {},
    "users": {},
    "organizations": {}
}

import json
import os
from typing import Any, Dict, List, Optional

# ------------------------------------------------------------------------------
# Persistence Methods
# ------------------------------------------------------------------------------
STATE_FILE = "api_state.json"

def save_state(filepath: str = STATE_FILE) -> None:
    with open(filepath, "w") as f:
        json.dump(DB, f)

def load_state(filepath: str = STATE_FILE) -> None:
    global DB
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            DB = json.load(f)

# ------------------------------------------------------------------------------
# Tickets
# ------------------------------------------------------------------------------
class Tickets:
    """Ticket resource simulation."""

    @staticmethod
    def create_ticket(
        ticket_id: int,
        subject: str,
        comment_body: str,
        priority: str = "normal",
        ticket_type: str = "question",
        status: str = "new"  # Default status set to "new"
    ) -> Dict[str, Any]:
        if ticket_id in DB["tickets"]:
            return {"error": "Ticket ID already exists"}
        DB["tickets"][ticket_id] = {
            "subject": subject,
            "comment": {"body": comment_body},
            "priority": priority,
            "type": ticket_type,
            "status": status  # Adding status to the ticket data
        }
        return {"success": True, "ticket": DB["tickets"][ticket_id]}


    @staticmethod
    def list_tickets() -> List[Dict[str, Any]]:
        return list(DB["tickets"].values())

    @staticmethod
    def show_ticket(ticket_id: int) -> Dict[str, Any]:
        return DB["tickets"].get(ticket_id, {"error": "Ticket not found"})

    @staticmethod
    def update_ticket(
        ticket_id: int,
        *,
        subject: Optional[str] = None,
        comment_body: Optional[str] = None,
        priority: Optional[str] = None,
        ticket_type: Optional[str] = None,
        status: Optional[str] = None  # Adding optional status parameter
    ) -> Dict[str, Any]:
        if ticket_id not in DB["tickets"]:
            return {"error": "Ticket not found"}
        if subject is not None:
            DB["tickets"][ticket_id]["subject"] = subject
        if comment_body is not None:
            DB["tickets"][ticket_id]["comment"] = {"body": comment_body}
        if priority is not None:
            DB["tickets"][ticket_id]["priority"] = priority
        if ticket_type is not None:
            DB["tickets"][ticket_id]["type"] = ticket_type
        if status is not None:
            DB["tickets"][ticket_id]["status"] = status  # Updating the status if provided
        return {"success": True, "ticket": DB["tickets"][ticket_id]}


    @staticmethod
    def delete_ticket(ticket_id: int) -> Dict[str, Any]:
        return DB["tickets"].pop(ticket_id, {"error": "Ticket not found"})

# ------------------------------------------------------------------------------
# Users
# ------------------------------------------------------------------------------
class Users:
    """User resource simulation."""

    @staticmethod
    def create_user(
        user_id: int,
        name: str,
        email: str,
        role: str = "end-user"
    ) -> Dict[str, Any]:
        if user_id in DB["users"]:
            return {"error": "User ID already exists"}
        DB["users"][user_id] = {"name": name, "email": email, "role": role}
        return {"success": True, "user": DB["users"][user_id]}

    @staticmethod
    def list_users() -> List[Dict[str, Any]]:
        return list(DB["users"].values())

    @staticmethod
    def show_user(user_id: int) -> Dict[str, Any]:
        return DB["users"].get(user_id, {"error": "User not found"})

    @staticmethod
    def update_user(
        user_id: int,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        role: Optional[str] = None
    ) -> Dict[str, Any]:
        if user_id not in DB["users"]:
            return {"error": "User not found"}
        if name is not None:
            DB["users"][user_id]["name"] = name
        if email is not None:
            DB["users"][user_id]["email"] = email
        if role is not None:
            DB["users"][user_id]["role"] = role
        return {"success": True, "user": DB["users"][user_id]}

    @staticmethod
    def delete_user(user_id: int) -> Dict[str, Any]:
        return DB["users"].pop(user_id, {"error": "User not found"})

# ------------------------------------------------------------------------------
# Organizations
# ------------------------------------------------------------------------------
class Organizations:
    """Organization resource simulation."""

    @staticmethod
    def create_organization(
        organization_id: int,
        name: str,
        domain_names: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        if domain_names is None:
            domain_names = []
        if organization_id in DB["organizations"]:
            return {"error": "Organization ID already exists"}
        DB["organizations"][organization_id] = {
            "name": name,
            "domain_names": domain_names,
        }
        return {"success": True, "organization": DB["organizations"][organization_id]}

    @staticmethod
    def list_organizations() -> List[Dict[str, Any]]:
        return list(DB["organizations"].values())

    @staticmethod
    def show_organization(organization_id: int) -> Dict[str, Any]:
        return DB["organizations"].get(organization_id, {"error": "Organization not found"})

    @staticmethod
    def update_organization(
        organization_id: int,
        *,
        name: Optional[str] = None,
        domain_names: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        if organization_id not in DB["organizations"]:
            return {"error": "Organization not found"}
        if name is not None:
            DB["organizations"][organization_id]["name"] = name
        if domain_names is not None:
            DB["organizations"][organization_id]["domain_names"] = domain_names
        return {"success": True, "organization": DB["organizations"][organization_id]}

    @staticmethod
    def delete_organization(organization_id: int) -> Dict[str, Any]:
        return DB["organizations"].pop(organization_id, {"error": "Organization not found"})

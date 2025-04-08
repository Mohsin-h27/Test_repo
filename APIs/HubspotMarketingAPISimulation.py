"""
Python simulation for resources from the Hubspot APIs,
with in-memory state, JSON persistence, and embedded tests.

Run this notebook end-to-end to execute tests verifying correctness of each method.
"""

import json
import unittest
from typing import List, Dict, Any, Optional, Union
import os
import hashlib
from unittest.mock import patch
import random
import uuid
import time
import datetime

# ---------------------------------------------------------------------------------------
# In-Memory Database Structure
# ---------------------------------------------------------------------------------------
DB: Dict[str, Any] = {
    "events": {},
    "attendees": {},
    "transactional_emails": {},
    "templates": {},
    "contacts": {},
    "marketing_emails": {},
    "campaigns": {},
    "events": {},
    "attendees": {},
    "forms": {},
    "marketing_events": {},
    "subscription_definitions": [],
    "subscriptions": {}

}

# -------------------------------------------------------------------
# Persistence Helpers
# -------------------------------------------------------------------
def save_state(filepath: str) -> None:
    """Saves the current state of the API to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(DB, f)


def load_state(filepath: str) -> None:
    """Loads the API state from a JSON file."""
    try:
        with open(filepath, "r") as f:
            global DB
            DB = json.load(f)
    except FileNotFoundError:
        pass


# -------------------------------------------------------------------
# Helper Function
# -------------------------------------------------------------------
def generate_hubspot_object_id(source=None):
    if source:
        # Create a consistent 9-digit ID using a hash of the source
        hash_value = int(hashlib.md5(source.encode()).hexdigest(), 16)
        object_id = (hash_value % 900000000) + 100000000  # Ensures exactly 9 digits
    else:
        # Generate a completely random 9-digit ID
        object_id = random.randint(100000000, 999999999)

    return object_id
# ---------------------------------------------------------------------------------------
# Templates Class & Methods
# ---------------------------------------------------------------------------------------
class Templates:
    """Represents the /content/api/v2/templates resource."""

    @staticmethod
    def get_templates(limit: Optional[int] = 20, offset: Optional[int] = 0, deleted_at: Optional[str] = None, id: Optional[str] = None, is_available_for_new_content: Optional[str] = None, label: Optional[str] = None, path: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all templates. Supports paging and filtering.

        Args:
            limit (Optional[int]): The maximum number of templates to return.
            offset (Optional[int]): The offset of the first template to return.

        Returns:
            List[Dict[str, Any]]: A list of template dictionaries.
        """
        templates = list(DB.get("templates", {}).values())
        filtered_templates = []
        for template in templates:
            if deleted_at and template.get("deleted_at") != deleted_at:
                continue
            if id and template.get("id") != id:
                continue
            if is_available_for_new_content and str(template.get("is_available_for_new_content")) != is_available_for_new_content:
                continue
            if label and template.get("label") != label:
                continue
            if path and template.get("path") != path:
                continue
            filtered_templates.append(template)

        return filtered_templates[offset:offset + limit]

    @staticmethod
    def create_template(source: str, created: str = None, template_type: int = 2, category_id: int = 2, folder: str = '/templates/', path:str = '/home/templates/', is_available_for_new_content: Optional[bool] = False) -> Dict[str, Any]:
        """
        Create a new coded template object in Design Manager.

        Args:
            source (str): The source of the template.
            created (str): The creation date of the template in milliseconds since epoch.
            template_type (int): This parameter accepts a numeric value and sets the type of template that is created. 2 - Email template, 4 - Page template, 11 - Error template, 12 - Subscription preferences template, 13 - Backup unsubscribe page template, 14 - Subscriptions update confirmation template, 19 - Password prompt page template, 27 - Search results template, 29 - Membership login template, 30 - Membership registration template, 31 - Membership reset password confirmation template, 32 - Membership reset password request template.
            category_id (int): This parameter category type: 0 - Unmapped, 1 - Landing Pages, 2 - Email, 3 - Blog Post, 4 - Site Page.
            folder (str): The name of the folder to save the template.
            path (str): The path to save the template.
            is_available_for_new_content (Optional[bool]): Used to determine if the template should be expected to pass page/content validation and be used with live content. This is equivalent to the Make Available for New Content? checkbox on Publish in the UI, and the Template vs. Template Partial radio select on template creation in the design manager beta. Default value is False.

        Returns:
            Dict[str, Any]: The created template dictionary.
        """
        template_id = str(generate_hubspot_object_id(source))

        counter = 0
        while template_id in DB.get("templates", {}):
            counter += 1
            template_id = str(int(template_id) + counter)

        new_template = {
            "id": template_id,
            "category_id": category_id,
            "folder": folder,
            "template_type": template_type,
            "source": source,
            "path": path,
            "created": created if created else str(int(time.time() * 1000)),
            "deleted_at": None,
            "is_available_for_new_content": is_available_for_new_content,
            "archived": False,
            "versions": [{"source": source, "version_id": "1"}]
        }
        if "templates" not in DB:
            DB["templates"] = {}
        DB["templates"][template_id] = new_template
        return new_template

    @staticmethod
    def get_template_by_id(template_id: str) -> Dict[str, Any]:
        """
        Get a specific template by ID.

        Args:
            template_id (str): The unique id of the template.

        Returns:
            Dict[str, Any]: The template dictionary.
        """
        return DB.get("templates", {}).get(template_id, {})

    @staticmethod
    def update_template_by_id(template_id: str, **kwargs) -> Dict[str, Any]:
        """
        Updates a template. If not all the fields are included in the body, we will only update the included fields.

        Args:
            template_id (str): Unique identifier for a particular template.
            **kwargs: The fields to update in the template. Can be any of the following:
                        category_id, folder, template_type,source markup, created, deleted_at, is_available_for_new_content, archived, versions.

        Returns:
            Dict[str, Any]: The updated template dictionary.
        """
        if template_id in DB.get("templates", {}):
            DB["templates"][template_id].update(kwargs)
            return DB["templates"][template_id]
        return {'error': 'Template not found'}

    @staticmethod
    def delete_template_by_id(template_id: str, deleted_at: str = None) -> None:
        """
        Marks the selected Template as deleted. The Template can be restored later via a POST to the restore-deleted endpoint.

        Args:
            template_id (str): Unique identifier for a particular template.
            deleted_at (str): Timestamp in milliseconds since epoch of when the template was deleted.
        """
        if template_id in DB.get("templates", {}):
            DB["templates"][template_id]["deleted_at"] = deleted_at if deleted_at else str(int(time.time() * 1000))

    @staticmethod
    def restore_deleted_template(template_id: str) -> Dict[str, Any]:
        """
        Restores a previously deleted Template.

        Args:
            template_id (str): Unique identifier for a particular template.

        Returns:
            Dict[str, Any]: The restored template dictionary.
        """
        if template_id in DB.get("templates", {}):
            DB["templates"][template_id]["deleted_at"] = None
            return DB["templates"][template_id]
        return {'error': 'Template not found'}

# ---------------------------------------------------------------------------------------
# Single Send Emails Class & Methods
# ---------------------------------------------------------------------------------------
class SingleSend:
    """
    Represents the /marketing/emails/single-send API endpoint.
    """

    @staticmethod
    def sendSingleEmail(
        template_id: str,
        message: Dict[str, Any],
        customProperties: Dict[str, Union[str, int, bool]] = None,
        contactProperties: Dict[str, Union[str, int, bool]] = None,
    ) -> Dict[str, Any]:
        """
        Sends a single transactional email based on a pre-existing email template.

        Args:
            template_id: The ID of the pre-existing transactional email template to send.
            message: An object containing email content and recipient info. Is a dictionary containing:
                to: A list of recipient objects with 'email' and 'name' properties. Must be provided.
                cc: A list of recipient objects with 'email' and 'name' properties (optional).
                bcc: A list of recipient objects with 'email' and 'name' properties (optional).
                from: An object with 'email' and 'name' properties (optional).
            customProperties: Custom property values for template personalization.
            contactProperties: Contact property values (takes precedence over customProperties).

        Returns:
            A dictionary representing the API response, including status and any errors.

        Raises:
            ValueError: If input parameters are invalid or the email template is not found.
        """

        if not all([template_id, message]):
            return {"status": "error", "message": "'template_id' and 'message' are required."}

        to = message.get("to", None)
        cc = message.get("cc", None)
        bcc = message.get("bcc", None)
        from_ = message.get("from", None)
        replyTo = message.get("replyTo", None)

        if not to:
            return {"status": "error", "message": "Each 'to' entry must be a dictionary with a non-empty 'email' string."}
        # Validate to
        for recipient in to:
            if not isinstance(recipient, dict) or not isinstance(recipient.get("email"), str) or not recipient["email"]:
                return {"status": "error", "message": "Each 'to' entry must be a dictionary with a non-empty 'email' string."}

        # Validate cc
        if cc is not None:
            for recipient in cc:
                if (
                    not isinstance(recipient, dict)
                    or "email" not in recipient
                    or not isinstance(recipient["email"], str)
                    or not recipient["email"]
                ):
                    return {"status": "error", "message": "Each 'cc' entry must be a dictionary with a non-empty 'email' string."}

        # Validate bcc
        if bcc is not None:
            for recipient in bcc:
                if (
                    not isinstance(recipient, dict)
                    or "email" not in recipient
                    or not isinstance(recipient["email"], str)
                    or not recipient["email"]
                ):
                    return {"status": "error", "message": "Each 'bcc' entry must be a dictionary with a non-empty 'email' string."}

        # Validate from_
        if from_ is not None:
            if not isinstance(from_, dict) or not isinstance(from_.get("email"), str) or not from_.get("email"):
                return {"status": "error", "message": "'from' field must be a dictionary with 'email' and 'name' properties."}

        # Validate replyTo
        if replyTo is not None:
            for recipient in replyTo:
                if (
                    not isinstance(recipient, dict)
                    or "email" not in recipient
                    or not isinstance(recipient["email"], str)
                    or not recipient["email"]
                ):
                    return {"status": "error", "message": "Each 'replyTo' entry must be a dictionary with a non-empty 'email' string."}

        # Check if the email template exists
        if not DB.get("templates", {}):
            DB["templates"] = {}
        if template_id not in DB["templates"]:
            return {
                "status": "error",
                "message": f"Email template with ID '{template_id}' not found.",
            }

        elif DB["templates"][template_id]["template_type"] != 2:
            return {
                "status": "error",
                "message": f"Template with ID '{template_id}' is not an email template.",
            }

        # --- HubSpot Contact Property Handling ---
        final_properties = customProperties.copy() if customProperties else {}

        # Iterate through recipients to apply contactProperties
        for recipient in to:
            recipient_email = recipient["email"]
            contact = DB["contacts"].get(recipient_email)
            if contact:
                # Merge contact properties with precedence over custom properties
                final_properties.update(contact)
            if contactProperties:
                final_properties.update(contactProperties)


        # Simulate sending the email (no actual sending)
        # Use a unique ID for each transactional email
        transactional_email_id = str(uuid.uuid4())
        log_entry = {
            "template_id": template_id,
            "transactional_email_id": transactional_email_id,  # Unique ID for the send
            "message": message,
            "properties": final_properties,  # Store merged properties
            "status": "sent",  # Assume successful send for simulation
        }
        DB["transactional_emails"][transactional_email_id] = log_entry  # Store by ID

        return {
            "status": "success",
            "message": f"Email sent successfully using template.",
            "template_id": template_id,
            "transactional_email_id": str(transactional_email_id), # Return the unique ID
            "log": log_entry,
        }

# ---------------------------------------------------------------------------------------
# Transactional Emails Class & Methods
# ---------------------------------------------------------------------------------------
class TransactionalEmails:
    """Represents the /transactional_emails resource."""

    @staticmethod
    def sendSingleEmail(message: Dict[str, Any], customProperties: Dict[str, Any] = None) -> Dict[str, Any]:
        """Sends a single transactional email.

        Args:
            message: An object containing email content and recipient info.
                     Required fields: 'to', 'from', 'subject', 'htmlBody'.
            customProperties: Optional custom properties for the email.
            email_id: Required. The ID of the email.

        Returns:
            A dictionary indicating success or failure, along with a message.
        """
        if not isinstance(message, dict):
            return {"success": False, "message": "Message must be an object."}
        if not all(key in message for key in ['to', 'from', 'subject', 'htmlBody']):
            return {"success": False, "message": "Message must contain 'to', 'from', 'subject', and 'htmlBody'."}

        email_id = str(uuid.uuid4())

        # Simulate sending the email (store in DB)
        if "transactional_emails" not in DB:
            DB["transactional_emails"] = {}

        if email_id not in DB["transactional_emails"]:
             DB["transactional_emails"][email_id] = []

        DB["transactional_emails"][email_id].append({
            "message": message,
            "customProperties": customProperties,
            "status": "sent",
            "email_id" : email_id
        })


        return {"success": True, "message": f"Transactional email sent successfully.", "email_id": email_id}

# ---------------------------------------------------------------------------------------
# Marketing Emails Class & Methods
# ---------------------------------------------------------------------------------------
class MarketingEmails:
    """Represents the /marketing_emails resource."""

    @staticmethod
    def create(name: str, subject: str = None, htmlBody: str = None, **kwargs: Any) -> Dict[str, Any]:
        """Creates a new marketing email.

        Args:
            name: The internal name of the email (required).
            subject: The email subject line.
            htmlBody:  The HTML body of the email.
            **kwargs: Other email properties.

        Returns:
            A dictionary containing the new email's ID and a success message, or an error message.
        """

        if not isinstance(name, str) or not name:
            return {"success": False, "message": "Name must be a non-empty string."}
        # Find next available email_id

        email_id = str(uuid.uuid4())


        DB["marketing_emails"][email_id] = {
            "name": name,
            "subject": subject,
            "htmlBody": htmlBody,
            "isTransactional": False,
            **kwargs
        }
        return {"success": True, "message": "Marketing email created successfully.", "email_id": email_id}

    @staticmethod
    def getById(email_id: str) -> Union[Dict[str, Any], None]:
        """Retrieves a marketing email by its ID.
        Args:
            email_id: The unique ID of the marketing email (required).

        Returns:
            The marketing email object if found, or None if not found.

        Raises:
            TypeError:  If the email_id isn't an integer
        """

        email = DB["marketing_emails"].get(email_id)

        return email if email else None

    @staticmethod
    def update(email_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Updates an existing marketing email.

        Args:
            email_id: The unique ID of the marketing email to update (required).
            **kwargs: Properties to update.

        Returns:
            A dictionary indicating success or failure and a message.
        """
        if email_id not in DB["marketing_emails"]:
            return {"success": False, "message": "Marketing email not found."}

        DB["marketing_emails"][email_id].update(kwargs)
        return {"success": True, "message": "Marketing email updated successfully."}

    @staticmethod
    def delete(email_id: str) -> Dict[str, Any]:
        """Deletes a marketing email.

        Args:
            email_id: The unique ID of the marketing email to delete (required).

        Returns:
            A dictionary indicating success or failure and a message.
        """
        if email_id not in DB["marketing_emails"]:
            return {"success": False, "message": "Marketing email not found."}

        del DB["marketing_emails"][email_id]
        return {"success": True, "message": "Marketing email deleted successfully."}

    @staticmethod
    def clone(email_id: str, name: str) -> Dict[str, Any]:
        """Clones an existing marketing email.

        Args:
            email_id: The ID of the marketing email to clone (required).
            name: The name for the new, cloned email (required).

        Returns:
             A dictionary containing the new email's ID and a success message, or an error message.
        """
        if email_id not in DB["marketing_emails"]:
            return {"success": False, "message": "Marketing email not found."}

        original_email = DB["marketing_emails"][email_id]
        # Find next available email_id
        next_id = str(uuid.uuid4())

        DB["marketing_emails"][next_id] = original_email.copy()  # Create a shallow copy
        DB["marketing_emails"][next_id]["name"] = name

        return {"success": True, "message": "Marketing email cloned successfully.", "email_id": next_id}

# ---------------------------------------------------------------------------------------
# Campaigns Class & Methods
# ---------------------------------------------------------------------------------------
class Campaigns:
    """
    Represents the /campaigns resource.
    """

    @staticmethod
    def get_campaigns(limit: Optional[int] = None, offset: Optional[int] = None,
                      created_at: Optional[str] = None, created_at__gt: Optional[str] = None,
                      created_at__gte: Optional[str] = None, created_at__lt: Optional[str] = None,
                      created_at__lte: Optional[str] = None, updated_at: Optional[str] = None,
                      updated_at__gt: Optional[str] = None, updated_at__gte: Optional[str] = None,
                      updated_at__lt: Optional[str] = None, updated_at__lte: Optional[str] = None,
                      name: Optional[str] = None, name__contains: Optional[str] = None,
                      name__icontains: Optional[str] = None, name__ne: Optional[str] = None,
                      id: Optional[str] = None, id__ne: Optional[str] = None,
                      type: Optional[str] = None, type__ne: Optional[str] = None) -> Dict:
        """
        Returns a list of marketing campaigns (Basic implementation).
        """

        campaigns_list = list(DB["campaigns"].values())

        # Very basic filtering (only id, name, and type for simplicity)
        if id:
            campaigns_list = [c for c in campaigns_list if c.get('id') == id]
        if name:
            campaigns_list = [c for c in campaigns_list if c.get('name') == name]
        if type:
            campaigns_list = [c for c in campaigns_list if c.get('type') == type]


        # Very basic pagination
        total_count = len(campaigns_list)
        if offset is not None:
            campaigns_list = campaigns_list[offset:]
        if limit is not None:
            campaigns_list = campaigns_list[:limit]

        return {
            "results": campaigns_list,
            "total": total_count,
            "limit": limit,
            "offset": offset
        }

    @staticmethod
    def create_campaign(name: str, slug: Optional[str] = None, description: Optional[str] = None,
                        start_year: Optional[int] = None, start_month: Optional[int] = None,
                        start_day: Optional[int] = None, end_year: Optional[int] = None,
                        end_month: Optional[int] = None, end_day: Optional[int] = None,
                        theme: Optional[str] = None, resource: Optional[str] = None,
                        color_label: Optional[str] = None) -> Dict[str, Any]:
        """
        Creates a new campaign.
        """
        campaign_id = str(uuid.uuid4())

        if slug is None:
            slug = f"{name.lower().replace(' ', '-')}-{campaign_id}"

        new_campaign = {
            "id": campaign_id,
            "name": name,
            "slug": slug,
            "description": description,
            "start_year": start_year,
            "start_month": start_month,
            "start_day": start_day,
            "end_year": end_year,
            "end_month": end_month,
            "end_day": end_day,
            "theme": theme,
            "resource": resource,
            "color_label": color_label,
            "created_at": campaign_id
        }
        DB["campaigns"][campaign_id] = new_campaign
        return new_campaign

    @staticmethod
    def get_campaign(campaign_id: int) -> Optional[Dict[str, Any]]:
        """
        Gets a single campaign by its ID.
        """
        return DB["campaigns"].get(campaign_id)

    @staticmethod
    def update_campaign(campaign_id: int, name: Optional[str] = None, slug: Optional[str] = None,
                        description: Optional[str] = None, start_year: Optional[int] = None,
                        start_month: Optional[int] = None, start_day: Optional[int] = None,
                        end_year: Optional[int] = None, end_month: Optional[int] = None,
                        end_day: Optional[int] = None, theme: Optional[str] = None,
                        resource: Optional[str] = None, color_label: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Updates a campaign.
        """
        campaign = DB["campaigns"].get(campaign_id)
        if campaign:
            if name is not None:
                campaign["name"] = name
            if slug is not None:
                campaign["slug"] = slug
            if description is not None:
                campaign["description"] = description
            if start_year is not None:
                campaign["start_year"] = start_year
            if start_month is not None:
                campaign["start_month"] = start_month
            if start_day is not None:
                campaign["start_day"] = start_day
            if end_year is not None:
                campaign["end_year"] = end_year
            if end_month is not None:
                campaign["end_month"] = end_month
            if end_day is not None:
                campaign["end_day"] = end_day
            if theme is not None:
                campaign["theme"] = theme
            if resource is not None:
                campaign["resource"] = resource
            if color_label is not None:
                campaign["color_label"] = color_label
            DB["campaigns"][campaign_id] = campaign
            return campaign
        return None

    @staticmethod
    def archive_campaign(campaign_id: int) -> bool:
        """
        Archives a campaign. Archived campaigns aren't included in the results when listing campaigns.
        """
        if campaign_id in DB["campaigns"]:
            DB["campaigns"][campaign_id]['is_archived'] = True
            return True
        return False

# ---------------------------------------------------------------------------------------
# Forms Class & Methods
# ---------------------------------------------------------------------------------------
class Forms:
    """
    Represents the /forms resource.
    """

    @staticmethod
    def get_forms(after: Optional[str] = None, limit: Optional[int] = None,
                  created_at: Optional[str] = None, created_at__gt: Optional[str] = None,
                  created_at__gte: Optional[str] = None, created_at__lt: Optional[str] = None,
                  created_at__lte: Optional[str] = None, updated_at: Optional[str] = None,
                  updated_at__gt: Optional[str] = None, updated_at__gte: Optional[str] = None,
                  updated_at__lt: Optional[str] = None, updated_at__lte: Optional[str] = None,
                  name: Optional[str] = None, id: Optional[str] = None) -> Dict:
        """
        Get all Marketing Forms.
        """
        forms_list = list(DB["forms"].values())

        # Filtering
        if created_at:
            created_at_dt = datetime.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            forms_list = [f for f in forms_list if
                          datetime.datetime.fromisoformat(f['createdAt'].replace("Z", "+00:00")) == created_at_dt]
        if created_at__gt:
            created_at_gt_dt = datetime.datetime.fromisoformat(created_at__gt.replace("Z", "+00:00"))
            forms_list = [f for f in forms_list if
                          datetime.datetime.fromisoformat(f['createdAt'].replace("Z", "+00:00")) > created_at_gt_dt]
        if created_at__gte:
            created_at__gte_dt = datetime.datetime.fromisoformat(created_at__gte.replace("Z", "+00:00"))
            forms_list = [f for f in forms_list if
                          datetime.datetime.fromisoformat(f['createdAt'].replace("Z", "+00:00")) >= created_at__gte_dt]
        if created_at__lt:
            created_at__lt_dt = datetime.datetime.fromisoformat(created_at__lt.replace("Z", "+00:00"))
            forms_list = [f for f in forms_list if
                          datetime.datetime.fromisoformat(f['createdAt'].replace("Z", "+00:00")) < created_at__lt_dt]
        if created_at__lte:
            created_at__lte_dt = datetime.datetime.fromisoformat(created_at__lte.replace("Z", "+00:00"))
            forms_list = [f for f in forms_list if
                          datetime.datetime.fromisoformat(f['createdAt'].replace("Z", "+00:00")) <= created_at__lte_dt]

        if updated_at:
            updated_at_dt = datetime.datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            forms_list = [f for f in forms_list if
                         datetime.datetime.fromisoformat(f['updatedAt'].replace("Z", "+00:00")) == updated_at_dt]
        if updated_at__gt:
            updated_at__gt_dt = datetime.datetime.fromisoformat(updated_at__gt.replace("Z", "+00:00"))
            forms_list = [f for f in forms_list if
                         datetime.datetime.fromisoformat(f['updatedAt'].replace("Z", "+00:00")) > updated_at__gt_dt]
        if updated_at__gte:
            updated_at__gte_dt = datetime.datetime.fromisoformat(updated_at__gte.replace("Z", "+00:00"))
            forms_list = [f for f in forms_list if
                         datetime.datetime.fromisoformat(f['updatedAt'].replace("Z", "+00:00")) >= updated_at__gte_dt]
        if updated_at__lt:
            updated_at__lt_dt = datetime.datetime.fromisoformat(updated_at__lt.replace("Z", "+00:00"))
            forms_list = [f for f in forms_list if
                         datetime.datetime.fromisoformat(f['updatedAt'].replace("Z", "+00:00")) < updated_at__lt_dt]
        if updated_at__lte:
            updated_at__lte_dt = datetime.datetime.fromisoformat(updated_at__lte.replace("Z", "+00:00"))
            forms_list = [f for f in forms_list if
                         datetime.datetime.fromisoformat(f['updatedAt'].replace("Z", "+00:00")) <= updated_at__lte_dt]
        if name:
            forms_list = [f for f in forms_list if f.get('name') == name]
        if id:
            forms_list = [f for f in forms_list if f.get('id') == id]


        # Pagination (using after and limit)
        total_count = len(forms_list)
        start_index = 0

        if after:
            try:
                # Find the index of the form with the given 'after' ID
                start_index = next(i for i, form in enumerate(forms_list) if form['id'] == after) + 1
            except StopIteration:
                # If 'after' ID not found, return empty results (or raise an error)
                return {"results": [], "total": total_count, "paging": None}
                # Alternative: raise ValueError(f"Form with id '{after}' not found")

        forms_list = forms_list[start_index:]

        if limit is not None:
            forms_list = forms_list[:limit]


        # Construct paging information
        paging = None
        if limit is not None and len(forms_list) == limit and start_index + limit < total_count:
            next_after = forms_list[-1]['id']
            paging = {"next": {"after": next_after}}

        return {
            "results": forms_list,
            "total": total_count,
            "paging": paging
        }

    @staticmethod
    def create_form(name: str, submitText: str, fieldGroups: List[Dict], legalConsentOptions: Dict) -> Dict:
        """Create a new Marketing Form."""
        new_form_id = str(uuid.uuid4())
        now = datetime.datetime.utcnow().isoformat() + "Z"
        new_form = {
            "id": new_form_id,
            "name": name,
            "submitText": submitText,
            "fieldGroups": fieldGroups,
            "legalConsentOptions": legalConsentOptions,
            "createdAt": now,
            "updatedAt": now
        }
        DB["forms"][new_form_id] = new_form
        return new_form

    @staticmethod
    def get_form(formId: str) -> Dict:
        """Get a Marketing Form by ID."""
        if formId not in DB["forms"]:
            raise ValueError(f"Form with id '{formId}' not found")  # Consistent error handling
        return DB["forms"][formId]

    @staticmethod
    def update_form(formId: str, name: Optional[str] = None, submitText: Optional[str] = None,
                    fieldGroups: Optional[List[Dict]] = None, legalConsentOptions: Optional[Dict] = None) -> Dict:
        """Update a Marketing Form."""

        if formId not in DB["forms"]:
             raise ValueError(f"Form with ID '{formId}' not found.")

        form = DB["forms"][formId]
        if name is not None:
            form["name"] = name
        if submitText is not None:
            form["submitText"] = submitText
        if fieldGroups is not None:
            form["fieldGroups"] = fieldGroups
        if legalConsentOptions is not None:
            form["legalConsentOptions"] = legalConsentOptions

        form["updatedAt"] = datetime.datetime.utcnow().isoformat() + "Z"
        return form

    @staticmethod
    def delete_form(formId: str) -> None:
        """Archive a form"""
        if formId not in DB["forms"]:
            return {"error": f"Form with ID '{formId}' not found."}
        del DB["forms"][formId]

# ---------------------------------------------------------------------------------------
# Global Forms Class & Methods
# ---------------------------------------------------------------------------------------
class FormGlobalEvents:
    """
    Represents the /forms/global-events resource.
    """

    @staticmethod
    def get_subscription_definitions() -> List[Dict]:
        """Get all global form event subscription definitions."""
        return DB["subscription_definitions"]

    @staticmethod
    def create_subscription(endpoint: str, subscriptionDetails: Dict) -> Dict:
        """Creates a new webhook subscription for global form events."""
        new_subscription_id = str(uuid.uuid4())
        new_subscription = {
            "id": new_subscription_id,
            "endpoint": endpoint,
            "subscriptionDetails": subscriptionDetails,
            "active": True  # Initially active
        }
        DB["subscriptions"][new_subscription_id] = new_subscription
        return new_subscription

    @staticmethod
    def get_subscriptions() -> List[Dict]:
        """Gets all webhook subscriptions for global form events."""
        return list(DB["subscriptions"].values())

    @staticmethod
    def delete_subscription(subscriptionId: int) -> None:
        """Deletes (unsubscribes) a webhook subscription."""
        subscriptionId = int(subscriptionId)  # Ensure correct type
        if subscriptionId not in DB["subscriptions"]:
            raise ValueError(f"Subscription with id '{subscriptionId}' not found")
        del DB["subscriptions"][subscriptionId]

    @staticmethod
    def update_subscription(subscriptionId: int, active: bool) -> Dict:
        """Updates (specifically, activates or deactivates) a webhook subscription."""
        subscriptionId = int(subscriptionId)  # Ensure correct type

        if subscriptionId not in DB["subscriptions"]:
           raise ValueError(f"Subscription with id '{subscriptionId}' not found")

        subscription = DB["subscriptions"][subscriptionId]
        subscription["active"] = active
        return subscription

# ---------------------------------------------------------------------------------------
# Marketing Events Class & Methods
# ---------------------------------------------------------------------------------------
class MarketingEvents:
    """
    Represents the /marketing-events resource.
    """

    @staticmethod
    def get_events(occurredAfter: Optional[str] = None, occurredBefore: Optional[str] = None,
                   limit: Optional[int] = None, after: Optional[str] = None) -> Dict:
        """Get all marketing events."""
        return {"results": list(DB["marketing_events"].values())}

    @staticmethod
    def create_event(externalEventId: str, externalAccountId: str, event_name: str, event_type: str, event_organizer: str,
                     start_date_time: Optional[str] = None, end_date_time: Optional[str] = None,
                     event_description: Optional[str] = None, event_url: Optional[str] = None,
                     custom_properties: Optional[List[Dict]] = None) -> Dict:
        """Create a marketing event.
        Args:
            externalEventId (str): The unique identifier for the marketing event as per the external system where the event was created.
            externalAccountId (str): The unique identifier for the account(external system) where the event was created.
            event_name (str): The name of the marketing event.
            event_type (str): The type of the marketing event.
            event_organizer (str): The organizer of the marketing event.
            start_date_time (str): The start date and time of the marketing event.
            end_date_time (str): The end date and time of the marketing event.
            event_description (str): A description of the marketing event.
            event_url (str): A URL for more information about the marketing event.
            custom_properties (List[Dict]): Custom properties associated with the marketing event.

        Returns:
            A dictionary representing the created marketing event.

        """
        event_id = externalEventId

        if not externalEventId:
            return {"error": "External Event ID is required."}
        if not externalAccountId:
            return {"error": "External Account ID is required."}

        event = {
            "externalEventId": externalEventId,
            "eventName": event_name,
            "eventType": event_type,
            "eventOrganizer": event_organizer,
            "startDateTime": start_date_time,
            "endDateTime": end_date_time,
            "eventDescription": event_description,
            "eventUrl": event_url,
            "customProperties": custom_properties,
            "externalAccountId": externalAccountId
        }
        DB["marketing_events"][event_id] = event
        return event

    @staticmethod
    def get_event(externalEventId: str, externalAccountId: str) -> Dict:
        """Get a marketing event by its external ID.

        Args:
            externalEventId (str): The unique identifier for the marketing event as per the external system where the event was created.
            externalAccountId (str): The unique identifier for the account where the event was created.

        Returns:
            A dictionary representing the marketing event.
        """
        if not externalEventId:
            return {"error": "External Event ID is required."}
        if not externalAccountId:
            return {"error": "External Account ID is required."}

        if externalEventId in DB["marketing_events"] and DB["marketing_events"][externalEventId]["externalAccountId"] == externalAccountId:
            return DB["marketing_events"][externalEventId]
        return {}

    @staticmethod
    def delete_event(externalEventId: str, externalAccountId: str) -> None:
        """Delete a marketing event.

        Args:
            externalEventId (str): The unique identifier for the marketing event as per the external system where the event was created.
            externalAccountId (str): The unique identifier for the account where the event was created.

        Returns:
            None
        """
        if not externalEventId:
            return {"error": "External Event ID is required."}
        if not externalAccountId:
            return {"error": "External Account ID is required."}
        if externalEventId in DB["marketing_events"] and DB["marketing_events"][externalEventId]["externalAccountId"] == externalAccountId:
            del DB["marketing_events"][externalEventId]

    @staticmethod
    def update_event(externalEventId: str, externalAccountId: str, event_name: Optional[str] = None,
                     event_type: Optional[str] = None, start_date_time: Optional[str] = None,
                     end_date_time: Optional[str] = None, event_organizer: Optional[str] = None,
                     event_description: Optional[str] = None, event_url: Optional[str] = None,
                     custom_properties: Optional[List[Dict]] = None) -> Dict:
        """Update a marketing event.

        Args:
            externalEventId (str): The unique identifier for the marketing event as per the external system where the event was created.
            externalAccountId (str): The unique identifier for the account where the event was created.
            event_name (str): The name of the marketing event.
            event_type (str): The type of the marketing event.
            start_date_time (str): The start date and time of the marketing event.
            end_date_time (str): The end date and time of the marketing event.
            event_organizer (str): The organizer of the marketing event.
            event_description (str): A description of the marketing event.
            event_url (str): A URL for more information about the marketing event.
            custom_properties (List[Dict]): Custom properties associated with the marketing event.

        Returns:
            A dictionary representing the updated marketing event.
        """
        if not externalEventId:
            return {"error": "External Event ID is required."}
        if not externalAccountId:
            return {"error": "External Account ID is required."}

        if externalEventId in DB["marketing_events"] and DB["marketing_events"][externalEventId]["externalAccountId"] == externalAccountId:
            event = DB["marketing_events"][externalEventId]
            if event_name:
                event["eventName"] = event_name
            if event_type:
                event["eventType"] = event_type
            if start_date_time:
                event["startDateTime"] = start_date_time
            if end_date_time:
                event["endDateTime"] = end_date_time
            if event_organizer:
                event["eventOrganizer"] = event_organizer
            if event_description:
                event["eventDescription"] = event_description
            if event_url:
                event["eventUrl"] = event_url
            if custom_properties:
                event["customProperties"] = custom_properties

            DB["marketing_events"][externalEventId] = event
            return event
        return {}

    @staticmethod
    def cancel_event(externalEventId: str, externalAccountId: str) -> Dict:
        """Marks an event as cancelled.

        Args:
            externalEventId (str): The unique identifier for the marketing event as per the external system where the event was created.
            externalAccountId (str): The unique identifier for the account where the event was created.

        Returns:
            A dictionary representing the cancelled marketing event.
        """
        if not externalEventId:
            return {"error": "External Event ID is required."}
        if not externalAccountId:
            return {"error": "External Account ID is required."}

        if externalEventId in DB["marketing_events"] and DB["marketing_events"][externalEventId]["externalAccountId"] == externalAccountId:
            DB["marketing_events"][externalEventId]["eventStatus"] = "CANCELED"
            return DB["marketing_events"][externalEventId]
        return {}


    @staticmethod
    def create_or_update_attendee(externalEventId: str, externalAccountId: str, email: str, joinedAt: str, leftAt: str) -> Dict:
        """Create or update an attendee for a marketing event.

        Args:
            externalEventId (str): The unique identifier for the marketing event as per the external system where the event was created.
            externalAccountId (str): The unique identifier for the account where the event was created.
            email (str): The email address of the attendee.
            joinedAt (str): The date and time when the attendee joined the event.
            leftAt (str): The date and time when the attendee left the event.

        Returns:
            A dictionary representing the updated attendee.
        """
        if not all([externalEventId, externalAccountId, email, joinedAt, leftAt]):
            return {"error": "Missing required parameters."}

        if not externalEventId in DB["marketing_events"]:
            return {"error": "Event not found."}

        if externalEventId not in DB["marketing_events"] or DB["marketing_events"][externalEventId]["externalAccountId"] != externalAccountId:
            return {}

        if not "attendees" in DB["marketing_events"][externalEventId]:
            DB["marketing_events"][externalEventId]["attendees"] = {}

        for attendee in DB["marketing_events"][externalEventId]["attendees"].values():
            if attendee["email"] == email:
                attendee["joinedAt"] = joinedAt
                attendee["leftAt"] = leftAt
                return attendee

        attendee_id = hashlib.sha256(f"{externalEventId}-{email}".encode()).hexdigest()[:8]
        attendee = {
            "attendeeId": attendee_id,
            "email": email,
            "eventId": externalEventId,
            "externalAccountId": externalAccountId
        }

        DB["marketing_events"][externalEventId]["attendees"][attendee_id] = attendee
        return attendee

    @staticmethod
    def get_attendees(externalEventId: str, limit: Optional[int] = None, after: Optional[str] = None) -> Dict:
        """Get attendees of a marketing event.

        Args:
            externalEventId (str): The unique identifier for the marketing event as per the external system where the event was created.
            limit (int): The maximum number of attendees to return.
            after (str): A cursor for pagination.

        Returns:
            A dictionary representing the attendees of the marketing event.
        """
        if not externalEventId:
            return {"error": "Event ID is required."}
        if externalEventId not in DB["marketing_events"]:
            return {"error": "Event not found."}
        attendees = list(DB["marketing_events"][externalEventId].get("attendees", {}).values())
        if limit:
            attendees = attendees[:limit]
        return {"results": attendees}

    @staticmethod
    def delete_attendee(externalEventId: str, attendeeId: str, externalAccountId: str) -> None:
        """Remove an attendee from a marketing event.

        Args:
            externalEventId (str): The unique identifier for the marketing event as per the external system where the event was created.
            attendeeId (str): The unique identifier for the attendee.

        Returns:
            None
        """
        if not externalEventId:
            return {"error": "Event ID is required."}
        if not attendeeId:
            return {"error": "Attendee ID is required."}
        if not externalAccountId:
            return {"error": "External Account ID is required."}

        if externalEventId not in DB["marketing_events"]:
            return {"error": "Event not found."}
        if "attendees" not in DB["marketing_events"][externalEventId]:
            return {"error": "Attendees not found."}
        if attendeeId not in DB["marketing_events"][externalEventId]["attendees"]:
            return {"error": "Attendee not found."}

        if DB["marketing_events"][externalEventId]["externalAccountId"] == externalAccountId:
            deleted = DB["marketing_events"][externalEventId]["attendees"].pop(attendeeId, None)
            return deleted
        else:
            return {"error": "Invalid external account ID."}
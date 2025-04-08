"""
Full Python simulation for all resources from the Workday Strategic Sourcing APIs,
with in-memory state, JSON persistence, and embedded tests.

Run this notebook end-to-end to execute tests verifying correctness of each method.
"""

import json
import unittest
from typing import List, Dict, Any, Optional
import os

# ---------------------------------------------------------------------------------------
# In-Memory Database Structure
# ---------------------------------------------------------------------------------------
DB: Dict[str, Any] = {
    'attachments': {},
    'awards': {'award_line_items': [], 'awards': []},
    'contracts': {'award_line_items': [],
                'awards': {},
                'contract_types': {},
                'contracts': {}},
    'events': {'bid_line_items': {},
                'bids': {},
                'event_templates': {},
                'events': {},
                'line_items': {},
                'worksheets': {}},
    'fields': {'field_groups': {}, 'field_options': {}, 'fields': {}},
    'payments': {'payment_currencies': [],
                'payment_currency_id_counter': "",
                'payment_term_id_counter': "",
                'payment_terms': [],
                'payment_type_id_counter': "",
                'payment_types': []},
    'projects': {'project_types': {}, 'projects': {}},
    'reports': {'contract_milestone_reports_entries': [],
                'contract_milestone_reports_schema': {},
                'contract_reports_entries': [],
                'contract_reports_schema': {},
                'event_reports': [],
                'event_reports_1_entries': [],
                'event_reports_entries': [],
                'event_reports_schema': {},
                'performance_review_answer_reports_entries': [],
                'performance_review_answer_reports_schema': {},
                'performance_review_reports_entries': [],
                'performance_review_reports_schema': {},
                'project_milestone_reports_entries': [],
                'project_milestone_reports_schema': {},
                'project_reports_1_entries': [],
                'project_reports_entries': [],
                'project_reports_schema': {},
                'savings_reports_entries': [],
                'savings_reports_schema': {},
                'supplier_reports_entries': [],
                'supplier_reports_schema': {},
                'supplier_review_reports_entries': [],
                'supplier_review_reports_schema': {},
                'suppliers': []},
    'scim': {'resource_types': [],
            'schemas': [],
            'service_provider_config': {},
            'users': []},
    'spend_categories': {},
    'suppliers': {'contact_types': {},
                'supplier_companies': {},
                'supplier_company_segmentations': {},
                'supplier_contacts': {}}}

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

# ---------------------------------------------------------------------------------------
# Attachments Classes & Methods
# ---------------------------------------------------------------------------------------
class Attachments:
    """Represents the /attachments resource."""

    @staticmethod
    def get(filter_id_equals: str) -> List[Dict[str, Any]]:
        """Returns a filtered list of attachments."""
        ids = filter_id_equals.split(",")
        result = []
        for attachment_id, attachment in DB["attachments"].items():
            if str(attachment_id) in ids:
                result.append(attachment)
            if len(result) >= 50:
                break
        return result

    @staticmethod
    def post(data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates an attachment."""
        external_id = data.get("external_id")

        # Check if external_id already exists
        if external_id and any(
            attachment.get("external_id") == external_id for attachment in DB["attachments"].values()
        ):
            return {"error": "Attachment with this external_id already exists."}

        attachment_id = max(
            [0] + [int(k) for k in DB["attachments"].keys()]
        ) + 1

        data["id"] = attachment_id
        DB["attachments"][str(attachment_id)] = data
        return data

    @staticmethod
    def list_attachments(filter_id_equals: str = None) -> Dict[str, Any]:
        """
        Returns a filtered list of attachments based on the `filter[id_equals]` param.
        The result is limited to 50 attachments.
        """
        attachments = list(DB["attachments"].values())
        if filter_id_equals:
            ids = filter_id_equals.split(",")
            attachments = [
                attachment
                for attachment in attachments
                if str(attachment.get("id")) in ids
            ]
        return {
            "data": attachments[:50],
            "links": {
                "self": "services/attachments/v1/attachments"
            },
            "meta": {"count": len(attachments[:50])},
        }


    @staticmethod
    def get_attachment_by_id(id: int) -> Optional[Dict[str, Any]]:
        """Retrieves the details of an existing attachment by ID."""
        attachment = DB["attachments"].get(str(id))
        return attachment

    @staticmethod
    def patch_attachment_by_id(id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Updates an attachment by ID."""
        if str(id) in DB["attachments"]:
            DB["attachments"][str(id)].update(data)
            DB["attachments"][str(id)]["id"] = id
            return DB["attachments"][str(id)]
        return None

    @staticmethod
    def delete_attachment_by_id(id: int) -> bool:
        """Deletes an attachment by ID."""
        if str(id) in DB["attachments"]:
            del DB["attachments"][str(id)]
            return True
        return False

    @staticmethod
    def get_attachment_by_external_id(external_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves the details of an existing attachment by external ID."""
        for attachment in DB["attachments"].values():
            if attachment.get("external_id") == external_id:
                return attachment
        return None

    @staticmethod
    def patch_attachment_by_external_id(external_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Updates an attachment by external ID."""
        for attachment_id, attachment in DB["attachments"].items():
            if attachment.get("external_id") == external_id:
                DB["attachments"][attachment_id].update(data)
                DB["attachments"][attachment_id]["external_id"] = external_id
                return DB["attachments"][attachment_id]
        return None

    @staticmethod
    def delete_attachment_by_external_id(external_id: str) -> bool:
        """Deletes an attachment by external ID."""
        for attachment_id, attachment in DB["attachments"].items():
            if attachment.get("external_id") == external_id:
                del DB["attachments"][attachment_id]
                return True
        return False

# ---------------------------------------------------------------------------------------
# Awards Classes & Methods
# ---------------------------------------------------------------------------------------
class Awards:
    @staticmethod
    def get(
        filter_state_equals: Optional[List[str]] = None,
        filter_updated_at_from: Optional[str] = None,
        filter_updated_at_to: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Returns a list of awards.

        Args:
            filter_state_equals: Find awards by their state.
            filter_updated_at_from: Return awards updated on or after the specified timestamp.
            filter_updated_at_to: Return awards updated on or before the specified timestamp.

        Returns:
            A list of awards matching the filter criteria.
        """
        results = DB["awards"]["awards"][:]

        if filter_state_equals:
            results = [
                award
                for award in results
                if award.get("state") in filter_state_equals
            ]

        if filter_updated_at_from:
            results = [
                award
                for award in results
                if award.get("updated_at", "") >= filter_updated_at_from
            ]

        if filter_updated_at_to:
            results = [
                award
                for award in results
                if award.get("updated_at", "") <= filter_updated_at_to
            ]

        return results

    @staticmethod
    def get_award_line_items(
        award_id: int,
        filter_is_quoted_equals: Optional[bool] = None,
        filter_line_item_type_equals: Optional[List[str]] = None,
        include: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Returns a list of line items for a specific award.

        Args:
            award_id: Award identifier.
            filter_is_quoted_equals: Return awards line items by their quoted state.
            filter_line_item_type_equals: Return awards line items with specified line item types.
            include: Use the include parameter to request related resources along with the primary resource.

        Returns:
            A list of award line items matching the filter criteria.
        """
        results = [
            item
            for item in DB["awards"]["award_line_items"]
            if item.get("award_id") == award_id
        ]

        if filter_is_quoted_equals is not None:
            results = [
                item
                for item in results
                if item.get("is_quoted") == filter_is_quoted_equals
            ]

        if filter_line_item_type_equals:
            results = [
                item
                for item in results
                if item.get("line_item_type") in filter_line_item_type_equals
            ]

        if include:
            # Simulate include logic
            pass

        return results

    @staticmethod
    def get_award_line_item(
        id: str,
        include: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves the details of an existing award line items. You need to supply the unique award line items identifier.

        Args:
            id: Unique Award Line Items identifier.
            include: Use the include parameter to request related resources along with the primary resource.

        Returns:
            The award line item details, or None if not found.
        """
        for item in DB["awards"]["award_line_items"]:
            if item.get("id") == id:
                if include:
                    #simulate include logic
                    pass
                return item
        return None

# ---------------------------------------------------------------------------------------
# Contracts Classes & Methods
# ---------------------------------------------------------------------------------------
class Contracts:
    @staticmethod
    def get(filter: Optional[Dict] = None, include: Optional[str] = None, page: Optional[Dict] = None) -> List[Dict]:
        """Returns a list of contracts for the specified criteria."""
        contracts = list(DB["contracts"]["contracts"].values())
        if filter:
            contracts = [c for c in contracts if all(c.get(k) == v for k, v in filter.items())]
        if include:
            # simulate include logic
            pass
        if page:
            contracts = contracts[:page.get("size", 50)]
        return contracts

    @staticmethod
    def post(include: Optional[str] = None, body: Optional[Dict] = None) -> Dict:
        """Create a contract with given attributes."""
        if not body or "id" not in body:
            raise ValueError("Body must be provided and contain an 'id'.")
        contract_id = body["id"]
        if include:
            # simulate include logic
            pass
        DB["contracts"]["contracts"][contract_id] = body
        return body

    @staticmethod
    def get_contract_by_id(id: int, include: Optional[str] = None) -> Dict:
        """Retrieves the details of an existing contract."""
        if id not in DB["contracts"]["contracts"]:
            raise KeyError(f"Contract with id {id} not found.")
        if include:
            # simulate include logic
            pass
        return DB["contracts"]["contracts"][id]

    @staticmethod
    def patch_contract_by_id(id: int, include: Optional[str] = None, body: Optional[Dict] = None) -> Dict:
        """Updates the details of an existing contract."""
        if id not in DB["contracts"]["contracts"]:
            raise KeyError(f"Contract with id {id} not found.")
        if not body or body.get("id") != id:
            raise ValueError("Body must contain the correct 'id'.")
        DB["contracts"]["contracts"][id].update(body)
        return DB["contracts"]["contracts"][id]

    @staticmethod
    def delete_contract_by_id(id: int) -> None:
        """Deletes a contract."""
        if id not in DB["contracts"]["contracts"]:
            raise KeyError(f"Contract with id {id} not found.")
        del DB["contracts"]["contracts"][id]

    @staticmethod
    def get_contract_by_external_id(external_id: str, include: Optional[str] = None) -> Dict:
        """Retrieves the details of an existing contract by external ID."""
        for contract in DB["contracts"]["contracts"].values():
            if contract.get("external_id") == external_id:
                return contract
        raise KeyError(f"Contract with external_id {external_id} not found.")

    @staticmethod
    def patch_contract_by_external_id(external_id: str, include: Optional[str] = None, body: Optional[Dict] = None) -> Dict:
        """Updates the details of an existing contract by external ID."""
        contract = None
        for c in DB["contracts"]["contracts"].values():
            if c.get("external_id") == external_id:
                contract = c
                break
        if not contract:
            raise KeyError(f"Contract with external_id {external_id} not found.")
        if not body or body.get("external_id") != external_id:
            raise ValueError("Body must contain the correct 'external_id'.")
        contract.update(body)
        return contract

    @staticmethod
    def delete_contract_by_external_id(external_id: str) -> None:
        """Deletes a contract by external ID."""
        contract_id = None
        for id, contract in DB["contracts"]["contracts"].items():
            if contract.get("external_id") == external_id:
                contract_id = id
                break
        if contract_id is None:
            raise KeyError(f"Contract with external_id {external_id} not found.")
        del DB["contracts"]["contracts"][contract_id]

    @staticmethod
    def get_contracts_description() -> List[str]:
        """Returns a list of fields for the contract object."""
        if DB["contracts"]["contracts"]:
            return list(DB["contracts"]["contracts"][list(DB["contracts"]["contracts"].keys())[0]].keys())
        return []

    @staticmethod
    def get_contract_types() -> List[Dict]:
        """Returns a list of all contract types."""
        return list(DB["contracts"]["contract_types"].values())

    @staticmethod
    def post_contract_types(body: Optional[Dict] = None) -> Dict:
        """Create a contract type with given parameters."""
        if not body or "id" not in body:
            raise ValueError("Body must be provided and contain an 'id'.")
        contract_type_id = body["id"]
        DB["contracts"]["contract_types"][contract_type_id] = body
        return body

    @staticmethod
    def get_contract_type_by_id(id: int) -> Dict:
        """Retrieves the details of an existing contract type."""
        if id not in DB["contracts"]["contract_types"]:
            raise KeyError(f"Contract type with id {id} not found.")
        return DB["contracts"]["contract_types"][id]

    @staticmethod
    def patch_contract_type_by_id(id: int, body: Optional[Dict] = None) -> Dict:
        """Updates the details of an existing contract type."""
        if id not in DB["contracts"]["contract_types"]:
            raise KeyError(f"Contract type with id {id} not found.")
        if not body or body.get("id") != id:
            raise ValueError("Body must contain the correct 'id'.")
        DB["contracts"]["contract_types"][id].update(body)
        return DB["contracts"]["contract_types"][id]

    @staticmethod
    def delete_contract_type_by_id(id: int) -> None:
        """Deletes a contract type."""
        if id not in DB["contracts"]["contract_types"]:
            raise KeyError(f"Contract type with id {id} not found.")
        del DB["contracts"]["contract_types"][id]

    @staticmethod
    def get_contract_type_by_external_id(external_id: str) -> Dict:
        """Retrieves the details of an existing contract type by external ID."""
        for contract_type in DB["contracts"]["contract_types"].values():
            if contract_type.get("external_id") == external_id:
                return contract_type
        raise KeyError(f"Contract type with external_id {external_id} not found.")

    @staticmethod
    def patch_contract_type_by_external_id(external_id: str, body: Optional[Dict] = None) -> Dict:
        """Updates the details of an existing contract type by external ID."""
        contract_type = None
        for c in DB["contracts"]["contract_types"].values():
            if c.get("external_id") == external_id:
                contract_type = c
                break
        if not contract_type:
            raise KeyError(f"Contract type with external_id {external_id} not found.")
        if not body or body.get("external_id") != external_id:
            raise ValueError("Body must contain the correct 'external_id'.")
        contract_type.update(body)
        return contract_type

    @staticmethod
    def delete_contract_type_by_external_id(external_id: str) -> None:
        """Deletes a contract type by external ID."""
        contract_type_id = None
        for id, contract_type in DB["contracts"]["contract_types"].items():
            if contract_type.get("external_id") == external_id:
                contract_type_id = id
                break
        if contract_type_id is None:
            raise KeyError(f"Contract type with external_id {external_id} not found.")
        del DB["contracts"]["contract_types"][contract_type_id]

class ContractAward:
    @staticmethod
    def list_awards():
        """Returns a list of all awards."""
        return list(DB["contracts"]["awards"].values())

    @staticmethod
    def get_award(id: int):
        """Retrieves the details of an existing award."""
        if id not in DB["contracts"]["awards"]:
            raise KeyError(f"Award with id {id} not found.")
        return DB["contracts"]["awards"][id]

    @staticmethod
    def list_contract_award_line_items(award_id: int):
        """Returns a list of all award line items for a given award."""
        return [item for item in DB["contracts"]["award_line_items"] if item.get("award_id") == award_id]

    @staticmethod
    def get_contract_award_line_item(id: str):
        """Retrieves the details of an existing award line item."""
        for item in DB["contracts"]["award_line_items"]:
            if item.get("id") == id:
                return item
        raise KeyError(f"Award line item with id {id} not found.")

# ---------------------------------------------------------------------------------------
# Events Classes & Methods
# ---------------------------------------------------------------------------------------

class EventTemplates:
    @staticmethod
    def get():
        """Returns a list of all event templates."""
        return list(DB["events"]["event_templates"].values())

    @staticmethod
    def get_by_id(id: int):
        """Retrieves the details of an existing event template."""
        return DB["events"]["event_templates"].get(id, None)

class Events:
    @staticmethod
    def get(filter: dict = None, page: dict = None):
        """Returns a list of events for the specified criteria."""
        events = list(DB["events"]["events"].values())
        if filter:
            filtered_events = []
            for event in events:
                match = True
                for key, value in filter.items():
                    if key not in event or event[key] != value:
                        match = False
                        break
                if match:
                    filtered_events.append(event)
            events = filtered_events

        if page and 'size' in page:
            size = page['size']
            events = events[:size]

        return events

    @staticmethod
    def post(data: dict):
        """Events can only be created from a template. When a creation request is issued, the base event object will be created from the template and returned with the response. Child records such as attachments, price sheets and custom values, will be scheduled for copy asynchronously. Current duplication status can be retrieved from the duplication_state attribute, which will have one of following values:
        * scheduled - duplication is scheduled, but not yet started;
        * started - duplication started, but not yet finished;
        * finished - duplication completed;
        * failed - there was an error duplicating relationships.
        An event should always have an associated project. Please make sure to specify it as a relationship object.
        A new event will automatically inherit its spend category from the event template.
        Please note, this endpoint does not support auction creation/duplication."""
        new_id = max(DB["events"]["events"].keys(), default=0) + 1
        new_event = {
            "id": new_id,
            "duplication_state": "scheduled",
            **data
        }
        DB["events"]["events"][new_id] = new_event
        return new_event

    @staticmethod
    def get_by_id(id: int):
        """Retrieves the details of an existing event. You need to supply the unique event identifier that was returned upon event creation."""
        if id in DB["events"]["events"]:
            return DB["events"]["events"][id]
        else:
            return None

    @staticmethod
    def patch(id: int, data: dict):
        """Updates the details of an existing event. You need to supply the unique identifier that was returned upon event creation. Please note, that request body must include an id attribute with the value of your event unique identifier (the same one you passed in the URL)."""
        if id in DB["events"]["events"] and data.get("id") == id:
            DB["events"]["events"][id].update(data)
            return DB["events"]["events"][id]
        else:
            return None

    @staticmethod
    def delete(id: int):
        """Deletes an event. You need to supply the unique event identifier that was returned upon event creation."""
        if id in DB["events"]["events"]:
            del DB["events"]["events"][id]
            return True
        else:
            return False

class EventWorksheets:
    @staticmethod
    def get(event_id: int):
        """Returns a list of all worksheets."""
        worksheets = []
        for id, worksheet in DB["events"]["worksheets"].items():
            if worksheet["event_id"] == event_id:
                worksheets.append(worksheet)
        return worksheets

class EventWorksheetById:
    @staticmethod
    def get(event_id: int, id: int):
        """Retrieves the details of an existing worksheet. You need to supply the unique worksheet identifier that was returned upon worksheet creation."""
        if id in DB["events"]["worksheets"] and DB["events"]["worksheets"][id]["event_id"] == event_id:
            return DB["events"]["worksheets"][id]
        else:
            return None


class EventWorksheetLineItems:
    @staticmethod
    def get(event_id: int, worksheet_id: int):
        """Returns a list of line items for the specified criteria."""
        line_items = []
        for id, line_item in DB["events"]["line_items"].items():
            if line_item["event_id"] == event_id and line_item["worksheet_id"] == worksheet_id:
                line_items.append(line_item)
        return line_items

    @staticmethod
    def post(event_id: int, worksheet_id: int, data: dict):
        """Create a line item with given cell values."""
        new_id = max(DB["events"]["line_items"].keys(), default=0) + 1
        new_line_item = {
            "id": new_id,
            "event_id": event_id,
            "worksheet_id": worksheet_id,
            **data
        }
        DB["events"]["line_items"][new_id] = new_line_item
        return new_line_item

    @staticmethod
    def post_multiple(event_id: int, worksheet_id: int, data: list):
        """Create multiple line items in a given worksheet. You can create up to 200 line items in a single request."""
        created_items = []
        for item_data in data:
            new_id = max(DB["events"]["line_items"].keys(), default=0) + 1
            new_line_item = {
                "id": new_id,
                "event_id": event_id,
                "worksheet_id": worksheet_id,
                **item_data
            }
            DB["events"]["line_items"][new_id] = new_line_item
            created_items.append(new_line_item)
        return created_items

class EventWorksheetLineItemById:
    @staticmethod
    def get(event_id: int, worksheet_id: int, id: int):
        """Retrieves the details of an existing line item. You need to supply the unique line item identifier that was returned upon line item creation."""
        if id in DB["events"]["line_items"] and DB["events"]["line_items"][id]["event_id"] == event_id and DB["events"]["line_items"][id]["worksheet_id"] == worksheet_id:
            return DB["events"]["line_items"][id]
        else:
            return None

    @staticmethod
    def patch(event_id: int, worksheet_id: int, id: int, data: dict):
        """Updates the details of an existing line item. You need to supply the unique line item that was returned upon line item creation. Please note, that request body must include the id attribute with the value of your line item unique identifier (the same one you passed in the URL)."""
        if id in DB["events"]["line_items"] and DB["events"]["line_items"][id]["event_id"] == event_id and DB["events"]["line_items"][id]["worksheet_id"] == worksheet_id and data.get("id") == id:
            DB["events"]["line_items"][id].update(data)
            return DB["events"]["line_items"][id]
        else:
            return None

    @staticmethod
    def delete(event_id: int, worksheet_id: int, id: int):
        """Deletes a line item. You need to supply the unique line item identifier that was returned upon line item creation."""
        if id in DB["events"]["line_items"] and DB["events"]["line_items"][id]["event_id"] == event_id and DB["events"]["line_items"][id]["worksheet_id"] == worksheet_id:
            del DB["events"]["line_items"][id]
            return True
        else:
            return False

class EventSupplierCompanies:
    @staticmethod
    def post(event_id: int, data: dict):
        """Add suppliers to an event. Only events of type RFP are supported. The operation will be rolled back upon any failure, and invitations won't be sent. For best performance, we recommend inviting 10 or less suppliers in a single request."""
        if event_id not in DB["events"]["events"]:
            return None
        event = DB["events"]["events"][event_id]
        if event.get("type") != "RFP":
            return None
        if "suppliers" not in event:
            event["suppliers"] = []
        event["suppliers"].extend(data.get("supplier_ids", []))
        return event

    @staticmethod
    def delete(event_id: int, data: dict):
        """Remove suppliers from an event. Only events of type RFP are supported. The operation will be rolled back upon any failure, and invitations won't be removed. For best performance, we recommend removing 10 or less suppliers in a single request."""
        if event_id not in DB["events"]["events"]:
            return None
        event = DB["events"]["events"][event_id]
        if event.get("type") != "RFP":
            return None
        if "suppliers" in event:
            for supplier_id in data.get("supplier_ids", []):
                if supplier_id in event["suppliers"]:
                    event["suppliers"].remove(supplier_id)
            return event
        return None

class EventSupplierCompaniesExternalId:
    @staticmethod
    def post(event_external_id: str, data: dict):
        """Add suppliers to an event. Only events of type RFP are supported. You must supply the unique event external identifier (the one you used when created the event). You must supply the external identifiers of the supplier companies too. The operation will be rolled back upon any failure, and invitations won't be sent. For best performance, we recommend inviting 10 or less suppliers in a single request."""
        event = next((event for event in DB["events"]["events"].values() if event.get("external_id") == event_external_id), None)
        if not event or event.get("type") != "RFP":
            return None

        if "suppliers" not in event:
            event["suppliers"] = []
        event["suppliers"].extend(data.get("supplier_external_ids", []))
        return event

    @staticmethod
    def delete(event_external_id: str, data: dict):
        """Remove suppliers from an event. Only events of type RFP are supported. You must supply the unique event external identifier (the one you used when created the event). You must supply the external identifiers of the supplier companies too. The operation will be rolled back upon any failure, and invitations won't be removed. For best performance, we recommend removing 10 or less suppliers in a single request."""
        event = next((event for event in DB["events"]["events"].values() if event.get("external_id") == event_external_id), None)
        if not event or event.get("type") != "RFP":
            return None

        if "suppliers" in event:
            for supplier_external_id in data.get("supplier_external_ids", []):
                if supplier_external_id in event["suppliers"]:
                    event["suppliers"].remove(supplier_external_id)
            return event
        return None

class EventSupplierContacts:
    @staticmethod
    def post(event_id: int, data: dict):
        """Add suppliers to an event using supplier contacts. Only events of type RFP are supported. For best performance, we recommend inviting 10 or less supplier contacts in a single request."""
        if event_id not in DB["events"]["events"]:
            return None
        event = DB["events"]["events"][event_id]
        if event.get("type") != "RFP":
            return None
        if "supplier_contacts" not in event:
            event["supplier_contacts"] = []
        event["supplier_contacts"].extend(data.get("supplier_contact_ids", []))
        return event

    @staticmethod
    def delete(event_id: int, data: dict):
        """Remove suppliers from an event using supplier contacts. Only events of type RFP are supported. For best performance, we recommend removing 10 or less supplier contacts in a single request."""
        if event_id not in DB["events"]["events"]:
            return None
        event = DB["events"]["events"][event_id]
        if event.get("type") != "RFP":
            return None
        if "supplier_contacts" in event:
            for supplier_contact_id in data.get("supplier_contact_ids", []):
                if supplier_contact_id in event["supplier_contacts"]:
                    event["supplier_contacts"].remove(supplier_contact_id)
            return event
        return None

class EventSupplierContactsExternalId:
    @staticmethod
    def post(event_external_id: str, data: dict):
        """Add suppliers to an event using supplier contacts. Only events of type RFP are supported. You must supply the unique event external identifier (the one you used when created the event). You must supply the external identifiers of the supplier contacts too. The operation will be rolled back upon any failure, and invitations won't be sent. For best performance, we recommend inviting 10 or less supplier contacts in a single request."""
        event = next((event for event in DB["events"]["events"].values() if event.get("external_id") == event_external_id), None)
        if not event or event.get("type") != "RFP":
            return None

        if "supplier_contacts" not in event:
            event["supplier_contacts"] = []
        event["supplier_contacts"].extend(data.get("supplier_contact_external_ids", []))
        return event

    @staticmethod
    def delete(event_external_id: str, data: dict):
        """Remove suppliers from an event using supplier contacts. Only events of type RFP are supported. You must supply the unique event external identifier (the one you used when created the event). You must supply the external identifiers of the supplier contacts too. The operation will be rolled back upon any failure, and invitations won't be removed. For best performance, we recommend removing 10 or less supplier contacts in a single request."""
        event = next((event for event in DB["events"]["events"].values() if event.get("external_id") == event_external_id), None)
        if not event or event.get("type") != "RFP":
            return None

        if "supplier_contacts" in event:
            for supplier_contact_external_id in data.get("supplier_contact_external_ids", []):
                if supplier_contact_external_id in event["supplier_contacts"]:
                    event["supplier_contacts"].remove(supplier_contact_external_id)
            return event
        return None

class EventBids:
    @staticmethod
    def get(event_id: int, filter: dict = None, include: str = None, page: dict = None):
        """Returns a list of all bids. Only bids for events of type RFP are returned."""
        if event_id not in DB["events"]["events"] or DB["events"]["events"][event_id].get("type") != "RFP":
            return []
        bids = [bid for bid in DB["events"]["bids"].values() if bid.get("event_id") == event_id]

        if filter:
            filtered_bids = []
            for bid in bids:
                match = True
                for key, value in filter.items():
                    if key not in bid or bid[key] != value:
                        match = False
                        break
                if match:
                    filtered_bids.append(bid)
            bids = filtered_bids

        if page and 'size' in page:
            size = page['size']
            bids = bids[:size]

        return bids

class BidsById:
    @staticmethod
    def get(id: int, include: str = None):
        """Retrieves the details of an existing bid. You need to supply the unique bid identifier that was returned upon bid creation."""
        if id in DB["events"]["bids"]:
            return DB["events"]["bids"][id]
        else:
            return None

class BidsDescribe:
    @staticmethod
    def get():
        """Returns a list of fields for the bid object."""
        return list(DB['events']['bids'][list(DB["events"]["bids"].keys())[0]].keys())

class BidLineItems:
    @staticmethod
    def get(bid_id: int):
        """Returns a list of line items for a specific bid."""
        return [item for item in DB["events"]["bid_line_items"].values() if item.get("bid_id") == bid_id]

class BidLineItemById:
    @staticmethod
    def get(id: int):
        """Retrieves the details of an existing bid line item."""
        if id in DB["events"]["bid_line_items"]:
            return DB["events"]["bid_line_items"][id]
        else:
            return None

class BidLineItemsList:
    @staticmethod
    def get(filter: dict = None):
        """Returns a list of all bid line items."""
        items = list(DB["events"]["bid_line_items"].values())
        if filter:
            filtered_items = []
            for item in items:
                match = True
                for key, value in filter.items():
                    if key not in item or item[key] != value:
                        match = False
                        break
                if match:
                    filtered_items.append(item)
            items = filtered_items
        return items

class BidLineItemsDescribe:
    @staticmethod
    def get():
        """Returns a list of fields for bid line item object."""
        return list(DB['events']['bid_line_items'][list(DB['events']['bid_line_items'].keys())[0]].keys())

# ---------------------------------------------------------------------------------------
# Fields Classes & Methods
# ---------------------------------------------------------------------------------------
class Fields:
    @staticmethod
    def get(filter: dict = None):
        """Returns a list of custom fields for the specified criteria."""
        if filter is None:
            return list(DB["fields"]["fields"].values())
        else:
            filtered_fields = []
            for field in DB["fields"]["fields"].values():
                match = True
                for key, value in filter.items():
                    if key not in field or field[key] != value:
                        match = False
                        break
                if match:
                    filtered_fields.append(field)
            return filtered_fields

    @staticmethod
    def post(new_id:str, options: dict):
        """Create a field with given parameters."""
        if new_id not in DB["fields"]["fields"].keys():
            DB["fields"]["fields"][new_id] = options
            return options
        else:
            return None

class FieldById:
    @staticmethod
    def get(id: str):
        """Retrieves the details of an existing field."""
        if id in DB["fields"]["fields"]:
            return DB["fields"]["fields"][id]
        else:
            return None

    @staticmethod
    def patch(id: str, options: dict):
        """Updates the details of an existing field."""
        if id in DB["fields"]["fields"]:
            DB["fields"]["fields"][id] = options
            return options
        else:
            return None

    @staticmethod
    def delete(id: int):
        """Deletes a field."""
        if id in DB["fields"]["fields"]:
            del DB["fields"]["fields"][id]
            return True
        else:
            return False

class FieldOptionsByFieldId:
    @staticmethod
    def get(field_id: int):
        """Returns a list of field options for the specified field."""
        field_options_list = []
        for option_id, option in DB["fields"]["field_options"].items():
            if option.get("field_id") == field_id:
                field_options_list.append(option)
        return field_options_list

class FieldOptions:
    @staticmethod
    def post(new_id:str, options: list):
        """Create a field options with given parameters."""
        if new_id not in DB["fields"]["field_options"]:
            new_field_option = {"field_id": new_id, "options": options}
            DB["fields"]["field_options"][new_id] = new_field_option
            return new_field_option
        else:
            return None

class FieldOptionById:
    @staticmethod
    def patch(id: str, new_options: list):
        """Update a field options with given parameters."""
        if id in DB["fields"]["field_options"]:
            DB["fields"]["field_options"][id]["options"] = new_options
            return DB["fields"]["field_options"][id]
        else:
            return None

    @staticmethod
    def delete(id: int):
        """Deletes a field option."""
        if id in DB["fields"]["field_options"]:
            del DB["fields"]["field_options"][id]
            return True
        else:
            return False

class FieldGroups:
    @staticmethod
    def get():
        """Returns a list of field groups."""
        return list(DB["fields"]["field_groups"].values())

    @staticmethod
    def post(name: str, description: str = ""):
        """Create a field group with given parameters."""
        new_id = str(max(map(int, DB["fields"]["field_groups"].keys()), default=0) + 1)
        new_field_group = {"id": new_id, "name": name, "description": description}
        DB["fields"]["field_groups"][new_id] = new_field_group
        return new_field_group
        DB["fields"]["field_groups"][new_id] = new_field_group
        return new_field_group

class FieldGroupById:
    @staticmethod
    def get(id: int):
        """Retrieves the details of an existing field group."""
        if id in DB["fields"]["field_groups"]:
            return DB["fields"]["field_groups"][id]
        else:
            return None

    @staticmethod
    def patch(id: str, options: dict):
        """Updates the details of an existing field group."""
        if id in DB["fields"]["field_groups"]:
            DB["fields"]["field_groups"][id] = options
            return options
        else:
            return None

    @staticmethod
    def delete(id: int):
        """Deletes a field group."""
        if id in DB["fields"]["field_groups"]:
            del DB["fields"]["field_groups"][id]
            return True
        else:
            return False

# ---------------------------------------------------------------------------------------
# Payments Classes & Methods
# ---------------------------------------------------------------------------------------
class PaymentTerms:
    @staticmethod
    def get():
        """Returns a list of payment terms."""
        return DB["payments"]["payment_terms"]

    @staticmethod
    def post(name: str, external_id: str = None):
        """Create a payment term with given parameters."""
        new_term = {
            "id": DB["payments"]["payment_term_id_counter"],
            "name": name,
            "external_id": external_id,
        }
        DB["payments"]["payment_terms"].append(new_term)
        DB["payments"]["payment_term_id_counter"] += 1
        return new_term

class PaymentTermsId:
    @staticmethod
    def patch(id: int, name: str, external_id: str = None):
        """Updates the details of an existing payment term."""
        for term in DB["payments"]["payment_terms"]:
            if term["id"] == id:
                term["name"] = name
                term["external_id"] = external_id
                return term
        return None

    @staticmethod
    def delete(id: int):
        """Deletes a payment term."""
        DB["payments"]["payment_terms"] = [term for term in DB["payments"]["payment_terms"] if term["id"] != id]
        return True

class PaymentTermsExternalId:
    @staticmethod
    def patch(external_id: str, name: str):
        """Updates the details of an existing payment term by external ID."""
        for term in DB["payments"]["payment_terms"]:
            if term.get("external_id") == external_id:
                term["name"] = name
                return term
        return None

    @staticmethod
    def delete(external_id: str):
        """Deletes a payment term by external ID."""
        DB["payments"]["payment_terms"] = [
            term for term in DB["payments"]["payment_terms"] if term.get("external_id") != external_id
        ]
        return True

class PaymentTypes:
    @staticmethod
    def get():
        """Returns a list of payment types."""
        return DB["payments"]["payment_types"]

    @staticmethod
    def post(name: str, payment_method: str, external_id: str = None):
        """Create a payment type with given parameters."""
        new_type = {
            "id": DB["payments"]["payment_type_id_counter"],
            "name": name,
            "external_id": external_id,
            "payment_method": payment_method,
        }
        DB["payments"]["payment_types"].append(new_type)
        DB["payments"]["payment_type_id_counter"] += 1
        return new_type

class PaymentTypesId:
    @staticmethod
    def patch(id: int, name: str, payment_method: str = None, external_id: str = None):
        """Updates the details of an existing payment type."""
        for type_ in DB["payments"]["payment_types"]:
            if type_["id"] == id:
                type_["name"] = name
                if external_id is not None:
                    type_["external_id"] = external_id
                if payment_method is not None:
                    type_["payment_method"] = payment_method
                return type_
        return None

    @staticmethod
    def delete(id: int):
        """Deletes a payment type."""
        DB["payments"]["payment_types"] = [type_ for type_ in DB["payments"]["payment_types"] if type_["id"] != id]
        return True

class PaymentTypesExternalId:
    @staticmethod
    def patch(external_id: str, name: str, payment_method: str = None):
        """Updates the details of an existing payment type by external ID."""
        for type_ in DB["payments"]["payment_types"]:
            if type_.get("external_id") == external_id:
                type_["name"] = name
                if payment_method is not None:
                    type_["payment_method"] = payment_method
                return type_
        return None

    @staticmethod
    def delete(external_id: str):
        """Deletes a payment type by external ID."""
        DB["payments"]["payment_types"] = [
            type_ for type_ in DB["payments"]["payment_types"] if type_.get("external_id") != external_id
        ]
        return True

class PaymentCurrencies:
    @staticmethod
    def get():
        """Returns a list of payment currencies."""
        return DB["payments"]["payment_currencies"]

    @staticmethod
    def post(alpha: str, numeric: str, external_id: str = None):
        """Create a payment currency with given parameters."""
        new_currency = {
            "id": DB["payments"]["payment_currency_id_counter"],
            "alpha": alpha,
            "numeric": numeric,
            "external_id": external_id,
        }
        DB["payments"]["payment_currencies"].append(new_currency)
        DB["payments"]["payment_currency_id_counter"] += 1
        return new_currency

class PaymentCurrenciesId:
    @staticmethod
    def patch(id: int, alpha: str, numeric: str, external_id: str = None):
        """Updates the details of an existing payment currency."""
        for currency in DB["payments"]["payment_currencies"]:
            if currency["id"] == id:
                currency["alpha"] = alpha
                currency["numeric"] = numeric
                currency["external_id"] = external_id
                return currency
        return None

    @staticmethod
    def delete(id: int):
        """Deletes a payment currency."""
        DB["payments"]["payment_currencies"] = [
            currency for currency in DB["payments"]["payment_currencies"] if currency["id"] != id
        ]
        return True

class PaymentCurrenciesExternalId:
    @staticmethod
    def patch(external_id: str, alpha: str, numeric: str):
        """Updates the details of an existing payment currency by external ID."""
        for currency in DB["payments"]["payment_currencies"]:
            if currency.get("external_id") == external_id:
                currency["alpha"] = alpha
                currency["numeric"] = numeric
                return currency
        return None

    @staticmethod
    def delete(external_id: str):
        """Deletes a payment currency by external ID."""
        DB["payments"]["payment_currencies"] = [
            currency for currency in DB["payments"]["payment_currencies"] if currency.get("external_id") != external_id
        ]
        return True

# ---------------------------------------------------------------------------------------
# Projects Classes & Methods
# ---------------------------------------------------------------------------------------
class Projects:
    def get(self, filter: dict = None, page: dict = None):
        """Returns a list of projects for the specified criteria."""
        projects = list(DB["projects"]["projects"].values())
        if filter:
            filtered_projects = []
            for project in projects:
                match = True
                for key, value in filter.items():
                    if project.get(key) != value:
                        match = False
                        break
                if match:
                    filtered_projects.append(project)
            projects = filtered_projects
        if page and "size" in page:
            size = page["size"]
            return projects[:size]
        return projects

    def post(self, project_data: dict):
        """Create a project with given attributes."""
        if "id" not in project_data:
            project_id = len(DB["projects"]["projects"]) + 1
            project_data["id"] = project_id
        DB["projects"]["projects"][project_data["id"]] = project_data
        return project_data


class ProjectById:
    def get(self, id: int):
        """Retrieves the details of an existing project. You need to supply the unique project identifier that was returned upon project creation."""
        return DB["projects"]["projects"].get(id)

    def patch(self, id: int, project_data: dict):
        """Updates the details of an existing project. You need to supply the unique supplier project that was returned upon project creation. Please note, that request body must include an id attribute with the value of your project unique identifier (the same one you passed in the URL)."""
        if id != project_data.get("id"):
            return None
        if id in DB["projects"]["projects"]:
            DB["projects"]["projects"][id].update(project_data)
            return DB["projects"]["projects"][id]
        return None

    def delete(self, id: int):
        """Deletes a project. You need to supply the unique project identifier that was returned upon project creation."""
        if id in DB["projects"]["projects"]:
            del DB["projects"]["projects"][id]
            return True
        return False


class ProjectByExternalId:
    def get(self, external_id: str):
        """Retrieves the details of an existing project. You need to supply the unique project external identifier (the one you used when created the project)."""
        for project in DB["projects"]["projects"].values():
            if project.get("external_id") == external_id:
                return project
        return None

    def patch(self, external_id: str, project_data: dict):
        """Updates the details of an existing project. You need to supply the unique project external identifier (the one you used when created the project). Please note, that request body must include an id attribute with the value of your project external identifier (the same one you passed in the URL)."""
        if external_id != project_data.get("external_id"):
            return None
        for id, project in DB["projects"]["projects"].items():
            if project.get("external_id") == external_id:
                DB["projects"]["projects"][id].update(project_data)
                return DB["projects"]["projects"][id]
        return None

    def delete(self, external_id: str):
        """Deletes a project. You need to supply the unique project external identifier (the one you used when created the project)."""
        for id, project in DB["projects"]["projects"].items():
            if project.get("external_id") == external_id:
                del DB["projects"]["projects"][id]
                return True
        return False


class ProjectsDescribe:
    def get(self):
        """Returns a list of fields for the project object."""
        if DB["projects"]["projects"]:
            example_project = next(iter(DB["projects"]["projects"].values()))
            return list(example_project.keys())
        return []


class ProjectRelationshipsSupplierCompanies:
    def post(self, project_id: int, supplier_ids: list):
        """Add suppliers to a project. For best performance, we recommend inviting 10 or less suppliers in a single request."""
        if project_id in DB["projects"]["projects"]:
            if "supplier_companies" not in DB["projects"]["projects"][project_id]:
                DB["projects"]["projects"][project_id]["supplier_companies"] = []
            DB["projects"]["projects"][project_id]["supplier_companies"].extend(supplier_ids)
            return True
        return False

    def delete(self, project_id: int, supplier_ids: list):
        """Remove suppliers from a project. For best performance, we recommend removing 10 or less suppliers in a single request."""
        if project_id in DB["projects"]["projects"] and "supplier_companies" in DB["projects"]["projects"][project_id]:
            DB["projects"]["projects"][project_id]["supplier_companies"] = [
                sid for sid in DB["projects"]["projects"][project_id]["supplier_companies"] if sid not in supplier_ids
            ]
            return True
        return False


class ProjectRelationshipsSupplierCompaniesExternalId:
    def post(self, project_external_id: str, supplier_external_ids: list):
        """Add suppliers to a project. You must supply the unique project external identifier (the one you used when created the project). You must supply the external identifiers of the supplier companies too. For best performance, we recommend inviting 10 or less suppliers in a single request."""
        for id, project in DB["projects"]["projects"].items():
            if project.get("external_id") == project_external_id:
                if "supplier_companies" not in DB["projects"]["projects"][id]:
                    DB["projects"]["projects"][id]["supplier_companies"] = []
                DB["projects"]["projects"][id]["supplier_companies"].extend(supplier_external_ids)
                return True
        return False

    def delete(self, project_external_id: str, supplier_external_ids: list):
        """Remove suppliers from a project. You must supply the unique project external identifier (the one you used when created the project). You must supply the external identifiers of the supplier companies too. For best performance, we recommend removing 10 or less suppliers in a single request."""
        for id, project in DB["projects"]["projects"].items():
            if project.get("external_id") == project_external_id and "supplier_companies" in DB["projects"]["projects"][id]:
                DB["projects"]["projects"][id]["supplier_companies"] = [
                    sid for sid in DB["projects"]["projects"][id]["supplier_companies"] if sid not in supplier_external_ids
                ]
                return True
        return False

class ProjectRelationshipsSupplierContacts:
    def post(self, project_id: int, supplier_contact_ids: list):
        """Add suppliers to a project using supplier contacts. For best performance, we recommend inviting 10 or less supplier contacts in a single request."""
        if project_id in DB["projects"]["projects"]:
            if "supplier_contacts" not in DB["projects"]["projects"][project_id]:
                DB["projects"]["projects"][project_id]["supplier_contacts"] = []
            DB["projects"]["projects"][project_id]["supplier_contacts"].extend(supplier_contact_ids)
            return True
        return False

    def delete(self, project_id: int, supplier_contact_ids: list):
        """Remove suppliers from a project using supplier contacts. For best performance, we recommend removing 10 or less supplier contacts in a single request."""
        if project_id in DB["projects"]["projects"] and "supplier_contacts" in DB["projects"]["projects"][project_id]:
            DB["projects"]["projects"][project_id]["supplier_contacts"] = [
                sid for sid in DB["projects"]["projects"][project_id]["supplier_contacts"] if sid not in supplier_contact_ids
            ]
            return True
        return False


class ProjectRelationshipsSupplierContactsExternalId:
    def post(self, project_external_id: str, supplier_contact_external_ids: list):
        """Add suppliers to a project using supplier contacts. You must supply the unique project external identifier (the one you used when created the project). You must supply the external identifiers of the supplier contacts too. For best performance, we recommend inviting 10 or less supplier contacts in a single request."""
        for id, project in DB["projects"]["projects"].items():
            if project.get("external_id") == project_external_id:
                if "supplier_contacts" not in DB["projects"]["projects"][id]:
                    DB["projects"]["projects"][id]["supplier_contacts"] = []
                DB["projects"]["projects"][id]["supplier_contacts"].extend(supplier_contact_external_ids)
                return True
        return False

    def delete(self, project_external_id: str, supplier_contact_external_ids: list):
        """Remove suppliers from a project using supplier contacts. You must supply the unique project external identifier (the one you used when created the project). You must supply the external identifiers of the supplier contacts too. For best performance, we recommend removing 10 or less supplier contacts in a single request."""
        for id, project in DB["projects"]["projects"].items():
            if project.get("external_id") == project_external_id and "supplier_contacts" in DB["projects"]["projects"][id]:
                DB["projects"]["projects"][id]["supplier_contacts"] = [
                    sid
                    for sid in DB["projects"]["projects"][id]["supplier_contacts"]
                    if sid not in supplier_contact_external_ids
                ]
                return True
        return False


class ProjectTypes:
    def get(self):
        """Returns a list of all project types."""
        return list(DB["projects"]["project_types"].values())


class ProjectTypeById:
    def get(self, id: int):
        """Retrieves the details of an existing project type."""
        return DB["projects"]["project_types"].get(id)

# ---------------------------------------------------------------------------------------
# Reports Classes & Methods
# ---------------------------------------------------------------------------------------
class ContractMilestoneReports:
    @staticmethod
    def get_entries():
        """Returns a list of milestone report entries."""
        return DB["reports"].get('contract_milestone_reports_entries', [])

    @staticmethod
    def get_schema():
        """Returns the contract milestone report schema."""
        return DB["reports"].get('contract_milestone_reports_schema', {})

class ContractReports:
    @staticmethod
    def get_entries():
        """Returns a list of contract report entries."""
        return DB["reports"].get('contract_reports_entries', [])

    @staticmethod
    def get_schema():
        """Returns the contract report schema."""
        return DB["reports"].get('contract_reports_schema', {})

class EventReports:
    @staticmethod
    def get_entries():
        """Returns a list of event report entries."""
        return DB["reports"].get('event_reports_entries', [])

    @staticmethod
    def get_event_report_entries(event_report_id: int):
        """Returns a list of event report entries."""
        return DB["reports"].get(f'event_reports_{event_report_id}_entries', [])

    @staticmethod
    def get_reports():
        """Returns a list of reports owned by the user."""
        return DB["reports"].get('event_reports', [])

    @staticmethod
    def get_schema():
        """Returns the event report schema."""
        return DB["reports"].get('event_reports_schema', {})

class PerformanceReviewAnswerReports:
    @staticmethod
    def get_entries():
        """Returns a list of performance review answer entries."""
        return DB["reports"].get('performance_review_answer_reports_entries', [])

    @staticmethod
    def get_schema():
        """Returns the performance review answer report schema."""
        return DB["reports"].get('performance_review_answer_reports_schema', {})

class PerformanceReviewReports:
    @staticmethod
    def get_entries():
        """Returns a list of peformance review entries."""
        return DB["reports"].get('performance_review_reports_entries', [])

    @staticmethod
    def get_schema():
        """Returns the performance review report schema."""
        return DB["reports"].get('performance_review_reports_schema', {})

class ProjectMilestoneReports:
    @staticmethod
    def get_entries():
        """Returns a list of project milestone entries."""
        return DB["reports"].get('project_milestone_reports_entries', [])

    @staticmethod
    def get_schema():
        """Returns the project milestone report schema."""
        return DB["reports"].get('project_milestone_reports_schema', {})

class ProjectReports:
    @staticmethod
    def get_project_report_entries(project_report_id: int):
        """Returns a list of project report entries."""
        return DB["reports"].get(f'project_reports_{project_report_id}_entries', [])

    @staticmethod
    def get_entries():
        """Returns a list of project reports owned by the user."""
        return DB["reports"].get('project_reports_entries', [])

    @staticmethod
    def get_schema():
        """Returns the project report schema."""
        return DB["reports"].get('project_reports_schema', {})

class SavingsReports:
    @staticmethod
    def get_entries():
        """Returns a list of savings entries."""
        return DB["reports"].get('savings_reports_entries', [])

    @staticmethod
    def get_schema():
        """Returns the savings report schema."""
        return DB["reports"].get('savings_reports_schema', {})

class SupplierReports:
    @staticmethod
    def get_entries():
        """Returns a list of supplier entries."""
        return DB["reports"].get('supplier_reports_entries', [])

    @staticmethod
    def get_schema():
        """Returns the supplier report schema."""
        return DB["reports"].get('supplier_reports_schema', {})

class SupplierReviewReports:
    @staticmethod
    def get_entries():
        """Returns a list of supplier review entries."""
        return DB["reports"].get('supplier_review_reports_entries', [])

    @staticmethod
    def get_schema():
        """Returns the supplier review report schema."""
        return DB["reports"].get('supplier_review_reports_schema', {})

class Suppliers:
    @staticmethod
    def get_suppliers():
        """Returns a list of all suppliers."""
        return DB["reports"].get('suppliers', [])

    @staticmethod
    def get_supplier(supplier_id: int):
        """Returns a single supplier."""
        suppliers = DB["reports"].get('suppliers', [])
        for supplier in suppliers:
            if supplier.get('id') == supplier_id:
                return supplier
        return None

# ---------------------------------------------------------------------------------------
# SCIM Classes & Methods
# ---------------------------------------------------------------------------------------
class Users:
    @staticmethod
    def get(attributes: Optional[str] = None, filter: Optional[str] = None, startIndex: Optional[int] = None,
            count: Optional[int] = None, sortBy: Optional[str] = None, sortOrder: Optional[str] = None) -> List[Dict]:
        """
        Returns a list of users for the specified criteria. The pagination size is 100 results per request.
        """
        users = DB["scim"]["users"]
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

    @staticmethod
    def post(body: Dict) -> Dict:
        """
        Create a user with given attributes.
        """
        user_id = str(len(DB["scim"]["users"]) + 1)
        body["id"] = user_id
        DB["scim"]["users"].append(body)
        return body


class UserById:
    @staticmethod
    def get(id: str, attributes: Optional[str] = None, filter: Optional[str] = None) -> Optional[Dict]:
        """
        Retrieves a User resource by Id (see section 3.4.1 of RFC 7644).
        """
        for user in DB["scim"]["users"]:
            if user.get("id") == id:
                if attributes:
                    attrs = attributes.split(",")
                    return {attr: user.get(attr) for attr in attrs if attr in user}
                return user
        return None

    @staticmethod
    def patch(id: str, body: Dict) -> Optional[Dict]:
        """
        Updates one or more attributes of a User resource using a sequence of additions, removals, and replacements operations. See section 3.5.2 of RFC 7644.
        """
        for user in DB["scim"]["users"]:
            if user.get("id") == id:
                for operation in body.get("Operations", []):
                    op = operation.get("op")
                    path = operation.get("path")
                    value = operation.get("value")
                    if op == "replace" and path and value:
                        parts = path.split(".")
                        if len(parts) == 1:
                            user[parts[0]] = value
                return user
        return None

    @staticmethod
    def put(id: str, body: Dict) -> Optional[Dict]:
        """
        Updates a User resource (see section 3.5.1 of RFC 7644).
        """
        for i, user in enumerate(DB["scim"]["users"]):
            if user.get("id") == id:
                DB["scim"]["users"][i] = body
                body["id"] = id
                return body
        return None

    @staticmethod
    def delete(id: str) -> bool:
        """
        Deactivates a user.
        """
        for i, user in enumerate(DB["scim"]["users"]):
            if user.get("id") == id:
                del DB["scim"]["users"][i]
                return True
        return False


class Schemas:
    @staticmethod
    def get() -> List[Dict]:
        """
        Endpoint used to retrieve information about schemas supported. See section 3.4 of RFC 7644.
        """
        return DB["scim"]["schemas"]


class SchemaById:
    @staticmethod
    def get(uri: str) -> Optional[Dict]:
        """
        Retrieves information about a specific resource.
        """
        for schema in DB["scim"]["schemas"]:
            if schema.get("uri") == uri:
                return schema
        return None


class ResourceTypes:
    @staticmethod
    def get() -> List[Dict]:
        """
        This endpoint is used to discover the types of resources available (see section 4 of RFC 7644).
        """
        return DB["scim"]["resource_types"]


class ResourceTypeById:
    @staticmethod
    def get(resource: str) -> Optional[Dict]:
        """
        Describes the endpoint, schemas and extensions supported by a specific kind of resource.
        """
        for resource_type in DB["scim"]["resource_types"]:
            if resource_type.get("resource") == resource:
                return resource_type
        return None


class ServiceProviderConfig:
    @staticmethod
    def get() -> Dict:
        """
        Describes the SCIM specification features available (see section 5 of RFC 7643).
        """
        return DB["scim"]["service_provider_config"]

# ---------------------------------------------------------------------------------------
# Spend Categories Classes & Methods
# ---------------------------------------------------------------------------------------
class SpendCategories:
    @staticmethod
    def get():
        """Returns a list of spend categories."""
        return list(DB["spend_categories"].values())

    @staticmethod
    def post(name: str, external_id: str = None, usages: list = None):
        """Create a Spend Category with given parameters."""
        new_id = len(DB["spend_categories"]) + 1
        new_category = {
            "id": new_id,
            "name": name,
            "external_id": external_id,
            "usages": usages,
        }
        DB["spend_categories"][new_id] = new_category
        return new_category

class SpendCategoryById:
    @staticmethod
    def get(id: int):
        """Retrieves the details of an existing Spend Category."""
        return DB["spend_categories"].get(id)

    @staticmethod
    def patch(id: int, name: str = None, external_id: str = None, usages: list = None):
        """Updates the details of an existing Spend Category."""
        if id not in DB["spend_categories"]:
            return None
        category = DB["spend_categories"][id]
        if name is not None:
            category["name"] = name
        if external_id is not None:
            category["external_id"] = external_id
        if usages is not None:
            category["usages"] = usages
        return category

    @staticmethod
    def delete(id: int):
        """Deletes a Spend Category."""
        if id in DB["spend_categories"]:
            del DB["spend_categories"][id]
            return True
        return False

class SpendCategoryByExternalId:
    @staticmethod
    def get(external_id: str):
        """Retrieves the details of an existing Spend Category."""
        for category in DB["spend_categories"].values():
            if category.get("external_id") == external_id:
                return category
        return None

    @staticmethod
    def patch(external_id: str, name: str = None, new_external_id: str = None, usages: list = None):
        """Updates the details of an existing Spend Category."""
        for id, category in DB["spend_categories"].items():
            if category.get("external_id") == external_id:
                if name is not None:
                    category["name"] = name
                if new_external_id is not None:
                    category["external_id"] = new_external_id
                if usages is not None:
                    category["usages"] = usages
                return category
        return None

    @staticmethod
    def delete(external_id: str):
        """Deletes a Spend Category."""
        for id, category in DB["spend_categories"].items():
            if category.get("external_id") == external_id:
                del DB["spend_categories"][id]
                return True
        return False

# ---------------------------------------------------------------------------------------
# Supplier Classes & Methods
# ---------------------------------------------------------------------------------------
class SupplierCompanies:
    @staticmethod
    def get(filter: dict = None, include: str = None, page: dict = None):
        """Returns a list of supplier companies for the specified criteria."""
        companies = list(DB["suppliers"]["supplier_companies"].values())
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

    @staticmethod
    def post(include: str = None, body: dict = None):
        """Create a supplier company with given attributes, relationships, and related complex resources."""
        if not body:
            return {"error": "Body is required"}, 400
        company_id = len(DB["suppliers"]["supplier_companies"]) + 1
        company = {"id": company_id, **body}
        DB["suppliers"]["supplier_companies"][company_id] = company
        if include:
            # Simulate include logic (not fully implemented)
            pass
        return company, 201


class SupplierCompanyById:
    @staticmethod
    def get(id: int, include: str = None):
        """Retrieves the details of an existing supplier company."""
        company = DB["suppliers"]["supplier_companies"].get(id)
        if not company:
            return {"error": "Company not found"}, 404
        if include:
            # Simulate include logic (not fully implemented)
            pass
        return company, 200

    @staticmethod
    def patch(id: int, include: str = None, body: dict = None):
        """Updates the details of an existing supplier company."""
        company = DB["suppliers"]["supplier_companies"].get(id)
        if not company:
            return {"error": "Company not found"}, 404
        if not body:
            return {"error": "Body is required"}, 400
        company.update(body)
        if include:
            # Simulate include logic (not fully implemented)
            pass
        return company, 200

    @staticmethod
    def delete(id: int):
        """Deletes a supplier company."""
        if id not in DB["suppliers"]["supplier_companies"]:
            return {"error": "Company not found"}, 404
        del DB["suppliers"]["supplier_companies"][id]
        return {}, 204


class SupplierCompanyByExternalId:
    @staticmethod
    def get(external_id: str, include: str = None):
        """Retrieves the details of an existing supplier company."""
        for company in DB["suppliers"]["supplier_companies"].values():
            if company.get("external_id") == external_id:
                if include:
                    #simulate include
                    pass
                return company, 200
        return {"error": "Company not found"}, 404

    @staticmethod
    def patch(external_id: str, include: str = None, body: dict = None):
        """Updates the details of an existing supplier company."""
        for company_id, company in DB["suppliers"]["supplier_companies"].items():
            if company.get("external_id") == external_id:
                if not body:
                    return {"error": "Body is required"}, 400
                if body.get("id") != external_id:
                    return {"error": "External id in body must match url"}, 400

                company.update(body)
                if include:
                    #simulate include
                    pass
                return company, 200
        return {"error": "Company not found"}, 404

    @staticmethod
    def delete(external_id: str):
        """Deletes a supplier company."""
        company_id_to_delete = None
        for company_id, company in DB["suppliers"]["supplier_companies"].items():
            if company.get("external_id") == external_id:
                company_id_to_delete = company_id
                break
        if company_id_to_delete is None:
            return {"error": "Company not found"}, 404
        del DB["suppliers"]["supplier_companies"][company_id_to_delete]
        return {}, 204

class SupplierCompanyContacts:
    @staticmethod
    def get(company_id: int, include: str = None, filter: dict = None):
        """Retrieves the list of contacts for an existing supplier company."""
        contacts = [c for c in DB["suppliers"]["supplier_contacts"].values() if c.get("company_id") == company_id]
        if filter:
            filtered_contacts = []
            for contact in contacts:
                match = True
                for key, value in filter.items():
                    if contact.get(key) != value:
                        match = False
                        break
                if match:
                    filtered_contacts.append(contact)
            contacts = filtered_contacts
        if include:
            # Simulate include logic (not fully implemented)
            pass
        return contacts, 200

class SupplierCompaniesDescribe:
    @staticmethod
    def get():
        """Returns a list of fields for the supplier company object."""
        return list(DB["suppliers"]["supplier_companies"][list(DB["suppliers"]["supplier_companies"].keys())[0]].keys()), 200

class SupplierContacts:
    @staticmethod
    def post(include: str = None, body: dict = None):
        """Create a supplier contact with given attributes."""
        if not body:
            return {"error": "Body is required"}, 400
        contact_id = len(DB["suppliers"]["supplier_contacts"]) + 1
        contact = {"id": contact_id, **body}
        DB["suppliers"]["supplier_contacts"][contact_id] = contact
        if include:
            #simulate include
            pass
        return contact, 201

class SupplierContactById:
    @staticmethod
    def get(id: int, include: str = None):
        """Retrieves the details of an existing supplier contact."""
        contact = DB["suppliers"]["supplier_contacts"].get(id)
        if not contact:
            return {"error": "Contact not found"}, 404
        if include:
            #simulate include
            pass
        return contact, 200

    @staticmethod
    def patch(id: int, include: str = None, body: dict = None):
        """Updates the details of an existing supplier contact."""
        contact = DB["suppliers"]["supplier_contacts"].get(id)
        if not contact:
            return {"error": "Contact not found"}, 404
        if not body:
            return {"error": "Body is required"}, 400
        if body.get("id") != id:
            return {"error": "Id in body must match url"}, 400
        contact.update(body)
        if include:
            #simulate include
            pass
        return contact, 200

    @staticmethod
    def delete(id: int):
        """Deletes a supplier contact."""
        if id not in DB["suppliers"]["supplier_contacts"]:
            return {"error": "Contact not found"}, 404
        del DB["suppliers"]["supplier_contacts"][id]
        return {}, 204

class SupplierCompanyContactsByExternalId:
    @staticmethod
    def get(external_id: str, include: str = None, filter: dict = None):
        """Retrieves the list of contacts for an existing supplier company by Supplier Company External ID."""
        company_id = None
        for company in DB["suppliers"]["supplier_companies"].values():
            if company.get("external_id") == external_id:
                company_id = company.get("id")
                break
        if company_id is None:
            return {"error": "Company not found"}, 404
        contacts = [c for c in DB["suppliers"]["supplier_contacts"].values() if c.get("company_id") == company_id]
        if filter:
            filtered_contacts = []
            for contact in contacts:
                match = True
                for key, value in filter.items():
                    if contact.get(key) != value:
                        match = False
                        break
                if match:
                    filtered_contacts.append(contact)
            contacts = filtered_contacts
        if include:
            # Simulate include logic (not fully implemented)
            pass
        return contacts, 200

class SupplierContactByExternalId:
    @staticmethod
    def get(external_id: str, include: str = None):
        """Retrieves the details of an existing supplier contact by Supplier Contact External ID."""
        for contact in DB["suppliers"]["supplier_contacts"].values():
            if contact.get("external_id") == external_id:
                if include:
                    #simulate include
                    pass
                return contact, 200
        return {"error": "Contact not found"}, 404

    @staticmethod
    def patch(external_id: str, include: str = None, body: dict = None):
        """Updates the details of an existing supplier contact by Supplir Contact External ID."""
        for contact_id, contact in DB["suppliers"]["supplier_contacts"].items():
            if contact.get("external_id") == external_id:
                if not body:
                    return {"error": "Body is required"}, 400
                if body.get("id") != external_id:
                    return {"error": "External id in body must match url"}, 400
                contact.update(body)
                if include:
                    #simulate include
                    pass
                return contact, 200
        return {"error": "Contact not found"}, 404

    @staticmethod
    def delete(external_id: str):
        """Deletes a supplier contact by Supplier Contact External ID."""
        contact_id_to_delete = None
        for contact_id, contact in DB["suppliers"]["supplier_contacts"].items():
            if contact.get("external_id") == external_id:
                contact_id_to_delete = contact_id
                break
        if contact_id_to_delete is None:
            return {"error": "Contact not found"}, 404
        del DB["suppliers"]["supplier_contacts"][contact_id_to_delete]
        return {}, 204

class ContactTypes:
    @staticmethod
    def get():
        """Returns a list of contact types."""
        return list(DB["suppliers"]["contact_types"].values()), 200

    @staticmethod
    def post(body: dict = None):
        """Create a contact type with given parameters."""
        if not body:
            return {"error": "Body is required"}, 400
        contact_type_id = len(DB["suppliers"]["contact_types"]) + 1
        contact_type = {"id": contact_type_id, **body}
        DB["suppliers"]["contact_types"][contact_type_id] = contact_type
        return contact_type, 201

class ContactTypeById:
    @staticmethod
    def patch(id: int, body: dict = None):
        """Updates the details of an existing contact type."""
        contact_type = DB["suppliers"]["contact_types"].get(id)
        if not contact_type:
            return {"error": "Contact type not found"}, 404
        if not body:
            return {"error": "Body is required"}, 400
        if body.get("id") != id:
            return {"error": "Id in body must match url"}, 400
        contact_type.update(body)
        return contact_type, 200

    @staticmethod
    def delete(id: int):
        """Deletes a contact type."""
        if id not in DB["suppliers"]["contact_types"]:
            return {"error": "Contact type not found"}, 404
        del DB["suppliers"]["contact_types"][id]
        return {}, 204

class ContactTypeByExternalId:
    @staticmethod
    def patch(external_id: str, body: dict = None):
        """Updates the details of an existing contact type."""
        for contact_type_id, contact_type in DB["suppliers"]["contact_types"].items():
            if contact_type.get("external_id") == external_id:
                if not body:
                    return {"error": "Body is required"}, 400
                if body.get("id") != external_id:
                    return {"error": "External id in body must match url"}, 400
                contact_type.update(body)
                return contact_type, 200
        return {"error": "Contact type not found"}, 404

    @staticmethod
    def delete(external_id: str):
        """Deletes a contact type."""
        contact_type_id_to_delete = None
        for contact_type_id, contact_type in DB["suppliers"]["contact_types"].items():
            if contact_type.get("external_id") == external_id:
                contact_type_id_to_delete = contact_type_id
                break
        if contact_type_id_to_delete is None:
            return {"error": "Contact type not found"}, 404
        del DB["suppliers"]["contact_types"][contact_type_id_to_delete]
        return {}, 204

class SupplierCompanySegmentations:
    @staticmethod
    def get():
        """Returns a list of supplier company segmentations."""
        return list(DB["suppliers"]["supplier_company_segmentations"].values()), 200

    @staticmethod
    def post(body: dict = None):
        """Create a supplier company segmentation with given parameters."""
        if not body:
            return {"error": "Body is required"}, 400
        segmentation_id = len(DB["suppliers"]["supplier_company_segmentations"]) + 1
        segmentation = {"id": segmentation_id, **body}
        DB["suppliers"]["supplier_company_segmentations"][segmentation_id] = segmentation
        return segmentation, 201
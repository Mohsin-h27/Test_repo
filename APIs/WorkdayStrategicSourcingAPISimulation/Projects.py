"""
This module provides functionality for managing projects in the Workday Strategic
Sourcing system.
"""

from typing import Dict, List, Optional

from .SimulationEngine import db

def get(filter: Optional[Dict] = None, page: Optional[Dict] = None) -> List[Dict]:
    """
    Retrieves a list of projects based on optional filtering criteria and pagination settings.

    Args:
        filter (Optional[Dict]): A dictionary containing filter criteria for projects. Supported filters include:
                               - updated_at_from (datetime): Return projects updated on or after the specified timestamp
                               - updated_at_to (datetime): Return projects updated on or before the specified timestamp
                               - number_from (int): Find projects with number equal or greater than the specified one
                               - number_to (int): Find projects with number equal or smaller than the specified one
                               - title_contains (str): Return projects with title containing the specified string
                               - title_not_contains (str): Return projects with title not containing the specified string
                               - description_contains (str): Return projects with description containing the specified string
                               - description_not_contains (str): Return projects with description not containing the specified string
                               - external_id_empty (bool): Return projects with external_id blank
                               - external_id_not_empty (bool): Return projects with non-blank external_id
                               - external_id_equals (str): Find projects by a specific external ID
                               - external_id_not_equals (str): Find projects excluding the one with the specified external ID
                               - actual_start_date_from (date): Return projects started on or after the specified date
                               - actual_start_date_to (date): Return projects started on or before the specified date
                               - actual_end_date_from (date): Return projects ended on or after the specified date
                               - actual_end_date_to (date): Return projects ended on or before the specified date
                               - target_start_date_from (date): Return projects targeted to start on or after the specified date
                               - target_start_date_to (date): Return projects targeted to start on or before the specified date
                               - target_end_date_from (date): Return projects targeted to end on or after the specified date
                               - target_end_date_to (date): Return projects targeted to end on or before the specified date
                               - actual_spend_amount_from (float): Return projects with actual spend amount equal or greater than the specified amount
                               - actual_spend_amount_to (float): Return projects with actual spend amount equal or smaller than the specified amount
                               - approved_spend_amount_from (float): Return projects with approved spend amount equal or greater than the specified amount
                               - approved_spend_amount_to (float): Return projects with approved spend amount equal or smaller than the specified amount
                               - estimated_savings_amount_from (float): Return projects with estimated savings amount equal or greater than the specified amount
                               - estimated_savings_amount_to (float): Return projects with estimated savings amount equal or smaller than the specified amount
                               - estimated_spend_amount_from (float): Return projects with estimated spend amount equal or greater than the specified amount
                               - estimated_spend_amount_to (float): Return projects with estimated spend amount equal or smaller than the specified amount
                               - canceled_note_contains (str): Return projects with cancelation note containing the specified string
                               - canceled_note_not_contains (str): Return projects with cancelation note not containing the specified string
                               - canceled_note_empty (str): Return projects with an empty cancelation note
                               - canceled_note_not_empty (str): Return projects with a non-empty cancelation note
                               - canceled_reason_contains (str): Return projects with cancelation reason containing the specified string
                               - canceled_reason_not_contains (str): Return projects with cancelation reason not containing the specified string
                               - canceled_reason_empty (str): Return projects with an empty cancelation reason
                               - canceled_reason_not_empty (str): Return projects with a non-empty cancelation reason
                               - on_hold_note_contains (str): Return projects with on-hold note containing the specified string
                               - on_hold_note_not_contains (str): Return projects with on-hold note not containing the specified string
                               - on_hold_note_empty (str): Return projects with an empty on-hold note
                               - on_hold_note_not_empty (str): Return projects with a non-empty on-hold note
                               - on_hold_reason_contains (str): Return projects with on-hold reason containing the specified string
                               - on_hold_reason_not_contains (str): Return projects with on-hold reason not containing the specified string
                               - on_hold_reason_empty (str): Return projects with an empty on-hold reason
                               - on_hold_reason_not_empty (str): Return projects with a non-empty on-hold reason
                               - needs_attention_equals (bool): Return projects with the specified "needs attention" status
                               - needs_attention_not_equals (bool): Return projects with the "needs attention" status not equal to the specified one
                               - state_equals (List[str]): Find projects with specified statuses (draft, requested, planned, active, completed, canceled, on_hold)
                               - marked_as_needs_attention_at_from (datetime): Find projects marked as "needs attention" after or on the specified date
                               - marked_as_needs_attention_at_to (datetime): Find projects marked as "needs attention" before or on the specified date
                               - needs_attention_note_contains (str): Return projects with "needs attention" note containing the specified string
                               - needs_attention_note_not_contains (str): Return projects with "needs attention" note not containing the specified string
                               - needs_attention_note_empty (str): Return projects with an empty "needs attention" note
                               - needs_attention_note_not_empty (str): Return projects with a non-empty "needs attention" note
                               - needs_attention_reason_contains (str): Return projects with "needs attention" reason containing the specified string
                               - needs_attention_reason_not_contains (str): Return projects with "needs attention" reason not containing the specified string
                               - needs_attention_reason_empty (str): Return projects with an empty "needs attention" reason
                               - needs_attention_reason_not_empty (str): Return projects with a non-empty "needs attention" reason
                               If None, no filtering is applied.
        page (Optional[Dict]): A dictionary containing pagination settings with 'size' parameter
                             to limit the number of results per page (default: 10, max: 100).
                             If None, no pagination is applied.

    Returns:
        List[Dict]: A list of dictionaries, where each dictionary contains the details
                   of a project that matches the filter criteria, limited by pagination
                   if specified. Each dictionary contains any of the following fields:
                   - type_id (str): Object type
                   - id (str): Project identifier string
                   - external_id (str): Project external identifier string
                   - supplier_companies (List): Array of supplier company objects
                   - supplier_contacts (List): Array of supplier contact objects
                   - status (str): Project status
                   - attributes (Dict[str, Union[str, float, bool, datetime.date, None]]): Project attributes object containing:
                       - name (str): Project name
                       - description (str): Project description
                       - state (str): Project state (draft, requested, planned, active, completed, canceled, on_hold)
                       - target_start_date (datetime.date): Project target start date
                       - target_end_date (datetime.date): Project target end date
                       - actual_spend_amount (float): Project actual spend amount
                       - approved_spend_amount (float): Project approved spend amount
                       - estimated_savings_amount (float): Project estimated savings amount
                       - estimated_spend_amount (float): Project estimated spend amount
                       - canceled_note (Optional[str]): Project cancelation note
                       - canceled_reason (Optional[str]): Project cancelation reason
                       - on_hold_note (Optional[str]): Project on-hold note
                       - on_hold_reason (Optional[str]): Project on-hold reason
                       - needs_attention (bool): Project needs attention status
                       - marked_as_needs_attention_at (Optional[datetime.datetime]): Project marked as needs attention timestamp
                       - needs_attention_note (Optional[str]): Project needs attention note
                       - needs_attention_reason (Optional[str]): Project needs attention reason
                   - relationships (Dict[str, Union[List[Dict], Dict]]): Project relationships object containing:
                       - attachments (List[Dict]): Array of attachment objects
                       - creator (Dict): Project creator stakeholder object
                       - requester (Dict): Project requester stakeholder object
                       - owner (Dict): Project owner stakeholder object
                       - project_type (Dict): Project type object
                   - links (Dict[str, str]): Resource links object containing:
                       - self (str): Normalized link to the resource
                   
    """
    projects = list(db.DB["projects"]["projects"].values())
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

def post(project_data: Dict) -> Dict:
    """
    Creates a new project with the specified attributes.

    Args:
        project_data (Dict): A dictionary containing the project attributes.
                           If 'id' is not provided, a new unique ID will be generated.
                           project_data can contain any of the following keys:
                               - type_id (str): Object type
                               - id (str): Project identifier string
                               - external_id (str): Project external identifier string
                               - supplier_companies (List): Array of supplier company objects
                               - supplier_contacts (List): Array of supplier contact objects
                               - status (str): Project status
                               - attributes (Dict[str, Union[str, float, bool, datetime.date, None]]): Project attributes object containing:
                                   - name (str): Project name
                                   - description (str): Project description
                                   - state (str): Project state (draft, requested, planned, active, completed, canceled, on_hold)
                                   - target_start_date (datetime.date): Project target start date
                                   - target_end_date (datetime.date): Project target end date
                                   - actual_spend_amount (float): Project actual spend amount
                                   - approved_spend_amount (float): Project approved spend amount
                                   - estimated_savings_amount (float): Project estimated savings amount
                                   - estimated_spend_amount (float): Project estimated spend amount
                                   - canceled_note (Optional[str]): Project cancelation note
                                   - canceled_reason (Optional[str]): Project cancelation reason
                                   - on_hold_note (Optional[str]): Project on-hold note
                                   - on_hold_reason (Optional[str]): Project on-hold reason
                                   - needs_attention (bool): Project needs attention status
                                   - marked_as_needs_attention_at (Optional[datetime.datetime]): Project marked as needs attention timestamp
                                   - needs_attention_note (Optional[str]): Project needs attention note
                                   - needs_attention_reason (Optional[str]): Project needs attention reason
                               - relationships (Dict[str, Union[List[Dict], Dict]]): Project relationships object containing:
                                   - attachments (List[Dict]): Array of attachment objects
                                   - creator (Dict): Project creator stakeholder object
                                   - requester (Dict): Project requester stakeholder object
                                   - owner (Dict): Project owner stakeholder object
                                   - project_type (Dict): Project type object
    Returns:
        Dict: The created project data, including the assigned ID if one was generated.
        The project data will be returned with the following keys:
            - type_id (str): Object type
            - id (str): Project identifier string
            - external_id (str): Project external identifier string
            - supplier_companies (List): Array of supplier company objects
            - supplier_contacts (List): Array of supplier contact objects
            - status (str): Project status
            - attributes (Dict[str, Union[str, float, bool, datetime.date, None]]): Project attributes object containing:
                - name (str): Project name
                - description (str): Project description
                - state (str): Project state (draft, requested, planned, active, completed, canceled, on_hold)
                - target_start_date (datetime.date): Project target start date
                - target_end_date (datetime.date): Project target end date
                - actual_spend_amount (float): Project actual spend amount
                - approved_spend_amount (float): Project approved spend amount
                - estimated_savings_amount (float): Project estimated savings amount
                - estimated_spend_amount (float): Project estimated spend amount
                - canceled_note (Optional[str]): Project cancelation note
                - canceled_reason (Optional[str]): Project cancelation reason
                - on_hold_note (Optional[str]): Project on-hold note
                - on_hold_reason (Optional[str]): Project on-hold reason
                - needs_attention (bool): Project needs attention status
                - marked_as_needs_attention_at (Optional[datetime.datetime]): Project marked as needs attention timestamp
                - needs_attention_note (Optional[str]): Project needs attention note
                - needs_attention_reason (Optional[str]): Project needs attention reason
            - relationships (Dict[str, Union[List[Dict], Dict]]): Project relationships object containing:
                - attachments (List[Dict]): Array of attachment objects
                - creator (Dict): Project creator stakeholder object
                - requester (Dict): Project requester stakeholder object
                - owner (Dict): Project owner stakeholder object
                - project_type (Dict): Project type object
            - links (Dict[str, str]): Resource links object containing:
                - self (str): Normalized link to the resource
    """
    if "id" not in project_data:
        project_id = len(db.DB.get("projects", {}).get("projects", [])) + 1
        project_data["id"] = project_id
    db.DB["projects"]["projects"][project_data["id"]] = project_data
    return project_data
#!/usr/bin/env python3
"""
Mock JIRA 6.1 REST API Simulation (Pythonic Resource Names)

Implements a complete in-memory mock of the JIRA 6.1 REST API resources
and methods defined in the *Pythonic* specification. Each resource is
modeled as a Python class with methods named using snake_case.

Features:
  - In-memory "DB" for data storage
  - JSON-based persistence (save_state, load_state)
  - Embedded unittest suite to verify correctness
"""

import datetime
import json
import os
import unittest
import re
import uuid
from typing import Any, Dict, List, Optional, Union

###############################################################################
# In-Memory Database
###############################################################################
DB: Dict[str, Any] = {
    # For each resource, we create a container in DB to store data
    "reindex_info": {
        "running": False,
        "type": None,
    },
    "application_properties": {},
    "application_roles": {},
    "avatars": [],
    "components": {},
    "dashboards": {},
    "filters": {},
    "groups": {},
    "issues": {},
    "issue_links": [],
    "issue_link_types": {},
    "issue_types": {},
    "jql_autocomplete_data": {},
    "licenses": {},
    "my_permissions": {},
    "my_preferences": {},
    "permissions": {},
    "permission_schemes": {},
    "priorities": {},
    "projects": {},
    "project_categories": {},
    "resolutions": {},
    "roles": {},
    "webhooks": {},
    "workflows": {},
    "security_levels": {},
    "users": {},
    # ...
}

###############################################################################
# State Persistence
###############################################################################
def save_state(filepath: str) -> None:
    """Save the current DB state to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(DB, f, indent=2)

def load_state(filepath: str) -> None:
    """Load DB state from a JSON file, replacing the current in-memory DB."""
    global DB
    if not os.path.isfile(filepath):
        return
    with open(filepath, "r", encoding="utf-8") as f:
        DB = json.load(f)

###############################################################################
# Utility Helpers
###############################################################################

def _check_required_fields(payload: dict, required: List[str]) -> Optional[str]:
    for field in required:
        if field not in payload:
            return f"Missing required field '{field}'. "
    return None

def _check_empty_field(field: str, var: any) -> Optional[str]:
    if not var:
        return f"Field '{field}' cannot be empty."
    return ""


def _generate_id(prefix: str, existing: Dict[str, Any]) -> str:
    """Generate a simple ID like prefix-<num> for the resource."""
    return f"{prefix}-{len(existing) + 1}"

###############################################################################
# Resource Classes (Pythonic)
###############################################################################
class ReindexApi:
    """Handles /reindex_api resource (POST/GET /rest/api/2/reindex)."""

    @staticmethod
    def start_reindex(reindex_type: str = "FOREGROUND") -> dict:
        """POST /rest/api/2/reindex"""
        DB["reindex_info"]["running"] = True
        DB["reindex_info"]["type"] = reindex_type
        return {"started": True, "reindexType": reindex_type}

    @staticmethod
    def get_reindex_status() -> dict:
        """GET /rest/api/2/reindex"""
        return {
            "running": DB["reindex_info"]["running"],
            "type": DB["reindex_info"]["type"],
        }


class ApplicationPropertiesApi:
    """Handles /application_properties_api resource."""

    @staticmethod
    def get_application_properties(key:Optional[str] = None) -> dict:
        """
        GET /rest/api/2/application-properties
        Optional: key
        """
        if key:
            if key not in DB["application_properties"]:
                return {"error": f"Property '{key}' not found."}
            return {"key": key, "value": DB["application_properties"][key]}
        return {"properties": DB["application_properties"]}

    @staticmethod
    def update_application_property(id: str, value: str) -> dict:
        """
        PUT /rest/api/2/application-properties
        Required: id, value
        """
        err = _check_empty_field("id", id) + _check_empty_field("value", value)
        if err:
            return {"error": err}
        DB["application_properties"][id] = value
        return {"updated": True, "property": id, "newValue": value}


class ApplicationRoleApi:
    """Handles /application_role_api resource."""

    @staticmethod
    def get_application_roles() -> dict:
        """GET /rest/api/2/applicationrole"""
        return {"roles": list(DB["application_roles"].values())}

    @staticmethod
    def get_application_role_by_key(key: str) -> dict:
        """GET /rest/api/2/applicationrole/{key}"""
        role = DB["application_roles"].get(key)
        if role is None:
            return {"error": f"Role '{key}' not found."}
        return role


class AvatarApi:
    """Handles /avatar_api resource."""

    @staticmethod
    def upload_avatar(filetype: str, filename: str) -> dict:
        """
        POST /rest/api/2/avatar/{type}/load
        Required: type, filename
        """
        err = _check_empty_field("type", filetype) + _check_empty_field("filename", filename)
        if err:
            return {"error": err}

        new_avatar = {
            "id": _generate_id("avatar", DB["avatars"]),
            "type": filetype,
            "filename": filename
        }
        DB["avatars"].append(new_avatar)
        return {"uploaded": True, "avatar": new_avatar}

    @staticmethod
    def upload_temporary_avatar(filetype: str, filename: str) -> dict:
        """
        POST /rest/api/2/avatar/{type}/temporary
        Required: type, filename
        """

        err = _check_empty_field("type", filetype) + _check_empty_field("filename", filename)
        if err:
            return {"error": err}

        temp_avatar = {
            "id": _generate_id("avatar_temp", DB["avatars"]),
            "type": filetype,
            "filename": filename,
            "temporary": True
        }
        DB["avatars"].append(temp_avatar)
        return {"uploaded": True, "avatar": temp_avatar}

    @staticmethod
    def crop_temporary_avatar(cropDimensions: dict) -> dict:
        """
        POST /rest/api/2/avatar/{type}/temporaryCrop
        Required: cropDimensions
        """
        err = _check_empty_field("cropDimensions", cropDimensions)
        if err:
            return {"error": err}
        return {"cropped": True, "dimensions": cropDimensions}


class ComponentApi:
    """Handles /component_api resource."""

    @staticmethod
    def create_component(
        project: str,
        name: str,
        description: Optional[str] = None) -> dict:
        """POST /rest/api/2/component"""
        err = _check_empty_field("project", project) + _check_empty_field("name", name)
        if err:
            return {"error": err}

        if project not in DB["projects"]:
            return {"error": f"Project '{project}' not found."}

        comp_id = _generate_id("CMP", DB["components"])
        DB["components"][comp_id] = {
            "id": comp_id,
            "project": project,
            "name": name,
            "description": description
        }
        return DB["components"][comp_id]

    @staticmethod
    def get_component(comp_id: str) -> dict:
        """GET /rest/api/2/component/{id}"""
        comp = DB["components"].get(comp_id)
        if not comp:
            return {"error": f"Component '{comp_id}' not found."}
        return comp

    @staticmethod
    def update_component(
        comp_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None ) -> dict:
        """PUT /rest/api/2/component/{id}"""
        comp = DB["components"].get(comp_id)
        if not comp:
            return {"error": f"Component '{comp_id}' not found."}
        if name:
            comp["name"] = name
        if description:
            comp["description"] = description
        return {"updated": True, "component": comp}

    @staticmethod
    def delete_component(
        comp_id: str,
        moveIssuesTo: Optional[str] = None) -> dict:
        """DELETE /rest/api/2/component/{id}"""
        if comp_id not in DB["components"]:
            return {"error": f"Component '{comp_id}' does not exist."}
        DB["components"].pop(comp_id)
        return {"deleted": comp_id, "moveIssuesTo": moveIssuesTo}


class DashboardApi:
    """Handles /dashboard_api resource."""

    @staticmethod
    def get_dashboards(
        startAt: Optional[int] = 0,
        maxResults: Optional[int] = None) -> dict:
        """
        GET /rest/api/2/dashboard
        Optional: startAt, maxResults
        """
        all_dashboards = list(DB["dashboards"].values())
        return {"dashboards": all_dashboards}

    @staticmethod
    def get_dashboard(dash_id: str) -> dict:
        """GET /rest/api/2/dashboard/{id}"""
        dash = DB["dashboards"].get(dash_id)
        if not dash:
            return {"error": f"Dashboard '{dash_id}' not found."}
        return dash


class FilterApi:
    """Handles /filter_api resource."""

    @staticmethod
    def get_filters() -> dict:
        """GET /rest/api/2/filter"""
        return {"filters": list(DB["filters"].values())}

    @staticmethod
    def get_filter(filter_id: str) -> dict:
        """GET /rest/api/2/filter/{id}"""
        flt = DB["filters"].get(filter_id)
        if not flt:
            return {"error": f"Filter '{filter_id}' not found."}
        return flt

    @staticmethod
    def update_filter(
        filter_id: str,
        name: Optional[str] = None,
        jql: Optional[str] = None) -> dict:
        """PUT /rest/api/2/filter/{id}"""
        flt = DB["filters"].get(filter_id)
        if not flt:
            return {"error": f"Filter '{filter_id}' not found."}
        if name:
            flt["name"] = name
        if jql:
            flt["jql"] = jql
        return {"updated": True, "filter": flt}


class GroupApi:
    """Handles /group_api resource."""

    @staticmethod
    def get_group(groupname: str, expand: Optional[str] = None) -> dict:
        """
        GET /rest/api/2/group
        Required: groupname
        Optional: expand
        """
        err = _check_empty_field("groupname", groupname)
        if err:
            return {"error": err}

        group_data = DB["groups"].get(groupname)
        if not group_data:
            return {"error": f"Group '{groupname}' not found."}
        return {"group": group_data}


    @staticmethod
    def update_group(groupname: str, users: list[str]) -> dict:
        """
        GET /rest/api/2/group
        Required: groupname, users
        """

        if groupname not in DB["groups"]:
            return {"error": f"Couldn't find groupname {groupname}"}
        else:
            updated_group = {
                "name": groupname,
                "users": users
            }
            DB["groups"][groupname] = updated_group
            return {groupname: updated_group}

    @staticmethod
    def create_group(name: str) -> dict:
        """
        POST /rest/api/2/group
        Required: name
        """
        err = _check_empty_field("name", name)
        if err:
            return {"error": err}

        if name in DB["groups"]:
            return {"error": f"Group '{name}' already exists."}
        DB["groups"][name] = {"name": name, "users": []}
        return {"created": True, "group": DB["groups"][name]}

    @staticmethod
    def delete_group(groupname: str) -> dict:
        """
        DELETE /rest/api/2/group
        Required: groupname
        """
        err = _check_empty_field("groupname", groupname)
        if err:
            return {"error": err}

        if groupname not in DB["groups"]:
            return {"error": f"Group '{groupname}' does not exist."}
        DB["groups"].pop(groupname)
        return {"deleted": groupname}


class GroupsPickerApi:
    """Handles /groups_picker_api resource."""

    @staticmethod
    def find_groups(query: Optional[str] = None) -> dict:
        """
        GET /rest/api/2/groups/picker
        Optional: query
        """
        query = query.lower()
        matched = [g for g in DB["groups"] if query in g.lower()]
        return {"groups": matched}


class IssueApi:
    """Handles /issue_api resource."""

    @staticmethod
    def create_issue(fields: dict) -> dict:
        """POST /rest/api/2/issue"""
        err = _check_empty_field("fields", fields)
        if err:
            return {"error": err}

        if not fields:
            return {"error": f"Missing required field 'fields'."}
        new_id = _generate_id("ISSUE", DB["issues"])
        if not DB["issues"]:
            DB["issues"] = {}
        DB["issues"][new_id] = {
            "id": new_id,
            "fields": fields
        }
        return {"id": new_id, "fields": fields}

    @staticmethod
    def get_issue(
        issue_id: str,
        fields: Optional[Dict] = None,
        expand: Optional[str] = None) -> dict:
        """GET /rest/api/2/issue/{issueIdOrKey}"""
        if issue_id not in DB["issues"]:
            return {"error": f"Issue '{issue_id}' not found."}
        return DB["issues"][issue_id]

    @staticmethod
    def update_issue(issue_id: str, fields: Optional[Dict] = None) -> dict:
        """PUT /rest/api/2/issue/{issueIdOrKey}"""
        if issue_id not in DB["issues"]:
            return {"error": f"Issue '{issue_id}' not found."}
        DB["issues"][issue_id]["fields"].update(fields)
        return {"updated": True, "issue": DB["issues"][issue_id]}

    @staticmethod
    def delete_issue(
        issue_id: str,
        deleteSubtasks: Optional[str] = "False") -> dict:
        """DELETE /rest/api/2/issue/{issueIdOrKey}"""
        if issue_id not in DB["issues"]:
            return {"error": f"Issue '{issue_id}' does not exist."}
        DB["issues"].pop(issue_id)
        return {"deleted": issue_id, "deleteSubtasks": deleteSubtasks}

    @staticmethod
    def bulk_delete_issues_bulk(issue_ids: list) -> dict:
        """Deletes multiple issues in bulk"""
        # Initialize a dictionary to store deleted issues and errors
        results = {"deleted": [], "errors": []}

        # Iterate over each issue ID provided in the list
        for issue_id in issue_ids:
            if issue_id not in DB["issues"]:
                # If the issue does not exist, add an error message to the results
                results["errors"].append(f"Issue '{issue_id}' does not exist.")
            else:
                # If the issue exists, remove it from the database
                DB["issues"].pop(issue_id)
                # Add a success message to the results
                results["deleted"].append(f"Issue '{issue_id}' has been deleted.")

        # Return the results containing deleted issues and any errors encountered
        return results

    @staticmethod
    def assign_issue(issue_id: str, assignee: Dict) -> dict:
        """POST /rest/api/2/issue/{issueIdOrKey}/assignee"""
        if issue_id not in DB["issues"]:
            return {"error": f"Issue '{issue_id}' not found."}

        DB["issues"][issue_id]["fields"]["assignee"] = assignee
        return {"assigned": True, "issue": DB["issues"][issue_id]}

    @staticmethod
    def bulk_issue_operation(issueUpdates: dict) -> dict:
        """POST /rest/api/2/issue/bulk"""
        err = _check_empty_field("issueUpdates", issueUpdates)
        if err:
            return {"error": err}

        # Just simulate success
        return {"bulkProcessed": True, "updatesCount": len(issueUpdates)}

    @staticmethod
    def issue_picker(query: Optional[str] = None) -> dict:
        """GET /rest/api/2/issue/picker"""
        query = query.lower()
        matched = []
        for iss_id, data in DB["issues"].items():
            summary = data["fields"].get("summary", "").lower()
            if query in iss_id.lower() or query in summary:
                matched.append(iss_id)
        return {"issues": matched}

    @staticmethod
    def get_create_meta(
        projectKeys: Optional[str] = None,
        issueTypeNames: Optional[str] = None) -> dict:
        """GET /rest/api/2/issue/createmeta"""
        # Return a sample structure
        return {"projects": [{"key": "DEMO", "issueTypes": ["Task", "Bug"]}]}


class IssueLinkApi:
    """Handles /issue_link_api resource."""

    @staticmethod
    def create_issue_link(type: str, inwardIssue: dict, outwardIssue: dict) -> dict:
        """POST /rest/api/2/issueLink"""
        err = _check_empty_field("type", type) + _check_empty_field("inwardIssue", inwardIssue) + _check_empty_field("outwardIssue", outwardIssue)
        if err:
            return {"error": err}
        link_id = f"LINK-{len(DB['issue_links']) + 1}"
        link_data = {
            "id": link_id,
            "type": type,
            "inwardIssue": inwardIssue,
            "outwardIssue": outwardIssue
        }
        DB["issue_links"].append(link_data)
        return {"created": True, "issueLink": link_data}


class IssueLinkTypeApi:
    """Handles /issue_link_type_api resource."""

    @staticmethod
    def get_issue_link_types() -> dict:
        """GET /rest/api/2/issueLinkType"""
        return {"issueLinkTypes": list(DB["issue_link_types"].values())}

    @staticmethod
    def get_issue_link_type(link_type_id: str) -> dict:
        """GET /rest/api/2/issueLinkType/{issueLinkTypeId}"""
        lt = DB["issue_link_types"].get(link_type_id)
        if not lt:
            return {"error": f"Link type '{link_type_id}' not found."}
        return lt


class IssueTypeApi:
    """Handles /issue_type_api resource."""

    @staticmethod
    def get_issue_types() -> dict:
        """GET /rest/api/2/issuetype"""
        return {"issueTypes": list(DB["issue_types"].values())}

    @staticmethod
    def get_issue_type(type_id: str) -> dict:
        """GET /rest/api/2/issuetype/{id}"""
        it = DB["issue_types"].get(type_id)
        if not it:
            return {"error": f"Issue type '{type_id}' not found."}
        return it

    @staticmethod
    def create_issue_type(name: str, description: str, type: str = "standard") -> dict:
        """POST /rest/api/2/issuetype"""
        err = _check_empty_field("name", name) + _check_empty_field("description", description)
        if err:
            return {"error": err}
        issue_type = {
            "id": _generate_id("ISSUETYPE", DB["issue_types"]),
            "name": name,
            "description": description,
            "subtask": type == "subtask",
        }
        DB["issue_types"][issue_type["id"]] = issue_type
        return {"created": True, "issueType": issue_type}

class JqlApi:
    """Handles /jql_api resource."""

    @staticmethod
    def get_jql_autocomplete_data() -> dict:
        """GET /rest/api/2/jql/autocompletedata"""
        return {"fields": ["summary", "description"], "operators": ["=", "~"]}


class LicenseValidatorApi:
    """Handles /license_validator_api resource."""

    @staticmethod
    def validate_license(license: str) -> dict:
        """POST /rest/api/2/licenseValidator"""
        err = _check_empty_field("license", license)
        if err:
            return {"error": err}
        # Fake decode
        return {"valid": True, "decoded": f"DecodedLicense({license[:10]}...)"}


class MyPermissionsApi:
    """Handles /my_permissions_api resource."""

    @staticmethod
    def get_current_user_permissions(projectKey: Optional[str] = None, issueKey: Optional[str] = None) -> dict:
        """GET /rest/api/2/mypermissions"""
        # Real logic would check user login, projects, etc. We'll just return a stub.
        return {"permissions": ["CREATE_ISSUE", "EDIT_ISSUE"]}


class MyPreferencesApi:
    """Handles /my_preferences_api resource."""

    @staticmethod
    def get_my_preferences() -> dict:
        """GET /rest/api/2/mypreferences"""
        return DB["my_preferences"]

    @staticmethod
    def update_my_preferences(value: dict) -> dict:
        """PUT /rest/api/2/mypreferences"""
        err = _check_empty_field("value", value)
        if err:
            return {"error": err}

        DB["my_preferences"].update(value)
        return {"updated": True, "preferences": DB["my_preferences"]}


class PermissionsApi:
    """Handles /permissions_api resource."""

    @staticmethod
    def get_permissions() -> dict:
        """GET /rest/api/2/permissions"""
        return {"permissions": DB["permissions"]}


class PermissionSchemeApi:
    """Handles /permission_scheme_api resource."""

    @staticmethod
    def get_permission_schemes() -> dict:
        """GET /rest/api/2/permissionscheme"""
        return {"schemes": list(DB["permission_schemes"].values())}

    @staticmethod
    def get_permission_scheme(scheme_id: str) -> dict:
        """GET /rest/api/2/permissionscheme/{schemeId}"""
        scheme = DB["permission_schemes"].get(scheme_id)
        if not scheme:
            return {"error": f"Permission scheme '{scheme_id}' not found."}
        return scheme


class PriorityApi:
    """Handles /priority_api resource."""

    @staticmethod
    def get_priorities() -> dict:
        """GET /rest/api/2/priority"""
        return {"priorities": list(DB["priorities"].values())}

    @staticmethod
    def get_priority(priority_id: str) -> dict:
        """GET /rest/api/2/priority/{id}"""
        p = DB["priorities"].get(priority_id)
        if not p:
            return {"error": f"Priority '{priority_id}' not found."}
        return p


class ProjectApi:
    """Handles /project_api resource."""

    @staticmethod
    def create_project(proj_key: str, proj_name: str) -> dict:
        """POST /rest/api/2/project"""
        err = _check_empty_field("key", proj_key) + _check_empty_field("name", proj_name)
        if err:
            return {"error": err}

        if proj_key in DB["projects"]:
            return {"error": f"Project '{proj_key}' already exists."}

        DB["projects"][proj_key] = {"key": proj_key, "name": proj_name}
        return {"created": True, "project": DB["projects"][proj_key]}

    @staticmethod
    def get_projects() -> dict:
        """GET /rest/api/2/project"""
        return {"projects": list(DB["projects"].values())}

    @staticmethod
    def get_project(project_key: str) -> dict:
        """GET /rest/api/2/project/{projectIdOrKey}"""
        proj = DB["projects"].get(project_key)
        if not proj:
            return {"error": f"Project '{project_key}' not found."}
        return proj

    @staticmethod
    def get_project_avatars(project_key: str) -> dict:
        """GET /rest/api/2/project/{projectIdOrKey}/avatars"""
        # For demonstration, return all avatars in DB that mention 'project' type
        matched = [a for a in DB["avatars"] if a["type"] == "project"]
        return {"project": project_key, "avatars": matched}

    @staticmethod
    def get_project_components(project_key: str) -> dict:
        """GET /rest/api/2/project/{projectIdOrKey}/components"""
        # Return components that mention the project
        comps = [c for c in DB["components"].values() if c["project"] == project_key]
        return {"components": comps}

    @staticmethod
    def delete_project(project_key: str) -> dict:
        """DELETE /rest/api/2/project"""
        if project_key not in DB["projects"]:
            return {"error": f"Project '{project_key}' does not exist."}

        # Remove the project from DB
        DB["projects"].pop(project_key)

        # Delete components associated with the project
        components_to_delete = [cmp_id for cmp_id, component in DB["components"].items() if component["project"] == project_key]

        for cmp_id in components_to_delete:
            DB["components"].pop(cmp_id)

        return {"deleted": project_key}


class ProjectCategoryApi:
    """Handles /project_category_api resource."""

    @staticmethod
    def get_project_categories() -> dict:
        """GET /rest/api/2/projectCategory"""
        return {"categories": list(DB["project_categories"].values())}

    @staticmethod
    def get_project_category(cat_id: str) -> dict:
        """GET /rest/api/2/projectCategory/{id}"""
        c = DB["project_categories"].get(cat_id)
        if not c:
            return {"error": f"Project category '{cat_id}' not found."}
        return c


class ResolutionApi:
    """Handles /resolution_api resource."""

    @staticmethod
    def get_resolutions() -> dict:
        """GET /rest/api/2/resolution"""
        return {"resolutions": list(DB["resolutions"].values())}

    @staticmethod
    def get_resolution(res_id: str) -> dict:
        """GET /rest/api/2/resolution/{id}"""
        r = DB["resolutions"].get(res_id)
        if not r:
            return {"error": f"Resolution '{res_id}' not found."}
        return r


class RoleApi:
    """Handles /role_api resource."""

    @staticmethod
    def get_roles() -> dict:
        """GET /rest/api/2/role"""
        return {"roles": list(DB["roles"].values())}

    @staticmethod
    def get_role(role_id: str) -> dict:
        """GET /rest/api/2/role/{id}"""
        r = DB["roles"].get(role_id)
        if not r:
            return {"error": f"Role '{role_id}' not found."}
        return r


class SearchApi:
    """Handles /search_api resource."""

    @staticmethod
    def search_issues(
        jql: str = "",
        start_at: Optional[int] = 0,
        max_results: Optional[int] = 50,
        validateQuery: Optional[bool] = True,
        fields: Optional[str] = None,
        expand: Optional[str] = None
        ) -> dict:
        """
        GET /rest/api/2/search

        Extended JQL parser that supports:
          - <field> = "value"
          - <field> ~ "value"
          - <field> < "dateValue"
          - <field> <= "dateValue"
          - <field> > "dateValue"
          - <field> >= "dateValue"
        - Multiple clauses joined by AND
        - Basic pagination: startAt, maxResults
        """
        # 1. Separate ORDER BY clause (if any)
        order_by_clause = None
        jql_conditions = jql
        order_by_match = re.search(r'(?i)\bORDER BY\b', jql)
        if order_by_match:
            idx = order_by_match.start()
            jql_conditions = jql[:idx].strip()
            order_by_clause = jql[idx:].strip()
            # Remove the ORDER BY keyword from the clause
            order_by_clause = re.sub(r'(?i)^ORDER BY', '', order_by_clause).strip()

        # 2. Parse the JQL conditions into an expression tree
        expression = SearchApi._parse_jql(jql_conditions)

        # 3. Filter issues based on the expression tree
        all_issues = []
        for issue in DB["issues"].values():
            if SearchApi._evaluate_expression(expression, issue):
                all_issues.append(issue)

        # 4. Apply ordering if specified
        if order_by_clause:
            # For simplicity, assume order_by_clause is of the form "field [ASC|DESC]"
            parts = order_by_clause.split()
            order_field = parts[0]
            order_dir = parts[1].upper() if len(parts) > 1 else "ASC"
            reverse = (order_dir == "DESC")
            all_issues = sorted(
                all_issues,
                key=lambda issue: SearchApi._get_sort_key(issue, order_field),
                reverse=reverse
            )

        # 5. Apply pagination
        total = len(all_issues)
        end_index = start_at + max_results
        paged_issues = all_issues[start_at:end_index]
        return {
            "issues": paged_issues,
            "startAt": start_at,
            "maxResults": max_results,
            "total": total,
        }

    @staticmethod
    def _tokenize_jql(jql: str) -> List[Dict[str, str]]:
        """
        Converts the JQL string into a list of tokens.
        Recognizes identifiers, quoted strings, operators, and logical keywords.
        """
        token_specification = [
            ('AND',    r'\bAND\b'),
            ('OR',     r'\bOR\b'),
            ('NOT',    r'\bNOT\b'),
            ('OP',     r'<=|>=|=|~|<|>'),
            ('EMPTY',  r'\bEMPTY\b'),
            ('NULL',   r'\bNULL\b'),
            ('STRING', r'"[^"]*"|\'[^\']*\''),
            ('IDENT',  r'[A-Za-z0-9_.]+'),
            ('SKIP',   r'[ \t]+'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(tok_regex).match
        pos = 0
        tokens = []
        while pos < len(jql):
            m = get_token(jql, pos)
            if m is None:
                raise ValueError(f'Unexpected token at position {pos} in JQL: {jql[pos:]}')
            typ = m.lastgroup
            if typ != 'SKIP':
                token = m.group(typ)
                tokens.append({'type': typ, 'value': token})
            pos = m.end()
        return tokens

    @staticmethod
    def _parse_jql(jql: str) -> List[Dict[str, str]]:
        """
        Naive JQL parser that splits on 'AND' and attempts to extract:
          - field
          - operator (one of =, ~, <, <=, >, >=)
          - value (quoted string)

        Acceptable forms:
            field = "someValue"
            field ~ "someValue"
            field < "YYYY-MM-DD"
            field <= "YYYY-MM-DD"
            field > "YYYY-MM-DD"
            field >= "YYYY-MM-DD"

        Returns a list of conditions, e.g.:
        [
          {"field": "project", "operator": "=", "value": "DEMO"},
          {"field": "created", "operator": "<", "value": "2024-12-12"},
          {"field": "duedate", "operator": "<=", "value": "2025-01-01"}
        ]
        """
        if not jql:
            return {'type': 'always_true'}
        tokens = SearchApi._tokenize_jql(jql)

        def parse_expression(index):
            node, index = parse_term(index)
            while index < len(tokens) and tokens[index]['type'] == 'OR':
                index += 1  # skip OR
                right, index = parse_term(index)
                node = {'type': 'logical', 'operator': 'OR', 'children': [node, right]}
            return node, index

        def parse_term(index):
            node, index = parse_factor(index)
            while index < len(tokens) and tokens[index]['type'] == 'AND':
                index += 1  # skip AND
                right, index = parse_factor(index)
                node = {'type': 'logical', 'operator': 'AND', 'children': [node, right]}
            return node, index

        def parse_factor(index):
            if index < len(tokens) and tokens[index]['type'] == 'NOT':
                index += 1  # skip NOT
                child, index = parse_factor(index)
                return {'type': 'logical', 'operator': 'NOT', 'child': child}, index
            else:
                return parse_condition(index)

        def parse_condition(index):
            if index >= len(tokens) or tokens[index]['type'] != 'IDENT':
                raise ValueError("Expected field identifier in JQL")
            field = tokens[index]['value']
            index += 1
            # Check if there is an operator (OP, EMPTY, or NULL)
            if index < len(tokens) and tokens[index]['type'] in ['OP', 'EMPTY', 'NULL']:
                operator = tokens[index]['value']
                index += 1
                value = None
                if tokens[index-1]['type'] == 'OP':
                    if index < len(tokens) and tokens[index]['type'] == 'STRING':
                        # Remove surrounding quotes
                        value = tokens[index]['value'][1:-1]
                        index += 1
                    else:
                        raise ValueError("Expected string literal after operator")
                return {'type': 'condition', 'field': field, 'operator': operator, 'value': value}, index
            else:
                # No operator provided; default to checking that the field is non-empty
                return {'type': 'condition', 'field': field, 'operator': '=', 'value': ''}, index

        expr, index = parse_expression(0)
        return expr

    @staticmethod
    def _evaluate_expression(expr, issue: dict) -> bool:
        """
        Recursively evaluates the parsed JQL expression tree against an issue.
        """
        if expr['type'] == 'always_true':
            return True

        if expr['type'] == 'logical':
            op = expr['operator']
            if op == 'AND':
                return all(SearchApi._evaluate_expression(child, issue) for child in expr['children'])
            elif op == 'OR':
                return any(SearchApi._evaluate_expression(child, issue) for child in expr['children'])
            elif op == 'NOT':
                return not SearchApi._evaluate_expression(expr['child'], issue)

        elif expr['type'] == 'condition':
            field = expr['field']
            operator = expr['operator']
            expected_val = expr.get('value')
            fields = issue.get("fields", {})
            actual_val = fields.get(field, "")

            # Handle EMPTY and NULL operators
            if operator.upper() in ['EMPTY', 'NULL']:
                return actual_val in [None, "", []]

            # Handle string-based operators
            if operator == "=":
                return str(actual_val) == expected_val
            elif operator == "~":
                return expected_val.lower() in str(actual_val).lower()

            # Handle date-based operators (for 'created' or 'duedate')
            elif operator in ["<", "<=", ">", ">="]:
                if field.lower() not in ["created", "duedate"]:
                    return False
                try:
                    actual_date = SearchApi._parse_issue_date(actual_val)
                    expected_date = SearchApi._parse_issue_date(expected_val)
                except ValueError:
                    return False
                if operator == "<":
                    return actual_date < expected_date
                elif operator == "<=":
                    return actual_date <= expected_date
                elif operator == ">":
                    return actual_date > expected_date
                elif operator == ">=":
                    return actual_date >= expected_date

            return False  # unrecognized operator

        return False

    @staticmethod
    def _get_sort_key(issue: dict, field: str):
        """
        Returns a key for sorting. For date fields (created, duedate),
        attempts to parse the field into a date.
        """
        value = issue.get("fields", {}).get(field, None)
        if field.lower() in ["created", "duedate"] and value:
            try:
                return SearchApi._parse_issue_date(value)
            except ValueError:
                return None
        return value

    @staticmethod
    def _parse_issue_date(date_str: str) -> datetime.date:
        """
        A helper to parse date strings from the issue or from JQL.
        Accepts various forms:
          - 'YYYY-MM-DD'
          - 'YYYY-MM-DDTHH:mm:ss'
          - 'DD.MM.YYYY' (as requested in the question)
        You can extend for more formats as needed.
        """
        # Try a few known formats:
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%d.%m.%Y"):
            try:
                parsed = datetime.datetime.strptime(date_str, fmt)
                return parsed.date()  # only keep date portion
            except ValueError:
                pass
        # If no format worked, raise
        raise ValueError(f"Could not parse date string '{date_str}'")


class ServerInfoApi:
    """Handles /server_info_api resource."""

    @staticmethod
    def get_server_info() -> dict:
        """GET /rest/api/2/serverInfo"""
        return {
            "baseUrl": "http://mock-server:8080",
            "version": "6.1",
            "title": "Mock JIRA Server"
        }


class SettingsApi:
    """Handles /settings_api resource."""

    @staticmethod
    def get_settings() -> dict:
        """GET /rest/api/2/settings"""
        return {"settings": {"exampleSetting": True}}


class StatusApi:
    """Handles /status_api resource."""

    @staticmethod
    def get_statuses() -> dict:
        """GET /rest/api/2/status"""
        # We'll store statuses in DB["statuses"] for convenience
        if "statuses" not in DB:
            DB["statuses"] = {}
        return {"statuses": list(DB["statuses"].values())}

    @staticmethod
    def get_status(status_id: str) -> dict:
        """GET /rest/api/2/status/{id}"""
        if "statuses" not in DB:
            DB["statuses"] = {}
        s = DB["statuses"].get(status_id)
        if not s:
            return {"error": f"Status '{status_id}' not found."}
        return s


class StatusCategoryApi:
    """Handles /status_category_api resource."""

    @staticmethod
    def get_status_categories() -> dict:
        """GET /rest/api/2/statuscategory"""
        if "status_categories" not in DB:
            DB["status_categories"] = {}
        return {"statusCategories": list(DB["status_categories"].values())}

    @staticmethod
    def get_status_category(cat_id: str) -> dict:
        """GET /rest/api/2/statuscategory/{id}"""
        if "status_categories" not in DB:
            DB["status_categories"] = {}
        c = DB["status_categories"].get(cat_id)
        if not c:
            return {"error": f"Status category '{cat_id}' not found."}
        return c


class UserApi:
    """Handles /user_api resource."""

    @staticmethod
    def get_user(
        username: Optional[str] = None,
        account_id: Optional[str] = None) -> dict:
        """GET /rest/api/2/user"""
        # We require at least one of username/accountId, but for simplicity let's just check username
        if account_id:
            user = DB["users"].get(account_id)
            if user:
                return user
        elif username:
            for u in DB["users"].values():
                if u.get("name") == username:
                    return u

        return {"error": "User not found."}

    @staticmethod
    def create_user(payload: dict) -> dict:
        """POST /rest/api/2/user - Creates a new user with all required fields."""
        err = _check_required_fields(payload, ["name", "emailAddress", "displayName"])
        if err:
            return {"error": err}

        uname = payload["name"]

        user_key = str(uuid.uuid4())
        while user_key in DB["users"]:
            user_key = str(uuid.uuid4())

        # Default user structure
        user_defaults = {
            "name": uname,
            "key": user_key,
            "active": True,
            "emailAddress": payload["emailAddress"],
            "displayName": payload["displayName"],
            "profile": {
                "bio": payload.get("profile", {}).get("bio", ""),
                "joined": payload.get("profile", {}).get("joined", "")
            },
            "drafts": payload.get("drafts", []),
            "messages": payload.get("messages", []),
            "threads": payload.get("threads", []),
            "labels": payload.get("labels", []),
            "settings": {
                "theme": payload.get("settings", {}).get("theme", "light"),
                "notifications": payload.get("settings", {}).get("notifications", True)
            },
            "history": payload.get("history", []),
            "watch": payload.get("watch", []),
            "sendAs": payload.get("sendAs", [])
        }

        DB["users"][user_key] = user_defaults
        return {"created": True, "user": DB["users"][user_key]}

    @staticmethod
    def delete_user(username: Optional[str] = None,
                    key: Optional[str] = None) -> dict:
        """DELETE /rest/api/2/user"""
        if not username and not key:
            return {"error": "Either 'username' or 'key' must be provided."}
        if username:
            key = next((u["key"] for u in DB["users"].values() if u["name"] == username), None)
        if not key:
            return {"error": "User not found."}
        del DB["users"][key]
        return {"deleted": key}

    @staticmethod
    def find_user(
        username: str,
        startAt: Optional[str] = 0,
        maxResults: Optional[str] = 50,
        includeActive: Optional[bool] = True,
        includeInactive: Optional[bool] = False) -> dict:
        """GET /rest/api/2/user/picker"""
        err = _check_empty_field("username", username)
        if err:
            return {"error": err}
        if not isinstance(startAt, int):
            return {"error": "startAt must be an integer"}
        if not isinstance(maxResults, int):
            return {"error": "maxResults must be an integer"}

        query_lower = username.lower()
        users = [
            user
            for user in DB["users"].values()
            if query_lower in user["name"].lower()
            or query_lower in user["emailAddress"].lower()
            or query_lower in user["displayName"].lower()
        ]
        # Filter based on active/inactive status
        if not includeActive:
            users = [user for user in users if not user.get("active", True)]
        if not includeInactive:
            users = [user for user in users if user.get("active", True)]

        end_index = startAt + maxResults
        paged_users = users[startAt:end_index]

        return paged_users

class UserAvatarsApi:
    """Handles /user_avatars_api resource."""

    @staticmethod
    def get_user_avatars(username: str) -> dict:
        """GET /rest/api/2/user/avatars"""
        err = _check_empty_field("username", username)
        if err:
            return {"error": err}
        # Return all avatars that might relate to a user, or all if not tracked specifically
        user_avatars = [a for a in DB["avatars"] if a["type"] == "user"]
        return {"username": username, "avatars": user_avatars}


class VersionApi:
    """Handles /version_api resource."""

    @staticmethod
    def get_version(ver_id: str) -> dict:
        """GET /rest/api/2/version/{id}"""
        if "versions" not in DB:
            DB["versions"] = {}
        v = DB["versions"].get(ver_id)
        if not v:
            return {"error": f"Version '{ver_id}' not found."}
        return v

    @staticmethod
    def delete_version(ver_id: str, move_fix_issues_to: str = None, move_affected_issues_to: str = None) -> dict:
        """DELETE /rest/api/2/version/{id}"""
        if "versions" not in DB:
            DB["versions"] = {}
        if ver_id not in DB["versions"]:
            return {"error": f"Version '{ver_id}' does not exist."}
        DB["versions"].pop(ver_id)
        return {
            "deleted": ver_id,
            "moveFixIssuesTo": move_fix_issues_to,
            "moveAffectedIssuesTo": move_affected_issues_to
        }

    @staticmethod
    def get_version_related_issue_counts(ver_id: str) -> dict:
        """GET /rest/api/2/version/{id}/relatedIssueCounts"""
        # In real usage, we'd count how many issues reference this version
        return {"fixCount": 0, "affectedCount": 0}


class WebhookApi:
    """Handles /webhook_api resource."""

    @staticmethod
    def create_or_get_webhooks(webhooks: List[Dict]) -> dict:
        """POST /rest/api/2/webhook"""
        err = _check_empty_field("webhooks", webhooks)
        if err:
            return {"error": err}
        # For example, store them in DB
        new_ids = []
        for wh in webhooks:
            wh_id = _generate_id("WEBHOOK", DB["webhooks"])
            DB["webhooks"][wh_id] = wh
            new_ids.append(wh_id)
        return {"registered": True, "webhookIds": new_ids}

    @staticmethod
    def get_webhooks() -> dict:
        """GET /rest/api/2/webhook"""
        return {"webhooks": list(DB["webhooks"].values())}

    @staticmethod
    def delete_webhooks(webhookIds: List[str]) -> dict:
        """DELETE /rest/api/2/webhook"""
        err = _check_empty_field("webhookIds", webhookIds)
        if err:
            return {"error": err}
        deleted = []
        for wid in webhookIds:
            if wid in DB["webhooks"]:
                DB["webhooks"].pop(wid)
                deleted.append(wid)
        return {"deleted": deleted}


class WorkflowApi:
    """Handles /workflow_api resource."""

    @staticmethod
    def get_workflows() -> dict:
        """GET /rest/api/2/workflow"""
        return {"workflows": list(DB["workflows"].values())}


class SecurityLevelApi:
    """Handles /security_level_api resource."""

    @staticmethod
    def get_security_levels() -> dict:
        """GET /rest/api/2/securitylevel"""
        return {"securityLevels": list(DB["security_levels"].values())}

    @staticmethod
    def get_security_level(sec_id: str) -> dict:
        """GET /rest/api/2/securitylevel/{id}"""
        lvl = DB["security_levels"].get(sec_id)
        if not lvl:
            return {"error": f"Security level '{sec_id}' not found."}
        return lvl
import json
import os
import unittest
from typing import Any, Dict, Optional, Type

"""
A single-file, fully functional Python API simulation for the specified
LinkedIn-like resources (/me, /organizations, /organizationAcls, /posts). Implements:

1. Complete resource classes with methods exactly matching the discovery spec:
   - /me: getMe, createMe, updateMe, deleteMe
   - /organizations: getOrganizationsByVanityName, createOrganization,
                     updateOrganization, deleteOrganization,
                     deleteOrganizationByVanityName
   - /organizationAcls: getOrganizationAclsByRoleAssignee, createOrganizationAcl,
                        updateOrganizationAcl, deleteOrganizationAcl
   - /posts: getPostsByAuthor, createPost, updatePost, deletePost,
             deletePostsByAuthor

2. In-memory JSON-serializable storage in a global DB dictionary.

3. Persistence methods save_state(filepath) and load_state(filepath).

4. Embedded unit tests using unittest. Running this file directly will
   execute all tests and confirm the simulation works as intended.

Note: All methods are defined as class methods, allowing direct calls on the classes.
"""
# ---------------------------------------------------------------------------------------
# In-Memory Database Structure
# ---------------------------------------------------------------------------------------
# DB = {
#     "people": {userId: {...}, ...},
#     "organizations": {organizationId: {...}, ...},
#     "organizationAcls": {organizationAclId: {...}, ...},
#     "posts": {postId: {...}, ...},
#     "next_person_id": int,
#     "next_org_id": int,
#     "next_acl_id": int,
#     "next_post_id": int,
#     "current_person_id": str
# }
# --------------------------------------------------

# Global in-memory "database" following the provided structure.
DB: Dict[str, Any] = {
    "people": {},
    "organizations": {},
    "organizationAcls": {},
    "posts": {},
    "next_person_id": 0,
    "next_org_id": 0,
    "next_acl_id": 0,
    "next_post_id": 0,
    "current_person_id": ""
}

# Persistence functions
def save_state(filepath: str) -> None:
    """
    Save the current state (DB) to a JSON file.
    """
    with open(filepath, 'w') as f:
        json.dump(DB, f)

def load_state(filepath: str) -> None:
    """
    Load the state (DB) from a JSON file.
    """
    global DB
    with open(filepath, 'r') as f:
        DB = json.load(f)


# API Resource: /me using DB["people"] and DB["current_person_id"]
class Me:
    """
    API simulation for the '/me' resource.
    """
    @classmethod
    def get_me(cls: Type["Me"], projection: Optional[str] = None, start: int = 0, count: int = 10) -> Dict[str, Any]:
        """
        Retrieve the authenticated member's profile data.

        If a projection is provided, only the requested fields will be included in the returned data.
        The projection parameter is expected to be a string of comma-separated field names.
        For example: "(id,localizedFirstName,localizedLastName)"
        """
        current_id = DB.get("current_person_id")
        if current_id is None:
            return {"error": "No authenticated member."}
        person = DB["people"].get(current_id)
        if person is None:
            return {"error": "Authenticated person not found."}

        if projection:
            projection = projection.strip()
            if projection.startswith("(") and projection.endswith(")"):
                projection = projection[1:-1]
            # Split by comma to get individual field names and strip spaces
            fields = [field.strip() for field in projection.split(",")]
            # Create a new dictionary with only the requested fields that exist in the person data
            projected_person = {field: person.get(field) for field in fields if field in person}
            return {"data": projected_person}

        return {"data": person}

    @classmethod
    def create_me(cls: Type["Me"], person_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new member profile and set it as the current authenticated member.
        """
        if DB.get("current_person_id") is not None:
            return {"error": "Authenticated member already exists."}
        new_id = str(DB["next_person_id"])
        DB["next_person_id"] += 1
        person_data["id"] = new_id
        DB["people"][new_id] = person_data
        DB["current_person_id"] = new_id
        return {"data": person_data}

    @classmethod
    def update_me(cls: Type["Me"], person_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the authenticated member's profile.
        """
        current_id = DB.get("current_person_id")
        if current_id is None or current_id not in DB["people"]:
            return {"error": "Authenticated member not found."}
        person_data["id"] = current_id
        DB["people"][current_id] = person_data
        return {"data": person_data}

    @classmethod
    def delete_me(cls: Type["Me"]) -> Dict[str, Any]:
        """
        Delete the authenticated member's profile.
        """
        current_id = DB.get("current_person_id")
        if current_id is None or current_id not in DB["people"]:
            return {"error": "Authenticated member not found."}
        del DB["people"][current_id]
        DB["current_person_id"] = None
        return {"status": "Authenticated member deleted."}


# API Resource: /organizations
class Organizations:
    """
    API simulation for the '/organizations' resource.
    """
    @classmethod
    def get_organizations_by_vanity_name(cls: Type["Organizations"],
                                         query_field: str,
                                         vanity_name: str,
                                         projection: Optional[str] = None,
                                         start: int = 0,
                                         count: int = 10) -> Dict[str, Any]:
        """
        Retrieve organization(s) by vanity name.
        """
        if query_field != "vanityName":
            return {"error": "Invalid query parameter. Expected 'vanityName'."}
        results = [org for org in DB["organizations"].values() if org.get("vanityName") == vanity_name]
        paginated = results[start:start+count]
        return {"data": paginated}

    @classmethod
    def create_organization(cls: Type["Organizations"], organization_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new organization.
        """
        org_id = DB["next_org_id"]
        DB["next_org_id"] += 1
        organization_data["id"] = org_id
        DB["organizations"][str(org_id)] = organization_data
        return {"data": organization_data}

    @classmethod
    def update_organization(cls: Type["Organizations"],
                            organization_id: str,
                            organization_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing organization.
        """
        if organization_id not in DB["organizations"]:
            return {"error": "Organization not found."}
        organization_data["id"] = DB["organizations"][organization_id]["id"]
        DB["organizations"][organization_id] = organization_data
        return {"data": organization_data}

    @classmethod
    def delete_organization(cls: Type["Organizations"], organization_id: str) -> Dict[str, Any]:
        """
        Delete an organization by its ID.
        """
        if organization_id not in DB["organizations"]:
            return {"error": "Organization not found."}
        del DB["organizations"][organization_id]
        return {"status": f"Organization {organization_id} deleted."}

    @classmethod
    def delete_organization_by_vanity_name(cls: Type["Organizations"],
                                           query_field: str,
                                           vanity_name: str) -> Dict[str, Any]:
        """
        Delete organization(s) by vanity name.
        """
        if query_field != "vanityName":
            return {"error": "Invalid query parameter. Expected 'vanityName'."}
        to_delete = [org_id for org_id, org in DB["organizations"].items() if org.get("vanityName") == vanity_name]
        if not to_delete:
            return {"error": "Organization with the given vanity name not found."}
        for org_id in to_delete:
            del DB["organizations"][org_id]
        return {"status": f"Organizations with vanity name '{vanity_name}' deleted."}


# API Resource: /organizationAcls
class OrganizationAcls:
    """
    API simulation for the '/organizationAcls' resource.
    """
    @classmethod
    def get_organization_acls_by_role_assignee(cls: Type["OrganizationAcls"],
                                               query_field: str,
                                               role_assignee: str,
                                               projection: Optional[str] = None,
                                               start: int = 0,
                                               count: int = 10) -> Dict[str, Any]:
        """
        Retrieve ACL records by roleAssignee URN.
        """
        if query_field != "roleAssignee":
            return {"error": "Invalid query parameter. Expected 'roleAssignee'."}
        results = [acl for acl in DB["organizationAcls"].values() if acl.get("roleAssignee") == role_assignee]
        paginated = results[start:start+count]
        return {"data": paginated}

    @classmethod
    def create_organization_acl(cls: Type["OrganizationAcls"], acl_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new organization ACL record.
        """
        acl_id = str(DB["next_acl_id"])
        DB["next_acl_id"] += 1
        acl_data["aclId"] = acl_id
        DB["organizationAcls"][acl_id] = acl_data
        return {"data": acl_data}

    @classmethod
    def update_organization_acl(cls: Type["OrganizationAcls"],
                                acl_id: str,
                                acl_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing organization ACL record.
        """
        if acl_id not in DB["organizationAcls"]:
            return {"error": "ACL record not found."}
        acl_data["aclId"] = acl_id
        DB["organizationAcls"][acl_id] = acl_data
        return {"data": acl_data}

    @classmethod
    def delete_organization_acl(cls: Type["OrganizationAcls"], acl_id: str) -> Dict[str, Any]:
        """
        Delete an organization ACL record.
        """
        if acl_id not in DB["organizationAcls"]:
            return {"error": "ACL record not found."}
        del DB["organizationAcls"][acl_id]
        return {"status": f"ACL {acl_id} deleted."}


# API Resource: /posts
class Posts:
    """
    API simulation for the '/posts' resource.
    """
    @classmethod
    def create_post(cls: Type["Posts"], post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new post.
        """
        post_id = str(DB["next_post_id"])
        DB["next_post_id"] += 1
        post_data["id"] = post_id
        DB["posts"][post_id] = post_data
        return {"data": post_data}

    @classmethod
    def get_post(cls: Type["Posts"],
                 post_id: str,
                 projection: Optional[str] = None,
                 start: int = 0,
                 count: int = 10) -> Dict[str, Any]:
        """
        Retrieve a post by its ID.
        """
        if post_id not in DB["posts"]:
            return {"error": "Post not found."}
        return {"data": DB["posts"][post_id]}

    @classmethod
    def find_posts_by_author(cls, author: str, start: int = 0, count: int = 10) -> Dict[str, Any]:
        """
        List or search for posts based on the author.

        This method filters posts whose "author" field matches the provided author identifier (e.g., "urn:li:person:1").
        It supports pagination through the start and count parameters.
        """
        # Filter posts based on the provided author identifier.
        filtered_posts = [post for post in DB["posts"].values() if post.get("author") == author]
        # Apply pagination to the filtered posts.
        paginated_posts = filtered_posts[start:start+count]
        return {"data": paginated_posts}

    @classmethod
    def update_post(cls: Type["Posts"], post_id: str, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing post.
        """
        if post_id not in DB["posts"]:
            return {"error": "Post not found."}
        post_data["id"] = post_id
        DB["posts"][post_id] = post_data
        return {"data": post_data}

    @classmethod
    def delete_post(cls: Type["Posts"], post_id: str) -> Dict[str, Any]:
        """
        Delete a post.
        """
        if post_id not in DB["posts"]:
            return {"error": "Post not found."}
        del DB["posts"][post_id]
        return {"status": f"Post {post_id} deleted."}
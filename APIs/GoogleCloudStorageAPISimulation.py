"""
Full Python simulation for all resources from the Youtube API Discovery JSON,
with in-memory state, JSON persistence, and embedded tests.

Run this notebook end-to-end to execute tests verifying correctness of each method.
"""
import json
import unittest
import os
from typing import Dict, Any, List, Tuple, Optional, Union

# ---------------------------------------------------------------------------------------
# In-Memory Database Structure for Buckets
# ---------------------------------------------------------------------------------------
# We store bucket data under DB['buckets'][bucketName], which is a dictionary containing:
#   - 'name': str (The name of the bucket)
#   - 'project': str (The project the bucket belongs to)
#   - 'metageneration': str (The metageneration number of the bucket)
#   - 'softDeleted': bool (Indicates if the bucket is soft-deleted)
#   - 'objects': list (List of object names stored in the bucket)
#   - 'enableObjectRetention': bool (Indicates if object retention is enabled)
#   - 'iamPolicy': dict (IAM policy bindings for the bucket)
#   - 'storageLayout': dict (Storage layout details)
#   - 'generation': str (The generation number of the bucket)
#   - 'retentionPolicyLocked': bool (Indicates if the retention policy is locked)
#
# Each bucket entry is uniquely identified by its name within the 'buckets' dictionary.

# Define a global DB for simulation
DB = {
    "buckets": {
        "test-bucket-1": {
            "name": "test-bucket-1",
            "project": "test-project",
            "metageneration": "1",
            "softDeleted": False,
            "objects": [],
            "enableObjectRetention": False,
            "iamPolicy": {"bindings": []},
            "storageLayout": {},
            "generation": "1",
            "retentionPolicyLocked": False
        },
        "test-bucket-2": {
            "name": "test-bucket-2",
            "project": "test-project",
            "metageneration": "2",
            "softDeleted": True,
            "objects": ["file1", "file2"],
            "enableObjectRetention": True,
            "iamPolicy": {"bindings": []},
            "storageLayout": {},
            "generation": "2",
            "retentionPolicyLocked": True
        }
    }
}

# ---------------------------------------------------------------------------------------
# Persistence Class
# ---------------------------------------------------------------------------------------

def save_state(filepath: str) -> None:
    """Saves the current API state to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(DB, f, indent=4)

def load_state(filepath: str) -> None:
    """Loads the API state from a JSON file."""
    global DB
    try:
        with open(filepath, 'r') as f:
            DB = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {filepath}. Starting with an empty state.")
        DB = {"buckets": {}}

# ---------------------------------------------------------------------------------------
# Resource: Buckets
# ---------------------------------------------------------------------------------------

class Buckets:
    """Represents the /buckets resource."""

    @staticmethod
    def delete(
        bucket: str,
        if_metageneration_match: Optional[str] = None,
        if_metageneration_not_match: Optional[str] = None,
        user_project: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Deletes an empty bucket. Deletions are permanent unless soft delete is enabled on the bucket.
        """
        if bucket not in DB["buckets"]:
            return {"error": "Bucket not found"}

        bucket_data = DB["buckets"][bucket]

        if if_metageneration_match:
            if bucket_data.get("metageneration") != if_metageneration_match:
                return {"error": "Metageneration mismatch"}
        if if_metageneration_not_match:
            if bucket_data.get("metageneration") == if_metageneration_not_match:
                return {"error": "Metageneration mismatch"}

        if bucket_data.get("objects"):
            if len(bucket_data["objects"]) > 0:
                return {"error": "Bucket is not empty"}

        del DB["buckets"][bucket]
        return {"message": f"Bucket '{bucket}' deleted successfully"}

    @staticmethod
    def restore(
        bucket: str,
        generation: str,
        projection: str = "full",
        user_project: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Restores a soft-deleted bucket.
        """
        if bucket not in DB["buckets"]:
            return {"error": "Bucket not found"}
        bucket_data = DB["buckets"][bucket]
        if not bucket_data.get("softDeleted"):
            return {"error": "Bucket is not soft deleted"}
        if bucket_data.get("generation") != generation:
            return {"error": "Generation mismatch"}

        bucket_data["softDeleted"] = False
        return {"message": f"Bucket '{bucket}' restored successfully", "bucket": bucket_data}

    @staticmethod
    def relocate(bucket: str) -> Dict[str, Any]:
        """
        Initiates a long-running Relocate Bucket operation on the specified bucket.
        """
        if bucket not in DB["buckets"]:
            return {"error": "Bucket not found"}

        return {"message": f"Relocation initiated for bucket '{bucket}'"}

    @staticmethod
    def get(
        bucket: str,
        generation: Optional[str] = None,
        soft_deleted: bool = False,
        if_metageneration_match: Optional[str] = None,
        if_metageneration_not_match: Optional[str] = None,
        projection: str = "noAcl",
        user_project: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Returns metadata for the specified bucket.
        """
        if bucket not in DB["buckets"]:
            return {"error": "Bucket not found"}

        bucket_data = DB["buckets"][bucket]

        if soft_deleted and not bucket_data.get("softDeleted"):
            return {"error": "Bucket is not soft deleted"}

        if soft_deleted and generation and bucket_data.get("generation") != generation:
            return {"error": "Generation mismatch"}

        if if_metageneration_match:
            if bucket_data.get("metageneration") != if_metageneration_match:
                return {"error": "Metageneration mismatch"}
        if if_metageneration_not_match:
            if bucket_data.get("metageneration") == if_metageneration_not_match:
                return {"error": "Metageneration mismatch"}

        if projection == "full":
            return {"bucket": bucket_data}
        else:
            return {"bucket": {k: v for k, v in bucket_data.items() if k not in ["acl", "defaultObjectAcl"]}}

    @staticmethod
    def getIamPolicy(
        bucket: str,
        options_requested_policy_version: Optional[int] = None,
        user_project: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Returns an IAM policy for the specified bucket.
        """
        if bucket not in DB["buckets"]:
            return {"error": "Bucket not found"}

        bucket_data = DB["buckets"][bucket]
        iam_policy = bucket_data.get("iamPolicy", {"bindings": []})
        if options_requested_policy_version and options_requested_policy_version < 1:
            return {"error": "invalid policy version"}
        return {"iamPolicy": iam_policy}

    @staticmethod
    def getStorageLayout(bucket: str, prefix: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns the storage layout configuration for the specified bucket. Note that this operation requires storage.objects.list permission.
        """
        if bucket not in DB["buckets"]:
            return {"error": "Bucket not found"}
        bucket_data = DB["buckets"][bucket]
        storage_layout = bucket_data.get("storageLayout", {})
        return {"storageLayout": storage_layout}

    @staticmethod
    def insert(
        project: str,
        predefinedAcl: Optional[str] = None,
        predefined_default_object_acl: Optional[str] = None,
        projection: str = "noAcl",
        user_project: Optional[str] = None,
        enableObjectRetention: bool = False,
    ) -> Dict[str, Any]:
        """
        Creates a new bucket.
        """
        bucket_name = f"bucket-{len(DB['buckets']) + 1}"
        new_bucket = {
            "name": bucket_name,
            "project": project,
            "metageneration": 1,
            "softDeleted": False,
            "objects": [],
            "enableObjectRetention": enableObjectRetention,
            "iamPolicy": {"bindings": []},
            "storageLayout": {},
        }
        DB["buckets"][bucket_name] = new_bucket
        if projection == "full":
            return {"bucket": new_bucket}
        else:
            return {"bucket": {k: v for k, v in new_bucket.items() if k not in ["acl", "defaultObjectAcl"]}}

    @staticmethod
    def delete(
        bucket: str,
        if_metageneration_match: Optional[str] = None,
        if_metageneration_not_match: Optional[str] = None,
        user_project: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Deletes an empty bucket. Deletions are permanent unless soft delete is enabled on the bucket.
        """
        if bucket not in DB["buckets"]:
            return {"error": "Bucket not found"}

        bucket_data = DB["buckets"][bucket]

        if if_metageneration_match:
            if bucket_data.get("metageneration") != if_metageneration_match:
                return {"error": "Metageneration mismatch"}
        if if_metageneration_not_match:
            if bucket_data.get("metageneration") == if_metageneration_not_match:
                return {"error": "Metageneration mismatch"}

        if bucket_data.get("objects"):
            if len(bucket_data["objects"]) > 0:
                return {"error": "Bucket is not empty"}

        del DB["buckets"][bucket]
        return {"message": f"Bucket '{bucket}' deleted successfully"}

    @staticmethod
    def restore(
        bucket: str,
        generation: str,
        projection: str = "full",
        user_project: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Restores a soft-deleted bucket.
        """
        if bucket not in DB["buckets"]:
            return {"error": "Bucket not found"}
        bucket_data = DB["buckets"][bucket]
        if not bucket_data.get("softDeleted"):
            return {"error": "Bucket is not soft deleted"}
        if bucket_data.get("generation") != generation:
            return {"error": "Generation mismatch"}

        bucket_data["softDeleted"] = False
        return {"message": f"Bucket '{bucket}' restored successfully", "bucket": bucket_data}

    @staticmethod
    def relocate(bucket: str) -> Dict[str, Any]:
        """
        Initiates a long-running Relocate Bucket operation on the specified bucket.
        """
        if bucket not in DB["buckets"]:
            return {"error": "Bucket not found"}

        return {"message": f"Relocation initiated for bucket '{bucket}'"}

    @staticmethod
    def get(
        bucket: str,
        generation: Optional[str] = None,
        soft_deleted: bool = False,
        if_metageneration_match: Optional[str] = None,
        if_metageneration_not_match: Optional[str] = None,
        projection: str = "noAcl",
        user_project: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Returns metadata for the specified bucket.
        """
        if bucket not in DB["buckets"]:
            return {"error": "Bucket not found"}

        bucket_data = DB["buckets"][bucket]

        if soft_deleted and not bucket_data.get("softDeleted"):
            return {"error": "Bucket is not soft deleted"}

        if soft_deleted and generation and bucket_data.get("generation") != generation:
            return {"error": "Generation mismatch"}

        if if_metageneration_match:
            if bucket_data.get("metageneration") != if_metageneration_match:
                return {"error": "Metageneration mismatch"}
        if if_metageneration_not_match:
            if bucket_data.get("metageneration") == if_metageneration_not_match:
                return {"error": "Metageneration mismatch"}

        if projection == "full":
            return {"bucket": bucket_data}
        else:
            return {"bucket": {k: v for k, v in bucket_data.items() if k not in ["acl", "defaultObjectAcl"]}}

    @staticmethod
    def getIamPolicy(
        bucket: str,
        options_requested_policy_version: Optional[int] = None,
        user_project: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Returns an IAM policy for the specified bucket.
        """
        if bucket not in DB["buckets"]:
            return {"error": "Bucket not found"}

        bucket_data = DB["buckets"][bucket]
        iam_policy = bucket_data.get("iamPolicy", {"bindings": []})
        if options_requested_policy_version and options_requested_policy_version < 1:
            return {"error": "invalid policy version"}
        return {"iamPolicy": iam_policy}

    @staticmethod
    def getStorageLayout(bucket: str, prefix: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns the storage layout configuration for the specified bucket. Note that this operation requires storage.objects.list permission.
        """
        if bucket not in DB["buckets"]:
            return {"error": "Bucket not found"}
        bucket_data = DB["buckets"][bucket]
        storage_layout = bucket_data.get("storageLayout", {})
        return {"storageLayout": storage_layout}

    @staticmethod
    def insert(
        project: str,
        predefinedAcl: Optional[str] = None,
        predefined_default_object_acl: Optional[str] = None,
        projection: str = "noAcl",
        user_project: Optional[str] = None,
        enableObjectRetention: bool = False,
    ) -> Dict[str, Any]:
        """
        Creates a new bucket.
        """
        bucket_name = f"bucket-{len(DB['buckets']) + 1}"
        new_bucket = {
            "name": bucket_name,
            "project": project,
            "metageneration": 1,
            "softDeleted": False,
            "objects": [],
            "enableObjectRetention": enableObjectRetention,
            "iamPolicy": {"bindings": []},
            "storageLayout": {},
        }
        DB["buckets"][bucket_name] = new_bucket
        if projection == "full":
            return {"bucket": new_bucket}
        else:
            return {"bucket": {k: v for k, v in new_bucket.items() if k not in ["acl", "defaultObjectAcl"]}}

    @staticmethod
    def list(
        project: str,
        max_results: int = 1000,
        page_token: Optional[str] = None,
        prefix: Optional[str] = None,
        soft_deleted: bool = False,
        projection: str = "noAcl",
        user_project: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves a list of buckets for a given project.
        """
        matching_buckets = []
        for bucket_name, bucket_data in DB["buckets"].items():
            if bucket_data["project"] == project:
                if prefix and not bucket_name.startswith(prefix):
                    continue
                if soft_deleted and not bucket_data.get("softDeleted", False):
                    continue
                if not soft_deleted and bucket_data.get("softDeleted", False):
                    continue
                if projection == "full":
                    matching_buckets.append(bucket_data)
                else:
                    matching_buckets.append({k: v for k, v in bucket_data.items() if k not in ["acl", "defaultObjectAcl"]})
        return {"items": matching_buckets[:max_results]}

    @staticmethod
    def lockRetentionPolicy(
        bucket: str,
        if_metageneration_match: str,
        user_project: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Locks retention policy on a bucket.
        """
        if bucket not in DB["buckets"]:
            return {"error": "Bucket not found"}
        bucket_data = DB["buckets"][bucket]
        if bucket_data.get("metageneration") != if_metageneration_match:
            return {"error": "Metageneration mismatch"}
        bucket_data["retentionPolicyLocked"] = True
        return {"message": f"Retention policy locked for bucket '{bucket}'"}


    @staticmethod
    def patch(
        bucket: str,
        if_metageneration_match: Optional[str] = None,
        if_metageneration_not_match: Optional[str] = None,
        predefinedAcl: Optional[str] = None,
        predefined_default_object_acl: Optional[str] = None,
        projection: Optional[str] = None,
        user_project: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], int]:
        """
        Patches a bucket. Changes to the bucket will be readable immediately after writing, but configuration changes may take time to propagate.
        """
        if bucket not in DB.get("buckets", {}):
            return {"error": f"Bucket {bucket} not found"}, 404

        bucket_data = DB["buckets"][bucket]

        if if_metageneration_match is not None and str(bucket_data.get("metageneration", 0)) != if_metageneration_match:
            return {"error": "Metageneration mismatch"}, 412

        if if_metageneration_not_match is not None and str(bucket_data.get("metageneration", 0)) == if_metageneration_not_match:
            return {"error": "Metageneration mismatch"}, 412

        # Simulate patching
        if predefinedAcl:
            bucket_data["acl"] = predefinedAcl
        if predefined_default_object_acl:
            bucket_data["defaultObjectAcl"] = predefined_default_object_acl
        bucket_data["metageneration"] = bucket_data.get("metageneration", 0) + 1  # simulate metageneration change.

        if "buckets" not in DB:
            DB["buckets"] = {}
        DB["buckets"][bucket] = bucket_data

        return bucket_data, 200

    @staticmethod
    def setIamPolicy(
        bucket: str,
        user_project: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], int]:
        """Updates an IAM policy for the specified bucket."""
        if bucket not in DB.get("buckets", {}):
            return {"error": f"Bucket {bucket} not found"}, 404

        # Simulate setting IAM policy
        DB["buckets"][bucket]["iamPolicy"] = {"bindings": []}

        return DB["buckets"][bucket]["iamPolicy"], 200

    @staticmethod
    def testIamPermissions(
        bucket: str,
        permissions: str,
        user_project: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], int]:
        """Tests a set of permissions on the given bucket to see which, if any, are held by the caller."""
        if bucket not in DB.get("buckets", {}):
            return {"error": f"Bucket {bucket} not found"}, 404

        # Simulate testing permissions
        return {"permissions": [permissions]}, 200

    @staticmethod
    def update(
        bucket: str,
        if_metageneration_match: Optional[str] = None,
        if_metageneration_not_match: Optional[str] = None,
        predefinedAcl: Optional[str] = None,
        predefined_default_object_acl: Optional[str] = None,
        projection: Optional[str] = None,
        user_project: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], int]:
        """
        Updates a bucket. Changes to the bucket will be readable immediately after writing, but configuration changes may take time to propagate.
        """
        return Buckets.patch(
            bucket,
            if_metageneration_match,
            if_metageneration_not_match,
            predefinedAcl,
            predefined_default_object_acl,
            projection,
            user_project,
        )

# ---------------------------------------------------------------------------------------
# Resource: Channels
# ---------------------------------------------------------------------------------------

class Channels:
    """Represents the /channels resource."""

    @staticmethod
    def stop() -> Tuple[Dict[str, Any], int]:
        """Stop watching resources through this channel."""
        # Simulate stopping a channel
        return {"message": "Channel stopped"}, 200
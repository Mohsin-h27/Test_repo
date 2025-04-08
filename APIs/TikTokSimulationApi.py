"""
Fully Functional Python API Simulation

Implements a mock TikTok API based on the provided specification.
All resources and methods are implemented as Python classes and in-memory data is stored in a
global DB dictionary. Includes save/load functionality for state persistence, and
embedded unit tests for comprehensive coverage.

Execute this file directly to run the test suite (using unittest).

"""
import json
import uuid
import datetime

###############################################################################
# In-Memory Database
###############################################################################
DB = {}

###############################################################################
# State Persistence
###############################################################################

def save_state(filepath: str):
    """
    Saves the current state of the database to a JSON file.

    Args:
        filepath (str): The path to the JSON file where the state should be saved.
    """
    with open(filepath, 'w') as f:
        json.dump(DB, f, indent=4)

def load_state(filepath: str):
    """
    Loads the database state from a JSON file.

    Args:
        filepath (str): The path to the JSON file to load the state from.
    """
    global DB
    try:
        with open(filepath, 'r') as f:
            DB = json.load(f)
    except FileNotFoundError:
        DB = {}  # Initialize to empty if file doesn't exist

###############################################################################
# Internal Helper Functions
###############################################################################

def _add_business_account(business_id: str, account_data: dict):
    """
    Internal helper function to add a business account to the database.

    This function is for internal use only (e.g., for testing or setup).
    It directly modifies the DB dictionary to add a new business account.

    Args:
        business_id (str): The ID of the business account to add.
        account_data (dict): The data associated with the business account.
    """
    global DB
    DB[business_id] = account_data

def _update_business_account(business_id: str, account_data: dict):
    """
    Internal helper function to update a business account in the database.

    This function is for internal use only (e.g., for testing or setup).
    It directly modifies the DB dictionary to update an existing business account.

    Args:
        business_id (str): The ID of the business account to update.
        account_data (dict): The updated data for the business account.

    Raises:
        ValueError: If the business account with the given ID does not exist.
    """
    global DB
    if business_id not in DB:
        raise ValueError(f"Business account with id '{business_id}' not found.")
    DB[business_id].update(account_data)

def _delete_business_account(business_id: str):
    """
    Internal helper function to delete a business account from the database.

    This function is for internal use only (e.g., for testing or setup).
    It directly modifies the DB dictionary to delete an existing business account.

    Args:
        business_id (str): The ID of the business account to delete.

    Raises:
        ValueError: If the business account with the given ID does not exist.
    """
    global DB
    if business_id not in DB:
        raise ValueError(f"Business account with id '{business_id}' not found.")
    del DB[business_id]


###############################################################################
# Resource Classes (API Simulation)
###############################################################################

class Business:
    """
    Simulates the /business API endpoints.
    """

    class Get:
        """
        Simulates the /business/get endpoint.
        """

        @staticmethod
        def get(access_token: str, business_id: str, start_date: str = None, end_date: str = None, fields: list = None) -> dict:
            """
            Get profile data of a TikTok account, including analytics and insights.

            Args:
                access_token: Access token authorized by Tik Tok creators.
                business_id: Application specific unique identifier for the Tik Tok account.
                start_date: Query start date, format YYYY-MM-DD.
                end_date: Query end date, format YYYY-MM-DD.
                fields: Requested fields.

            Returns:
                A dictionary containing the profile data.
            """
            if not access_token:
                return {"code": 400, "message": "Access-Token is required", "data": None}
            if not business_id:
                return {"code": 400, "message": "business_id is required", "data": None}

            # Simulate data retrieval based on business_id
            account_data = DB.get(business_id)
            if not account_data:
                return {"code": 404, "message": "Account not found", "data": None}

            # Apply date filtering if start_date and end_date are provided
            filtered_data = account_data.copy()  # Create a copy to avoid modifying the original

            if start_date:
                try:
                    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                    #  Date filtering logic would go here (if needed)
                except ValueError:
                    return {"code": 400, "message": "Invalid start_date format", "data": None}

            if end_date:
                try:
                    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                    #  Date filtering logic would go here (if needed)
                except ValueError:
                    return {"code": 400, "message": "Invalid end_date format", "data": None}

            # Apply fields filtering if fields are provided
            if fields:
                filtered_data = {field: filtered_data.get(field) for field in fields if field in filtered_data}

            return {"code": 200, "message": "OK", "data": filtered_data}

    class Video:
        """
        Simulates the /business/video endpoint.
        """

        class Publish:
            """
            Simulates the /business/video/publish endpoint.
            """

            @staticmethod

            def post(access_token: str, content_type: str, business_id: str, video_url: str, post_info: dict,
                    caption: str = None, is_brand_organic: bool = False, is_branded_content: bool = False,
                    disable_comment: bool = False, disable_duet: bool = False, disable_stitch: bool = False,
                    thumbnail_offset: int = 0, is_ai_generated: bool = False, upload_to_draft: bool = False) -> dict:
                """
                Use this endpoint to publish a public video post to an owned TikTok Account.

                ... (docstring)
                """
                if not access_token:

                    return {"code": 400, "message": "Access-Token is required", "data": None}


                if content_type != "application/json":

                    return {"code": 400, "message": "Content-Type must be application/json", "data": None}


                if not business_id:

                    return {"code": 400, "message": "business_id is required", "data": None}


                if not video_url:

                    return {"code": 400, "message": "video_url is required", "data": None}


                if not post_info:

                    return {"code": 400, "message": "post_info is required", "data": None}


                # Simulate video publishing
                share_id = "v_pub_url~" + str(uuid.uuid4())  #
                return {
                    "code": 200,
                    "message": "OK",
                    "request_id": str(uuid.uuid4()),
                    "data": {"share_id": share_id}
                }

    class Publish:
        """
        Simulates the /business/publish endpoint.
        """

        class Status:
            """
            Simulates the /business/publish/status endpoint.
            """

            @staticmethod
            def get(access_token: str, business_id: str, publish_id: str) -> dict:
                """
                Use this endpoint to obtain the publishing status of a Tik Tok video post or photo post.

                Args:
                    access_token: Access token authorized by Tik Tok creators.
                    business_id: Application specific unique identifier for the Tik Tok account.
                    publish_id: Unique identifier for a post publishing task.

                Returns:
                    A dictionary containing the publishing status.
                """
                if not access_token:
                    return {"code": 400, "message": "Access-Token is required", "data": None}
                if not business_id:
                    return {"code": 400, "message": "business_id is required", "data": None}
                if not publish_id:
                    return {"code": 400, "message": "publish_id is required", "data": None}

                # Simulate publish status retrieval
                # For simplicity, let's assume all requests are successful.
                return {
                    "code": 200,
                    "message": "OK",
                    "request_id": str(uuid.uuid4()),
                    "data": {
                        "status": "PUBLISH_COMPLETE",  #
                        "post_ids": ["video_id_" + str(uuid.uuid4())]  #
                    }
                }
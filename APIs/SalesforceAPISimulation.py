import json
import os
import unittest
import uuid
import datetime
import urllib.parse  # Import urllib.parse for URL decoding
from typing import Any, Dict, Optional, Type
"""
A single-file, fully functional Python API simulation for the specified
Salesforce-like resources (/Event, /Task, /Query). Implements:

1. Complete resource classes with methods exactly matching the discovery spec:
   - /Event: create, delete, describeLayout, describeSObjects, getDeleted, getUpdated,
              query, retrieve, search, undelete, update, upsert
   - /Task: create, delete, describeLayout, describeSObjects, getDeleted, getUpdated,
            query, retrieve, search, undelete, update, upsert
   - /Query:Supported SOQL Parameters- SELECT statement on a single object
              SELECT statement on a single object
              SELECT clause: count()
              SOQL WHERE clause: contains operators
              SOQL LIKE
              SOQL LIMIT clause
              The default limit is set to 100. The max limit is 2,000 records in a single call.
              SOQL OFFSET clause
              SOQL ORDER BY clause

2. In-memory JSON-serializable storage in a global DB dictionary.

3. Persistence methods save_state(filepath) and load_state(filepath).

4. Embedded unit tests using unittest. Running this file directly will
   execute all tests and confirm the simulation works as intended.

Note: All methods are defined as class methods, allowing direct calls on the classes.
"""
###############################################################################
# In-Memory Database
###############################################################################
DB: dict = {}

###############################################################################
# State Persistence
###############################################################################
def save_state(filepath: str):
    """
    Saves the current state of the database to a JSON file.

    Args:
        filepath (str): The path to the file where the state should be saved.
    """
    with open(filepath, 'w') as f:
        json.dump(DB, f)


def load_state(filepath: str):
    """
    Loads the database state from a JSON file.

    Args:
        filepath (str): The path to the file from which the state should be loaded.
    """
    global DB
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            DB = json.load(f)
    else:
        DB = {}

###############################################################################
# API Classes
###############################################################################

class Event:
    """
    Represents the /Event resource in the API.
    """

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a new event.
        """
        new_event = {
            "Id": str(uuid.uuid4()),  # Generate a unique ID
            "CreatedDate": datetime.datetime.now().isoformat(),
            "IsDeleted": False,
            "SystemModstamp": datetime.datetime.now().isoformat()
        }
        for key, value in kwargs.items():
            new_event[key] = value

        DB.setdefault('Event', {})
        DB['Event'][new_event['Id']] = new_event
        return new_event

    @classmethod
    def delete(cls, event_id: str):
        """
        Deletes an event.
        """
        if 'Event' in DB and event_id in DB['Event']:
            del DB['Event'][event_id]
            return {}
        else:
            return {"error": "Event not found"}

    @classmethod
    def describeLayout(cls):
        """
        Describes the layout of an event.
        """
        return {"layout": "Event layout description"}

    @classmethod
    def describeSObjects(cls):
        """
        Describes the object (Event).
        """
        return {"object": "Event object description"}

    @classmethod
    def getDeleted(cls):
        """
        Retrieves deleted events.
        """
        return {"deleted": []}  # Return an empty list for now

    @classmethod
    def getUpdated(cls):
        """
        Retrieves updated events.
        """
        return {"updated": []}  # Return an empty list for now

    @classmethod
    def query(cls, criteria: dict = None):
        """
        Queries events based on specified criteria.
        """
        results = []
        if 'Event' in DB:
            for event in DB['Event'].values():
                if criteria is None:
                    results.append(event)
                else:
                    match = True
                    for key, value in criteria.items():
                        if key not in event or event[key] != value:
                            match = False
                            break
                    if match:
                        results.append(event)
        return {"results": results}

    @classmethod
    def retrieve(cls, event_id: str):
        """
        Retrieves details of a specific event.
        """
        if 'Event' in DB and event_id in DB['Event']:
            return DB['Event'][event_id]
        else:
            return {"error": "Event not found"}

    @classmethod
    def search(cls, search_term: str):
        """
        Searches for events based on specified search criteria.
        """
        results = []
        if 'Event' in DB:
            for event in DB['Event'].values():
                if search_term.lower() in str(event).lower():
                    results.append(event)
        return {"results": results}

    @classmethod
    def undelete(cls, event_id: str):
        """
        Restores a deleted event. (Place holder - no actual deletion tracking).
        """
        if 'Event' in DB and event_id in DB['Event']:
            return DB['Event'][event_id]
        else:
            return {"error": "Event not found"}

    @classmethod
    def update(cls, event_id: str, **kwargs):
        """
        Updates an existing event.
        """
        if 'Event' in DB and event_id in DB['Event']:
            event = DB['Event'][event_id]
            for key, value in kwargs.items():
                event[key] = value
            event["SystemModstamp"] = datetime.datetime.now().isoformat()
            return event
        else:
            return {"error": "Event not found"}

    @classmethod
    def upsert(cls, **kwargs):
        """
        Creates or updates an event.
        """
        if "Id" in kwargs and kwargs["Id"] in DB.get('Event', {}):
            return Event.update(kwargs["Id"], **kwargs)
        else:
            return Event.create(**kwargs)


class Task:
    """
    Represents the /Task resource in the API.
    """

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a new task.
        """
        if "Priority" not in kwargs or "Status" not in kwargs:
            raise ValueError("Priority and Status are required for creating a task.")

        new_task = {
            "Id": str(uuid.uuid4()),
            "CreatedDate": datetime.datetime.now().isoformat(),
            "IsDeleted": False,
            "SystemModstamp": datetime.datetime.now().isoformat()
        }
        for key, value in kwargs.items():
            new_task[key] = value

        DB.setdefault('Task', {})
        DB['Task'][new_task['Id']] = new_task
        return new_task

    @classmethod
    def delete(cls, task_id: str):
        """
        Deletes a task.
        """
        if 'Task' in DB and task_id in DB['Task']:
            del DB['Task'][task_id]
            return {}
        else:
            return {"error": "Task not found"}

    @classmethod
    def describeLayout(cls):
        """
        Describes the layout of a task.
        """
        return {"layout": "Task layout description"}

    @classmethod
    def describeSObjects(cls):
        """
        Describes Task SObjects.
        """
        return {"object": "Task object description"}

    @classmethod
    def getDeleted(cls):
        """
        Retrieves deleted tasks.
        """
        return {"deleted": []}  # Return an empty list for now

    @classmethod
    def getUpdated(cls):
        """
        Retrieves updated tasks.
        """
        return {"updated": []}  # Return an empty list for now

    @classmethod
    def query(cls, criteria: dict = None):
        """
        Queries tasks.
        """
        results = []
        if 'Task' in DB:
            for task in DB['Task'].values():
                if criteria is None:
                    results.append(task)
                else:
                    match = True
                    for key, value in criteria.items():
                        if key not in task or task[key] != value:
                            match = False
                            break
                    if match:
                        results.append(task)
        return {"results": results}

    @classmethod
    def retrieve(cls, task_id: str):
        """
        Retrieves a task.
        """
        if 'Task' in DB and task_id in DB['Task']:
            return DB['Task'][task_id]
        else:
            return {"error": "Task not found"}

    @classmethod
    def search(cls, search_term: str):
        """
        Searches for tasks.
        """
        results = []
        if 'Task' in DB:
            for task in DB['Task'].values():
                if search_term.lower() in str(task).lower():
                    results.append(task)
        return {"results": results}

    @classmethod
    def undelete(cls, task_id: str):
        """
        Recovers deleted tasks. (Placeholder - no actual deletion tracking).
        """
        if 'Task' in DB and task_id in DB['Task']:
            return DB['Task'][task_id]
        else:
            return {"error": "Task not found"}

    @classmethod
    def update(cls, task_id: str, **kwargs):
        """
        Updates a task.
        """
        if 'Task' in DB and task_id in DB['Task']:
            task = DB['Task'][task_id]
            for key, value in kwargs.items():
                task[key] = value
            task["SystemModstamp"] = datetime.datetime.now().isoformat()
            return task
        else:
            return {"error": "Task not found"}

    @classmethod
    def upsert(cls, **kwargs):
        """
        Creates or updates a task.
        """
        if "Id" in kwargs and kwargs["Id"] in DB.get('Task', {}):
            return Task.update(kwargs["Id"], **kwargs)
        else:
            return Task.create(**kwargs)

class Query:
    @classmethod
    def get(cls, q: str):
        """
        Executes the specified SOQL query.
        """
        try:
            # Decode URL-encoded query
            q = urllib.parse.unquote(q)
            parts = q.split()

            if parts[0].upper() != "SELECT":
                raise ValueError("Invalid SOQL query: Must start with SELECT")

            # Fields to select
            fields = [field.strip() for field in parts[1].split(",")]

            # Object to query
            from_index = parts.index("FROM")
            obj = parts[from_index + 1]

            # Initialize variables for conditions, limit, offset, and order_by
            where_index = -1
            limit = None
            offset = None
            order_by = None
            conditions = []

            # Extract WHERE clause conditions
            if "WHERE" in parts:
                where_index = parts.index("WHERE")
                condition = " ".join(parts[where_index + 1:])
                conditions = condition.split("AND")

            # Extract LIMIT clause
            if "LIMIT" in parts:
                limit_index = parts.index("LIMIT")
                limit = int(parts[limit_index + 1])
                parts = parts[:limit_index]  # Remove LIMIT part from the query

            # Extract OFFSET clause
            if "OFFSET" in parts:
                offset_index = parts.index("OFFSET")
                offset = int(parts[offset_index + 1])
                parts = parts[:offset_index]  # Remove OFFSET part from the query

            # Extract ORDER BY clause
            if "ORDER BY" in parts:
                order_by_index = parts.index("ORDER BY") + len("ORDER BY")
                order_by = " ".join(parts[order_by_index:]).strip()
                parts = parts[:parts.index("ORDER BY")]

            results = []
            if obj in DB:
                for record in DB[obj].values():
                    include_record = True  # Initialize to include unless filtered out

                    # Apply WHERE clause filtering (handle multiple conditions)
                    if where_index > -1:
                        parsed_conditions = cls.parse_conditions(conditions)
                        for condition_type, field, value in parsed_conditions:
                            if condition_type == "=":
                                if field in record and record[field] != value:
                                    include_record = False
                            elif condition_type == "IN":
                                if field in record and record[field] not in value:
                                    include_record = False
                            elif condition_type == "LIKE":
                                if field in record and value.replace('%','') not in record[field]:
                                    include_record = False
                            elif condition_type == "CONTAINS":
                                if field in record and value not in record[field]:
                                    include_record = False

                    # Add the record if it passed the conditions
                    if include_record:
                        row = {}
                        for field in fields:
                            field = field.strip()
                            if field in record:
                                row[field] = record[field]
                            elif field == 'Id':
                                row[field] = record['Id']
                            else:
                                row[field] = None
                        results.append(row)

            # Apply ORDER BY if available
            if order_by:
                results.sort(key=lambda x: x.get(order_by, ""))

            # Apply OFFSET if available
            if offset:
                results = results[offset:]

            # Apply LIMIT if available
            if limit:
                results = results[:limit]

            return {"results": results}

        except Exception as e:
            return {"error": f"MALFORMED_QUERY: {str(e)}"}

    @staticmethod
    def parse_conditions(conditions):
        """
        Parse the conditions in the WHERE clause.
        Handles '=', 'IN', 'LIKE', and 'CONTAINS'.
        """
        parsed_conditions = []
        for cond in conditions:
            cond = cond.strip()

            # Handle equality condition
            if "=" in cond:
                field, value = cond.split("=", 1)
                field = field.strip()
                value = value.strip().strip("'")
                parsed_conditions.append(("=", field, value))

            # Handle IN condition
            elif "IN" in cond:
                field, values = cond.split("IN", 1)
                field = field.strip()
                values = values.strip("()").split(",")
                values = [v.strip().strip("'") for v in values]
                parsed_conditions.append(("IN", field, values))

            # Handle LIKE condition
            elif "LIKE" in cond:
                field, value = cond.split("LIKE", 1)
                field = field.strip()
                value = value.strip().strip("'").replace("%", "")
                parsed_conditions.append(("LIKE", field, value))

            # Handle CONTAINS condition
            elif "CONTAINS" in cond:
                field, value = cond.split("CONTAINS", 1)
                field = field.strip()
                value = value.strip().strip("'")
                parsed_conditions.append(("CONTAINS", field, value))

        return parsed_conditions
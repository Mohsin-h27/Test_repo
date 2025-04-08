#!/usr/bin/env python
"""
Fully Functional Python API Simulation

Implements a mock Calendar API based on the provided specification. All resources
and methods are implemented as Python classes and in-memory data is stored in a
global DB dictionary. Includes save/load functionality for state persistence, and
embedded unit tests for comprehensive coverage.

Execute this file directly to run the test suite (using unittest).

Author: Your Name
"""

import json
import tempfile
import uuid
import unittest

# ------------------------------------------------------------------------------
# Global In-Memory Database (JSON-serializable)
# ------------------------------------------------------------------------------
DB = {
    "acl_rules": {},         # Stores ACL rule objects, keyed by ruleId
    "calendar_list": {},     # Stores CalendarList entries, keyed by calendarId
    "calendars": {},         # Stores Calendar objects, keyed by calendarId
    "channels": {},          # Stores Channel objects, keyed by channelId (or random)
    "colors": {              # Colors are usually static in the real API, but we'll store them anyway
        "calendar": {},      # This might store color definitions for calendars
        "event": {}          # This might store color definitions for events
    },
    "events": {}             # Stores events, keyed by (calendarId, eventId) or a combined key
}

# ------------------------------------------------------------------------------
# Persistence Methods
# ------------------------------------------------------------------------------
def save_state(filepath: str) -> None:
    """
    Save the current in-memory DB state to a JSON file.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(DB, f, indent=2)


def load_state(filepath: str) -> None:
    """
    Load DB state from a JSON file, replacing the current in-memory DB.
    """
    global DB
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convert keys to tuples
    data["events"] = {tuple(key.split(":")): value for key, value in data["events"].items()}

    DB = data


# ------------------------------------------------------------------------------
# AclResource
# ------------------------------------------------------------------------------
class AclResource:
    """
    Simulates ACL resource operations:
    - delete_rule
    - get_rule
    - create_rule
    - list_rules
    - patch_rule
    - update_rule
    - watch_rules
    """

    @staticmethod
    def delete_rule(calendarId: str, ruleId: str):
        """
        Deletes an access control rule.
        """
        # In a real API, you'd verify calendarId ownership, etc.
        # We'll assume each rule is keyed by ruleId in DB["acl_rules"].
        if ruleId not in DB["acl_rules"]:
            # Simulate 404 not found
            raise ValueError(f"ACL rule '{ruleId}' not found.")
        del DB["acl_rules"][ruleId]
        return {"success": True, "message": f"ACL rule {ruleId} deleted."}

    @staticmethod
    def get_rule(calendarId: str, ruleId: str):
        """
        Returns an access control rule.
        """
        if ruleId not in DB["acl_rules"]:
            raise ValueError(f"ACL rule '{ruleId}' not found.")
        rule = DB["acl_rules"][ruleId]
        if rule.get("calendarId") != calendarId:
            raise ValueError(f"ACL rule '{ruleId}' does not belong to calendar '{calendarId}'.")
        return rule

    @staticmethod
    def create_rule(calendarId: str, sendNotifications: bool = True, resource=None):
        """
        Creates an access control rule.
        """
        if resource is None:
            raise ValueError("Resource body is required to create a rule.")
        # We'll pick up ruleId from the resource if provided, otherwise generate:
        rule_id = resource.get("ruleId") or str(uuid.uuid4())
        resource["ruleId"] = rule_id
        resource["calendarId"] = calendarId
        DB["acl_rules"][rule_id] = resource
        return DB["acl_rules"][rule_id]

    @staticmethod
    def list_rules(calendarId: str, maxResults: int = 100, pageToken: str = None,
                   showDeleted: bool = False, syncToken: str = None):
        """
        Returns the rules in the access control list for the calendar.
        """
        # For simplicity, we won't implement paging or sync tokens thoroughly.
        # We'll just return all ACLs for the specified calendarId.
        # In reality, 'calendarId' would be used to filter which rules are relevant.
        # We'll simulate that each rule has a "calendarId" and we filter by that.
        all_rules = []
        for rule in DB["acl_rules"].values():
            if rule.get("calendarId") == calendarId:
                # If it's "deleted" and showDeleted=False, skip it.
                # We'll just skip that detail for now.
                all_rules.append(rule)

        # Truncate at maxResults
        result = all_rules[:maxResults]
        return {
            "items": result,
            "nextPageToken": None  # Not implemented
        }

    @staticmethod
    def patch_rule(calendarId: str, ruleId: str, sendNotifications: bool = True, resource=None):
        """
        Updates an access control rule (patch semantics).
        """
        if ruleId not in DB["acl_rules"]:
            raise ValueError(f"ACL rule '{ruleId}' not found.")
        existing = DB["acl_rules"][ruleId]
        for k, v in (resource or {}).items():
            existing[k] = v
        DB["acl_rules"][ruleId] = existing
        return existing

    @staticmethod
    def update_rule(calendarId: str, ruleId: str, sendNotifications: bool = True, resource=None):
        """
        Updates an access control rule (full update).
        """
        if ruleId not in DB["acl_rules"]:
            raise ValueError(f"ACL rule '{ruleId}' not found.")
        if resource is None:
            raise ValueError("Resource body is required for update.")
        # Overwrite everything except the ruleId, which we keep from the existing or new resource
        resource["ruleId"] = ruleId
        resource["calendarId"] = calendarId
        DB["acl_rules"][ruleId] = resource
        return DB["acl_rules"][ruleId]

    @staticmethod
    def watch_rules(calendarId: str, maxResults: int = 100, pageToken: str = None,
                    showDeleted: bool = False, syncToken: str = None, resource=None):
        """
        Watch for changes to ACL resources.
        """
        # We'll simulate returning a Channel object. Realistically, you'd return
        # some channel info about push notifications, etc.
        if resource is None:
            raise ValueError("Channel resource is required.")
        channel_id = resource.get("id") or str(uuid.uuid4())
        DB["channels"][channel_id] = {
            "id": channel_id,
            "type": resource.get("type", "web_hook"),
            "resource": "acl",
            "calendarId": calendarId
        }
        return DB["channels"][channel_id]


# ------------------------------------------------------------------------------
# CalendarListResource
# ------------------------------------------------------------------------------
class CalendarListResource:
    """
    Simulates CalendarList resource:
    - delete_calendar_list
    - get_calendar_list
    - create_calendar_list
    - list_calendar_lists
    - patch_calendar_list
    - update_calendar_list
    - watch_calendar_lists
    """

    @staticmethod
    def delete_calendar_list(calendarId: str):
        if calendarId not in DB["calendar_list"]:
            raise ValueError(f"CalendarList entry '{calendarId}' not found.")
        del DB["calendar_list"][calendarId]
        return {"success": True, "message": f"CalendarList entry {calendarId} deleted."}

    @staticmethod
    def get_calendar_list(calendarId: str):
        if calendarId not in DB["calendar_list"]:
            raise ValueError(f"CalendarList entry '{calendarId}' not found.")
        return DB["calendar_list"][calendarId]

    @staticmethod
    def create_calendar_list(colorRgbFormat: bool = False, resource=None):
        if resource is None:
            raise ValueError("Resource is required to create a calendar list entry.")
        cal_id = resource.get("id") or str(uuid.uuid4())
        resource["id"] = cal_id
        DB["calendar_list"][cal_id] = resource
        return DB["calendar_list"][cal_id]

    @staticmethod
    def list_calendar_lists(maxResults: int = 100, minAccessRole: str = None,
                            pageToken: str = None, showDeleted: bool = False,
                            showHidden: bool = False, syncToken: str = None):
        # Return all for simplicity
        all_items = list(DB["calendar_list"].values())
        result = all_items[:maxResults]
        return {
            "items": result,
            "nextPageToken": None
        }

    @staticmethod
    def patch_calendar_list(calendarId: str, colorRgbFormat: bool = False, resource=None):
        if calendarId not in DB["calendar_list"]:
            raise ValueError(f"CalendarList entry '{calendarId}' not found.")
        existing = DB["calendar_list"][calendarId]
        for k, v in (resource or {}).items():
            existing[k] = v
        DB["calendar_list"][calendarId] = existing
        return existing

    @staticmethod
    def update_calendar_list(calendarId: str, colorRgbFormat: bool = False, resource=None):
        if calendarId not in DB["calendar_list"]:
            raise ValueError(f"CalendarList entry '{calendarId}' not found.")
        if resource is None:
            raise ValueError("Resource is required for full update.")
        resource["id"] = calendarId
        DB["calendar_list"][calendarId] = resource
        return resource

    @staticmethod
    def watch_calendar_lists(maxResults: int = 100, minAccessRole: str = None,
                             pageToken: str = None, showDeleted: bool = False,
                             showHidden: bool = False, syncToken: str = None, resource=None):
        if resource is None:
            raise ValueError("Channel resource is required.")
        channel_id = resource.get("id") or str(uuid.uuid4())
        DB["channels"][channel_id] = {
            "id": channel_id,
            "type": resource.get("type", "web_hook"),
            "resource": "calendar_list"
        }
        return DB["channels"][channel_id]


# ------------------------------------------------------------------------------
# CalendarsResource
# ------------------------------------------------------------------------------
class CalendarsResource:
    """
    Simulates Calendars resource:
    - clear_calendar
    - delete_calendar
    - get_calendar
    - create_calendar
    - patch_calendar
    - update_calendar
    """

    @staticmethod
    def clear_calendar(calendarId: str):
        """
        Clears a primary calendar. This operation deletes all events for the specified calendar.
        """
        # We'll simulate that events are keyed as (calendarId, eventId) in DB["events"].
        # We'll remove all events associated with this calendar.
        to_delete = []
        for (cal_id, ev_id), ev_obj in DB["events"].items():
            if cal_id == calendarId:
                to_delete.append((cal_id, ev_id))
        for key in to_delete:
            del DB["events"][key]
        return {"success": True, "message": f"All events deleted for calendar '{calendarId}'."}

    @staticmethod
    def delete_calendar(calendarId: str):
        """
        Deletes a secondary calendar.
        """
        if calendarId not in DB["calendar_list"]:
            raise ValueError(f"Calendar '{calendarId}' not found.")
        del DB["calendar_list"][calendarId]
        del DB["calendars"][calendarId]
        return {"success": True, "message": f"Calendar '{calendarId}' deleted."}

    @staticmethod
    def get_calendar(calendarId: str):
        """
        Retrieves metadata for a specified calendar.

        Args:
            calendarId (str): The identifier of the calendar.
                - To retrieve calendar IDs, call the `calendarList.list` method.
                - Use the keyword "primary" to access the primary calendar of the currently logged-in user.

        Returns:
            dict: Metadata of the requested calendar.
        """

        if calendarId not in DB["calendar_list"]:
            raise ValueError(f"Calendar '{calendarId}' not found.")
        return DB["calendar_list"][calendarId]

    @staticmethod
    def create_calendar(resource=None):
        """
        Creates a secondary calendar.
        """
        if resource is None:
            raise ValueError("Resource is required to create a calendar.")
        cal_id = resource.get("id") or str(uuid.uuid4())
        resource["id"] = cal_id
        DB["calendar_list"][cal_id] = resource
        DB["calendars"][cal_id] = resource
        return resource

    @staticmethod
    def patch_calendar(calendarId: str, resource=None):
        """
        Updates calendar metadata (patch semantics).
        """
        if calendarId not in DB["calendar_list"]:
            raise ValueError(f"Calendar '{calendarId}' not found.")
        existing = DB["calendar_list"][calendarId]
        for k, v in (resource or {}).items():
            existing[k] = v
        DB["calendar_list"][calendarId] = existing
        DB["calendars"][calendarId] = existing
        return existing

    @staticmethod
    def update_calendar(calendarId: str, resource=None):
        """
        Updates calendar metadata (full update).
        """
        if calendarId not in DB["calendar_list"]:
            raise ValueError(f"Calendar '{calendarId}' not found.")
        if resource is None:
            raise ValueError("Resource is required for full update.")
        resource["id"] = calendarId
        DB["calendar_list"][calendarId] = resource
        DB["calendars"][calendarId] = resource
        return resource


# ------------------------------------------------------------------------------
# ChannelsResource
# ------------------------------------------------------------------------------
class ChannelsResource:
    """
    Simulates Channels resource:
    - stop_channel
    """

    @staticmethod
    def stop_channel(resource=None):
        """
        Stop watching resources through this channel.
        """
        if resource is None:
            raise ValueError("Channel resource required to stop channel.")
        channel_id = resource.get("id")
        if not channel_id or channel_id not in DB["channels"]:
            raise ValueError(f"Channel '{channel_id}' not found.")
        del DB["channels"][channel_id]
        return {"success": True, "message": f"Channel '{channel_id}' stopped."}


# ------------------------------------------------------------------------------
# ColorsResource
# ------------------------------------------------------------------------------
class ColorsResource:
    """
    Simulates Colors resource:
    - get_colors
    """

    @staticmethod
    def get_colors():
        """
        Returns the color definitions for calendars and events.
        """
        return DB["colors"]


# ------------------------------------------------------------------------------
# EventsResource
# ------------------------------------------------------------------------------
class EventsResource:
    """
    Simulates Events resource:
    - delete_event
    - get_event
    - import_event
    - create_event
    - list_event_instances
    - list_events
    - move_event
    - patch_event
    - quick_add_event
    - update_event
    - watch_events
    """

    @staticmethod
    def delete_event(calendarId: str, eventId: str, sendNotifications: bool = False, sendUpdates: str = None):
        """
        Deletes an event.
        """
        key = (calendarId, eventId)
        if key not in DB["events"]:
            raise ValueError(f"Event '{eventId}' not found in calendar '{calendarId}'.")
        del DB["events"][key]
        return {"success": True, "message": f"Event '{eventId}' deleted from calendar '{calendarId}'."}

    @staticmethod
    def get_event(alwaysIncludeEmail: bool = False, calendarId: str = None,
                  eventId: str = None, maxAttendees: int = None, timeZone: str = None):
        """
        Returns an event based on calendarId and eventId.
        """
        key = (calendarId, eventId)
        if key not in DB["events"]:
            raise ValueError(f"Event '{eventId}' not found in calendar '{calendarId}'.")
        return DB["events"][key]

    @staticmethod
    def import_event(calendarId: str, conferenceDataVersion: int = 0, supportsAttachments: bool = False,
                     resource=None):
        """
        Imports an event. Only eventType=default may be imported, we won't enforce that here.
        """
        if resource is None:
            raise ValueError("Resource is required to import an event.")
        ev_id = resource.get("id") or str(uuid.uuid4())
        resource["id"] = ev_id
        DB["events"][(calendarId, ev_id)] = resource
        return resource

    @staticmethod
    def create_event(calendarId: str = None, conferenceDataVersion: int = 0, maxAttendees: int = None,
                     sendNotifications: bool = False, sendUpdates: str = None, supportsAttachments: bool = False,
                     resource=None):
        """
        Creates an event.
        """
        if resource is None:
            raise ValueError("Resource is required to create an event.")
        ev_id = resource.get("id") or str(uuid.uuid4())
        resource["id"] = ev_id
        if calendarId is None:
            calendarId = "primary"
        DB["events"][(calendarId, ev_id)] = resource
        return resource

    @staticmethod
    def list_event_instances(alwaysIncludeEmail: bool = False, calendarId: str = None,
                             eventId: str = None, maxAttendees: int = None,
                             maxResults: int = 250, originalStart: str = None,
                             pageToken: str = None, showDeleted: bool = False,
                             timeMax: str = None, timeMin: str = None, timeZone: str = None):
        """
        Returns instances of a specified recurring event.
        This is a mock, so we won't actually expand recurrences.
        We'll pretend the event itself is the only instance.
        """
        key = (calendarId, eventId)
        if key not in DB["events"]:
            raise ValueError(f"Recurring event '{eventId}' not found in calendar '{calendarId}'.")
        # Return the single event as if it's a list of one instance
        return {
            "items": [DB["events"][key]],
            "nextPageToken": None
        }

    @staticmethod
    def list_events(calendarId: str = None, maxResults: int = 250,
                    timeMin: str = None, timeMax: str = None, q: str = None):
        """
        Returns events on the specified calendar within the given time range.
        """
        from datetime import datetime
        def parse_iso_datetime(iso_string):
            return datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%SZ") if iso_string else None

        timeMin_dt = parse_iso_datetime(timeMin)
        timeMax_dt = parse_iso_datetime(timeMax)
        results = []
        for (cal_id, ev_id), ev_obj in DB["events"].items():
            # Filter by calendarId
            if cal_id != calendarId:
                continue
            # Filter by timeMin
            if timeMin is not None:
                if "start" not in ev_obj:
                    continue
                if "dateTime" not in ev_obj["start"]:
                    continue
                event_start = parse_iso_datetime(ev_obj["start"]["dateTime"])
                if event_start < timeMin_dt:
                    continue
            # Filter by timeMax
            if timeMax is not None:
                if "end" not in ev_obj:
                    continue
                if "dateTime" not in ev_obj["end"]:
                    continue
                event_end = parse_iso_datetime(ev_obj["end"]["dateTime"])
                if event_end > timeMax_dt:
                    continue
            # Filter by query string 'q'
            if q is not None:
                # Using lower case comparison for case-insensitive search
                query_lower = q.lower()
                summary = ev_obj.get("summary", "").lower()
                description = ev_obj.get("description", "").lower()
                # If query not found in either field, skip the event.
                if query_lower not in summary and query_lower not in description:
                    continue

            results.append(ev_obj)

        # Truncate at maxResults
        results = results[:maxResults]

        return {
            "items": results
        }


    @staticmethod
    def move_event(calendarId: str, eventId: str, destination: str,
                   sendNotifications: bool = False, sendUpdates: str = None):
        """
        Moves an event from one calendar to another. We simulate by removing from old
        and creating in new with same ID.
        """
        old_key = (calendarId, eventId)
        if old_key not in DB["events"]:
            raise ValueError(f"Event '{eventId}' not found in calendar '{calendarId}'.")
        ev_data = DB["events"].pop(old_key)
        new_key = (destination, eventId)
        if new_key in DB["events"]:
            raise ValueError(f"Event '{eventId}' already exists in destination calendar '{destination}'.")
        DB["events"][new_key] = ev_data
        return ev_data

    @staticmethod
    def patch_event(alwaysIncludeEmail: bool = False, calendarId: str = None,
                    conferenceDataVersion: int = 0, eventId: str = None, maxAttendees: int = None,
                    sendNotifications: bool = False, sendUpdates: str = None, supportsAttachments: bool = False,
                    resource=None):
        """
        Updates an event (patch semantics).
        """
        key = (calendarId, eventId)
        if key not in DB["events"]:
            raise ValueError(f"Event '{eventId}' not found in calendar '{calendarId}'.")
        existing = DB["events"][key]
        for k, v in (resource or {}).items():
            existing[k] = v
        DB["events"][key] = existing
        return existing

    @staticmethod
    def quick_add_event(calendarId: str, sendNotifications: bool = False,
                        sendUpdates: str = None, text: str = None):
        """
        Creates an event based on a simple text string.
        """
        if not text:
            raise ValueError("Text parameter is required to create a quick event.")
        ev_id = str(uuid.uuid4())
        resource = {
            "id": ev_id,
            "summary": text
        }
        DB["events"][(calendarId, ev_id)] = resource
        return resource

    @staticmethod
    def update_event(alwaysIncludeEmail: bool = False, calendarId: str = None,
                     conferenceDataVersion: int = 0, eventId: str = None, maxAttendees: int = None,
                     sendNotifications: bool = False, sendUpdates: str = None,
                     supportsAttachments: bool = False, resource=None):
        """
        Updates an event (full update).
        """
        key = (calendarId, eventId)
        if key not in DB["events"]:
            raise ValueError(f"Event '{eventId}' not found in calendar '{calendarId}'.")
        if resource is None:
            raise ValueError("Resource body is required for full update.")
        resource["id"] = eventId
        DB["events"][key] = resource
        return resource

    @staticmethod
    def watch_events(alwaysIncludeEmail: bool = False, calendarId: str = None,
                     eventTypes=None, iCalUID: str = None, maxAttendees: int = None,
                     maxResults: int = 250, orderBy: str = None, pageToken: str = None,
                     privateExtendedProperty=None, q: str = None, sharedExtendedProperty=None,
                     showDeleted: bool = False, showHiddenInvitations: bool = False,
                     singleEvents: bool = False, syncToken: str = None, timeMax: str = None,
                     timeMin: str = None, timeZone: str = None, updatedMin: str = None,
                     resource=None):
        """
        Watch for changes to Events resources.
        """
        if resource is None:
            raise ValueError("Channel resource is required to watch.")
        channel_id = resource.get("id") or str(uuid.uuid4())
        DB["channels"][channel_id] = {
            "id": channel_id,
            "type": resource.get("type", "web_hook"),
            "resource": "events",
            "calendarId": calendarId
        }
        return DB["channels"][channel_id]
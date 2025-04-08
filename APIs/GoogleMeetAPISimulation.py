"""
Full Python simulation for all resources from the Youtube API Discovery JSON,
with in-memory state, JSON persistence, and embedded tests.

Run this notebook end-to-end to execute tests verifying correctness of each method.
"""
import json
import unittest
import os
from typing import Dict, Any, List, Optional, Union

# ---------------------------------------------------------------------------------------
# In-Memory Database Structure for Conference Records and Related Data
# ---------------------------------------------------------------------------------------
# This database stores conference records, recordings, transcripts, entries, participants, and participant sessions.
#
# DB['conferenceRecords']: { conferenceId: { 'id': conferenceId, 'start_time': startTime }, ... }
#   - Stores conference records, indexed by conference ID.
#   - Each conference record includes its ID and start time.
#
# DB['recordings']: { recordingId: { 'id': recordingId, 'parent': conferenceId, 'start_time': startTime }, ... }
#   - Stores recording records, indexed by recording ID.
#   - Each recording record includes its ID, parent conference ID, and start time.
#
# DB['transcripts']: { transcriptId: { 'id': transcriptId, 'parent': conferenceId, 'start_time': startTime }, ... }
#   - Stores transcript records, indexed by transcript ID.
#   - Each transcript record includes its ID, parent conference ID, and start time.
#
# DB['entries']: { entryId: { 'id': entryId, 'parent': transcriptId, 'start_time': startTime }, ... }
#   - Stores transcript entries, indexed by entry ID.
#   - Each entry record includes its ID, parent transcript ID, and start time.
#
# DB['participants']: { participantId: { 'id': participantId, 'conferenceRecordId': conferenceId, 'join_time': joinTime }, ... }
#   - Stores participant records, indexed by participant ID.
#   - Each participant record includes its ID, associated conference record ID, and join time.
#
# DB['participantSessions']: { sessionId: { 'id': sessionId, 'participantId': participantId, 'join_time': joinTime }, ... }
#   - Stores participant session records, indexed by session ID.
#   - Each session record includes its ID, associated participant ID, and join time.


DB = {
    "conferenceRecords": {
            "conf1": {"id": "conf1", "start_time": "10:00"},
            "conf2": {"id": "conf2", "start_time": "11:00"},
            "conf3": {"id": "conf3", "start_time": "12:00"},
            "conf4": {"id": "conf4", "start_time": "13:00"},
            "conf5": {"id": "conf5", "start_time": "14:00"},
        },
     "recordings": {
            "rec1": {"id": "rec1", "parent": "conf1", "start_time": "10:05"},
            "rec2": {"id": "rec2", "parent": "conf1", "start_time": "10:10"},
            "rec3": {"id": "rec3", "parent": "conf2", "start_time": "11:05"},
        },
    "transcripts": {
            "trans1": {"id": "trans1", "parent": "conf1", "start_time": "10:15"},
            "trans2": {"id": "trans2", "parent": "conf1", "start_time": "10:20"},
            "trans3": {"id": "trans3", "parent": "conf2", "start_time": "11:15"},
        },
    "entries": {
            "entry1": {"id": "entry1", "parent": "trans1", "start_time": "10:16"},
            "entry2": {"id": "entry2", "parent": "trans1", "start_time": "10:18"},
            "entry3": {"id": "entry3", "parent": "trans2", "start_time": "10:21"},
        },
    "participants": {
            "part1": {"id": "part1", "conferenceRecordId": "conf1", "join_time": "09:59"},
            "part2": {"id": "part2", "conferenceRecordId": "conf1", "join_time": "10:01"},
            "part3": {"id": "part3", "conferenceRecordId": "conf2", "join_time": "11:00"},
        },
    "participantSessions": {
            "session1": {"id": "session1", "participantId": "part1", "join_time": "09:59"},
            "session2": {"id": "session2", "participantId": "part2", "join_time": "10:01"},
            "session3": {"id": "session3", "participantId": "part1", "join_time": "10:30"},
        },
    "spaces": {
        "space1": {"id": "spaces/jQCFfuBOdN5z",  "meetingCode": "abc-mnop-xyz",
                    "meetingUri": "https://meet.google.com/abc-mnop-xyz", "accessType": "TRUSTED", "entryPointAccess": "ALL"},
        "space2": {"id": "spaces/A1B2C3D4E5",  "meetingCode": "def-ghi-jkl",
                    "meetingUri": "https://meet.google.com/def-ghi-jkl", "accessType": "RESTRICTED", "entryPointAccess": "CREATOR_APP_ONLY"},
        "space3": {"id": "spaces/X9Y8Z7W6V5",  "meetingCode": "mno-pqr-stu",
                    "meetingUri": "https://meet.google.com/mno-pqr-stu", "accessType": "OPEN", "entryPointAccess": "ALL"},
    }
}

# ---------------------------------------------------------------------------------------
# Persistence Class
# ---------------------------------------------------------------------------------------
class GoogleMeetAPI:
  """
  The top-level class that handles the in-memory DB and provides
  save/load functionality for JSON-based state persistence.
  """

  @staticmethod
  def save_state(filepath: str) -> None:
      """
      Saves the current state of the database to a JSON file.

      Args:
          filepath: The path to the JSON file where the state will be saved.
      """
      with open(filepath, 'w') as f:
          json.dump(DB, f, indent=4)

  def load_state(filepath: str):
      """
      Loads the state of the database from a JSON file.

      Args:
          filepath: The path to the JSON file to load the state from.
      """
      global DB
      try:
        with open(filepath, 'r') as f:
            DB = json.load(f)
      except FileNotFoundError:
          print(f"State file {filepath} not found. Starting with empty state.")

# ---------------------------------------------------------------------------------------
# Resource: Spaces
# ---------------------------------------------------------------------------------------

class Spaces:

    @staticmethod
    def patch(name: str,
              update_mask: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Updates details about a meeting space.

        Args:
            name: The name of the space to update.
            update_mask: A dictionary containing the fields to update and their new values.

        Returns:
            The updated space details, or an error message if the space is not found.
        """
        if name not in DB["spaces"]:
            return {"error": "Space not found"}

        space = DB["spaces"][name].copy()
        if update_mask:
            for field, value in update_mask.items():
                if field in space:
                    space[field] = value

        DB["spaces"][name] = space
        return space

    @staticmethod
    def get(name: str) -> Dict[str, Any]:
        """
        Gets details about a meeting space.

        Args:
            name: The name of the space to retrieve.

        Returns:
            The space details, or an error message if the space is not found.
        """
        if name in DB["spaces"]:
            return DB["spaces"][name]
        else:
            return {"error": "Space not found"}

    @staticmethod
    def create(space_name: str,
               space_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new meeting space.

        Args:
            space_name: The name of the new space.
            space_content: A dictionary containing the details of the new space.

        Returns:
            A message indicating the space was created successfully.
        """
        new_space = space_content.copy()
        DB["spaces"][space_name] = new_space
        return {"message": f"Space {space_name} created successfully"}

    @staticmethod
    def endActiveConference(name: str) -> Dict[str, Any]:
        """
        Ends an active conference in a meeting space, if one exists.

        Args:
            name: The name of the space.

        Returns:
            A message indicating whether an active conference was ended.
        """
        if name not in DB["spaces"]:
            return {"error": "Space not found"}

        space = DB["spaces"][name]
        if "activeConference" in space:
            del space["activeConference"]
            DB["spaces"][name] = space
            return {"message": "Active conference ended"}
        else:
            return {"message": "No active conference to end"}

# ---------------------------------------------------------------------------------------
# Resource: Conference Records
# ---------------------------------------------------------------------------------------

class ConferenceRecords:

    @staticmethod
    def get(name: str) -> Dict[str, Any]:
        """
        Gets a conference record by conference ID.

        Args:
            name: Resource name of the conference.

        Returns:
            The conference record, or an error message if not found.
        """
        if name in DB["conferenceRecords"]:
            return DB["conferenceRecords"][name]
        else:
            return {"error": "Conference record not found"}

    @staticmethod
    def list(filter: Optional[str] = None,
             pageToken: Optional[str] = None,
             pageSize: Optional[int] = None) -> Dict[str, Any]:
        """
        Lists the conference records. By default, ordered by start time and in descending order.

        Args:
            filter: An optional filter string to apply to the records.
            pageToken: An optional token for pagination.
            pageSize: An optional maximum number of records to return.

        Returns:
            A dictionary containing the list of conference records and a next page token, if applicable.
        """
        records: List[Dict[str, Any]] = list(DB["conferenceRecords"].values())

        if filter:
            records = [r for r in records if filter in str(r)]

        if pageToken:
            try:
                start_index = records.index(DB["conferenceRecords"][pageToken]) + 1
                records = records[start_index:]
            except (ValueError, KeyError):
                return {"error": "Invalid pageToken"}

        if pageSize:
            records = records[:pageSize]

        next_pageToken: Optional[str] = None
        if pageSize and len(DB["conferenceRecords"]) > pageSize and records and records[-1]["name"] in DB["conferenceRecords"]:
            next_pageToken = records[-1]["name"]

        return {"conferenceRecords": records, "nextPageToken": next_pageToken}

    # ---------------------------------------------------------------------------------------
    # Resource: Recordings
    # ---------------------------------------------------------------------------------------

    class Recordings:

      @staticmethod
      def get(name: str) -> Dict[str, Any]:
        """
        Gets a recording by recording ID.

        Args:
            name: Resource name of the recording.

        Returns:
            The recording details, or an error message if not found.
        """
        if name in DB["recordings"]:
            return DB["recordings"][name]
        else:
            return {"error": "Recording not found"}

      @staticmethod
      def list(parent: str,
               parent_conference_record: str,
               pageSize: Optional[int] = None, pageToken: Optional[str] = None) -> Dict[str, Any]:
        """
        Lists the recording resources from the conference record. By default, ordered by start time and in ascending order.

        Args:
            parent: The parent resource name (e.g., "conferenceRecords/{parent_conference_record}").
            parent_conference_record: The ID of the parent conference record.
            pageSize: An optional maximum number of recordings to return.
            pageToken: An optional token for pagination.

        Returns:
            A dictionary containing the list of recordings and a next page token, if applicable.
        """
        if parent != f"conferenceRecords/{parent_conference_record}":
            return {"error": "Invalid parent"}

        if parent_conference_record not in DB["conferenceRecords"]:
            return {"error": "Conference record not found"}

        recordings: List[Dict[str, Any]] = DB["conferenceRecords"][parent_conference_record].get("recordings", [])

        if pageToken:
            try:
                start_index = recordings.index(next(r for r in recordings if r["name"] == pageToken)) + 1
                recordings = recordings[start_index:]
            except (ValueError, StopIteration):
                return {"error": "Invalid pageToken"}

        if pageSize:
            recordings = recordings[:pageSize]

        nextpageToken: Optional[str] = None
        if pageSize and len(recordings) > pageSize and recordings:
            nextpageToken = recordings[-1]["name"]

        return {"recordings": recordings, "nextPageToken": nextpageToken}

    # ---------------------------------------------------------------------------------------
    # Resource: Transcripts
    # ---------------------------------------------------------------------------------------

    class Transcripts:

      @staticmethod
      def get(name: str) -> Dict[str, Any]:
        """
        Gets a transcript by transcript ID.

        Args:
            name: Resource name of the transcript.

        Returns:
            The transcript, or an error message if not found.
        """
        if name in DB["transcripts"]:
            return DB["transcripts"][name]
        else:
            return {"error": "Transcript not found"}

      @staticmethod
      def list(parent: str,
               parent_conference_record: str,
               pageToken: Optional[str] = None,
               pageSize: Optional[int] = None) -> Dict[str, Any]:
        """
        Lists the set of transcripts from the conference record. By default, ordered by start time and in ascending order.

        Args:
            parent: The parent resource name (e.g., "conferenceRecords/{parent_conference_record}").
            parent_conference_record: The ID of the parent conference record.
            pageToken: An optional token for pagination.
            pageSize: An optional maximum number of transcripts to return.

        Returns:
            A dictionary containing the list of transcripts and a next page token, if applicable.
        """
        if parent != f"conferenceRecords/{parent_conference_record}":
            return {"error": "Invalid parent"}

        if parent_conference_record not in DB["conferenceRecords"]:
            return {"error": "Conference record not found"}

        transcripts: List[Dict[str, Any]] = DB["conferenceRecords"][parent_conference_record].get("transcripts", [])

        if pageToken:
            try:
                start_index = transcripts.index(next(t for t in transcripts if t["name"] == pageToken)) + 1
                transcripts = transcripts[start_index:]
            except (ValueError, StopIteration):
                return {"error": "Invalid pageToken"}

        if pageSize:
            transcripts = transcripts[:pageSize]

        next_pageToken: Optional[str] = None
        if pageSize and len(transcripts) > pageSize and transcripts:
            next_pageToken = transcripts[-1]["name"]

        return {"transcripts": transcripts, "nextPageToken": next_pageToken}

      # ---------------------------------------------------------------------------------------
      # Resource: Entries
      # ---------------------------------------------------------------------------------------

      class Entries:

        @staticmethod
        def get(name: str) -> Dict[str, Any]:
            """
            Gets a TranscriptEntry resource by entry ID.

            Args:
                name: Resource name of the TranscriptEntry.

            Returns:
                The transcript entry, or an error message if not found.
            """
            if name in DB["entries"]:
                return DB["entries"][name]
            else:
                return {"error": "TranscriptEntry not found"}

        @staticmethod
        def list(parent: str,
                 pageSize: Optional[int] = None,
                 pageToken: Optional[str] = None) -> Dict[str, Any]:
            """
            Lists the structured transcript entries per transcript. By default, ordered by start time and in ascending order.

            Args:
                parent: The parent resource name (e.g., "conferenceRecords/{conference_record_id}/transcripts/{transcript_id}").
                pageSize: An optional maximum number of entries to return.
                pageToken: An optional token for pagination.

            Returns:
                A dictionary containing the list of transcript entries and a next page token, if applicable.
            """
            parts = parent.split('/')
            if len(parts) != 4 or parts[0] != "conferenceRecords" or parts[2] != "transcripts":
                return {"error": "Invalid parent"}
            conference_record_id = parts[1]
            transcript_id = parts[3]

            if conference_record_id not in DB["conferenceRecords"]:
                return {"error": "Conference record not found"}

            transcript = next((t for t in DB["conferenceRecords"][conference_record_id].get("transcripts", []) if t["name"] == transcript_id), None)
            if not transcript:
                return {"error": "Transcript not found"}

            entries: List[Dict[str, Any]] = transcript.get("entries", [])

            if pageToken:
                try:
                    start_index = entries.index(next(e for e in entries if e["name"] == pageToken)) + 1
                    entries = entries[start_index:]
                except (ValueError, StopIteration):
                    return {"error": "Invalid pageToken"}

            if pageSize:
                entries = entries[:pageSize]

            next_pageToken: Optional[str] = None
            if pageSize and len(entries) > pageSize and entries:
                next_pageToken = entries[-1]["name"]

            return {"entries": entries, "nextPageToken": next_pageToken}

    # ---------------------------------------------------------------------------------------
    # Resource: Participants
    # ---------------------------------------------------------------------------------------

    class Participants:

      @staticmethod
      def list(parent: str,
               parent_conference_record: str,
               filter: Optional[str] = None,
               pageSize: Optional[int] = None,
               pageToken: Optional[str] = None) -> Dict[str, Any]:
        """
        Lists the participants in a conference record. By default, ordered by join time and in descending order.

        Args:
            parent: The parent resource name (e.g., "conferenceRecords/{parent_conference_record}").
            parent_conference_record: The ID of the parent conference record.
            filter: An optional filter string to apply to the participants.
            pageSize: An optional maximum number of participants to return.
            pageToken: An optional token for pagination.

        Returns:
            A dictionary containing the list of participants and a next page token, if applicable.
        """
        if parent != f"conferenceRecords/{parent_conference_record}":
            return {"error": "Invalid parent"}

        if parent_conference_record not in DB["conferenceRecords"]:
            return {"error": "Conference record not found"}

        participants: List[Dict[str, Any]] = DB["conferenceRecords"][parent_conference_record].get("participants", [])

        if filter:
            participants = [p for p in participants if filter in str(p)]

        if pageToken:
            try:
                start_index = participants.index(next(p for p in participants if p["name"] == pageToken)) + 1
                participants = participants[start_index:]
            except (ValueError, StopIteration):
                return {"error": "Invalid pageToken"}

        if pageSize:
            participants = participants[:pageSize]

        next_pageToken: Optional[str] = None
        if pageSize and len(participants) > pageSize and participants:
            next_pageToken = participants[-1]["name"]

        return {"participants": participants, "nextPageToken": next_pageToken}


      @staticmethod
      def get(name: str) -> Dict[str, Any]:
        """
        Gets a participant by participant ID.

        Args:
            name: The ID of the participant to retrieve.

        Returns:
            The participant details, or an error message if not found.
        """
        for record in DB["conferenceRecords"].values():
            if "participants" in record:
                for participant in record["participants"]:
                    if participant["name"] == name:
                        return participant
        return {"error": "Participant not found"}

      # ---------------------------------------------------------------------------------------
      # Resource: Participants/ParticipantSessions
      # ---------------------------------------------------------------------------------------

      class ParticipantSessions:


        @staticmethod
        def list(parent: str,
                 filter: Optional[str] = None,
                 pageSize: Optional[int] = None,
                 pageToken: Optional[str] = None) -> Dict[str, Any]:
            """
            Lists the participant sessions of a participant in a conference record. By default, ordered by join time and in descending order.

            Args:
                parent: The parent resource name (e.g., "conferenceRecords/{conference_record_id}/participants/{participant_id}").
                filter: An optional filter string to apply to the participant sessions.
                pageSize: An optional maximum number of participant sessions to return.
                pageToken: An optional token for pagination.

            Returns:
                A dictionary containing the list of participant sessions and a next page token, if applicable.
            """
            parts = parent.split('/')
            if len(parts) != 4 or parts[0] != "conferenceRecords" or parts[2] != "participants":
                return {"error": "Invalid parent"}

            conference_record_id = parts[1]
            participant_id = parts[3]

            if conference_record_id not in DB["conferenceRecords"]:
                return {"error": "Conference record not found"}

            participant = next((p for p in DB["conferenceRecords"][conference_record_id].get("participants", []) if p["name"] == participant_id), None)
            if not participant:
                return {"error": "Participant not found"}

            sessions: List[Dict[str, Any]] = participant.get("participantSessions", [])

            if filter:
                sessions = [s for s in sessions if filter in str(s)]

            if pageToken:
                try:
                    start_index = sessions.index(next(s for s in sessions if s["name"] == pageToken)) + 1
                    sessions = sessions[start_index:]
                except (ValueError, StopIteration):
                    return {"error": "Invalid pageToken"}

            if pageSize:
                sessions = sessions[:pageSize]

            next_pageToken: Optional[str] = None
            if pageSize and len(sessions) > pageSize and sessions:
                next_pageToken = sessions[-1]["name"]

            return {"participantSessions": sessions, "nextPageToken": next_pageToken}


        @staticmethod
        def get(name: str) -> Dict[str, Any]:
            """
            Gets a participant session by participant session ID.

            Args:
                name: The ID of the participant session to retrieve.

            Returns:
                The participant session details, or an error message if not found.
            """
            for record in DB["conferenceRecords"].values():
                if "participants" in record:
                    for participant in record["participants"]:
                        if "participantSessions" in participant:
                            for session in participant["participantSessions"]:
                                if session["name"] == name:
                                    return session
            return {"error": "Participant session not found"}
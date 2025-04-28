import os
import subprocess
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import mimetypes
from google.oauth2 import service_account
import json
from googleapiclient.http import MediaFileUpload


# === CONFIGURATION ===
FOLDER_CONFIGS = {
    "APIs/": "1hC2gnOjsybwJ2cN3cbhyZXmEzmAk4QVl"
}

# === HELPERS ===

import requests

def get_changed_files_via_api(pr_number):
    """Fetch changed files in a PR using GitHub REST API."""
    print(f"🔍 Getting changed files for PR #{pr_number} using REST API...")
    
    repo = os.getenv("GITHUB_REPOSITORY")  # example: "user/repo"
    token = os.getenv("GITHUB_TOKEN")  # personal access token or GitHub Actions token
    
    if not repo or not token:
        print("❌ Missing GITHUB_REPOSITORY or GITHUB_TOKEN environment variables.")
        return []
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    
    changed_files = []
    page = 1

    while True:
        response = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            print(f"❌ Failed to fetch changed files: {response.status_code} {response.text}")
            return []
        
        files = response.json()
        if not files:
            break
        
        changed_files.extend(file["filename"] for file in files)
        page += 1

    return changed_files



def authenticate():
    """Authenticate using service account."""
    creds_dict = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds)

def get_changed_api_folders(changed_files):
    """Identify which API subfolders have changes."""
    changed_files_updated = list()
    for file_path in changed_files:
        if file_path.startswith("APIs/"):
            changed_files_updated.append(file_path)

    return changed_files_updated


def find_file_in_folder(service, folder_id, name, mime_type=None):
    """Find file/folder with `name` in given `folder_id`."""
    query = f"'{folder_id}' in parents and trashed=false and name='{name}'"
    if mime_type:
        query += f" and mimeType='{mime_type}'"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    files = results.get('files', [])
    return files[0] if files else None

def traverse_path_to_file(service, root_folder_id, path_segments):
    """Traverse path, creating missing folders/files, and return file ID."""
    current_id = root_folder_id

    for segment in path_segments[:-1]:
        folder = find_file_in_folder(service, current_id, segment, mime_type='application/vnd.google-apps.folder')
        if not folder:
            # Create missing folder
            folder_metadata = {
                'name': segment,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [current_id]
            }
            folder = service.files().create(body=folder_metadata, fields='id').execute()
        current_id = folder['id']

    # Handle the final file
    filename = path_segments[-1]
    file = find_file_in_folder(service, current_id, filename)
    if not file:
        # Create missing file (empty)
        file_metadata = {
            'name': filename,
            'parents': [current_id],
            'mimeType': 'application/octet-stream'
        }
        media = service.files().create(body=file_metadata, fields='id').execute()
        return media['id']
    
    return file['id']

def update_drive_file_content(service, file_id, local_path):
    """Update the Drive file content from local file."""
    mime_type, _ = mimetypes.guess_type(local_path)
    media = MediaFileUpload(local_path, resumable=True)
    try:
        service.files().update(
            fileId=file_id,
            media_body=media,
            media_mime_type=mime_type
        ).execute()
    except HttpError as error:
        raise RuntimeError(f"Drive update failed: {error}")

def sync_local_file_to_drive_path(drive_folder_id: str, filepath: str):
    """
    Sync local file to a matching path in Drive folder.
    Example: filepath='spaces/messages/init.py'
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Local file '{filepath}' not found.")

    service = authenticate()
    path_parts = filepath.replace("\\", "/").split("/")
    try:
        file_id = traverse_path_to_file(service, drive_folder_id, path_parts[1:])
        update_drive_file_content(service, file_id, filepath)
        print(f"✅ Synced: {filepath} → Drive file ID {file_id}")
    except Exception as e:
        print(f"❌ Error: {e}")



# === MAIN ===

if __name__ == "__main__":
    pr_number = os.getenv("PR_NUMBER")
    if not pr_number:
        print("❌ PR number not found in environment.")
        exit(1)

    changed_files = get_changed_files_via_api(pr_number)
    if not changed_files:
        print("🟡 No changes detected in PR.")
        exit(0)

    service = authenticate()
    changed_api_files = get_changed_api_folders(changed_files)

    if changed_api_files:
        api_drive_folder_id = FOLDER_CONFIGS["APIs/"]
        for file in changed_api_files:
            sync_local_file_to_drive_path(api_drive_folder_id, file)
    else:
        print("🟡 No API changes detected in PR.")

                

import os
import subprocess
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
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
    changed_folders = set()
    for file_path in changed_files:
        if file_path.startswith("APIs/"):
            parts = file_path.split('/')
            if len(parts) >= 2:
                changed_folders.add(parts[1])
    return list(changed_folders)

def find_drive_file(service, parent_id, name, is_folder=True):
    """Find file or folder by name inside a parent folder."""
    mime_type = "application/vnd.google-apps.folder" if is_folder else None
    query = f"'{parent_id}' in parents and name = '{name}' and trashed = false"
    if mime_type:
        query += f" and mimeType = '{mime_type}'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    return files[0] if files else None

def delete_drive_folder(service, folder_id):
    """Move a folder to trash."""
    try:
        service.files().update(fileId=folder_id, body={"trashed": True}).execute()
        print(f"🗑️ Trashed folder ID: {folder_id}")
    except Exception as e:
        print(f"⚠️ Failed to trash folder: {e}")

def upload_folder_to_drive(service, local_folder_path, parent_drive_id):
    """Recursively upload a local folder and maintain subfolders structure."""
    folder_name = os.path.basename(local_folder_path)
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_drive_id]
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    folder_id = folder['id']

    for root, dirs, files in os.walk(local_folder_path):
        # Create subfolder paths inside Drive
        rel_path = os.path.relpath(root, local_folder_path)
        if rel_path == '.':
            current_drive_folder_id = folder_id
        else:
            # Create nested folders if needed
            path_parts = rel_path.split(os.sep)
            current_drive_folder_id = folder_id
            for part in path_parts:
                existing = find_drive_file(service, current_drive_folder_id, part, is_folder=True)
                if existing:
                    current_drive_folder_id = existing['id']
                else:
                    subfolder_metadata = {
                        'name': part,
                        'mimeType': 'application/vnd.google-apps.folder',
                        'parents': [current_drive_folder_id]
                    }
                    created = service.files().create(body=subfolder_metadata, fields='id').execute()
                    current_drive_folder_id = created['id']

        for file_name in files:
            file_path = os.path.join(root, file_name)
            upload_file_to_drive(service, file_path, current_drive_folder_id)
    print(f"✅ Uploaded full folder: {folder_name}")
    return folder_id


def upload_file_to_drive(service, local_file_path, parent_folder_id):
    """Upload a single file."""
    file_metadata = {
        'name': os.path.basename(local_file_path),
        'parents': [parent_folder_id]
    }
    media = MediaFileUpload(local_file_path, resumable=True)
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"⬆️ Uploaded file: {local_file_path}")

def find_drive_folder_for_file(file_path):
    """Find the drive folder ID based on file path prefix."""
    for prefix, folder_id in FOLDER_CONFIGS.items():
        if file_path.startswith(prefix):
            return folder_id
    return None

def upload_or_update_file(service, local_path, drive_folder_id):
    """Upload or update an individual file."""
    file_name = os.path.basename(local_path)
    query = f"'{drive_folder_id}' in parents and name = '{file_name}' and trashed = false"
    result = service.files().list(q=query, fields="files(id, parents)").execute()
    existing_files = result.get("files", [])

    if existing_files:
        for file in existing_files:
            try:
                media = MediaFileUpload(local_path, resumable=True)
                service.files().update(
                    fileId=file['id'],
                    media_body=media,
                    supportsAllDrives=True,
                    fields='id, name'
                ).execute()
                print(f"⬆️ Updated: {local_path}")
            except Exception as e:
                print(f"⚠️ Cannot update {file_name}: {e}")
    else:
        try:
            metadata = {"name": file_name, "parents": [drive_folder_id]}
            media = MediaFileUpload(local_path, resumable=True)
            service.files().create(body=metadata, media_body=media, fields="id").execute()
            print(f"📁 Created: {file_name}")
        except Exception as e:
            print(f"⚠️ Cannot create {file_name}: {e}")

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
    changed_api_folders = get_changed_api_folders(changed_files)

    if changed_api_folders:
        api_drive_folder_id = FOLDER_CONFIGS["APIs/"]
        for api_folder_name in changed_api_folders:
            # 1. Delete existing folder in Drive
            drive_api_folder = find_drive_file(service, api_drive_folder_id, api_folder_name)
            if drive_api_folder:
                delete_drive_folder(service, drive_api_folder["id"])

            # 2. Upload fresh local folder
            local_api_path = os.path.join("APIs", api_folder_name)
            if os.path.exists(local_api_path):
                upload_folder_to_drive(service, local_api_path, api_drive_folder_id)
            else:
                print(f"⚠️ Local API folder not found: {local_api_path}")

                

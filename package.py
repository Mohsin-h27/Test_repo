import os
import subprocess
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

DRIVE_APP_FOLDER_ID = "1mBqlXzksUFBThWal__fNAYkQATTWUyW8"

def get_changed_files(pr_number):
    print(f"🔍 Getting changed files for PR #{pr_number}...")
    result = subprocess.run(
        ["gh", "pr", "diff", str(pr_number), "--name-only"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("❌ Failed to get changed files from GitHub CLI.")
        print(result.stderr)
        return []

    changed_files = result.stdout.strip().splitlines()
    return changed_files

def authenticate():
    creds_dict = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds)

def delete_drive_folder_contents(service, folder_id):
    query = f"'{folder_id}' in parents"
    while True:
        results = service.files().list(q=query, fields="files(id)").execute()
        files = results.get("files", [])
        if not files:
            break
        for file in files:
            service.files().delete(fileId=file["id"]).execute()

def upload_folder(service, local_folder_path, drive_folder_id):
    folder_map = {local_folder_path: drive_folder_id}
    for root, dirs, files in os.walk(local_folder_path):
        parent_id = folder_map[root]
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            metadata = {
                "name": dir_name,
                "parents": [parent_id],
                "mimeType": "application/vnd.google-apps.folder",
            }
            folder = service.files().create(body=metadata, fields="id").execute()
            folder_map[dir_path] = folder["id"]

        for file_name in files:
            file_path = os.path.join(root, file_name)
            metadata = {"name": file_name, "parents": [parent_id]}
            media = MediaFileUpload(file_path, resumable=True)
            service.files().create(body=metadata, media_body=media, fields="id").execute()

if __name__ == "__main__":
    pr_number = os.getenv("PR_NUMBER")
    if not pr_number:
        print("❌ PR number not found in environment.")
        exit(1)

    changed_files = get_changed_files(pr_number)
    if not any(f.startswith("app/") for f in changed_files):
        print("🟡 No changes in App folder. Skipping upload.")
        exit(0)

    print("✅ Changes detected in App/. Starting sync...")

    service = authenticate()
    delete_drive_folder_contents(service, DRIVE_APP_FOLDER_ID)
    upload_folder(service, "app", DRIVE_APP_FOLDER_ID)

    print("✅ App folder synced to Google Drive.")

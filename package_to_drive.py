import os
import subprocess
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Mapping of GitHub folder prefixes to Google Drive folder IDs
FOLDER_CONFIGS = {
    "APIs/": "1ALwo4BhKBDU7CZDecYH2D6YUlX-MM7CZ",
    "Unit Tests/": "12j_G3LYQq6N0l_ODddCNEn1w3SXPF701",
    "DefaultDBs/": "1KYlSrkyPl7Z3bhiUMVDq0rKYyJasSS9r",
    "NLDescriptions/Machine Ingestible/": "19eJPV08VqELlelolOt6qzgv4UrBZI6ux",
    "NLDescriptions/Human Friendly/": "1YcV7DBCjb7xdDiGXgt5hx5YhdpoF4ZPS",
}

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
    return result.stdout.strip().splitlines()

def authenticate():
    creds_dict = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds)

def upload_or_update_file(service, local_path, drive_folder_id):
    file_name = os.path.basename(local_path)

    # Look for existing file with the same name in the folder
    query = f"'{drive_folder_id}' in parents and name = '{file_name}' and trashed = false"
    result = service.files().list(q=query, fields="files(id, parents)").execute()
    existing_files = result.get("files", [])

    for file in existing_files:
        try:
            service.files().delete(fileId=file["id"]).execute()
            print(f"🗑️ Deleted existing: {file_name}")
        except Exception as e:
            print(f"⚠️ Cannot delete {file_name}: {e}. Trying to remove from folder...")
            try:
                service.files().update(
                    fileId=file["id"],
                    removeParents=drive_folder_id,
                    fields="id, parents"
                ).execute()
                print(f"📁 Removed from folder instead: {file_name}")
            except Exception as inner_e:
                print(f"❌ Failed to remove {file_name} from folder: {inner_e}")
                return  # Skip upload if unable to clean up

    metadata = {"name": file_name, "parents": [drive_folder_id]}
    media = MediaFileUpload(local_path, resumable=True)
    service.files().create(body=metadata, media_body=media, fields="id").execute()
    print(f"⬆️ Uploaded: {local_path}")

def find_drive_folder_for_file(file_path):
    for prefix, folder_id in FOLDER_CONFIGS.items():
        if file_path.startswith(prefix):
            return folder_id
    return None

if __name__ == "__main__":
    pr_number = os.getenv("PR_NUMBER")
    if not pr_number:
        print("❌ PR number not found in environment.")
        exit(1)

    changed_files = get_changed_files(pr_number)
    if not changed_files:
        print("🟡 No changes detected in PR.")
        exit(0)

    service = authenticate()

    for file_path in changed_files:
        drive_folder_id = find_drive_folder_for_file(file_path)
        if not drive_folder_id:
            continue  # Not a tracked folder

        if not os.path.exists(file_path):
            print(f"⚠️ File not found locally: {file_path}")
            continue

        upload_or_update_file(service, file_path, drive_folder_id)

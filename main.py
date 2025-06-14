from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

FOLDER_ID = "1m7Tu1L2MoZSt0PludUBaneaL64TTmS6J"
CREDS_PATH = "credentials.json"

creds = service_account.Credentials.from_service_account_file(
    CREDS_PATH, scopes=["https://www.googleapis.com/auth/drive"]
)
drive_service = build("drive", "v3", credentials=creds)

@app.route("/", methods=["POST"])
def handle_request():
    data = request.json
    name = data.get("name", "default.txt")
    content = data.get("content", "Hello from Cloud Run.")

    file_metadata = {
        "name": name,
        "parents": [FOLDER_ID],
        "mimeType": "text/plain",
    }

    from googleapiclient.http import MediaInMemoryUpload
    media = MediaInMemoryUpload(content.encode("utf-8"), mimetype="text/plain")

    created_file = drive_service.files().create(
        body=file_metadata, media_body=media, fields="id"
    ).execute()

    return jsonify({"file_id": created_file["id"]})

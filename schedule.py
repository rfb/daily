import os, json, re
import requests

from today import today

from dotenv import load_dotenv

load_dotenv()

API_BASE = os.environ.get("AZURA_API_BASE")
STATION_ID = os.environ.get("AZURA_STATION_ID")
API_KEY = os.environ.get("AZURA_API_KEY")
PLAYLIST_ID = os.environ.get("PLAYLIST_ID")

filename = "shedfm-daily-%s.mp3" % today.strftime("%Y-%m-%d")

print("uploading %s" % filename)

files = { "file": (filename, open(filename, 'rb'), 'audio/mpeg') }
headers = { "X-API-Key": API_KEY }

requests.post(
    API_BASE + "/station/%s/files/upload" % STATION_ID,
    headers=headers,
    files=files).raise_for_status()

print("requesting list of media files")

response = requests.get(
    API_BASE + "/station/%s/files" % STATION_ID,
    headers=headers)
response.raise_for_status()

records = response.json()

for rec in filter(lambda rec: re.match("shedfm-daily", rec["path"]), records):
    payload = {"playlists": [ { "id": PLAYLIST_ID } ] if rec["path"] == filename else []}

    print("setting playlists on %s to %s", (rec["path"], json.dumps(payload)))

    requests.put(
        API_BASE + "/station/%s/file/%d" % (STATION_ID, rec["id"]),
        headers=headers | { "content-type": "application/json" },
        data=json.dumps(payload)).raise_for_status()

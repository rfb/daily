import os, json, re
import requests

from datetime import datetime
from zoneinfo import ZoneInfo
from glom import glom, Match, Iter

from dotenv import load_dotenv

import logging
import http.client

load_dotenv()
tz = ZoneInfo(os.environ.get("TZ"))
date = datetime.now(tz)

filename = "shedfm-daily-%s.mp3" % date.strftime("%Y-%m-%d")

API_BASE = os.environ.get("AZURA_API_BASE")
STATION_ID = os.environ.get("AZURA_STATION_ID")
API_KEY = os.environ.get("AZURA_API_KEY")
PLAYLIST_ID = os.environ.get("PLAYLIST_ID")

files = { "file": (filename, open(filename, 'rb'), 'audio/mpeg') }
headers = { "X-API-Key": API_KEY }

print("uploading %s" % filename)

requests.post(
    API_BASE + "/station/%s/files/upload" % STATION_ID,
    headers=headers,
    files=files).raise_for_status()

print("searching for daily news files")

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

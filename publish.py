import os, shutil
from template import template
from zoneinfo import ZoneInfo
from datetime import datetime
from dotenv import load_dotenv

OUTPUT_FILE = "output.mp3"

load_dotenv()
tz = ZoneInfo(os.environ.get("TZ"))

def artifact(filename, content):
    with open(filename, "w") as f:
        f.write(content)

def podcast(date, filebase):
    artifact("feed.xml",
             template("feed.xml.jinja")
             .render({
                'filebase': filebase,
                'pubdate': date }))

def web(date, filebase):
    args = {
        'filebase': filebase,
        'pubdate': date,
        'prompt': open("prompt.txt").read(),
        'script': open("script.txt").read(),
        'report': open("report.json").read(),
        'voicing': open("voicing.txt").read()
    }

    artifact("index.html",
             template("index.html.jinja").render(args))

if __name__ == "__main__":
    date = datetime.now(tz)
    filebase = "shedfm-daily-%s" % date.strftime("%Y-%m-%d")
    shutil.copyfile(OUTPUT_FILE, "%s.mp3" % filebase)
    os.system(f"ffmpeg -y -hide_banner -loglevel error -i {OUTPUT_FILE} -codec:a aac {filebase}.aac")
    podcast(date, filebase)
    web(date, filebase)


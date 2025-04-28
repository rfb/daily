import os
from template import template
from zoneinfo import ZoneInfo
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
tz = ZoneInfo(os.environ.get("TZ"))

def artifact(filename, content):
    with open(filename, "w") as f:
        f.write(content)

def podcast():
    artifact("feed.xml",
             template("feed.xml.jinja")
             .render({ 'pubdate': datetime.now(tz) }))

def web():
    args = {
        'pubdate': datetime.now(tz),
        'prompt': open("prompt.txt").read(),
        'script': open("script.txt").read(),
        'report': open("report.json").read(),
        'voicing': open("voicing.txt").read()
    }

    artifact("index.html",
             template("index.html.jinja").render(args))

if __name__ == "__main__":
    podcast()
    web()


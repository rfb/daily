import os, shutil
from template import template
from zoneinfo import ZoneInfo
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
tz = ZoneInfo(os.environ.get("TZ"))

def artifact(filename, content):
    with open(filename, "w") as f:
        f.write(content)

def podcast(date, filenameOpus):
    artifact("feed.xml",
             template("feed.xml.jinja")
             .render({
                'filenameOpus': filenameOpus,
                'pubdate': date }))

def web(date, filenameOpus):
    args = {
        'filenameOpus': filenameOpus,
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
    filenameOpus = "%s.opus" % filebase
    filenameAac = "%s.aac" % filebase
    shutil.copyfile("output.opus", filenameOpus)
    os.system("ffmpeg -y -hide_banner -loglevel error -i output.opus -codec:a aac %s" % filenameAac)
    podcast(date, filenameOpus)
    web(date, filenameOpus)


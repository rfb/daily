import os, shutil

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

from template import template
from today import today

OUTPUT_FILE = "output.mp3"

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

def tag(filename, date):
    file = MP3(filename, ID3=EasyID3)
    file["title"] = f"ShedFM Daily for {date.strftime("%Y-%m-%d")}"
    file["artist"] = "ShedFM"
    file["date"] = date.strftime("%Y-%m-%d")
    file.save()

if __name__ == "__main__":
    tag(OUTPUT_FILE, today)
    filebase = "shedfm-daily-%s" % today.strftime("%Y-%m-%d")
    shutil.copyfile(OUTPUT_FILE, "%s.mp3" % filebase)
    os.system(f"ffmpeg -y -hide_banner -loglevel error -i {OUTPUT_FILE} -codec:a aac {filebase}.aac")
    podcast(today, filebase)
    web(today, filebase)

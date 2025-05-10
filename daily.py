import os, logging, json

from dotenv import load_dotenv
from openai import OpenAI

from weather import fetch_weather
from events import fetch_events
from prompts import mkprompt, mkvoicing
from publish import artifact, OUTPUT_FILE
from today import today

def main():
    load_dotenv()

    client = OpenAI( api_key=os.environ.get("OPENAI_API_KEY") )

    report = fetch_weather()
    report = report | {
        'events': fetch_events(),
        'day_of_the_week': today.strftime("%A")
    }

    artifact("report.json", json.dumps(report, indent=2))

    prompt = mkprompt(report)

    artifact("prompt.txt", prompt)

    voicing = mkvoicing(report)

    artifact("voicing.txt", voicing)

    response = client.responses.create(
        model="gpt-4o",
        input=prompt)

    script = response.output_text

    artifact("script.txt", script)

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="echo",
        instructions=voicing,
        response_format="mp3",
        input=script) as response:
        response.stream_to_file(OUTPUT_FILE)

main()

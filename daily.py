import os, logging

from dotenv import load_dotenv
from openai import OpenAI

from weather import fetch_weather
from events import fetch_events
from prompts import script, voicing

load_dotenv()

client = OpenAI( api_key=os.environ.get("OPENAI_API_KEY") )

report = fetch_weather()
report = report | { 'events': fetch_events() }

logging.debug(report)

script = script(report)
voicing = voicing(report)

logging.debug(script)
logging.debug(voicing)

response = client.responses.create(
        model="gpt-4o",
        input=script)

script = response.output_text

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="echo",
    instructions=voicing,
    input=script) as response:
    response.stream_to_file("output.mp3")


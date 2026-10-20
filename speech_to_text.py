from groq import Groq
from dotenv import load_dotenv
import os


class SpeechToText:
    def __init__(self):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])

    def transcribe(self, audio):
        transcription = self.groq_client.audio.transcriptions.create(
            file=(audio.name, audio.getvalue()),
            model="whisper-large-v3-turbo",
            language="fr",
        )
        return transcription.text

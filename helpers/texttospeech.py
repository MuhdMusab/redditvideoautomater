from gtts import gTTS
from nanoid import generate

class TextToSpeechGenerator:
    @staticmethod
    def get_speech_from_post(content):
        tts = gTTS(content)
        tts.save(generate() + ".mp3")
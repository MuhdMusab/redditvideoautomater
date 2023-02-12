from gtts import gTTS
from nanoid import generate

class TextToSpeechGenerator:
    @staticmethod
    def get_speech_from_post(content, pathname):
        tts = gTTS(content)
        tts.save(pathname)
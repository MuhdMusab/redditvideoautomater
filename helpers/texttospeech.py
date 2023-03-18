import edge_tts

class TextToSpeechGenerator:
    @staticmethod
    async def get_speech_from_post(content, pathname):
        OUTPUT_FILE = pathname + ".mp3" 
        voices = await edge_tts.VoicesManager.create()
        voice = voices.find(Gender="Male", Language="en")[4]["Name"]
        communicate = edge_tts.Communicate(content, voice)
        await communicate.save(OUTPUT_FILE)
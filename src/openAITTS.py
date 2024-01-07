from openai import OpenAI

class openAITTS:
    def __init__(self):
        return
    
    def speak(text, Rina):
        file = Path()
        response = openai.audio.speech.create(
            model="tts-1",
            voice="",
            input=text
        )
        response.stream_to_file(file)
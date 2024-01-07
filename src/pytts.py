import pyttsx3
engine = pyttsx3.init()
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
engine.setProperty('rate', 195)
engine.setProperty('volume', 1)

class TTS:
    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    def stop(self):
        engine.stop()
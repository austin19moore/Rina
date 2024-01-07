import pyttsx3

class TTS:

    engine = None
    rate = None
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
        self.engine.setProperty('rate', 195)
        self.engine.setProperty('volume', 1)
        return


    def start(self,text_):
        self.engine.say(text_)
        self.engine.runAndWait()
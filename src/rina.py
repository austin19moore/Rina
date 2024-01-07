from openai import OpenAI
from src.pytts import TTS
import threading
import time
import random
from src.speechRecognition import Speech
import os
from dotenv import load_dotenv


class Rina:

    def __init__(self, desktop, memory, response, temp):
        print("Initializing...")
        load_dotenv()

        self.desktopRec = []
        self.micRec = []
        self.lastResponses = []
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.lock = threading.Lock()

        self.Personality = []
        self.model = "gpt-3.5-turbo"
        self.useDesktop = desktop or False
        self.memorySize = memory or 2
        self.responseTime = response or 17
        self.temperature = temp or 0.5
        return


    def getResponse(self):
        passedMessages = self.Personality + self.desktopRec + self.micRec + self.lastResponses
        #print(passedMessages)
        response = self.client.chat.completions.create(
        model = self.model,
        messages = passedMessages,
        temperature=self.temperature
        )
        response = response.choices[0].message.content
        # print(passedMessages)

        with self.lock:
            if len(self.lastResponses) > self.memorySize:
                lastResponse = {
                    "role": "assistant", 
                    "content": "Rina you previously said: [" + str(response) + "]"
                }
                self.lastResponses.append(lastResponse)
            else:
                self.lastResponses = []
            
            self.desktopRec = []
            self.micRec = []

        print("Rina: " + response)
        tts = TTS()
        tts.start(response)
        del(tts)
        return


    def start(self):
        print("Starting, type 'stop' to exit...")
        sr = Speech()

        stop = False
        # useMic, stop, Rina
        stereoThread = threading.Thread(target=sr.getTranscription, args=(False, lambda: stop, self,))
        micThread = threading.Thread(target=sr.getTranscription, args=(True, lambda: stop, self,))
        # stop
        responseThread = threading.Thread(target=self.responseLoop, args=(lambda: stop,))

        # kill all threads on exit
        micThread.daemon = True
        stereoThread.daemon = True 
        responseThread.daemon = True

        # will combust if you try to run them at the same time, giving a sleep between starting them fixes the issue and accomplishes the same thing
        micThread.start()
        time.sleep(1)
        if self.useDesktop == True:
            stereoThread.start()
        time.sleep(5)
        responseThread.start()
        userIn = ""

        # wait for user to type stop (ideally could be changed with the addition of a UI)
        while userIn.find("stop") == -1:
            userIn = input()

        print("Stopping")
        # call thread stop and join threads
        stop = True
        micThread.join()
        if self.useDesktop == True:
            stereoThread.join()
        responseThread.join()
        return


    def responseLoop(self, stop):
        print("Starting responseLoop")
        try:
            while not stop():
                if len(self.micRec) > 0 or len(self.desktopRec) > 0:
                    getresponsethread = threading.Thread(target=self.getResponse)
                    getresponsethread.start()
                    getresponsethread.join(8)
                    time.sleep(random.choice([3, 4, 5]))
                
                # You are rate limited to 3 requests a minute on OPENAI free tier, ideally should be lowered dramatically (to like 1-5) to improve response time
                time.sleep(self.responseTime)

        except:
            print("Failed to run responseLoop")
        return
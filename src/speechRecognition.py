import speech_recognition as sr
import time

class Speech:
    def __init__(self):
        return
    
    def getTranscription(self, useMic, stop, Rina):
        
        try:
            stereoid = None
            for micid, index in enumerate(sr.Microphone.list_microphone_names()):
                # print(micid, index)
                if str(index).find("Stereo Mix") != -1:
                    stereoid = micid
                    # print("id: " + str(stereoid))
                    break
            mic = None
            if useMic == True:
                mic = sr.Microphone()
            else: 
                mic = sr.Microphone(device_index=stereoid)
            
            with mic as source:
                r = sr.Recognizer()
                r.dynamic_energy_threshold = True
                r.adjust_for_ambient_noise(source, duration=5)

            if useMic == True:
                print("Running speech to text on default Microphone")
            else:
                print("Running speech to text on stereo mix")

            while not stop():
                try:
                    with mic as source:
                        text = ""

                        try:
                            # can mess with the timeout/max phrase time limit to get better response time, 5/16 works pretty well tho
                            audio = r.listen(source, 5, 16)
                        except:
                            audio = None
                            #print("failed to listen / timeout")
                        
                        try:
                            text = r.recognize_google(audio)
                            #print("finished transcribing")
                        except:
                            text = None
                            #print("failed to transcribe / timeout")
                        
                        # solve issue of transcribing and sending the TTS response back in a loop
                        # does not work as the formatting on the response is different, to be fixed
                        copy = False
                        for message in Rina.lastResponses:
                            if str(message).lower().find(str(text).lower()) != -1:
                                copy = True

                        if text != None and copy == False:
                            print("Transcription: " + str(text))
                            if useMic == True:
                                newMessage = {
                                    "role": "user",
                                    "content": "User said: [" + str(text) + "]"
                                }
                                with Rina.lock:
                                    Rina.micRec.append(newMessage)
                            else:
                                newMessage = {
                                    "role": "user",
                                    "content": "Others said: [" + str(text) + "]"
                                }
                                with Rina.lock:
                                    Rina.desktopRec.append(newMessage)
                except:
                    print("failed to start speech recongition")

                # time.sleep(1)
            

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occurred")

        return
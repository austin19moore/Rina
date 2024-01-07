import espeakng

mySpeaker = espeakng.Speaker()
mySpeaker.voice = 'en-dutch'

mySpeaker.say("test", wait4prev=True)
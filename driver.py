import threading
from src.rina import Rina

# also use desktop audio (only works on windows with Realtek stereo mix enabled), memory size (dramatically increases cost), model temperature (how creative it will be)
rina = Rina(True, 2, 0.5)
# name of custom model if fine tuned
# rina.model = "ft:gpt-3.5-turbo:(your model id here)"
personality = {
    "role": "system",
    "content": "Rina is a conversational AI. Your goal is [insert here]. You will recieve the others message(s) in brackets. Try to keep your responses in plain text under 50 characters."
}
rina.Personality.append(personality)


# run and wait on "stop" input
driverthread = threading.Thread(target=rina.start())
driverthread.start()
driverthread.join()
print("Closed threads and exited")
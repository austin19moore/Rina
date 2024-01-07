Conversational chatbot the recieves microphone and desktop transcribed input as prompts and TTS's a response, output can be dramatically improved by using a fine-tuned openAI model (example included in data/finetuning/finetuning.txt).


<h3><strong>The driver creates the main thread, which then creates:</strong></h3>
- a response thread</br>
- a thread looping the microphone</br>
- a thread looping the desktop speech recognition.</br>
These transcriptions are put in buffers which are being checked by the response thread, when information is in the response thread it is sent to openAI for a response, and the response is appended to the response buffer to give the model context for the next response(s).
</br></br></br>

To setup:
Clone the repository, create a .env file in the root directory (same directory as the driver file), and add in your openai api key in .env as "OPENAI_API_KEY=you_api_key"



Example output:
![image](https://github.com/austin19moore/Rina/assets/80301847/b62b0b5b-9dd2-48de-9877-fde5a675c624)




here's my terrible paint diagram for my initial idea/concept that I used to built it:
![image](https://github.com/austin19moore/Rina/assets/80301847/2ee59a6f-6e04-4aa0-8b02-6a36c64f7fb7)

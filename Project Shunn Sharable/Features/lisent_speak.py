import pyttsx3
import speech_recognition as sr

Assistant = pyttsx3.init('sapi5')
voices = Assistant.getProperty('voices')
#print(voices)
Assistant.setProperty('voice' , voices[0].id)
Assistant.setProperty('rate', 200)

def speak(audio):
    print("   ")
    audio1 = "hi how are you helo " + str(audio)
    Assistant.say(audio1)
    print(f": {audio}")
    Assistant.runAndWait()

def takecommand():
    command = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.........")
        command.pause_threshold = 1
        audio = command.listen(source)

        try:
            print("Recognizing........")
            query = command.recognize_google(audio, language='en-in')
            print(f"You said : {query}")

        except Exception as Error:
            speak("Say that again please!")
            return "none"        
        return  query.lower()


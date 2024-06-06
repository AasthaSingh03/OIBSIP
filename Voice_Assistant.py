import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            return None

def respond_to_hello():
    speak("Hello! How can I help you today?")


def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    speak(f"The current time is {current_time}")


def tell_date():
    today = datetime.date.today()
    speak(f"Today's date is {today}")


def search_web(query):
    speak(f"Searching the web for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def main():
    speak("How can I assist you?")
    while True:
        command = listen()
        
        if command:
            if "hello" in command:
                respond_to_hello()
            elif "time" in command:
                tell_time()
            elif "date" in command:
                tell_date()
            elif "search for" in command:
                search_query = command.replace("search for", "").strip()
                search_web(search_query)
            elif "exit" in command or "quit" in command:
                speak("Goodbye!")
                break
            else:
                speak("Sorry, I can only respond to simple commands like hello, time, date, and search for.")

if __name__ == "__main__":
    main()

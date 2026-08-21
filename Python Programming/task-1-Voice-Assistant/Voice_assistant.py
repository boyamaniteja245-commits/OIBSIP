import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser
import urllib.parse

# Initialize speech recognition and text-to-speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()


# Text-to-speech
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


# Voice input
def listen():
    with sr.Microphone() as source:
        print("Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text.lower()

    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
        return ""

    except sr.RequestError:
        speak("Sorry, there is a problem with the speech recognition service.")
        return ""

    except Exception as e:
        print("Error:", e)
        speak("Something went wrong.")
        return ""


# Process commands
def process_command(command):

    # Hello
    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you?")

    # Time
    elif "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak("The current time is " + current_time)

    # Date
    elif "date" in command or "today" in command:
        current_date = datetime.now().strftime("%B %d, %Y")
        speak("Today's date is " + current_date)

    # Open YouTube
    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    # Open Google
    elif "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    # Open Instagram
    elif "open instagram" in command:
        speak("Opening Instagram.")
        webbrowser.open("https://www.instagram.com")

    # Open Gmail
    elif "open gmail" in command:
        speak("Opening Gmail.")
        webbrowser.open("https://mail.google.com")

    # YouTube search
    elif command.startswith("search youtube"):
        search_query = command.replace("search youtube", "", 1).strip()

        if search_query:
            speak("Searching YouTube for " + search_query)

            encoded_query = urllib.parse.quote(search_query)

            youtube_url = (
                "https://www.youtube.com/results?search_query="
                + encoded_query
            )

            webbrowser.open(youtube_url)

        else:
            speak("What would you like me to search for on YouTube?")

    # Play/search YouTube
    elif command.startswith("play"):
        video_query = command.replace("play", "", 1).strip()

        if video_query:
            speak("Searching YouTube for " + video_query)

            encoded_query = urllib.parse.quote(video_query)

            youtube_url = (
                "https://www.youtube.com/results?search_query="
                + encoded_query
            )

            webbrowser.open(youtube_url)

        else:
            speak("What would you like me to play?")

    # Google web search
    elif command.startswith("search"):
        search_query = command.replace("search", "", 1).strip()

        if search_query:
            speak("Searching for " + search_query)

            encoded_query = urllib.parse.quote(search_query)

            google_url = (
                "https://www.google.com/search?q="
                + encoded_query
            )

            webbrowser.open(google_url)

        else:
            speak("What would you like me to search for?")

    # Exit
    elif (
        "exit" in command
        or "quit" in command
        or "goodbye" in command
    ):
        speak("Goodbye! Have a great day.")
        return False

    # Unknown command
    else:
        speak("Sorry, I don't know that command yet.")

    return True


# Start assistant
speak("Hello! I am your Python voice assistant. How can I help you?")


# Continuous listening
while True:

    command = listen()

    if command:
        should_continue = process_command(command)

        if not should_continue:
            break
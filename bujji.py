import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import time
import requests
import pyjokes
import re
import webbrowser
from threading import Timer

# Initialize the speech recognition and text-to-speech engine
listener = sr.Recognizer()
machine = pyttsx3.init()

def talk(text):
    """Converts text to speech."""
    machine.say(text)
    machine.runAndWait()

def input_instruction(prompt=None):
    """Captures and returns the spoken instruction."""
    if prompt:
        talk(prompt)
    instruction = ""
    try:
        with sr.Microphone() as source:
            print("Bujji is Listening....")
            listener.adjust_for_ambient_noise(source)
            speech = listener.listen(source)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            if "bujji" in instruction:
                instruction = instruction.replace('bujji', '')
            print(f"Instruction: {instruction}")
    except sr.UnknownValueError:
        print("Sorry, I did not catch that. Please repeat.")
    except sr.RequestError:
        print("Sorry, my speech service is down. Please try again later.")
    
    return instruction

def parse_duration(duration):
    """Parses the duration string into total seconds."""
    pattern = re.compile(r'(?:(\d+)\s*hours?)?\s*(?:(\d+)\s*minutes?)?\s*(?:(\d+)\s*seconds?)?', re.IGNORECASE)
    match = pattern.fullmatch(duration.strip())
    if not match:
        return None
    hours, minutes, seconds = match.groups(default='0')
    total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    return total_seconds

def set_timer():
    """Sets a timer based on user input."""
    talk("For how long do you want to set the timer?")
    duration = input_instruction()
    total_seconds = parse_duration(duration)
    if total_seconds is not None:
        talk(f"Timer set for {total_seconds} seconds.")
        print(f"Timer set for {total_seconds} seconds.")
        time.sleep(total_seconds)
        talk("Time's up!")
    else:
        talk("Sorry, I didn't understand the duration. Please try again.")
        print(f"Invalid duration input: {duration}")

def set_medicine_timer():
    """Sets a timer to remind user to take medicine."""
    talk("How long until you need to take your medicine?")
    duration = input_instruction()
    total_seconds = parse_duration(duration)
    if total_seconds is not None:
        talk(f"Medicine reminder set for {total_seconds} seconds.")
        print(f"Medicine reminder set for {total_seconds} seconds.")
        Timer(total_seconds, lambda: talk("It's time to take your medicine!")).start()
    else:
        talk("Sorry, I didn't understand the duration. Please try again.")
        print(f"Invalid duration input: {duration}")

def get_weather():
    """Fetches and returns the weather information based on user input."""
    talk("Which city's weather would you like to know?")
    city = input_instruction()
    print(f"City: {city}")
    api_key = ""  # Replace with your actual OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    data = response.json()
    print(f"API Response: {data}")

    if data["cod"] == 200:
        main = data["main"]
        temperature = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        weather_description = data["weather"][0]["description"]
        weather_info = (f"Temperature: {temperature - 273.15:.2f}°C, "  # Convert Kelvin to Celsius
                        f"Pressure: {pressure}hPa, "
                        f"Humidity: {humidity}%, "
                        f"Description: {weather_description}")
        print(weather_info)
        talk(weather_info)
    elif data["cod"] == 401:
        talk("Invalid API key. Please check your API key and try again.")
        print("Invalid API key.")
    else:
        talk("City not found.")
        print("City not found.")

def say_goodbye():
    """Says goodbye and exits the program."""
    talk("Goodbye!")
    exit()

def open_youtube():
    """Opens YouTube in the default web browser."""
    talk("Opening YouTube.")
    webbrowser.open("https://www.youtube.com")

def open_spotify():
    """Opens Spotify in the default web browser."""
    talk("Opening Spotify.")
    webbrowser.open("https://www.spotify.com")

def health_advice():
    """Provides a health advice."""
    talk("Remember to stay hydrated, eat a balanced diet, and exercise regularly.")
    print("Health advice given.")

def play_Bujji():
    """Processes the instruction and performs the requested action."""
    instruction = input_instruction("How can I assist you?")
    if "play" in instruction:
        song = instruction.replace('play', "").strip()
        talk("Playing " + song)
        pywhatkit.playonyt(song)

    elif 'time' in instruction and 'set a timer' not in instruction and 'medicine' not in instruction:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + current_time)

    elif 'date' in instruction:
        current_date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk("Today's date is " + current_date)

    elif 'how are you' in instruction:
        talk('I am fine, how about you?')

    elif 'what is your name' in instruction:
        talk('I am Bujji, what can I do for you?')

    elif 'who is' in instruction:
        person = instruction.replace('who is', "").strip()
        info = wikipedia.summary(person, sentences=1)
        print(info)
        talk(info)

    elif 'set a timer' in instruction or 'timer' in instruction:
        set_timer()

    elif 'remind me to take medicine' in instruction or 'medicine' in instruction:
        set_medicine_timer()

    elif 'weather' in instruction:
        get_weather()

    elif 'tell me a joke' in instruction:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)

    elif 'goodbye' in instruction or 'bye' in instruction:
        say_goodbye()

    elif 'open youtube' in instruction:
        open_youtube()

    elif 'open spotify' in instruction:
        open_spotify()

    elif 'health advice' in instruction:
        health_advice()

    else:
        talk('Please repeat')

if __name__ == "__main__":
    while True:
        play_Bujji()

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class VirtualAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bujji - Virtual Assistant")
        self.root.geometry("800x600")

        # Load the avatar image
        self.avatar_image = Image.open("C:/creating virtual assistant/avatar.png")
        self.avatar_image = self.avatar_image.resize((100, 100), resample=Image.LANCZOS)

        self.avatar_photo = ImageTk.PhotoImage(self.avatar_image)

        # Create avatar label
        self.avatar_label = ttk.Label(self.root, image=self.avatar_photo, background="#f0f0f0")
        self.avatar_label.grid(row=0, column=0, padx=20, pady=20)

        # Create label with assistant's name
        self.name_label = ttk.Label(self.root, text="Bujji", font=("Arial", 16), background="#f0f0f0")
        self.name_label.grid(row=0, column=1, padx=20, pady=20)

        # Create buttons
        self.button_talk = ttk.Button(self.root, text="Talk to Assistant", command=self.talk_to_assistant)
        self.button_talk.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        self.button_exit = ttk.Button(self.root, text="Exit", command=self.root.quit)
        self.button_exit.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    def talk_to_assistant(self):
        # Example: Let's assume the assistant speaks a greeting
        print("Hello! How can I assist you today?")

def main():
    root = tk.Tk()
    app = VirtualAssistantApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

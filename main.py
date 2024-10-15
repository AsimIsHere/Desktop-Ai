import os
import pyttsx3
import webbrowser
import threading
import datetime
import pvporcupine
import time
from config import api
from config2 import key
import struct
import pyaudio
import google.generativeai as genai
import speech_recognition as sr
import re

# Initialize pyttsx3 engine once
engine = pyttsx3.init()

def say(text, rate=190):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        r.energy_threshold = 300  # Adjust if needed
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print(f"Error: {e}")
            say("Some error occurred.")
            return ""

chatStr = ""

def chat(query):
    global chatStr
    gemini_api_key = api  # Replace with your actual key
    chatStr += f"Asim: {query}\nUltron: "

    # Generate response using Gemini
    try:
        model = genai.GenerativeModel('gemini-pro')  # For text generation
        response = model.generate_content(chatStr)
        cleaned_response = re.sub(r'\*', '', response.text)
    except Exception as e:
        print(f"Error generating content: {e}")
        return

    print(cleaned_response)
    try:
        say(cleaned_response)  # Ensure say() function is defined elsewhere
    except Exception as e:
        print(f"Error saying response: {e}")

    chatStr += f"{cleaned_response}\n"
    return cleaned_response

def ai(prompt):
    # Generate response using Gemini
    try:
        model = genai.GenerativeModel('gemini-pro')  # For text generation
        response = model.generate_content(prompt)
        print(response.text)
    except Exception as e:
        print(f"Error generating AI response: {e}")

def wake_word_detected():
    porcupine = pvporcupine.create(
        access_key=key,
        keyword_paths=["C:\\Users\\DELL\\Downloads\\Jarvis_en_windows_v3_0_0.ppn"]
    )

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        result = porcupine.process(pcm)

        if result >= 0:
            say("Yes Sir?")
            query = takeCommand()

            sites = [["youtube", "https://www.youtube.com"], ["instagram", "https://www.instagram.com"],
                     ["google", "https://www.google.com"], ["wikipedia", "https://www.wikipedia.com"],
                     ["freelancer", "https://www.freelancer.in/dashboard"]]

            for site in sites:
                if f"open {site[0]}".lower() in query.lower():
                    say(f"Opening {site[0]} sir...")
                    webbrowser.open(site[1])
                    break  # Exit the loop once a site is opened

            if "open music" in query.lower():
                Musicpath = "C:\\Users\\DELL\\Downloads\\Music.mp3"
                say("Playing music, sir...")
                os.startfile(Musicpath)

            elif "the time" in query.lower():
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                say(f"Sir, the time is {strTime}")

            elif "open VS code".lower() in query.lower():
                vs = "C:\\Users\\DELL\\OneDrive\\Desktop\\Visual Studio Code.lnk"
                say("Opening VS Code sir...")
                os.startfile(vs)

            elif "shut down" in query.lower():
                say("Shutting down. Goodbye sir, have a great day!")
                return

            else:
                chat(query)

if __name__ == '__main__':
    genai.configure(api_key=api)  # Configure the Gemini API once globally
    print("Pycharm")

    while True:
        wake_word_detected()
        break

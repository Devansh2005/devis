import pyttsx3
from speech_recognition import Recognizer
from speech_recognition import Microphone
from speech_recognition import RequestError
from speech_recognition import UnknownValueError
from time import sleep, ctime
from re import search
import webbrowser
import wikipedia
import smtplib



tts_engine =pyttsx3.init("sapi5")

rate =tts_engine.getProperty("rate")
tts_engine.setProperty("rate", 140)

def speak_electrica(text):
    tts_engine.say(text)
    print(text)

    tts_engine.runAndWait()


sr_engine =Recognizer()
def record_audio(ask=False):
    if ask:
        speak_electrica(ask)
    with Microphone() as source:
        print("Speak Up! I am listning..")
        audio= sr_engine.listen(source)
        audio_text=""
        try:
            print("Now hold-on ! I'm recognising..")
            audio_text=sr_engine.recognize_google(audio, language="en-in")
            print(audio_text)
            return audio_text.lower()
        except UnknownValueError:
            speak_electrica("Sorry I didn't get that. kindly speak up again")
            say_again()


        except RequestError:
            speak_electrica("Sorry, unable to connect with engine")


def search_command(audio_text):
    #Devis Introduction
    if "your name" in audio_text:
        speak_electrica("my name is Devis.")
        sleep(3)
        something_else()

    #Current time
    elif "current time" in audio_text or "time" in audio_text:
        speak_electrica(ctime())
        sleep(3)
        something_else()
    #Google Search

    elif "google search" in audio_text:
        reg_ex=search("google search (.*)", audio_text)
        search_result = reg_ex.group(1)
        speak_electrica("Here's what are found for "+search_result+"on google.")
        url="http://google.com/search?=q" + search_result
        webbrowser.open(url, new=2)
        sleep(3)
        something_else()

    #Google maps

    elif "find loaction" in audio_text:
        location= record_audio("What location you want to search?")
        speak_electrica("Here's the loaction" +location)
        url = "https://google.nl/maps/place/"+ location+"/&amp;" 
        webbrowser.open(url, new=2)
        sleep(3)
        something_else()





    elif "exit" in audio_text:
        speak_electrica("Ok, Bye Bye")
        exit()

    
    else:
        speak_electrica("Sorry I didn't get that. kindly speak up again")
        say_again()


def say_again():
    speak_electrica("Give me the command..")
   
    audio_text=record_audio()
    search_command(audio_text)

def something_else():
    audio_text=record_audio("Do you want something else ? Yes or No")
    if "yes" in audio_text:
        say_again()
    else:
        speak_electrica("Ok, Bye Bye")
        exit()




speak_electrica("Hello, how can i help you")
say_again()
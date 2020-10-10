import pyttsx3
from speech_recognition import Recognizer
from speech_recognition import Microphone
from speech_recognition import RequestError
from speech_recognition import UnknownValueError


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

        except RequestError:
            speak_electrica("Sorry, unable to connect with engine")





speak_electrica("Hello, how can i help you")
audio_text=record_audio()
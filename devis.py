import pyttsx3
from speech_recognition import Recognizer
from speech_recognition import Microphone
from speech_recognition import UnknownValueError
from speech_recognition import RequestError
from time import ctime,sleep,strftime
from re import search
import webbrowser
import wikipedia
import smtplib
import subprocess
from cv2 import cv2
from tkinter import *
import PIL.Image, PIL.ImageTk
from nltk.tokenize import sent_tokenize 
# from cam_recorder2 import main

tts_engine= pyttsx3.init('sapi5')
rate = tts_engine.getProperty('rate') 
tts_engine.setProperty('rate', 140)

def speak_devis(text):
   var.set(text)
   interface.update()
   tts_engine.say(text)
   tts_engine.runAndWait()  

sr_engine = Recognizer()
def record_audio(ask=False):
    if ask:
        speak_devis(ask)
    with Microphone() as source:
        var.set("Speak-up! I am listening...")
        interface.update()
        audio = sr_engine.listen(source)
        audio_text = ''
        try:
            var.set("Now hold-on! I am recognizing...")
            interface.update()
            audio_text = sr_engine.recognize_google(audio,language='en-in')
            var1.set(audio_text)
            interface.update()
            return audio_text.lower()
        except UnknownValueError:
            speak_devis("Sorry, I didn't get that. Kindly Speak-up again!")
            say_again()
        except RequestError:
            speak_devis("Sorry, unable to connect to the server.")
            say_again()

contacts={'receiver_name':'receiver_mail'}
def sendemail(to, content):
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.ehlo()
   server.starttls()
   server.login('sender_mail', 'sender_pwd')
   server.sendmail('sender_mail', to, content)
   server.close()

def greeting():
   day_time = int(strftime('%H'))
   if day_time < 12:
      speak_devis('Hello Sir. Good morning')
   elif 12 <= day_time < 18:
      speak_devis('Hello Sir. Good afternoon')
   else:
      speak_devis('Hello Sir. Good evening')
   speak_devis("Press Command Button to give your command")

def search_command(audio_text):
   if 'your name' in audio_text:
      speak_devis("My name is Devis.")
      sleep(2)
      something_else()
    
   # Check Current Time
   elif 'time' in audio_text:
      speak_devis(ctime())
      sleep(2)
      something_else()
    
   # Google Search
   elif 'google search' in audio_text:
      reg_ex = search('google search (.*)', audio_text)
      search_result = reg_ex.group(1)
      speak_devis("Here's what I found for "+ search_result+' on google')
      url = 'https://google.com/search?q='+ search_result
      webbrowser.open(url,new=2) #new=2, open in new tab
      sleep(2)
      something_else()

   # Wikipedia Search
   elif 'tell me about' in audio_text:
      reg_ex = search('tell me about (.*)', audio_text)
      try:
         if reg_ex:
            topic = reg_ex.group(1)
            # pg = wikipedia.page(topic)
            # speak_devis(pg.content[:100].encode('utf-8'))
            results = wikipedia.summary(topic, sentences=2)
            speak_devis("According to wikipedia")
         for sentence in sent_tokenize(results):
            speak_devis(sentence)
         sleep(2)
         something_else()
      except Exception:
         speak_devis("Unable to get the topic from wikipedia.")
         speak_devis("Here's what I found for "+topic+' on google')
         url = 'https://google.com/search?q='+topic
         webbrowser.open(url,new=2)
         sleep(2)
         something_else()


   # Google Map Search
   elif 'find location' in audio_text:
      location = record_audio('what location you want to search?')
      speak_devis("Here's the location "+location)
      url = 'https://google.nl/maps/place/'+ location +'/&amp;'
      webbrowser.open(url,new=2)
      sleep(2)
      something_else()
   
   # Open Website
   elif 'open website' in audio_text:
      reg_ex = search('open website (.+)', audio_text)
      if reg_ex:
         domain = reg_ex.group(1)
         speak_devis('Opening '+ domain)
         url = 'https://www.' + domain
         webbrowser.open(url,new=2)
         speak_devis('The website you have requested has been opened for you Sir.')
         sleep(2)
         something_else()
      else:
         speak_devis("Unable to get the url of requested website")
         say_again()

    
   # Send Gmail
   elif 'send mail' in audio_text or 'send email' in audio_text:
      try:
         to = record_audio('to whome you want to send?')
         if to in contacts:
            content = record_audio('what should I write in mail?')
            sendemail(contacts[to], content)
            speak_devis('Email has been sent!')
            sleep(2)
            something_else()
         else:
            speak_devis('Unable to get the contact!')
            sleep(2)
            something_else()
      except Exception:
         speak_devis('Sorry Sir! Unable to send the email')
         say_again()

   # Take a selfie
   elif 'click photo' in audio_text or 'click selfie' in audio_text:
      speak_devis('Pose in front of camera')
      stream = cv2.VideoCapture(0)
      grabbed, frame = stream.read()
      if grabbed:
         cv2.imshow('pic', frame)
         cv2.imwrite('pic.jpg',frame)
      stream.release()
      sleep(2)
      something_else()

   elif 'exit' in audio_text or 'nothing' in audio_text:
      btn1.configure(bg = '#5C85FB')
      btn2['state'] = 'normal'
      btn0['state'] = 'normal'
      speak_devis("Ok Sir!")
      sleep(1)
      interface.destroy()
    
   else:
      speak_devis("Sorry, I didn't get that. Kindly Speak-up again!")
      say_again()

def say_again():
   speak_devis("Give me the command?")
   audio_text = record_audio()
   search_command(audio_text)

def something_else():
    speak_devis("Want to know something else?")
    audio_text = record_audio()
    if 'yes' in audio_text:
        say_again()
    else:
        speak_devis("Ok Sir!")
        exit()

def update(ind):
   frame = frames[(ind)%100]
   ind += 1
   label.configure(image=frame)
   interface.after(100, update, ind)

class FullScreenApp(object):
   def __init__(self, master, **kwargs):
      self.master=master
      pad=3
      self._geom='500x800+0+0'
      master.geometry("{0}x{1}+0+0".format(
         master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
      master.bind('<Escape>',self.toggle_geom)

   def toggle_geom(self,event):
      geom=self.master.winfo_geometry()
      self.master.geometry(self._geom)
      self._geom=geom

interface=Tk()
interface.title("DEVIS")
app=FullScreenApp(interface)


global var
var=StringVar()
global var1
var1=StringVar()

label2=Label(interface,textvariable=var1,bg='#FAB60C')
label2.config(font=("Courier",20))
var1.set('Your Command')
label2.pack()

label1=Label(interface,textvariable=var,bg='#ADD8E6',justify= LEFT, wraplength=1400)
label1.config(font=("Courier",20))
var.set('Assistant Response')
label1.pack()

frames=[PhotoImage(file='assistant.gif',format='gif -index %i' %(i)) for i in range(100)]

label=Label(interface,width=500,height=500)
label.pack()
interface.after(0,update,0)

btn0=Button(text='Greeting',width=20,command=greeting,bg='#5C85FB')
btn0.config(font=("Courier",12))
btn0.pack()

btn1 = Button(text='Command',width=20,command=say_again,bg = '#5C85FB')
btn1.config(font=("Courier", 12))
btn1.pack()

btn2 = Button(text='Exit',width=20, command=interface.destroy, bg = '#5C85FB')
btn2.config(font=("Courier",12))
btn2.pack()

interface.mainloop()

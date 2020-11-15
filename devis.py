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
import filetype
import subprocess
from cv2 import cv2
from assets.fileexplorer import fileExplorer
from assets.popup import popup, passpopup
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
def mail_service(email, password):
   from email.message import EmailMessage
   email_address = email
   email_password = password

   msg = EmailMessage()
   speak_devis('What is the subject of your message?')
   msg['Subject'] = record_audio()
   msg['From'] = email_address
   speak_devis('Who will you like to send the mail to?')
   receiver = popup('Email', 'Enter Recipient Email Address:')
   msg['To'] = receiver
   speak_devis('Please provide the content of the mail! Would you prefer to type it or say it?')
   while True:
      response = record_audio()
      if 'type' in response:
            content = popup('Email Content', 'Type in the Content of Your Mail:')
            break
      elif 'speak' in response:
            content = record_audio()
            break
      else: 
            speak_devis("I couldn't understand your response. Please use either the word type or speak!")
            continue
   msg.set_content(content)

   speak_devis(('Do you want to attach a file?'))
   attachcontent = record_audio()

   if attachcontent.lower() == 'yes':
      while True:
            try:
               speak_devis('How many files do you want to attach? ')
               attachcount = int(record_audio())
               attachments = 0
               while attachments < attachcount:
                  file_path = fileExplorer()
                  with open(file_path, 'rb') as f:
                        file_data = f.read()
                        file_mime = filetype.guess_mime(f.name)
                        file_type = filetype.guess_extension(f.name)
                        file_name = f.name.split('/')[-1]
                  msg.add_attachment(file_data, maintype=file_mime,
                                    subtype=file_type, filename=file_name)
                  attachments += 1
               break
            except ValueError:
               speak_devis('You were meant to type a number.')
               continue
            except FileNotFoundError:
               speak_devis('File could not be accessed!')
               continue
            except Exception as e:
               speak_devis("I ran into issues trying to process that. Let's try that again!")
               print(e)
               continue
   else:
         speak_devis('Message will be sent without an attachment!')

   with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
      smtp.login(email_address, email_password)
      smtp.send_message(msg)
   speak_devis('Your email has been sent!')
   return


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
         speak_devis('Please provide your email!')
         sender = popup('Email', 'Enter Your Email Address:')
         speak_devis('Please ensure you have configured your google mail to allow third party applications. You can also configure an app password')
         speak_devis('Enter Your Password:')
         password = passpopup('Password', 'Enter Your Email Password: ')
         mail_service(sender, password)
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

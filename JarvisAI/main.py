import datetime
from numpy import take
import pyttsx3
import speech_recognition as sr
import wikipedia 
import webbrowser
import os
import smtplib
import random

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!Boss")
    
    elif hour>=12 and hour<18:
        speak("Good Afternoon!Boss")

    else:
        speak("Good Evening!Boss")

    speak("Jarvis Here. Please tell me what to do")

def takeCommand():
    '''
    It takes microphone input from user and returns string output.
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1 # seconds of non-speaking audio before a phrase is considered complete
        audio = r.listen(source) #Records a single phrase from ``source`` (an ``AudioSource`` instance) into an ``AudioData`` instance, which it returns.
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print(e)

            print("Say that again Boss...")
            return "None"
        return query

def sendEmail(frommail, to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(frommail, "baba@110502")
    # server.login(frommail,"your-password-here") 
    server.sendmail(frommail, to, content)
    server.close()

if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand().lower()

        # Logic for executing based on query

        if 'wikipedia' in query:
            speak("Searching wikipedia...")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences = 2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("http://www.youtube.com/")

        elif 'open mail' in query:
            webbrowser.open("https://mail.google.com/mail/u/1/?ogbl#inbox")
        
        elif 'open google' in query:
            webbrowser.open("https://www.google.com/")

        elif 'open stack overflow' in query:
            webbrowser.open("https://stackoverflow.com/")

        elif 'play music' in query:
            music_dir = 'D:\\play\\music'
            songs = os.listdir(music_dir)
            # print(songs)
            os.startfile(os.path.join(music_dir, songs[random.randint(0,len(songs))]))

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            x = [i for i in strTime.split(":")]
            speak(f"Sir, the time is {x[0]}:{x[1]}.")
        
        elif 'open zotero' in query:
            codePath = "D:\\Zotero\\zotero.exe"
            os.startfile(codePath)
        
        elif 'send a mail' in query:
            try:
                speak("What should I say? Boss!")
                content = takeCommand()
                speak("Boss! From which mail should I send?")
                frommail = input()
                speak("Boss! Forgot to ask, To whom should I send this mail?")
                to = input()
                sendEmail(frommail, to,content)
                speak("Email has been sent Boss!")
            except Exception as e:
                print(e)
                speak("Sorry Boss, I am not able to send this mail.")

        elif 'take notes' in query:
            os.chdir("D://Notes")
            speak("Boss! What should be the name the file")
            name = takeCommand()
            f = open(f"{name}.txt","w")
            content = takeCommand()
            f.write(content)
            f.close()

        elif 'Bye' or 'Goodbye' or 'tata docomo' in query:
            speak("Bye Boss! Adios Amigo!")
            exit()

        else:
            continue;


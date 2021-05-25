import speech_recognition as sr
import pyttsx3
import webbrowser
import requests as req
from youtubesearchpython import VideosSearch
from bs4 import BeautifulSoup
from pynput.keyboard import Controller,Key
from googletrans import Translator
from gtts import gTTS
import os

recognizer = sr.Recognizer()
text = "bom"
html_text = req.get("https://developers.google.com/admin-sdk/directory/v1/languages").text
soup = BeautifulSoup(html_text, 'lxml')
langs = soup.findAll('td')
lang_Codes = []
for lang in langs:
    lang_Codes.append(lang.text.lower())
while True:
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration = 0.2)
            audio  = recognizer.listen(mic)
            text = recognizer.recognize_google(audio)
            text = text.lower()
            print(f"Recognized {text}")
            if "open youtube" in text:
                webbrowser.open("https://www.youtube.com/")
            if "google" in text:
                new_text = text
                new_text = new_text.replace("search for", "")
                new_text = new_text.replace("google", "")
                new_text = new_text.replace("on", "")
                webbrowser.open(f"https://www.google.com/search?q={new_text}")
            if "translate" in text:
                #new_text = text
                temp = text
                #new_text = new_text.replace("translate ", "")
                #new_text = new_text.replace(" ", "%20")
                #html_text = req.get(f'https://www.google.com/search?q={new_text}').text
                #soup = BeautifulSoup(html_text, 'lxml')
                #trans = soup.find('span', class_ = 'Y2IQFc')
                #print(trans)
                #webbrowser.open(f"https://www.google.com/search?q={new_text}")
                #webbrowser.open(f"https://translate.google.com/?hl=en&sl=auto&tl=fr&text={new_text}&op=translate")
                lang_text = temp.split("to ")[1]
                if lang_text in lang_Codes:
                    index = lang_Codes.index(lang_text)
                code = lang_Codes[index+1]
                final = temp.split("to ")[0]
                final = final.replace("translate", "")
                trans = Translator()
                #print(f"{final}, code = {code}")
                t = trans.translate(final, src = 'en', dest = code)
                sound = gTTS(text = (t.text), lang=code,slow = False)
                sound.save("welcome.mp3")
                os.system("start welcome.mp3")
                print(f" translation -> {t.text}")
                #translation = translator.translate(final, dest = code)
                #print(translation) 
                #webbrowser.open(f"https://translate.google.co.in/?sl=auto&tl={code}&text={final}&op=translate") 

            if "on youtube" in text and "search" in text:
                new_text = text
                new_text = new_text.replace("search for", "")
                new_text = new_text.replace("on youtube", "")
                new_text = new_text.replace(" ", '+')
                webbrowser.open(f'"https://www.youtube.com/results?search_query={new_text}')
            if "play" in text or ("on youtube" in text and "search" not in text):
                new_text = text
                new_text = new_text.replace("on", "")
                new_text = new_text.replace("youtube", "")
                new_text = new_text.replace("play", "")
                videosSearch = VideosSearch(new_text, limit = 1)
                arr = str(videosSearch.result()).split("'link': '")
                arr2 = arr[2].split("', 'shelfTitle")
                final_Link = arr2[0]
                webbrowser.open(final_Link)
                #webbrowser.open(f"https://www.youtube.com/results?search_query={new_text}")
    except sr.UnknownValueError():
        recognizer = sr.Recognizer()
        pass





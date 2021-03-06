#Library imports
import speech_recognition as sr
import pyttsx3
import wikipedia
import requests

#Text to speech and speech recognition initialization
r = sr.Recognizer()
tts = pyttsx3.init()

#Search Wikipedia Function
def searchWiki(term):
    print(f"Searching wikipedia for '{term}'...")
    say(f"Searching wikipedia for '{term}'...")
    search = term
    try:
        search = wikipedia.summary(term, sentences=3)
    except wikipedia.DisambiguationError as e:
        search2 = e.options[0]
        search = wikipedia.summary(search2, sentences=3)
        print("Warning, disambiguation detected, the result may not be exactly what you searched.")
        say("Warning, disambiguation detected, the result may not be exactly what you searched.")
    except requests.exceptions.ConnectionError:
        search = "Cannot connect to Wikipedia..."
    except wikipedia.PageError:
        search = "The page, {term}, does not exist, please try again."
    finally:
        print(search+"\n")
        say(search)

#Speak function, it exists to make speaking easier to work with for me
def say(words):
    tts.say(words)
    tts.runAndWait()

#The main voice recognition loop
def main():
    print("In search/awake mode...")
    print("What do you want to search Wikipedia for?")
    say("What do you want to search wikipedia for")
    
    #Gets mich input
    with sr.Microphone() as source:
        print("Wait 1 second before talking")
        r.adjust_for_ambient_noise(source)
        print(f"Energy threshold has been set to {r.energy_threshold}")
        print("Say something!")
        audio = r.listen(source)
    
    #Does speech recognition things
    try:
        text = r.recognize_google(audio)
        if "search wiki for " in text or "search for " in text or "search Wikipedia for " in text:
            text = text.replace("search wiki for ", "")
            text = text.replace("search for ", "")
            text = text.replace("search Wikipedia for ", "")
            print("Text has been replaced.")
        print(f"Google Speech Recognition thinks you said: {text}")
        if text == "quit":
            print("Quitting the program, goodbye.")
            say("Quitting the program, goodbye.")
            quit()
        elif text == "a random article" or text == "random artice" or text == "random":
            print("Ok, searching Wikipedia for a random article...")
            say("Ok, searching Wikipedia for a random article...")
            searchWiki(wikipedia.random(pages=1))
        elif text == "nevermind" or text == "never mind" or text == "cancel":
            print("Ok, cancelling search...")
            say("Ok, cancelling search...")
        else:
            searchWiki(text)
    
    #If it didn't understand what i said
    except sr.UnknownValueError:
        print("Speech not recognized, please try again.")
        say("Speech not recognized, please try again.")
    
    #If it couldn't connect to Google's voice recognition servers
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        say("Sorry, I could not get results from Google Speech Recognition, try again later.")

#The loop that listens in for the 'wake up' command
while True:
    print("In listener/idle mode...")
    #Gets mich input
    with sr.Microphone() as source2:
        print("Wait 1 second before talking")
        r.adjust_for_ambient_noise(source2)
        print(f"Energy threshold has been set to {r.energy_threshold}")
        print("Say something!")
        audio2 = r.listen(source2)
    
    #Does speech recognition stuff
    try:
        text2 = r.recognize_google(audio2)
        print(f"I heard '{text2}'")

        #If you say more than just 'hey wiki'
        if "hey wiki search for" in text2 or "hey Wiki search for" in text2:
            text2 = text2.replace("hey wiki search for ", "")
            text2 = text2.replace("hey Wiki search for ", "")
            print("Removed 'hey wiki search for ' from the text. Performing search...")
            searchWiki(text2)

        #If you just say 'hey wiki'
        elif text2 == "hey wiki" or "hey wiki" in text2 or text2 == "play wiki" or "play wiki" in text2:
            print(f"I heard '{text2}'")
            main()
        elif text2 == "quit":
            print("Quitting...")
            quit()
        else:
            print("Text not valid, looping back...")
    
    #If it didn't understand what I said
    except sr.UnknownValueError:
        print("Looping back to start of while true loop...\n")
    
    #If it couldn't connect to Google's voice recognition servers
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        #say("Sorry, I could not get results from Google Speech Recognition, try again later.")


#License below because why not :)))
"""
Made by Seb C: in 2020. I do not own any of the libraries used and some of the 
code was taken from the examples in their respective documentation and somewhat modified by me. All 
rights go to their respective owners.

-----------------------------------------------------------------------------------------------------

Copyright 2020 Seb C:

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

-----------------------------------------------------------------------------------------------------
|-------------------------|
|   ____    __     ______ |
|  / __/__ / /    / ___(_)|
| _\ \/ -_) _ \  / /___   |
|/___/\__/_.__/  \___(_)  |
|-------------------------|
Bruh moment.
"""

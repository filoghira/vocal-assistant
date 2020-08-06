import hueLights as Lights
from const import *
from exceptions import *
import os
import credenziali as cr
import speech_recognition as sr
import musicPlayer
import youtube
import time
import pyttsx3 as speech

def login(auth_state, key, voice):
    #Defining the audio source
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    #Noise adjust
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    #Get username
    while True:
        #Input
        with microphone as source:
            voice.say("Dimmi il tuo username")
            voice.runAndWait()
            audio = recognizer.listen(source, phrase_time_limit = 5)

        #Try recognize
        try:
            username = recognizer.recognize_google(audio, language="it-IT")
            break
        #No audio
        except sr.UnknownValueError:
            voice.say("Non ho capito cosa hai detto. Prova a ripetere.")
            voice.runAndWait()
        #Other errors
        except sr.RequestError as e:
            print("Error while recognizing the audio: {0}".format(e))

    #Get password
    while True:
        #Input
        with microphone as source:
            voice.say("Dimmi la password")
            voice.runAndWait()
            audio = recognizer.listen(source, phrase_time_limit = 5)

        #Try recognize
        try:
            password = recognizer.recognize_google(audio, language="it-IT")
            break
        #No audio
        except sr.UnknownValueError:
            voice.say("Non ho capito cosa hai detto. Prova a ripetere.")
            voice.runAndWait()
        #Other errors
        except sr.RequestError as e:
            print("Error while recognizing the audio: {0}".format(e))

    #Try to login
    try:
        auth_level = cr.login(username, password, key)
    except WrongPassword:
        voice.say("Login fallito. Password errata. L'accesso verrà eseguito come " + auth_levels[auth_state])
        voice.runAndWait()
    except UserNotFound:
        voice.say("Login fallito. Utente inesistente. L'accesso verrà eseguito come " + auth_levels[auth_state])
        voice.runAndWait()
    #Login successfully
    else:
        auth_state = auth_level
        voice.say('Login eseguito con successo. Benvenuto ' + username)

    return auth_state

def elaborate(text, auth_state, key, mixer):
    #Set variables
    running = True

    #Every possible command

    #Stop the program
    if text in turn_off:
        #If the user has enough authorization
        if auth_state >= auth_levels['Admin']:
            print("Spegnimento in corso...")
            running = False
        else:
            #Try to login with higher authorization level
            print("Livello di autorizzazione insufficiente. Esegui l'accesso.")
            auth_state = login(auth_state, key, voice)
            if auth_state >= admin:
                print("Spegnimento in corso...")
                running = False
            else:
                print("Impossibile spegnere il sistema. Autorizzazione insufficiente.")
    elif any(word in text for word in play_music):

        for word in play_music:
            if word in text:
                text = text.replace(word,' ')

        text.lstrip()

        link = youtube.search(text)

        path = youtube.download_mp4(link)

        path = youtube.convert_mp4_to_mp3(path)

        mixer = [musicPlayer.play(path) , path]
    elif text in pause_music:
        musicPlayer.pause(mixer[0])
    elif text in resume_music:
        musicPlayer.resume(mixer[0])
    elif text in stop_music:
        musicPlayer.stop(mixer[0],mixer[1])
    elif any(word in text for word in turn_on_lightroom):

        for word in turn_on_lightroom:
            if word in text:
                text = text.replace(word,' ')

        Lights.turn_on_room(text)
    #Do nothing
    elif text in cancel:
        print("Ok, come non detto")

    return running, auth_state, mixer

def main():
    #Setup the loop
    running = True
    #Initialize audio player
    mixer = {0:0}
    #Initialize text to speach
    voice = speech.init()
    #Adjusting speed rate
    voice.setProperty("rate",130)
    #Define audio source
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    #Adjust noise
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    #Key to decrypt files
    voice.say("Avvio del sistema in corso. Inserire la chiave di decrittazione.")
    voice.runAndWait()
    key = input('--> ')
    #Test the key
    try:
        cr.try_key(key)
    except WrongKey:
        #Shutdown
        voice.say("Chiave non corretta. Spengo il sistema.")
        voice.runAndWait()
        running = False
    else:
        voice.say("Decrittazione completata.")
        voice.runAndWait()

    #Initialize
    auth_state = 0
    #First login
    if running:
        auth_state = login(auth_levels['Ospite'], key, voice)

    #Main loop
    while running:
        #Get the audio
        with microphone as source:
            audio = recognizer.listen(source)

        #Try recognizing the audio with the google API
        try:
            text = recognizer.recognize_google(audio, language="it-IT").casefold()

            #If the audio contains a call to the assistant
            if text in call_assistant:

                voice.say("Dimmi")
                voice.runAndWait()

                done = False

                #Elaborate loop
                while not done:

                    #Wait for the command audio input
                    with microphone as source:
                        audio = recognizer.listen(source, phrase_time_limit = 5)

                    #Try to recognize it
                    try:
                        text = recognizer.recognize_google(audio, language="it-IT")

                    #If there is no audio, wait for other input
                    except sr.UnknownValueError:
                        voice.say("Non ho capito, prova a ripetere")

                    #Other errors
                    except sr.RequestError as e:
                        print("Error while analyzing the audio: {0}".format(e))

                    else:
                        done = True
                        print(text)

                #Send the audio to the elaborate function
                running, auth_state, mixer = elaborate(text.lower(), auth_state, key, mixer)

        #If there is no audio
        except sr.UnknownValueError:
            print("No input")
        #Other errors
        except sr.RequestError as e:
            print("Error while analyzing the audio: {0}".format(e))

if __name__ == "__main__":
    main()
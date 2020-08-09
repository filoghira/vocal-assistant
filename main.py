import hueLights as Lights
from const import *
from exceptions import *
import os
import crypt as cr
import speech_recognition as sr
import musicPlayer
import youtube
import time
import pyttsx3 as speech
import settings

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
        voice.runAndWait()

    return auth_state

def elaborate(text, auth_state, key, mixer, voice):
    #Set variables
    running = True

    #Every possible command

    #Stop the program
    if text in shutdown:
        #If the user has enough authorization
        if auth_state >= auth_levels['Admin']:
            voice.say("Spegnimento in corso")
            voice.runAndWait()
            running = False
        else:
            #Try to login with higher authorization level
            voice.say("Livello di autorizzazione insufficiente. Esegui l'accesso.")
            voice.runAndWait()
            auth_state = login(auth_state, key, voice)
            if auth_state >= auth_levels['Admin']:
                voice.say("Spegnimento in corso")
                voice.runAndWait()
                running = False
            else:
                voice.say("Impossibile spegnere il sistema. Livello di autorizzazione insufficiente.")
                voice.runAndWait()
    #Play a song
    elif any(word in text for word in play_music):

        for word in play_music:
            if word in text:
                text = text.replace(word,' ')

        text.lstrip()

        link = youtube.search(text)

        path = youtube.download_mp4(link)

        path = youtube.convert_mp4_to_mp3(path)

        mixer = [musicPlayer.play(path) , path]
    #Pause the song
    elif text in pause_music:
        musicPlayer.pause(mixer[0])
    #Resume the song
    elif text in resume_music:
        musicPlayer.resume(mixer[0])
    #Stop the song
    elif text in stop_music:
        musicPlayer.stop(mixer[0],mixer[1])
    #Turn on all lights in a room
    elif any(word in text for word in turn_on_light_room):

        for word in turn_on_light_room:
            if word in text:
                text = text.replace(word,' ')

        try:
            Lights.turn_on_room(text)
        except RoomNotFound:
            voice.say("Impossibile trovare la stanza.")
            voice.runAndWait()
        else:
            voice.say("Fatto")
            voice.runAndWait()
    #Turn off all lights in a room
    elif any(word in text for word in turn_off_light_room):

        for word in turn_off_light_room:
            if word in text:
                text = text.replace(word,' ')

        try:
            Lights.turn_off_room(text)
        except RoomNotFound:
            voice.say("Impossibile trovare la stanza.")
            voice.runAndWait()
        else:
            voice.say("Fatto")
            voice.runAndWait()
    #Turn on lights in the default room
    elif text == turn_on:

        room = setting.get_setting("lights_room")

        try:
            Lights.turn_on_room(room)
        except RoomNotFound:
            voice.say("Impossibile trovare la stanza.")
            voice.runAndWait()
        else:
            voice.say("Fatto")
            voice.runAndWait()
    #Turn off lights in the default room
    elif text == turn_off:

        room = setting.get_setting("lights_room")

        try:
            Lights.turn_off_room(room)
        except RoomNotFound:
            voice.say("Impossibile trovare la stanza.")
            voice.runAndWait()
        else:
            voice.say("Fatto")
            voice.runAndWait()
    #Change a setting
    elif text in set_setting:

        #Check authorization level
        if auth_state >= auth_levels['Utente generico']:
            settings.change_setting(voice)
        else:
            # Try to login with higher authorization level
            voice.say("Livello di autorizzazione insufficiente. Esegui l'accesso.")
            voice.runAndWait()
            auth_state = login(auth_state, key, voice)
            if auth_state >= auth_levels['Utente generico']:
                settings.change_setting(voice)
            else:
                voice.say("Impossibile modificare le impostazioni. Livello di autorizzazione insufficiente.")
                voice.runAndWait()
    #Reset settings
    elif text in reset_settings:
        # Check authorization level
        if auth_state >= auth_levels['Admin']:
            settings.reset_to_default(voice)
        else:
            # Try to login with higher authorization level
            voice.say("Livello di autorizzazione insufficiente. Esegui l'accesso.")
            voice.runAndWait()
            auth_state = login(auth_state, key, voice)
            if auth_state >= auth_levels['Admin']:
                settings.reset_to_default(voice)
            else:
                voice.say("Impossibile resettare le impostazioni. Livello di autorizzazione insufficiente.")
                voice.runAndWait()
    #Do nothing
    elif text in cancel:
        voice.say("Come non detto")
        voice.runAndWait()

    return running, auth_state, mixer

def main():
    #Setup the loop
    running = True

    #Initialize audio player
    mixer = {0:0}

    #Initialize text to speach
    voice = speech.init()
    #Adjusting speed rate
    try:
        voice.setProperty("rate",int(settings.get_setting("speech_rate")))
    except SettingNotFound:
        print("Can't set speech rate. Setting to default (130).")
        voice.setProperty("rate",130)
    try:
        voice.setProperty("volume",int(settings.get_setting("speech_volume")))
    except SettingNotFound:
        print("Can't set speech volume. Setting to default (1).")
        voice.setProperty("volume",1)

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
                running, auth_state, mixer = elaborate(text.lower(), auth_state, key, mixer, voice)

        #If there is no audio
        except sr.UnknownValueError:
            print("No input")
        #Other errors
        except sr.RequestError as e:
            print("Error while analyzing the audio: {0}".format(e))

if __name__ == "__main__":
    main()
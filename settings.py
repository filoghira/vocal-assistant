import json
import pyttsx3 as speech
import speech_recognition as sr
import shutil,os
from datetime import datetime
from exceptions import *

#Get the actual value of a setting
def get_setting(setting):

    #Get the setting
    file = open("/settings/settings.json", "r")

    data = json.load(file)

    #If it exists, save it
    if setting in data.keys():
        output = data[setting]
    else:
        raise SettingNotFound(setting)

    #Close file
    file.close()

    return output

#Set the value of a setting
def set_setting(setting, value):

    #Get all settings
    file = open("/settings/settings.json", "r")
    data = json.load(file)
    file.close()

    #Check if setting exists
    if setting in data.keys():
        #Update the setting
        data[setting] = value

        file = open("/settings/settings.json", "w")
        # noinspection PyTypeChecker
        json.dump(data,"")
        file.close()
    else:
        raise SettingNotFound(setting)

#Change a setting
def change_setting(voice):

    #Inizialize variables
    changing = True
    setting = ""
    value = ""

    # Defining the audio source
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Noise adjust
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    #Ask for the setting
    while True:
        #Input
        with microphone as source:
            voice.say("Quale impostazione vuoi modificare?")
            voice.runAndWait()
            audio = recognizer.listen(source, phrase_time_limit = 5)

        #Try recognize
        try:
            setting = recognizer.recognize_google(audio, language="it-IT")
            setting = setting.lower()

            #If the user asked to stop
            if setting in cancel:
                voice.say("Come non detto.")
                voice.runAndWait()

                changing = False
                break
            else:
                #Check if the setting exist
                try:
                    get_setting(setting)
                except SettingNotFound:
                    voice.say("L'impostazione non esiste. Prova ancora.")
                    voice.runAndWait()
                else:
                    break
        #No audio
        except sr.UnknownValueError:
            voice.say("Non ho capito cosa hai detto. Prova a ripetere.")
            voice.runAndWait()
        #Other errors
        except sr.RequestError as e:
            print("Error while recognizing the audio: {0}".format(e))

    #Ask for the new value
    if changing:
        while True:
            # Input
            with microphone as source:
                voice.say("Che valore vuoi impostare?")
                voice.runAndWait()
                audio = recognizer.listen(source, phrase_time_limit=5)

            # Try recognize
            try:
                value = recognizer.recognize_google(audio, language="it-IT")

                #If the user asked to stop
                if setting in cancel:
                    voice.say("Come non detto.")
                    voice.runAndWait()

                    changing = False
                    break
                else:
                    break
            # No audio
            except sr.UnknownValueError:
                voice.say("Non ho capito cosa hai detto. Prova a ripetere.")
                voice.runAndWait()
            # Other errors
            except sr.RequestError as e:
                print("Error while recognizing the audio: {0}".format(e))

    #Set the new value
    if changing:
        set_setting(setting,value)

        voice.say("Impostazione " + setting + "modificata con successo in " + value)
        voice.runAndWait()

#Create a backup of the settings file
def do_backup():

    #Count how many backups there are
    path, dirs, files = next(os.walk("/usr/lib"))
    backup_count = len(files)

    #Get date and time
    date_time = now.strftime("%d_%m_%Y_%H_%M_%S")

    #Create backup
    shutil.move("/settings/settings.json", "/settings/backups/settings_" + backup_count + "_" + datetime + ".json.backup")

#Reset settings to default values
def reset_settings():

    #Delete the old settings file
    if os.path.isfile("/settings/settings.json"):
        os.remove("/settings/settings.json")

    #Copy the default backup
    shutil.copy("/settings/settings_default.json.backup", "/settings/settings.json")

#Change settings to default value
def reset_to_default(voice):

    #Initialize variables
    changing = True
    backup = False

    # Defining the audio source
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Noise adjust
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    #Ask if the user is sure
    while True:
        #Input
        with microphone as source:
            voice.say("Sei sicuro di voler resettare le impostazioni?")
            voice.runAndWait()
            audio = recognizer.listen(source, phrase_time_limit = 5)

        #Try recognize
        try:
            answer = recognizer.recognize_google(audio, language="it-IT")
            answer = answer.lower()

            #If the user asked to stop
            if answer == "no":
                voice.say("Come non detto.")
                voice.runAndWait()

                changing = False
                break
            elif answer == "yes":
                break
        #No audio
        except sr.UnknownValueError:
            voice.say("Non ho capito cosa hai detto. Prova a ripetere.")
            voice.runAndWait()
        #Other errors
        except sr.RequestError as e:
            print("Error while recognizing the audio: {0}".format(e))

    #Ask if the user wants a backup of his settings
    if changing:
        while True:
            #Input
            with microphone as source:
                voice.say("Vuoi fare un backup delle tue attuali impostazioni?")
                voice.runAndWait()
                audio = recognizer.listen(source, phrase_time_limit = 5)

            #Try recognize
            try:
                answer = recognizer.recognize_google(audio, language="it-IT")
                answer = answer.lower()

                #If the user doesn't want a backup
                if answer == "no":
                    voice.say("Ok, proseguiamo")
                    voice.runAndWait()

                    break
                elif answer == "yes":
                    do_backup()

                    voice.say("Backup completato.")
                    voice.runAndWait()

            #No audio
            except sr.UnknownValueError:
                voice.say("Non ho capito cosa hai detto. Prova a ripetere.")
                voice.runAndWait()
            #Other errors
            except sr.RequestError as e:
                print("Error while recognizing the audio: {0}".format(e))

    #Restore settings
    if changing:
        reset_settings()

        voice.say("Ripristino delle impostazioni avvenuto con successo.")
        voice.runAndWait()
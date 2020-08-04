from hueLights import *
from const import *
from exceptions import *
from pytube import YouTube
from youtube_search import YoutubeSearch
from moviepy.editor import *
from pathvalidate import sanitize_filename
import os
import credenziali as cr
import speech_recognition as sr
import pygame.mixer_music


def login(auth_state, key):
    #Defining the audio source
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    #Setting variables
    username = ""
    password = ""

    #Noise adjust
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    #Get username
    while True:
        #Input
        with microphone as source:
            print("Nome utente: ")
            audio = recognizer.listen(source, phrase_time_limit = 5)

        #Try recognize
        try:
            username = recognizer.recognize_google(audio, language="it-IT")
            break
        #No audio
        except sr.UnknownValueError:
            print("Non ho capito cosa hai detto. Prova a ripetere.")
        #Other errors
        except sr.RequestError as e:
            print("Errore mentre provo a riconoscere l'audio: {0}".format(e))

    #Get password
    while True:
        #Input
        with microphone as source:
            print("Password: ")
            audio = recognizer.listen(source, phrase_time_limit = 5)

        #Try recognize
        try:
            password = recognizer.recognize_google(audio, language="it-IT")
            break
        #No audio
        except sr.UnknownValueError:
            print("Non ho capito cosa hai detto. Prova a ripetere.")
        #Other errors
        except sr.RequestError as e:
            print("Errore mentre provo a riconoscere l'audio: {0}".format(e))

    #Try to login
    try:
        auth_level = cr.login(username, password, key)
    except :
        print("Login fallito")
    #Login successfully
    else:
        auth_state = auth_level
        print('Login eseguito con successo. Benvenuto ' + username)

    return auth_state

def play(song):

    #Search on youtube and pick first result
    result = YoutubeSearch(song, max_results=1).to_dict()

    #Get the link
    link = 'https://www.youtube.com' + result[0].get('url_suffix')

    #Get the video object
    yt = YouTube(link)

    #Select the quality and type of video
    stream = yt.streams.filter().first()

    #Download the video
    stream.download()

    #Select path
    path = str(stream.default_filename)

    #Wait for download
    while not os.path.isfile(path):
        pass

    #Convert the video
    video = VideoFileClip(path)
    path_mp3 = path.rstrip("4")
    path_mp3 += "3"
    video.audio.write_audiofile(path_mp3)

    #Load and play the song
    pygame.mixer_music.load(path_mp3)
    pygame.mixer_music.play()

def elaborate(text, auth_state, key):
    #Set variables
    running = True

    #Every possible command

    #Stop the program
    if text in turn_off:
        #If the user has enough authorization
        if auth_state >= admin:
            print("Spegnimento in corso...")
            running = False
        else:
            #Try to login with higher authorization level
            print("Livello di autorizzazione insufficiente. Esegui l'accesso.")
            auth_state = login(auth_state, key)
            if auth_state >= admin:
                print("Spegnimento in corso...")
                running = False
            else:
                print("Impossibile spegnere il sistema. Autorizzazione insufficiente.")
    elif any(word in text for word in play_music):
        play(text)

    #Do nothing
    elif text in cancel:
        print("Ok, come non detto")

    return running, auth_state

running = True

#Key to decrypt files
print('Avvio del sistema.')
key = input('Inserire chiave di decrittazione: ')

try:
    cr.tryKey(key)
except WrongKey:
    print('Arresto del sistema')
    running = false
else:
    print('Chiave corretta. Inizializzo il sistema.')
play("old town road")
#First login
#auth_state = login(-1, key)
auth_state = 2

#Define audio source
recognizer = sr.Recognizer()
microphone = sr.Microphone()
#Adjust noise
with microphone as source:
    recognizer.adjust_for_ambient_noise(source)

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

            print("Dimmi pure")

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
                    print("Non ho capito, prova a ripetere")

                #Other errors
                except sr.RequestError as e:
                    print("Errore mentre provo a riconoscere l'audio: {0}".format(e))

                else:
                    done = True
                    print(text)

            #Send the audio to the elaborate function
            running, auth_state = elaborate(text.lower(), auth_state, key)

    #If there is no audio
    except sr.UnknownValueError:
        print("Nessun input")
    #Other errors
    except sr.RequestError as e:
        print("Errore mentre provo a riconoscere l'audio: {0}".format(e))

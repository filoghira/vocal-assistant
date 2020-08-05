import os
from audioplayer import AudioPlayer

def play(path):
    music = AudioPlayer(path)
    music.play()

    return music

def pause(music):
    music.pause()

def resume(music):
    music.resume()

def stop(music,path):
    music.stop()
    music.close()
    os.remove(path)
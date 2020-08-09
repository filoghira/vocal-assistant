import json
from exceptions import *

def get_setting(setting):

    #Get the setting
    file = open("settings.json", "r")

    data = json.load(file)

    #If it exists, save it
    if setting in data.keys():
        output = data[setting]
    else:
        raise SettingNotFound(setting)

    #Close file
    file.close()

    return output

def set_setting(setting, value):

    #Get all settings
    file = open("settings.json", "r")
    data = json.load(file)
    file.close()

    #Check if setting exists
    if setting in data.keys():
        #Update the setting
        data[setting] = value

        file = open("settings.json", "w")
        # noinspection PyTypeChecker
        json.dump(data,"")
        file.close()
    else:
        raise SettingNotFound(setting)
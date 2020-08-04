import pyAesCrypt
import os
from exceptions import *

# KEY = hCzJUPXWxuJP
# admin admin

buffer_size = 64 * 1024

def tryKey(key):
    pyAesCrypt.decryptFile("test.txt.aes", "testD.txt", key, buffer_size)

    with open('testD.txt','r') as file:
        #Get datas
        data = file.read()

        if data != "OK":
            raise WrongKey

        #Close file
        file.close()

    # Crypt and delete
    pyAesCrypt.encryptFile("testD.txt", "test.txt.aes", key, buffer_size)
    os.remove("testD.txt")

#Add a new user
def register(username, password, auth_level, key):

    #Set variables
    credentials = {}

    #Decrypt storage file
    pyAesCrypt.decryptFile("data.txt.aes", "dataout.txt", key, buffer_size)

    #Open decrypted file
    with open('dataout.txt','r+') as file:
        #Get datas
        for line in file:
            username_read, password_read, auth_level_read = line.strip().split(' ')
            credentials[username_read] = password_read

        #If there is already an user
        if username in credentials:
            raise UserAlreadyExist(username)
        #Else register the new user
        else:
            file.write(username + ' ' + password + ' ' + auth_level)

        #Close file
        file.close()

    #Crypt and delete
    pyAesCrypt.encryptFile("dataout.txt", "data.txt.aes", key, buffer_size)
    os.remove("dataout.txt")

#Remove an user
def removeUser(username, password, key):
    #Set variables
    credentials = {}

    #Decrypt file
    pyAesCrypt.decryptFile("data.txt.aes", "dataout.txt", key, buffer_size)

    #Open file
    with open('dataout.txt', 'r+') as file:
        #Get datas
        for line in file:
            username_read, password_read = line.strip().split(' ')
            credentials[username_read] = password_read

        #If there is'n the user
        if username not in credentials:
            raise UserNotFound
        #If the password is wrong
        elif credentials[username] != password:
            raise WrongPassword
        #Everything correct
        else:
            del credentials[username]

        #Close file
        file.close()

    #Open file and reset it
    with open('dataout.txt', 'w') as file:
        #Update credentials
        for user in credentials:
            file.write(username + ' ' + password)
        #Close file
        file.close()

    #Crypt and delete
    pyAesCrypt.encryptFile("dataout.txt", "data.txt.aes", key, buffer_size)
    os.remove("dataout.txt")

    return result

#Reset the credentials
def resetFile(key):

    file = open('dataout.txt', 'w+')
    file.close()

    #Crypt and delete
    pyAesCrypt.encryptFile("dataout.txt", "data.txt.aes", key, buffer_size)
    os.remove("dataout.txt")

#Login
def login(username, password, key):
    #Set variables
    credentials = {}

    #Decrypt
    pyAesCrypt.decryptFile("data.txt.aes", "dataout.txt", key, buffer_size)

    #Open file
    with open('dataout.txt', 'r+') as file:
        #Get datas
        for line in file:
            username_read, password_read, auth_level_read = line.strip().split(' ')
            credentials[username_read] = password_read

        #If username wrong password correct
        if username not in credentials:
            raise UserNotFound
        # If username correct password wrong
        if credentials[username] != password:
            raise WrongPassword
        #Everything correct
        else:
            auth_level = auth_level_read

        #Close file
        file.close()

    #Crypt and delete
    pyAesCrypt.encryptFile("dataout.txt", "data.txt.aes", key, buffer_size)
    os.remove("dataout.txt")

    return int(auth_level)
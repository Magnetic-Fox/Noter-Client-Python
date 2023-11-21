#! /usr/bin/env python3

###############################################################################
# Noter REST Client API 1.0
# (C)2021-2023 Bartłomiej "Magnetic-Fox" Węgrzyn!
###############################################################################

import requests

###############################################################################
# GLOBAL VARIABLES
###############################################################################

api_url=""
user_agent="Noter REST PY/1.0"
headers = {"User-Agent": user_agent}

###############################################################################
# HELPER FUNCTIONS
###############################################################################

# Init function
def setAPIUrl(new_api_url):
    global api_url
    api_url=new_api_url
    return

# Function for easy credentials tuple creation
def makeCredentials(username, password):
    return (username,password)

# Function for creating partial note (for adding or updating)
def makeNote(subject, entry):
    note = {}
    if(subject!=None):
        note["subject"]=subject
    if(entry!=None):
        note["entry"]=entry
    return note

# Function checking if there was an error in response
def isError(response):
    return ("error" in response) or ("error_code" in response)

# Function to add additional information to response if it was erroneus
def additionalOutput(response, statusCode):
    if(statusCode<200 or statusCode>=300):
        response["status_code"]=statusCode
    return response

###############################################################################
# MAIN API FUNCTIONS
###############################################################################

# Function for gathering server information
def getServerInfo():
    response = requests.get(api_url)
    return additionalOutput(response.json(),response.status_code)

# Function for creating new user
def createUser(credentials):
    request = {"username": credentials[0], "password": credentials[1]}
    response = requests.post(api_url+"/users", json=request, headers=headers)
    return additionalOutput(response.json(),response.status_code)

# Function for changing user password
def changeUserPassword(credentials, userID, oldPassword, newPassword):
    request = {"old_password": oldPassword, "new_password": newPassword}
    response = requests.put(api_url+"/users/"+str(userID)+"/password", auth=credentials, json=request, headers=headers)
    return response.status_code==204

# Function for gathering current user information
def getCurrentUserInfo(credentials):
    response = requests.get(api_url+"/users", auth=credentials, headers=headers)
    return additionalOutput(response.json(),response.status_code)

# Function for gathering user information using ID
def getUserInfo(credentials, userID):
    response = requests.get(api_url+"/users/"+str(userID), auth=credentials, headers=headers)
    return additionalOutput(response.json(),response.status_code)

# Function for deleting user by its ID
def deleteUser(credentials, userID, password):
    request = {"password": password}
    response = requests.delete(api_url+"/users/"+str(userID), auth=credentials, json=request, headers=headers)
    return response.status_code==204

# Function for gathering note list
def getNoteList(credentials):
    response = requests.get(api_url+"/notes", auth=credentials, headers=headers)
    return additionalOutput(response.json(),response.status_code)

# Function for gathering note by its ID
def getNote(credentials, noteID):
    response = requests.get(api_url+"/notes/"+str(noteID), auth=credentials, headers=headers)
    return additionalOutput(response.json(),response.status_code)

# Function for adding new note
def addNote(credentials, note):
    request = {"subject": note["subject"], "entry": note["entry"]}
    response = requests.post(api_url+"/notes", auth=credentials, json=request, headers=headers)
    return additionalOutput(response.json(),response.status_code)

# Function for updating a note by its ID
def updateNote(credentials, noteID, noteDiff):
    request = {}
    count = 0
    if("subject" in noteDiff):
        request["subject"]=noteDiff["subject"]
        count+=1
    if("entry" in noteDiff):
        request["entry"]=noteDiff["entry"]
        count+=1
    if(count<2):
        response=requests.patch(api_url+"/notes/"+str(noteID), auth=credentials, json=request, headers=headers)
    else:
        response=requests.put(api_url+"/notes/"+str(noteID), auth=credentials, json=request, headers=headers)
    return additionalOutput(response.json(),response.status_code)

# Function for locking note by its ID
def lockNote(credentials, noteID):
    request = {"locked": 1}
    response = requests.put(api_url+"/notes/"+str(noteID)+"/locked", auth=credentials, json=request, headers=headers)
    return additionalOutput(response.json(),response.status_code)

# Function for unlocking note by its ID
def unlockNote(credentials, noteID):
    request = {"locked": 0}
    response = requests.put(api_url+"/notes/"+str(noteID)+"/locked", auth=credentials, json=request, headers=headers)
    return additionalOutput(response.json(),response.status_code)

# Function for deleting note by its ID
def deleteNote(credentials, noteID):
    response = requests.delete(api_url+"/notes/"+str(noteID), auth=credentials, headers=headers)
    return response.status_code==204

###############################################################################    
# VERY ADDITIONAL FUNCTIONS
###############################################################################

# Function for printing note list in human-readable format
def printNoteList(noteList):
    for note in noteList:
        print(str(note["id"])+": "+note["subject"]+" ["+note["last_modified"]+"]")
    return

# Function for printing note in human-readable format
def printNote(note):
    print("ID:       "+str(note["id"]))
    print("Subject:  "+note["subject"])
    print("Entry:    \n\n"+note["entry"]+"\n")
    print("Added:    "+note["date_added"])
    print("...using: "+note["user_agent"])
    print("Modified: "+note["last_modified"])
    print("...using: "+note["last_user_agent"])
    print("Locked:   "+str((note["locked"]==1)))
    return
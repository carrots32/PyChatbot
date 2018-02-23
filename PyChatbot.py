"""
Name: Python ChatBot
Version: 3.4
Author: Matt Powell
Date: 06/07/2016 - Present

SCRIPT NOTES:
    Q = Question
    A = Answer
    Chat = the Questions with an Answer

"""

import time,random,sys,math,webbrowser,os,shutil
from os import system
from gtts import gTTS
from pygame import mixer
system("title ORION - Matt's Artificial Intelligence")
system("color 02")

global timestamp
global localtime
localtime = time.asctime(time.localtime(time.time()))
timestamp = "Startup Time: "+time.asctime(time.localtime(time.time()))+"\n\n"

#*****************************************************************************************************************************************************
# DEBUG FILE
#*****************************************************************************************************************************************************
def log(logType,texthere,value=''):
    global logfile
    logfile= open("debuglog.txt", "a") # Open log file for debugging output
    if logType== 'q':
        toLog= "User Asked:\t\t"
    elif logType== 'c':
        toLog= "User Command:\t\t"
    elif logType== 'a':
        toLog= "Orion Answered:\t\t"
    elif logType== 'n':
        toLog= "Log Note:\t\t"
    elif logType== 'e':
        toLog= "[ERROR]:\t\t"
    else:
        logfile.write("Logging ERROR. logType variable incorrect\n")
    logText= toLog+str(texthere)+str(value)+"\n"
    logfile.write(logText)
    logfile.close()

log('n',"\n\n****************NEW INSTANCE OF CHATBOT OPENED****************\n")
log('n',timestamp)

#*****************************************************************************************************************************************************
# INITIAL PROGRAM SETUP (Indexing all necessary lists from listQA.txt)
#*****************************************************************************************************************************************************
def initialSetup():
    log('n','intitialSetup() started')
    listQA= open("listQA.txt", "r") # Open QA File to read, makes into a list
    log('n','listQA.txt opened')
    global list_AllChat
    list_AllChat= listQA.read().split('<Q> ^ ')
    del list_AllChat[0] # Formatting: Delete \n

    list_Chat = [i.split('<A> ~ ') for i in list_AllChat] #Split Q/A

    global possibleChats

    # Counting Lines for Iteration
    num_lines = sum(1 for line in open('listQA.txt'))
    if (num_lines-1)%3 != 0: # Error Check
        log('e','Error with listQA.txt - there should be an even number of lines. Check readme.txt for formatting.')
        typeOutput("Error! 'listQA.txt' has not been correctly configured!")
        time.sleep(5)
        exit()
    possibleChats = int((num_lines-1)/3)
    log('n','Possible Questions - ',possibleChats)

    global AllQandA
    AllQandA=[]

    for x in range(possibleChats):
        list_ChatFormatted = [i.split('; ') for i in list_Chat[x]] #Split Q's and Split A's WITHIN 'Xth LIST ELEMENT' (which is another list)
        del list_ChatFormatted[0][-1] # Formatting: Delete \n (%n) from end
        del list_ChatFormatted[1][-1] # Formatting: Delete \n (%n) from end
        AllQandA.append(list_ChatFormatted)
        x=x+1
    
    log('n','All Questions and Answers formatted as lists. (AllQandA variable)')
    
    # To search only questions/answers
    # Here be dragons - don't judge my code here - I know it makes no sense but it's working...
    global allQ
    allQ =[single for double in AllQandA for single in double[::2]]
    log('n','All Questions formatted as separate lists. (allQ variable)')
    global allA
    allA =[single for double in AllQandA for single in double[1::2]]
    log('n','All Answers formatted as separate lists. (allA variable)')
    # Replace all '%n' to '\n'
    for i in range(possibleChats):
        for y in range(len(allA[i])):
            allA[i][y]=allA[i][y].replace("%n", "\n")
    
    # Close listQA file
    listQA.close()
    log('n','listQA.txt closed')
    log('n','intitialSetup() ended\n')

# Variable Descriptions:
#       list_AllChat:           ['QQQAAA','QQQAAA','QQQAAA'] (\n throughout) (also user's %n throughout A)
#       list_Chat:              [['QQQ','AAA'],['QQQ','AAA'],['QQQ','AAA']] (\n throughout)(also user's %n throughout A)
#       list_ChatFormatted      [['Q','Q','Q'],['A','A','A']] (Varying with each iteraion)(also user's %n throughout A)
#       AllQandA:               [[['Q','Q','Q'],['A','A','A']],[['Q','Q','Q'],['A','A','A']],[['Q','Q','Q'],['A','A','A']]] (\n removed and clear)(also user's %n throughout A)
#       AllQ:                   [['Q','Q','Q'],['Q','Q','Q'],['Q','Q','Q']]
#       AllA:                   [['A','A','A'],['A','A','A'],['A','A','A']] (Replaced %n with \n)

#*****************************************************************************************************************************************************
# OUTPUT PRESETS
#*****************************************************************************************************************************************************
# Setup for typed output
global typeOutput_speed
typeOutput_speed=(0.07)

# Typed output
def typeOutput(str):
    if speechEnabled:
        speech(str)
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(typeOutput_speed)
  
# Setup for speech output
speechcounter= 1    
currentDirectory= os.getcwd()
speechfileDirectory= currentDirectory+"\\speechfiles"
shutil.rmtree(speechfileDirectory)
os.makedirs(speechfileDirectory)
log('n','speechfile directory wiped')

# Default Speech Settings
speechEnabled = True
speechAccent = 'en-au'

# Speech output
def speech(toSpeak):
    global speechcounter
    global speechAccent
    speechfilename="speechfiles\speech"+str(speechcounter)+".mp3"
    tts = gTTS(text=toSpeak, lang=speechAccent)
    tts.save(speechfilename)
    mixer.init()
    mixer.music.load(speechfilename)
    mixer.music.play()
    speechcounter+=1
#*****************************************************************************************************************************************************
# USER INPUT AND RUNNING OF BOT
#*****************************************************************************************************************************************************
def runBot():
    userInput= input("\n\n > ").lower() # Retrieves User Input and converts to lowercase.
    # Ignore these special characters:
    userInput= userInput.replace(".", "")
    userInput= userInput.replace("?", "")
    userInput= userInput.replace("!", "")
    userInput= userInput.replace(",", "")
    userInput= userInput.replace("'", "")
        
    # BOT COMMANDS
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    availableCommands=['update','intro','exit','quit','close','help','wipe','erase','speed','commands','colour','color','speech', 'accent']
    if userInput in availableCommands:
        command(userInput)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    else:
        log('q',userInput)
        
        # Semi Correct Recognition Setup Process
        OnOffSemiCorrect=0 # For below stage
        userInputsplitinwords = userInput.split(' ') # Split input into a list of individual words
        for x in range(len(userInputsplitinwords)): # for the range of the length of that list (number of asked words)...
            if any(userInputsplitinwords[x] in y for y in allQ): # Checks if listofwords[x] is in a singlebracket(displayd here as y) for all singlebrackets in allQ.
                userInputsplitinwords_index= x # if so, assign to variable for below use
                OnOffSemiCorrect=1 # For below stage

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Perfect Recognition
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if any(userInput in x for x in allQ):
            for x in range(possibleChats): # From x=0
                if userInput in allQ[x]: # Checks if userInput is in allQ at index[x] (which is another list)
                    allQ_index= x # if so, assign to variable
                    break # stop looking for userInput

            OrionAnswer= " "+random.choice(allA[allQ_index])
            typeOutput(OrionAnswer)
            log('a', OrionAnswer)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Semi Correct Recognition
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        elif OnOffSemiCorrect==1:
            for x in range(possibleChats): # From x=0
                if userInputsplitinwords[userInputsplitinwords_index] in allQ[x]: # Checks if the listofwords' particular index (single word) is in allQ at index[x] (which is another list)
                    allQ_index= x # if so, assign to variable
                    break # stop looking for userInput

            OrionAnswer= " "+random.choice(allA[allQ_index])
            typeOutput(OrionAnswer)
            log('a', OrionAnswer)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # No Recognition
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
        else:
            typeOutput(" Sorry, I don't know what you mean.")
            log('e',"No Answer linked; Logged to unanswered.txt -> ",userInput)
            
            # Add to unanswered.txt
            unansweredTXT= open("unanswered.txt", "a")
            unansweredTXT.write(localtime+"\tUnanswered:\t"+userInput+"\n")
            unansweredTXT.close()
            
            # Google It?
            typeOutput("\n Would you like me to Google that for you?")
            YNgoogle= input(" [y/n]: ").lower()
            if (YNgoogle== 'y') or (YNgoogle== 'yes'):
                searchTerm=userInput.replace(" ", "+")
                log('n','Question Googled - ','https://www.google.com.au/search?q='+searchTerm)
                webbrowser.open('https://www.google.com.au/search?q='+searchTerm) 
            # TODO add option to add to list of questions (append txt file)
            
    runBot() # Loops entire function
    
#*****************************************************************************************************************************************************
# BOT COMMANDS (Must be included in availableCommands)
#*****************************************************************************************************************************************************
def command(attemptedCommand):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    if attemptedCommand=="update":
        log('c',attemptedCommand)
        log('n','================  UPDATE  ================')
        initialSetup()
        typeOutput(" Bot Updated Successfully.")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
    elif attemptedCommand=="speech":
        log('c',attemptedCommand)
        global speechEnabled
        speechEnabled= not speechEnabled # Toggles boolean value
        if speechEnabled:
            typeOutput(" Speech Enabled")
            log('n','User Re-Enabled Speech Output')
        else:
            typeOutput(" Speech Disabled")
            log('n','User Disabled Speech Output')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
    elif attemptedCommand=="accent":
        log('c',attemptedCommand)
        typeOutput(" Choose between an American, Australian, or British Accent for speech output.\n")
        selectAccent =input("           [ AU / UK / US ] : ").upper()
        global speechAccent
        if selectAccent== "AU":
            speechAccent='en-au'
        elif selectAccent== "UK":
            speechAccent='en-uk'
        elif selectAccent== "US":
            speechAccent='en-us'
        else:
            log('e','User tried to change Speech Accent to ',selectAccent)
            typeOutput(" Error! Invalid input.")
            return
        log('n','User Changed Speech Accent to ',selectAccent)
        typeOutput(" "+selectAccent+" Accent Selected")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       
    elif (attemptedCommand=="color") or (attemptedCommand=="colour"):
        log('c',attemptedCommand)
        print(
            "\t0 = Black\t8 = Gray\n"
            "\t1 = Blue\t9 = Light Blue\n"
            "\t2 = Green\tA = Light Green\n"
            "\t3 = Aqua\tB = Light Aqua\n"
            "\t4 = Red\t\tC = Light Red\n"
            "\t5 = Purple\tD = Light Purple\n"
            "\t6 = Yellow\tE = Light Yellow\n"
            "\t7 = White\tF = Bright White\n"
            )
        print(" Use the format BT where B is background and T is text")
        print(" For example, enter '02' for Green on Black.\n")
        colourVar =input(" Pick the teminal colour: ").lower()
        availableColours=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
        if (colourVar[0] in availableColours) and (colourVar[1] in availableColours):
            system("color "+ colourVar)
            log('n','Terminal colour changed to ',colourVar)
        else:
           log('e','User tried to change terminal colour to ',colourVar)
           typeOutput(" Error! Invalid input.")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~          
    elif (attemptedCommand=="exit") or (attemptedCommand=="quit") or (attemptedCommand=="close"):
        log('c',attemptedCommand)
        typeOutput(" Bye!")
        time.sleep(2)
        exit()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
    elif attemptedCommand=="help":
        log('c',attemptedCommand)
        typeOutput(" For a list of commands, type 'commands'.\nAll Responses come from listQA.txt\n")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
    elif (attemptedCommand=="wipe") or (attemptedCommand=="erase"):
        log('c',attemptedCommand)
        open("debuglog.txt", 'w').close()
        log('n',"Log Reset by user.")
        typeOutput(" Log file successfully erased.")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
    elif attemptedCommand=="speed":
        typespeedraw= input(" Enter new typing speed for Orion (Default 0.05 per letter. Choose between 0.01 and 0.5): ")
        typespeedraw= float(typespeedraw)
        if (typespeedraw >=0) and (typespeedraw <= 0.5):
            typeOutput_speed= typespeedraw
            log('n','typeOutput_speed changed to ',typeOutput_speed)
            typeOutput(" Typing speed altered successfully")
        else:
           log('e','User tried to change typeOutput_speed to ',typespeedraw)
           typeOutput(" Error! Invalid input.")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
    elif attemptedCommand=="commands":
        log('c',attemptedCommand)
        print("Available console commands:\n")
        print("Accent - Change between American, Australian, and Brittish Aceents for speech output")
        print("Close - Shuts down AI")
        print("Colour - Change terminal colour")
        print("Erase - Erases the contents of debuglog.txt")
        print("Exit - Shuts down AI")
        print("Help - Displays help information")
        print("Intro - Show startup information")
        print("Quit - Shuts down AI")
        print("Speech - Toggle voice output")
        print("Speed - Adjust Orion's typing speed")
        print("Update - Reloads listQA.txt")
        print("Wipe - Erases the contents of debuglog.txt")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
#*****************************************************************************************************************************************************
# GO!
#*****************************************************************************************************************************************************
initialSetup()
typeOutput("\n Hello and Welcome to Matt's AI... \n I am Orion, say something!")
runBot()

# If you get to here you've broken Python
print("You Are The Chosen One.")

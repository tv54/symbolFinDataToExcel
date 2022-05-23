from os import makedirs
from sys import exit
import datetime
import src.package.subpackage.othersrc.Constants as Constants

def handleError(error):
    formattedLine="Error received '{}'. Continue? (y,n): ".format(error)
    userIn=handleInput(formattedLine)
    match userIn.lower():
        case 'y':
            return
        case 'n':
            exitProgram()
    handleError(error)

def exitProgram():
    try:
        Constants.DISPLAYED_LINES_FILE.close()
        Constants.LOG_FILE.close()
    except:
        pass
    exit()

def readFile(filename):
    try:
        with open(filename, "r") as file:
            return file.read()
    except:
        return None

def checkKeyInDict(dict, key, defaultValue=0):
    if(key in dict):
        return dict[key]

    return defaultValue

def displayLine(line, printLine=True, addLineBreak=True):
    printLine and print(line)
    file=Constants.DISPLAYED_LINES_FILE
    if(file):
        try:
            if(addLineBreak):
                lBreak="\n"
            else:
                lBreak=""
            file.write("{}{}".format(line, lBreak))
        except:
            pass

def openDisplayedLinesFile():
    try:
        file=open("./" + Constants.OUTPUT_FOLDER + "/" + Constants.DISPLAYED_LINES_FILE_NAME, "w")
        file.write("\n---------------------------{}---------------------------\n".format(datetime.datetime.now()))
    except:
        file=None
    
    Constants.DISPLAYED_LINES_FILE=file

def log(data):
    if(Constants.LOG_DATA):
        try:
            with open("./" + Constants.OUTPUT_FOLDER + "/" + Constants.LOG_FILE_NAME, "a") as logFile:
                logFile.write("{}\n".format(str(data)))
        except:
            pass

def handleInput(inputText):
    displayLine(inputText, printLine=False)
    userInput=input(inputText)
    displayLine(userInput, printLine=False)
    return userInput

def createDir(dirName):
    try:
        makedirs(dirName)
    except:
        pass

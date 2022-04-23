from os import makedirs
from sys import exit
import datetime
from src.package.subpackage.othersrc.Constants import Constants

def handleError(error, logFile=None):
    formattedLine="Error received '{}'. Continue? (y,n): ".format(error)
    userIn=handleInput(formattedLine, logFile=logFile)
    match userIn.lower():
        case 'y':
            return
        case 'n':
            try:
                logFile.close()
            except:
                pass
            exitProgram()
    handleError(error, logFile)

def exitProgram():
    exit()

def readFile(filename):
    with open(filename, "r") as file:
        return file.read()

def checkKeyInDict(dict, key, defaultValue=0):
    if(key in dict):
        return dict[key]

    return defaultValue

def displayLine(line, file=None, printLine=True, addLineBreak=True):
    printLine and print(line)
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
        file=open("./" + Constants.OUTPUT_FOLDER + "/" + Constants.DISPLAYED_LINES_FILE, "w")
        file.write("\n---------------------------{}---------------------------\n".format(datetime.datetime.now()))
    except:
        file=0
    
    return file

def log(data):
    if (Constants.LOG_DATA):
        try:
            with open("./" + Constants.OUTPUT_FOLDER + "/" + Constants.LOG_FILE, "a") as logFile:
                logFile.write("{}\n".format(str(data)))
        except:
            pass

def handleInput(inputText, logFile=None):
    displayLine(inputText, file=logFile, printLine=False)
    userInput=input(inputText)
    displayLine(userInput, file=logFile, printLine=False)
    return userInput

def createDir(dirName):
    try:
        makedirs(dirName)
    except:
        pass

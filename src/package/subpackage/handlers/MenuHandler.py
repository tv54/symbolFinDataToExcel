from sys import stdout
from os import system
from datetime import date, datetime
from src.package.subpackage.othersrc.SearchData import SearchData
import src.package.subpackage.othersrc.Constants as Constants
from src.package.subpackage.othersrc.genFunc import exitProgram, handleInput, displayLine, exitProgram, readFile

class MenuHandler():

    def __printListWithInput(self, listDescriptor, selectionList, listItemPrefix="", lastItemNoPrefix=True):
        userIn = 0
        displayLine(listDescriptor + " (enter: 1)", printLine=True, addLineBreak=True)
        for i in range(len(selectionList)):
            if(i==len(selectionList)-1 and lastItemNoPrefix):
                listItemPrefix=""
            displayLine("\t{}. {}{}".format(i+1, listItemPrefix, selectionList[i]), printLine=True, addLineBreak=True)
        
        while(not type(userIn)==int or userIn>len(selectionList)+1 or userIn<1):
            userIn=handleInput("Selección: ")
            if(not userIn):
                userIn=1
            else:
                try:
                    userIn=int(userIn)
                except:
                    userIn=0
            
        return userIn

    def __clearConsole(self, searchData=[]):
        searchDataHeader=""
        system("cls")
        for data in searchData:
            searchDataHeader += "{} || ".format(data)
        displayLine(searchDataHeader, printLine=searchDataHeader)

    def __optionsMenu(self, selectedItemNumber=""):
        displayLine("No habilitado")

    def __dateValidator(self, dateToValidate, validateInputString=True, toDate=""):
        if(validateInputString):
            if(dateToValidate.__contains__("/")):
                try:
                    dateToValidate=datetime.strptime(dateToValidate, "%d/%m/%Y").date()
                except:
                    try:
                        dateToValidate=datetime.strptime(dateToValidate, "%d/%m/%y").date()
                    except:
                        dateToValidate=""
    
            else:
                dateToValidate=""
        if(dateToValidate and toDate and dateToValidate>toDate):
            return ""
        elif(dateToValidate and dateToValidate>datetime.now().date()):
            return datetime.now().date()
        return dateToValidate

    def __buildDataArr(self, *args):
        dataArr = []
        for data in args:
            if(data):
                dataArr.append(data)
        return dataArr

    def __mainProgMenu(self):
        symList=[]
        benchmark=""
        priceToDisplay=""
        toDate=""
        fromDate=""
        limit=0
        outputExcelName=""
        # ---- sym or list ----
        selectionList=["Escribir activo", "Lista de activos"]
        self.__clearConsole()
        userIn=self.__printListWithInput("Selección de activos:", selectionList)
        self.__clearConsole()
        match selectionList[userIn-1]:
            case "Escribir activo":
                sym=""
                while(not sym):
                    sym=handleInput("Activo a buscar: ").upper()
                symList.append(sym)
            case "Lista de activos":
                while(not symList):
                    userIn=input("Nombre del archivo con la lista (enter: 'symList.txt'): ")
                    if(not userIn):
                        userIn="./symList.txt"
                    elif(not userIn.__contains__(".")):
                        userIn+=".txt"
                        
                    listContent=readFile(f"./{userIn}")
                    if(listContent):
                        symList=listContent.split("\n")
                        sym=f"[{symList[0]}...]"
                
        # ---- benchmark ----
        self.__clearConsole(self.__buildDataArr(sym, benchmark, priceToDisplay, toDate, fromDate, outputExcelName))
        selectionList=["S&P500", "NASDAQ", "Sin benchmark"]
        userIn=self.__printListWithInput("Benchmark:", selectionList)
        if(selectionList[userIn-1]!="Sin benchmark"):
            benchmark=selectionList[userIn-1]
        self.__clearConsole(self.__buildDataArr(sym, benchmark, priceToDisplay, toDate, fromDate, outputExcelName))
        
        # ---- priceToDisplay ----
        selectionList=["close", "open"]
        userIn=self.__printListWithInput("Precio a usar:", selectionList)
        priceToDisplay=selectionList[userIn-1]
        self.__clearConsole(self.__buildDataArr(sym, benchmark, priceToDisplay, toDate, fromDate, outputExcelName))
        
        # ---- toDate ----
        while(not toDate):
            toDate=handleInput("Datos históricos diarios hasta fecha (d/m/a) (enter: hoy): ")
            if(not toDate.strip()):
                toDate = datetime.now().date()
            else:
                toDate=self.__dateValidator(toDate)
        self.__clearConsole(self.__buildDataArr(sym, benchmark, priceToDisplay, toDate, fromDate, outputExcelName))
        
        # ---- fromDate ----
        while(not fromDate):
            fromDate=handleInput("Datos históricos diarios desde fecha (d/m/a) o cantidad de años (max 5) (enter: 5 años): ")
            if(not fromDate.strip()):
                fromDate=date(toDate.year-5, datetime.now().month, datetime.now().day)
            else:
                try:
                    fromDate=int(fromDate)
                    fromDate=date(toDate.year-fromDate, datetime.now().month, datetime.now().day)
                except:
                    fromDate=self.__dateValidator(fromDate, toDate=toDate)
        self.__clearConsole(self.__buildDataArr(sym, benchmark, priceToDisplay, toDate, fromDate, outputExcelName))
        
        # ---- limit ----
        limit=toDate.year - fromDate.year
        if(limit>5):
            limit=5
        
        # ---- outputExcelName ----
        if(not symList):
            outputExcelName=handleInput("Nombre del excel (enter: {}.xlsx): ".format(sym))
            if(not outputExcelName):
                outputExcelName="{}.xlsx".format(sym)
            else:
                if(not outputExcelName.__contains__(".")):
                    outputExcelName += ".xlsx"
            self.__clearConsole(self.__buildDataArr(sym, benchmark, priceToDisplay, toDate, fromDate, outputExcelName))
        
        return SearchData(symList, benchmark, toDate, fromDate, limit, outputExcelName, priceToDisplay=priceToDisplay)

    def mainMenu(self):
        selectionList=["Iniciar aplicación", "Cerrar"]
        self.__clearConsole()
        userIn=self.__printListWithInput("Menu principal:", selectionList)
        self.__clearConsole()
        match selectionList[userIn-1]:
            case "Iniciar aplicación":
                searchData=self.__mainProgMenu()
                self.__clearConsole()
                return searchData
            case "Opciones":
                self.__optionsMenu(selectedItemNumber=userIn)
                return self.mainMenu()
            case "Cerrar":
                exitProgram()

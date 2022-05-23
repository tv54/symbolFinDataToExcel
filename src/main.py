from src.package.DataHandler import DataHandler
from src.package.subpackage.handlers.MenuHandler import MenuHandler
import src.package.subpackage.othersrc.Constants as Constants
from src.package.subpackage.othersrc.genFunc import handleError, handleInput, openDisplayedLinesFile, createDir, readFile

def main():
    setup()
    prog()

def prog():
    mh = MenuHandler()
    searchData=mh.mainMenu()
    symList=searchData.sym
    for i in range(len(symList)):
        searchData.sym=symList[i]
        searchData.outputExcelName=searchData.sym.upper()+".xlsx"
        
        dataHandler=DataHandler(
                                sym=searchData.sym, 
                                fromDate=searchData.fromDate, 
                                toDate=searchData.toDate, 
                                limit=searchData.limit, 
                                benchmark=searchData.benchmark, 
                                priceToDisplay=searchData.priceToDisplay,
                                )

        buildExcel(dataHandler)
        dataHandler.saveWorkbook(searchData.outputExcelName)
        
    if(len(symList)==1):
        input(f"Workbook saved successfully to '{Constants.OUTPUT_FOLDER}/{dataHandler.sym}', press any key to continue")
    else:
        input(f"Workbooks saved successfully to output folder '{Constants.OUTPUT_FOLDER}', press any key to continue")
        
    prog()
    
def setup():
    createDir(Constants.OUTPUT_FOLDER)
    openDisplayedLinesFile()
    
    apikeys=readFile("./apikeys.txt")
    
    if(not apikeys):
        handleError("No api key set (no api keys found in file 'apikeys.txt'")
        userIn=handleInput(f"Api key to use (enter:default key '{Constants.DEFAULT_API_KEY}'): ")
        if(not userIn):
            userIn=Constants.DEFAULT_API_KEY
            
        Constants.FMP_API_KEYS.append(userIn)
        
    else:
        Constants.FMP_API_KEYS=apikeys.split("\n")
    
def buildExcel(dataHandler):
    Constants.ENABLE_SUMMARY_SHEET and dataHandler.summarySheet()
    Constants.ENABLE_SYMBOL_HIST_DATA_SHEET and dataHandler.symbolHistData()
    Constants.ENABLE_CFS_SHEET and dataHandler.symbolFinancialStatements("cfs")
    Constants.ENABLE_BSS_SHEET and dataHandler.symbolFinancialStatements("bss")
    Constants.ENABLE_IS_SHEET and dataHandler.symbolFinancialStatements("is")
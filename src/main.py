from time import sleep
from src.package.DataHandler import DataHandler
from src.package.subpackage.handlers.MenuHandler import MenuHandler
from src.package.subpackage.othersrc.Constants import Constants
from src.package.subpackage.othersrc.genFunc import openDisplayedLinesFile, createDir

def main():
    createDir(Constants.OUTPUT_FOLDER)
    dlf = openDisplayedLinesFile()
    prog(dlf)

def prog(dlf):
    mh = MenuHandler(logFile=dlf)
    searchData=mh.mainMenu()

    dataHandler=DataHandler(
                            sym=searchData.sym, 
                            fromDate=searchData.fromDate, 
                            toDate=searchData.toDate, 
                            limit=searchData.limit, 
                            benchmark=searchData.benchmark, 
                            priceToDisplay=searchData.priceToDisplay,
                            logFile=dlf
                            )

    Constants.ENABLE_SUMMARY_SHEET and dataHandler.summarySheet()
    Constants.ENABLE_SYMBOL_HIST_DATA_SHEET and dataHandler.symbolHistData()
    Constants.ENABLE_CFS_SHEET and dataHandler.symbolFinancialStatements("cfs")
    Constants.ENABLE_BSS_SHEET and dataHandler.symbolFinancialStatements("bss")
    Constants.ENABLE_IS_SHEET and dataHandler.symbolFinancialStatements("is")
    dataHandler.saveWorkbook(searchData.outputExcelName)
    sleep(2)
    prog(dlf)
    
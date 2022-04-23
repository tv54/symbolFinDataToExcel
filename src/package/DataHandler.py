import datetime
from src.package.subpackage.handlers.FinSheetsHandler import FinSheetsHandler
from src.package.subpackage.handlers.ApiHandler import ApiHandler
from src.package.subpackage.othersrc.genFunc import log, displayLine, openDisplayedLinesFile

class DataHandler(FinSheetsHandler):

    def __init__(self, sym, fromDate=None, toDate=None, limit=0, benchmark="", priceToDisplay="close", logFile=None):
        self.sym=sym
        self.fromDate=fromDate
        self.toDate=toDate
        self.n=(toDate - fromDate).days
        self.limit=limit
        self.benchmark=benchmark
        self.priceToDisplay=priceToDisplay.lower()
        self.logFile=logFile
        self.bmkRes=self.__getBenchmark()
        super().__init__(n=self.n, benchmark=self.benchmark, bmkRes=self.bmkRes, priceToDisplay=self.priceToDisplay)

    def __getBenchmark(self):
        if(not self.benchmark):
            return
        sym=""
        match self.benchmark:
            case "S&P500":
                sym="^IXIC"
            case "NASDAQ":
                sym="^GSPC"

        if(sym):
            displayLine("Envíando petición de precios historicos del benchmark {}...".format(self.benchmark), self.logFile)
            res=ApiHandler.fmpApiHandler(sym, fromDate=self.fromDate, toDate=self.toDate, logFile=self.logFile)
            displayLine("Petición exitosa", self.logFile)
            log("Got response {}".format(res))
            return res

    def summarySheet(self):
        displayLine("Envíando petición de perfil del activo {}...".format(self.sym), self.logFile)
        res1=ApiHandler.fmpApiHandler(self.sym, data="profile", logFile=self.logFile)[0]
        displayLine("Petición exitosa", self.logFile)
        log("Got response {}".format(res1))
        self.sym=res1["symbol"]

        displayLine("Envíando petición de indicadores financieros del activo {}...".format(self.sym), self.logFile)
        res2=ApiHandler.fmpApiHandler(self.sym, data="ratios", logFile=self.logFile)[0]
        displayLine("Petición exitosa", self.logFile)
        log("Got response {}".format(res2))

        self.summarySheetBuilder(self.sym, res1, res2)

    def symbolHistData(self):
        displayLine("Envíando petición de precios historicos del activo {}...".format(self.sym), self.logFile)
        res=ApiHandler.fmpApiHandler(self.sym, data="hp", fromDate=self.fromDate, toDate=self.toDate, logFile=self.logFile)
        displayLine("Petición exitosa", self.logFile)
        log("Got response {}".format(res))
        self.n=len(res["historical"])
        self.sym=res["symbol"]
        self.histPricesSheetBuilder(self.sym, res)

    def symbolFinancialStatements(self, statement="cfs"):
        displayLine("Envíando petición de {} del activo {}...".format(statement, self.sym), self.logFile)
        res=ApiHandler.fmpApiHandler(self.sym, data=statement, limit=self.limit, logFile=self.logFile)
        displayLine("Petición exitosa", self.logFile)
        log("Got response {}".format(res))

        match statement:
            case "cfs":
                # ---- Cash Flow Statement (EFF) sheet ----
                self.cfsSheetBuilder(self.sym, res, self.limit)
            case "bss":
                # ---- Balance Sheet Statement (BG) sheet ----
                self.bssSheetBuilder(self.sym, res, self.limit)
            case "is":
                # ---- Income Statement (IS) sheet ----
                self.isSheetBuilder(self.sym, res, self.limit)

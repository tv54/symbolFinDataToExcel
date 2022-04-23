from datetime import datetime

class SearchData():
    def __init__(self, sym, benchmark, toDate=datetime.now().date(), fromDate=datetime.now().date(), limit=5, outputExcelName="output.xlsx", priceToDisplay="close"):
        self.sym=sym
        self.benchmark=benchmark
        self.toDate=toDate
        self.fromDate=fromDate
        self.limit=limit
        self.outputExcelName=outputExcelName
        self.priceToDisplay=priceToDisplay
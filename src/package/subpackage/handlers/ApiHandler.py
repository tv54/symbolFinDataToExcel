from time import sleep
import requests
from src.package.subpackage.othersrc.genFunc import displayLine, handleError, handleInput, log, checkKeyInDict
from src.package.subpackage.othersrc.Constants import Constants

class ApiHandler():
    
    @classmethod
    def getResponse(cls, url, logFile=None):
        log("Sending Request to " + url)
        try:
            res = requests.get(url)
            return (res.status_code, res)
        except:
            handleError("Error on GET request to {}".format(url), logFile=logFile)
            return ApiHandler.getResponse(url, logFile)

    @classmethod
    def fmpApiHandler(cls, sym, data="hp", fromDate="", toDate="", limit=5, logFile=None, apiKey=Constants.FMP_API_KEY, usedAltKey=False):
        # profile: Company profile, ratios: Company financial ratios (TTM), hp: Historical prices, cfs: Cash flow statement, bss: Balance sheet statement, is: Income statement
        sym = sym.upper()
        urlQuery = ""
        match data:
            case "profile":
                res = ApiHandler.getResponse("{}/{}/{}?apikey={}".format(Constants.FMP_API_URL, "profile", sym, apiKey))
            case "ratios":
                res = ApiHandler.getResponse("{}/{}/{}?apikey={}".format(Constants.FMP_API_URL, "ratios-ttm", sym, apiKey))
            case "hp":
                if(not fromDate or not toDate):
                    handleError("Peticion de datos historicos sin fromDate o toDate", logFile=logFile)
                res = ApiHandler.getResponse("{}/{}/{}?from={}&to={}&apikey={}".format(Constants.FMP_API_URL, "historical-price-full", sym, str(fromDate), str(toDate), apiKey), logFile=logFile)
            case "cfs":
                urlQuery = "cash-flow-statement"
            case "bss":
                urlQuery = "balance-sheet-statement"
            case "is":
                urlQuery = "income-statement"

        if(urlQuery):
            res = ApiHandler.getResponse("{}/{}/{}?limit={}&apikey={}".format(Constants.FMP_API_URL, urlQuery, sym, limit, apiKey), logFile=logFile)
        
        if(res):
            if(res[0] == 403 or checkKeyInDict(res[1].json(), "Error Message", False)):
                errMsg=""
                if(checkKeyInDict(res[1].json(), "Error Message", False)):
                    errMsg=res[1].json()["Error Message"]
                if(not usedAltKey):
                    # displayLine("Error en la petición: '" + errMsg + "'. Intentando con API key alternativa...")
                    return ApiHandler.fmpApiHandler(sym, data, fromDate, toDate, limit, logFile, apiKey=Constants.FMP_API_KEY_ALT, usedAltKey=True)
                displayLine("Error en la petición: '" + res[1].json()["Error Message"]+"'")
                if(res[1].json()["Error Message"].lower().__contains__("Invalid API KEY".lower())):
                    handleError("API key y API key alternativa invalidas", logFile=logFile)
                elif(res[1].json()["Error Message"].lower().__contains__("Limit Reach".lower())):
                    handleError("API key y API key alternativa invalidas", logFile=logFile)
                return ApiHandler.fmpApiHandler(sym, data, fromDate, toDate, limit, logFile, apiKey=input("New api key: ").strip(), usedAltKey=True)
            elif(res[0] == 429):
                handleError("API devolvió error por exceso de peticiones ¿Esperar {} segundos para realizar devuelta la petición?".format(Constants.SLEEP_SECONDS_BETWEEN_PETITIONS), logFile=logFile)
                sleep(Constants.SLEEP_SECONDS_BETWEEN_PETITIONS)
                return ApiHandler.fmpApiHandler(sym, data, fromDate, toDate, limit, logFile)
            elif(not res[1].json()):
                handleError("No hubo respuesta de la API ¿Buscar nuevo activo?".format(res[0]), logFile=logFile)
                return ApiHandler.fmpApiHandler(handleInput("New symbol search: ", logFile), data, fromDate, toDate, limit, logFile)
            elif(not res[0] == 200):
                handleError("api returned error code {}".format(res[0]), logFile=logFile)
                return ApiHandler.fmpApiHandler(handleInput("New symbol search: ", logFile), data, fromDate, toDate, limit, logFile)
            res = res[1].json()
        else:
            handleError("Error en la petición, no se recibió respuesta ¿Buscar nuevo activo?".format(res[0]), logFile=logFile)
            return ApiHandler.fmpApiHandler(handleInput("New symbol search: ", logFile), data, fromDate, toDate, limit, logFile)

        sleep(Constants.SLEEP_SECONDS_BETWEEN_PETITIONS)
        
        return res
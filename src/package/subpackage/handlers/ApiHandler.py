from time import sleep
import requests
from src.package.subpackage.othersrc.genFunc import displayLine, handleError, handleInput, log, checkKeyInDict
import src.package.subpackage.othersrc.Constants as Constants

class ApiHandler():
    
    apiKeyNumber=0
    
    @classmethod
    def getResponse(cls, url):
        log("Sending Request to " + url)
        try:
            res = requests.get(url)
            return (res.status_code, res)
        except:
            handleError("Error on GET request to {}".format(url))
            return ApiHandler.getResponse(url)

    @classmethod
    def fmpApiHandler(cls, sym, data="hp", fromDate="", toDate="", limit=5):
        """Call fmp api

        Args:
            sym (str): Lookup symbol
            data (str, optional): Data type to get. Defaults to "hp".
                profile: Company profile
                ratios: Company financial ratios (TTM)
                hp: Historical prices
                cfs: Cash flow statement
                bss: Balance sheet statement
                is: Income statement
            limit (int, optional): Range of years of data (max 5). Defaults to 5.

        Returns:
            json: Response from api
        """
        
        apiKey=Constants.FMP_API_KEYS[ApiHandler.apiKeyNumber]
        sym = sym.upper()
        urlQuery = ""
        match data:
            case "profile":
                res = ApiHandler.getResponse("{}/{}/{}?apikey={}".format(Constants.FMP_API_URL, "profile", sym, apiKey))
            case "ratios":
                res = ApiHandler.getResponse("{}/{}/{}?apikey={}".format(Constants.FMP_API_URL, "ratios-ttm", sym, apiKey))
            case "hp":
                if(not fromDate or not toDate):
                    handleError("Peticion de datos historicos sin fromDate o toDate")
                res = ApiHandler.getResponse("{}/{}/{}?from={}&to={}&apikey={}".format(Constants.FMP_API_URL, "historical-price-full", sym, str(fromDate), str(toDate), apiKey))
            case "cfs":
                urlQuery = "cash-flow-statement"
            case "bss":
                urlQuery = "balance-sheet-statement"
            case "is":
                urlQuery = "income-statement"

        if(urlQuery):
            res = ApiHandler.getResponse("{}/{}/{}?limit={}&apikey={}".format(Constants.FMP_API_URL, urlQuery, sym, limit, apiKey))
        
        if(res):
            if(res[0] == 403 or checkKeyInDict(res[1].json(), "Error Message", False)):
                if(checkKeyInDict(res[1].json(), "Error Message", False)):
                    errorMessage=res[1].json()["Error Message"]
                    displayLine(f"Error en la petición: '{errorMessage}'")
                
                    if(errorMessage.lower().__contains__("Invalid API KEY".lower()) or errorMessage.lower().__contains__("Limit Reach".lower())):
                        if(len(Constants.FMP_API_KEYS)<ApiHandler.apiKeyNumber+1):
                            handleError("API keys invalidas")
                            Constants.FMP_API_KEYS=[input("New api key: ").strip()]
                            ApiHandler.apiKeyNumber=0
                        
                        else:   
                            ApiHandler.apiKeyNumber+=1
                            
                        return ApiHandler.fmpApiHandler(sym, data, fromDate, toDate, limit)
                             
            
            elif(res[0] == 429):
                handleError("API devolvió error por exceso de peticiones ¿Esperar {} segundos para realizar devuelta la petición?".format(Constants.SLEEP_SECONDS_BETWEEN_PETITIONS))
                sleep(Constants.SLEEP_SECONDS_BETWEEN_PETITIONS)
                return ApiHandler.fmpApiHandler(sym, data, fromDate, toDate, limit)
            
            elif(not res[1].json()):
                handleError("No hubo respuesta de la API ¿Buscar nuevo activo?".format(res[0]))
                return ApiHandler.fmpApiHandler(handleInput("New symbol search: "), data, fromDate, toDate, limit)
            
            elif(not res[0] == 200):
                handleError("api returned error code {}".format(res[0]))
                return ApiHandler.fmpApiHandler(handleInput("New symbol search: "), data, fromDate, toDate, limit)
            
            res = res[1].json()
            
        else:
            handleError("Error en la petición, no se recibió respuesta ¿Buscar nuevo activo?".format(res[0]))
            return ApiHandler.fmpApiHandler(handleInput("New symbol search: "), data, fromDate, toDate, limit)
        
        return res
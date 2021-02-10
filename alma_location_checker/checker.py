import logzero
import argparse
import sys
from pyfiglet import Figlet
from requests import get, codes
from yaml import load, FullLoader
from colorama import init, Fore, Back, Style
from blessings import Terminal
from urllib import parse
from logzero import logger as log
from beautifultable import BeautifulTable
from .helpers import checkBarcode, mediumData

def getArgs():
    # CLI Params
    parser = argparse.ArgumentParser()
    parser.add_argument("--loglevel", help="DEBUG, INFO, ERROR, CRITICAL. Default INFO")
    parser.add_argument("--jsonlog", help="Log output as JSON. Default no")
    return vars(parser.parse_args())

def initLog():
    # Logging
    loglevelFromCli = getattr(sys.modules["logging"], args["loglevel"].upper() if args["loglevel"] else "INFO")
    jsonLogFromCli = args["jsonlog"].upper() if args["jsonlog"] else "N"
    logzero.loglevel(loglevelFromCli)

    # Do we want to log as json?
    if jsonLogFromCli == "Y" or jsonLogFromCli == "YES":
        logzero.json()

    # Log to file
    logzero.logfile("alma-location-checker.log", mode="a", disableStderrLogger=True) # "a" means append to logfile

def readConfig():
    configFile = "config.yml"

    try:
        with open(configFile, "r") as configString:
            parsedConfig = load(configString, Loader=FullLoader)
            log.debug("Read config file {0}, got {1}".format(configFile, parsedConfig))
            return parsedConfig

    except FileNotFoundError:
        log.critical("Can't read {0}!".format(configFile))
        print("Konnte die Configdatei nicht laden!")
        log.info("Program end.")
        exit(1)

def makeRequest(barcode):
    encodedBarcode = parse.quote_plus(barcode) # Our barcodes start with + and therefore have to be urlencoded
    targetUrl = "{0}/almaws/v1/items?item_barcode={1}".format(config["apiUrl"], encodedBarcode)

    headers = {
        "User-Agent": "alma-location-checker 0.1",
        "Accept": "application/json",
        "Authorization": "apikey {0}".format(config["apiKey"])
    }

    apiRequest = get(targetUrl, headers=headers)
    dataFromApi = apiRequest.json()

    if apiRequest.status_code != codes.ok:
        log.error("We got error code {0} and content {1}".format(apiRequest.status_code, apiRequest.text))
        print(term.bright_red("Ein Fehler ist bei der Abfrage der Daten aufgetreten!"))
        print("Die ALMA Schnittstelle meldet den Code {0} und die Fehlerbeschreibung {1}".format(dataFromApi["errorList"]["error"][0]["errorCode"], dataFromApi["errorList"]["error"][0]["errorMessage"]))
        raise RuntimeWarning("Invalid API Data")

    log.debug("API response {0}".format(apiRequest.text))

    return dataFromApi

def cli():
    global term
    global args
    global config

    init() # This inits colorama
    term = Terminal()
    args = getArgs()
    initLog()
    log.debug("Command Line Parameters: {0}".format(args))
    log.info("Program start.")
    config = readConfig()
    table = BeautifulTable(
        maxwidth=term.width
    )

    table.columns.header = ["Titel", "Autor", "Signatur", "Standort", "Prozesstyp"]
    table.columns.alignment = BeautifulTable.ALIGN_LEFT

    figlet = Figlet(font="big")
    print(figlet.renderText(format(config["libraryName"])))
    print("Drücke CTRL + D um zu beenden...")

    while True:
        try:
            barcode = input(term.bold("Bitte gib einen Barcode ein: "))
            print(term.clear())
        except EOFError:
            log.info("Program end.")
            return 0

        if checkBarcode(barcode):
            log.debug("User input {0} was valid!".format(barcode))
            try:
                mediumDataFromApi = makeRequest(barcode) # Make the request to the API
            except RuntimeWarning:
                continue

            medium = mediumData(mediumDataFromApi, term)
            log.debug("mediumData {0}".format(medium))

            table.rows.append(medium.values())
            print(table)
        else:
            print(term.bright_red("Ungültiger Barcode!"))
            log.error("User input {0} was invalid!".format(barcode))
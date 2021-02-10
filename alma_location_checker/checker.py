import logzero
import yaml
import argparse
import sys
import requests
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
            parsedConfig = yaml.load(configString, Loader=yaml.FullLoader)
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

    apiRequest = requests.get(targetUrl, headers=headers)
    dataFromApi = apiRequest.json()

    if apiRequest.status_code != requests.codes.ok:
        log.error("We got error code {0} and content {1}".format(apiRequest.status_code, apiRequest.text))
        print(term.bright_red("Ein Fehler ist bei der Abfrage der Daten aufgetreten!"))
        print("Die ALMA Schnittstelle meldet den Code {0} und die Fehlerbeschreibung {1}".format(dataFromApi["errorList"]["error"][0]["errorCode"], dataFromApi["errorList"]["error"][0]["errorMessage"]))
        raise RuntimeWarning("Invalid API Data")

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
    table = BeautifulTable()
    table.columns.header = ["Titel", "Autor", "Signatur", "Standort", "Prozesstyp"]

    print("Willkommen! Bibliothek: {0}".format(config["libraryName"]))
    print("Drücke CTRL + D um zu beenden...")

    while True:
        try:
            barcode = input("Bitte gib einen Barcode ein: ")
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

        else:
            print(term.bright_red("Ungültiger Barcode!"))
            log.error("User input {0} was invalid!".format(barcode))
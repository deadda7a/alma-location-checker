#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logzero
import argparse
import sys
import re
from requests import get, codes
from yaml import load, FullLoader
from colorama import init
from urllib import parse
from logzero import logger as log
from beautifultable import BeautifulTable
from blessed import Terminal

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
        sys.exit(1)

def checkBarcode(barcode):
    newBarcodeRegex = "\+XAW\d+\w?"
    oldBarcodeRegex = "\d{8}"
    if re.match(newBarcodeRegex, barcode) or re.match(oldBarcodeRegex, barcode):
        return True

    return False

def mediumData(mediumDataFromApi, term):
    medium = {
        "title": mediumDataFromApi["bib_data"]["title"],
        "author": mediumDataFromApi["bib_data"]["author"],
        "callNumber": mediumDataFromApi["holding_data"]["call_number"]
    }

    if mediumDataFromApi["item_data"]["location"]["value"] == "MAG4":  # Location of the item, L, LN, MAG1-4
        medium["location"] = term.on_blue(mediumDataFromApi["item_data"]["location"]["value"])  # MAG4 is blue
    elif mediumDataFromApi["item_data"]["location"]["value"] == "MAG3":
        medium["location"] = term.on_yellow(mediumDataFromApi["item_data"]["location"]["value"])  # MAG3 is yellow
    else:
        medium["location"] = mediumDataFromApi["item_data"]["location"]["value"]  # All other locations don't have a color

    if mediumDataFromApi["item_data"]["base_status"]["value"] == "0": # Is the item available?
        if mediumDataFromApi["item_data"]["process_type"]["desc"] == "Loan": # If not, and its of type "loan"
            medium["workOrderType"] = term.bright_red("Loan")
        else:
            # something like "Acquisition technical services"
            medium["workOrderType"] = term.bright_red(mediumDataFromApi["item_data"]["work_order_type"]["desc"])
    else:
        medium["workOrderType"] = ""

    return medium

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

print("           ,ggg, ,ggg,        gg   ,ggggggggggg,")
print("          dP\"\"8IdP\"\"Y8b       dP  dP\"\"\"88\"\"\"\"\"\"Y8,       ,dPYb,     ,dPYb,                   I8   ,dPYb,              ,dPYb,")
print("         dP   88Yb, `88      d8'  Yb,  88      `8b       IP'`Yb     IP'`Yb                   I8   IP'`Yb              IP'`Yb")
print("        dP    88 `\"  88    ,dP'    `\"  88      ,8P  gg   I8  8I     I8  8I  gg            88888888I8  8I              I8  8I")
print("       ,8'    88     88aaad8\"          88aaaad8P\"   \"\"   I8  8'     I8  8'  \"\"               I8   I8  8'              I8  8bgg,")
print("       d88888888     88\"\"\"\"Yb,         88\"\"\"\"Y8ba   gg   I8 dP      I8 dP   gg     ,ggggg,   I8   I8 dPgg,    ,ggg,   I8 dP\" \"8")
print(" __   ,8\"     88     88     \"8b        88      `8b  88   I8dP   88ggI8dP    88    dP\"  \"Y8gggI8   I8dP\" \"8I  i8\" \"8i  I8d8bggP\"")
print("dP\"  ,8P      Y8     88      `8i       88      ,8P  88   I8P    8I  I8P     88   i8'    ,8I ,I8,  I8P    I8  I8, ,8I  I8P' \"Yb,")
print("Yb,_,dP       `8b,   88       Yb,      88_____,d8'_,88,_,d8b,  ,8I ,d8b,_ _,88,_,d8,   ,d8',d88b,,d8     I8, `YbadP' ,d8    `Yb,")
print(" \"Y8P\"         `Y8   88        Y8     88888888P\"  8P\"\"Y88P'\"Y88P\"' 8P'\"Y888P\"\"Y8P\"Y8888P\"  8P\"\"Y888P     `Y8888P\"Y88888P      Y8")

print("Drücke CTRL + D um zu beenden...")

while True:
    try:
        barcode = input(term.bold("Bitte gib einen Barcode ein: "))
        barcode = term.strip(barcode)
        print(term.clear())
    except (EOFError, KeyboardInterrupt):
        log.info("Program end.")
        sys.exit(0)

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

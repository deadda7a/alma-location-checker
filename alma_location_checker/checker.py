import logzero
import yaml
import argparse
import sys
import requests
from logzero import logger as log
from .helpers import checkBarcode

def getArgs():
    # CLI Params
    parser = argparse.ArgumentParser()
    parser.add_argument("--loglevel", help="DEBUG, INFO, ERROR, CRITICAL. Default INFO")
    parser.add_argument("--jsonlog", help="Log output as JSON. Default no")
    return vars(parser.parse_args())

def initLog(args):
    # Logging
    loglevelFromCli = getattr(sys.modules["logging"], args["loglevel"].upper() if args["loglevel"] else "INFO")
    jsonLogFromCli = args["jsonlog"].upper() if args["jsonlog"] else "N"
    logzero.loglevel(loglevelFromCli)

    # Do we want to log as json?
    if (jsonLogFromCli == "Y" or jsonLogFromCli == "YES"):
        logzero.json()

    logzero.logfile("alma-location-checker.log", mode="w", disableStderrLogger=True)
    log.debug("Command Line Parameters: {0}".format(args))

def readConfig():
    # Read config
    configFile = "config.yml"

    try:
        with open(configFile, "r") as configString:
            parsedConfig = yaml.load(configString, Loader=yaml.FullLoader)
            log.debug("Read config file {0}, got {1}".format(configFile, parsedConfig))
            return parsedConfig

    except FileNotFoundError:
        log.critical("Can't read {0}!".format(configFile))
        print("Konnte die Configdatei nicht laden!")
        return 1

def makeRequest(barcode, config):
    payload = {
        "barcode": barcode
    }

    targetUrl = "{0}/almaws/v1/items".format(config["apiUrl"])

def cli():
    args = getArgs()
    initLog(args)
    log.info("Program start.")
    config = readConfig()

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
            bookData = makeRequest(barcode, config)
        else:
            print("Ungültiger Barcode!")
            log.error("User input {0} was invalid!".format(barcode))
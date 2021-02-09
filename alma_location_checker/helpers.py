import re

def checkBarcode(barcode):
    newBarcodeRegex = "\+XAW\d+\w?"
    oldBarcodeRegex = "\d{8}"
    if (re.compile(newBarcodeRegex).search(barcode)) or (re.compile(oldBarcodeRegex).search(barcode)):
        return True

    return False

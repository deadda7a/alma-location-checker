import re

def checkBarcode(barcode):
    newBarcodeRegex = "\+XAW\d+\w?"
    oldBarcodeRegex = "\d{8}"
    if re.match(newBarcodeRegex, barcode) or re.match(oldBarcodeRegex, barcode):
        return True

    return False
import re

def checkBarcode(barcode):
    newBarcodeRegex = "\+XAW\d+\w?"
    oldBarcodeRegex = "\d{8}"
    if re.match(newBarcodeRegex, barcode) or re.match(oldBarcodeRegex, barcode):
        return True

    return False


def mediumData(mediumDataFromApi, term):
    medium = {}
    medium["title"] = mediumDataFromApi["bib_data"]["title"]  # Title
    medium["author"] = mediumDataFromApi["bib_data"]["author"]  # Author
    medium["callNumber"] = mediumDataFromApi["holding_data"]["call_number"]  # call number eg B166500 or LN000.AL etc

    if mediumDataFromApi["item_data"]["location"]["value"] == "MAG4":  # Location of the item, L, LN, MAG1-4
        medium["location"] = "{t.blue}{0}{t.normal}".format(mediumDataFromApi["item_data"]["location"]["value"], t=term)  # MAG4 is blue
    elif mediumDataFromApi["item_data"]["location"]["value"] == "MAG3":
        medium["location"] = "{t.yellow}{0}{t.normal}".format(mediumDataFromApi["item_data"]["location"]["value"], t=term)  # MAG3 is yellow
    elif mediumDataFromApi["item_data"]["location"]["value"] == "LN":
        medium["location"] = "{t.red}{0}{t.normal}".format(mediumDataFromApi["item_data"]["location"]["value"], t=term)  # LN is red
    else:
        medium["location"] = mediumDataFromApi["item_data"]["location"]["value"]  # All other locations don't have a color

    medium["onLocation"] = mediumDataFromApi["item_data"]["base_status"]["value"]  # Is the item available?

    if not medium["onLocation"]:
        medium["processType"] = mediumDataFromApi["item_data"]["process_type"]["desc"]  # If not, why?
    else:
        medium["processType"] = ""

    if not medium["processType"] == "Loan":
        medium["workOrderType"] = mediumDataFromApi["item_data"]["work_order_type"][
            "desc"]  # Either loan or something like "Acquisition technical services"
    else:
        medium["workOrderType"] = ""

    return medium
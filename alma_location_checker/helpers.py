import re

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
        medium["location"] = "{t.blue}{0}{t.normal}".format(mediumDataFromApi["item_data"]["location"]["value"], t=term)  # MAG4 is blue
    elif mediumDataFromApi["item_data"]["location"]["value"] == "MAG3":
        medium["location"] = "{t.yellow}{0}{t.normal}".format(mediumDataFromApi["item_data"]["location"]["value"], t=term)  # MAG3 is yellow
    else:
        medium["location"] = mediumDataFromApi["item_data"]["location"]["value"]  # All other locations don't have a color

    if not mediumDataFromApi["item_data"]["base_status"]["value"]: # Is the item available? 
        if mediumDataFromApi["item_data"]["process_type"]["desc"] == "Loan":
            medium["workOrderType"] = "{t.red}Loan{t.normal}".format(t=term)
        else:
            # something like "Acquisition technical services"
            medium["workOrderType"] = "{t.red}{0}{t.normal}".format(mediumDataFromApi["item_data"]["work_order_type"]["desc"], t=term)
    else:
        medium["workOrderType"] = ""

    return medium
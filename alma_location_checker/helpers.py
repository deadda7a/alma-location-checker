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
using System.Text.RegularExpressions;

namespace alma_location_checker {
    public class Medium {
        internal bool CheckBarcode(string barcode) {
            Regex newBarcodePattern = new Regex(@"\+XAW\d+\w?", RegexOptions.Compiled | RegexOptions.IgnoreCase);
            Regex oldBarcodePattern = new Regex(@"\d{8}", RegexOptions.Compiled); // We don't need to be case insensitive here
            
            if (oldBarcodePattern.IsMatch(barcode) || newBarcodePattern.IsMatch(barcode)) {
                return true;
            }

            return false;
        }
    }
}
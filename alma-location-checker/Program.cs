using System;
using System.Globalization;
using System.IO;
using System.Text.RegularExpressions;
using Figgle;
using Serilog;
using Microsoft.Extensions.Configuration;

namespace alma_location_checker {
    class Program {
        private static bool CheckBarcode(string barcode) {
            Regex newBarcodePattern = new Regex(@"\+XAW\d+", RegexOptions.Compiled | RegexOptions.IgnoreCase);
            Regex oldBarcodePattern = new Regex(@"\d{8}", RegexOptions.Compiled); // We don't need to be case insensitive here
            
            if (oldBarcodePattern.IsMatch(barcode) || newBarcodePattern.IsMatch(barcode)) {
                return true;
            }

            return false;
        }
        
        static int Main(string[] args) {
            string configFile = "config.ini";
            string logFile = "alma-location-checker.log";
            
            // Initialize logging
            Log.Logger = new LoggerConfiguration().MinimumLevel.Debug().WriteTo.File(logFile).CreateLogger();
            Log.Information("Starting Application...");
            
            Console.WriteLine(FiggleFonts.Big.Render("AK Bibliothek"));
            
            // Check if config file exists
            if (!File.Exists(configFile)) {
                Console.WriteLine("Konnte die Configdatei nicht laden!");
                Console.WriteLine("Drücke eine Taste um das Programm zu beenden...");
                Log.Error(("Could not load the config file!"));
                Console.ReadKey();
                return 1;
            }
            
            // Read config
            var config = new ConfigurationBuilder().AddIniFile(configFile).Build();
            Log.Information("Successfully read config file.");
            string apiUrl = config["apiUrl"];
            string apiKey = config["apiKey"];
            Log.Information("{apiUrl}", apiUrl);
            
            Log.CloseAndFlush();
            return 0;
        }
    }
}
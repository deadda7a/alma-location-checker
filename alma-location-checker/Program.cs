using System;
using System.IO;
using Figgle;
using Serilog;
using Microsoft.Extensions.Configuration;

namespace alma_location_checker {
    class Program {
        private static void UserLog(string message, string level) {
            ConsoleColor oldForeground = Console.ForegroundColor;
            
            Console.ForegroundColor = level switch
            {
                "warning" => ConsoleColor.Yellow,
                "error" => ConsoleColor.Red,
                _ => Console.ForegroundColor
            };

            Console.WriteLine(message);
            Console.ForegroundColor = oldForeground;
        }
        
        static int Main(string[] args) {
            string configFile = "config.ini";
            string logFile = "alma-location-checker.log";
            
            // Initialize logging
            Log.Logger = new LoggerConfiguration().MinimumLevel.Debug().WriteTo.File(logFile).CreateLogger();
            Log.Information("Starting Application...");
            
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
            
            Console.WriteLine(FiggleFonts.Big.Render(config["libraryName"]));
            Console.WriteLine("Drücke q und ENTER um das Programm zu beenden!");

            string userInput = "";
            do {
                var medium = new Medium();
                userInput = Console.ReadLine();
                Log.Information("Scanned Barcode {barcode}", userInput);

                if (userInput == null) {
                    UserLog("Bitte gib einen Barcode ein!", "error");
                }

                if (userInput != "q" && medium.CheckBarcode(userInput)) {
                    Console.WriteLine("ok");
                } else {
                    Log.Error("Invalid Barcode!");
                    UserLog("Ungültiger Barcode!", "error");
                }
                
            } while (userInput != "q");
            
            Log.CloseAndFlush();
            return 0;
        }
    }
}
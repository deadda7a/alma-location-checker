using System;
using System.IO;
using Serilog;
using Microsoft.Extensions.Configuration;

namespace alma_location_checker {
    class Program {
        static int Main(string[] args) {
            string configFile = "config.ini";
            string logFile = "alma-location-checker.log";
            
            // Initialize logging
            Log.Logger = new LoggerConfiguration().MinimumLevel.Debug().WriteTo.File(logFile).CreateLogger();
            Log.Information("Starting Application...");
            
            // Try to read config
            if (!File.Exists(configFile)) {
                Console.WriteLine("Konnte die Configdatei nicht laden!");
                Console.WriteLine("Drücke eine Taste um das Programm zu beenden...");
                Log.Error(("Could not load the config file!"));
                Console.ReadKey();
                return 1;
            }
            
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
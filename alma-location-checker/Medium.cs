using System.Threading.Tasks;
using Newtonsoft.Json;
using Refit;

namespace alma_location_checker {
    [Headers("Accept: application/json", "User-Agent: akw-location-checker v0.1", "Authorization: apikey")]
    public interface AlmaApi {
        [Get("/almaws/v1/items?item_barcode={barcode}")]
        Task<Medium> GetData(string barcode);
    }
    
    public class Medium {
        [JsonProperty(PropertyName = "title")]
        public string title {get; set;}
        
        [JsonProperty(PropertyName = "location")]
        public string location {get; set;}
        
        [JsonProperty(PropertyName = "base_status")]
        public string baseStatus {get; set;}
        
        [JsonProperty(PropertyName = "work_order_type")]
        public string workOrderType {get; set;}
        
        [JsonProperty(PropertyName = "call_number")]
        public string callNumber {get; set;}
    }
}
import os
import requests

# Declare globals for API calls
FLIGHT_LIST_ENDPOINT = "https://api.sheety.co/82d56af10214fe30a34cd655bc68f8b5/melodyFlightTrackingSheet/sheet1"
BEARER = os.environ['SHEETY_AUTH']
AUTH_HEADER = {
    "Authorization": BEARER,
    "Content-Type": "application/json",
}


class DataManager:
    """
            Pulls flight data from a Google Sheet
            Creates a list named "sheet1" (how original) containing the following keys:
            City Name
            IATA Code
            Price Low for Alerting
            Line in sheet (starting at 2)
    """

    def __init__(self):
        self.flight_data = { }
        self.get_flight_data()


    def get_flight_data(self) -> dict:
        flight_from_sheet = requests.get(url=FLIGHT_LIST_ENDPOINT, headers=AUTH_HEADER)
        flight_from_sheet.raise_for_status()
        self.flight_data = flight_from_sheet.json()





test = DataManager()
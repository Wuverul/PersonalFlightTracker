from data_manager import DataManager
import os
import datetime
import requests

FROM_LOCATION = "JFK"

MIN_DATE = 30 #days
MAX_DATE = 180 #days
MIN_STAY = 5 #days
MAX_STAY = 14 #days

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"
TEQUILA_HEADER = {
    "apikey": os.environ["TEQUILA_APIKEY"],
}

TINY_ENDPOINT = "https://api.short.io/links"
TINY_HEADER = {
    "authorization": os.environ["SHORT_IO"],
    "Content-Type": "application/json",
}

EXCLUDE_AIRLINES = ""

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.flight_results = [

        ]

    def search_engine(self, data:DataManager):
        # ------------------------
        # Format time for search
        # ------------------------
        cur_date = datetime.date.today()
        travel_from = cur_date + datetime.timedelta(days=MIN_DATE)
        travel_from = travel_from.strftime("%d/%m/%Y")
        travel_to = cur_date + datetime.timedelta(days=MAX_DATE)
        travel_to = travel_to.strftime("%d/%m/%Y")
        print(cur_date)
        print(travel_from)
        print(travel_to)

        # ---------------
        # Run the search
        # ---------------
        for location in data.flight_data['sheet1']:
            # ------------------------------------
            # Set up the parameters for the search
            # ------------------------------------
            search_param = {
                "fly_from": FROM_LOCATION,
                "fly_to": location["iataCode"],
                "select_airlines_exclude": EXCLUDE_AIRLINES,
                "vehicle_type": "aircraft",
                "price_to": location["usdLow"],
                "curr": "USD",
                "flight_type": "round",
                "nights_in_dst_from": MIN_STAY,
                "nights_in_dst_to": MAX_STAY,
                "date_from": travel_from,
                "date_to": travel_to,
                "max_fly_duration": location['maxTravel']
            }

            # ----------
            # Run search
            # ----------
            search_res = requests.get(url=TEQUILA_ENDPOINT,params=search_param,headers=TEQUILA_HEADER)
            search_res.raise_for_status()
            search_res = search_res.json()
            # print(search_res)

            cheap_flight = {
                "dest_city": 0,
                "dest_iata": 0,
                "trip_price": 9999,
                "airline": 0,
                "date_from": 0,
                "date_to": 0,
                "link": 0,
            }
            for result in search_res["data"]:
                # --------------
                # Construct data
                # --------------
                if int(result['price']) < cheap_flight['trip_price']:
                    if result["availability"]["seats"] is not None:
                        cheap_flight = {
                            "dest_city": location['city'],
                            "dest_iata": location["iataCode"],
                            "trip_price": int(result['price']),
                            "airline": result['airlines'],
                            "date_from": result['route'][0]["local_departure"],
                            "date_to": result['route'][-1]["local_arrival"],
                            "link": result['deep_link'],
                        }

                        # -------------------------
                        # Convert date formats
                        # -------------------------
                        cheap_flight["date_from"] = str(cheap_flight["date_from"]).split("T")[0]
                        cheap_flight["date_to"] = str(cheap_flight["date_to"]).split("T")[0]

            # -----------------
            # Tiny URL for link
            # -----------------
            if cheap_flight['link'] != 0:
                tiny_param = {
                    "domain": "l.cl4p-tp.com",
                    "originalURL": cheap_flight["link"],
                }
                print(tiny_param)
                tiny_response = requests.post(url=TINY_ENDPOINT, json=tiny_param, headers=TINY_HEADER)
                print(tiny_response.text)
                tiny_response.raise_for_status()
                tiny_response_list = tiny_response.json()
                cheap_flight["link"] = tiny_response_list['shortURL']
                self.flight_results.append(cheap_flight)

        print(self.flight_results)





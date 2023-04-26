import os
import requests
import datetime
import time

# -----------------------------------------------------
#                  GLOBAL VALUES
#      Replace these with your own information
#     Note that some are environment variables
# Please configure your environment variables properly
# -----------------------------------------------------
#        This document utilizes the following:
#                     Amadeus
# -----------------------------------------------------

# -------------------------
# General query information
# -------------------------
AMADEUS_LOCATIONS_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
AMADEUS_PRICE_ENDPOINT = "https://test.api.amadeus.com/v3/shopping/hotel-offers"
PEOPLE_COUNT = 2
RADIUS = 10 #km

# ----------------------------------
# Authentication request information
# ----------------------------------
AMADEUS_AUTH_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
AMADEUS_CLIENT_ID = os.environ["AMADEUS_APIKEY"]
AMADEUS_CLIENT_SECRET = os.environ["AMADEUS_SECRET"]
AMADEUS_AUTH_HEAD = {"Content-Type": "application/x-www-form-urlencoded"}
AMADEUS_AUTH_BODY = f"grant_type=client_credentials" \
                    f"&client_id={AMADEUS_CLIENT_ID}" \
                    f"&client_secret={AMADEUS_CLIENT_SECRET}"

# -----------------
# END GLOBAL VALUES
# -----------------

def get_token() -> dict:
    """
        Takes in client app ID and client secret
        Acquires OAUTH2 token
        Returns authentication info for use for hotel queries as dictionary
    """

    auth_response = requests.post(url=AMADEUS_AUTH_ENDPOINT, headers=AMADEUS_AUTH_HEAD, data=AMADEUS_AUTH_BODY)
    auth_response.raise_for_status()
    auth_token = auth_response.json()
    return auth_token

def query(date_from: str, date_to: str, city_name: str, iata: str, token: dict):
    """
        Takes in the following:
        "date_from" : str
        "date_to" : str
        "iata" : str
        "city_name" : str
        "token" : dict (acquire with function get_token())

         Returns info on cheapest hotel in region
    """
    access_token = token["access_token"]
    auth_header = {
        "Authorization": f"Bearer {access_token}"
    }

    data_return = {
        "Hotel ID": None,
        "Hotel Name": None,
        "Hotel Price": 9999999,
    }

    request_body_location_search = {
        "cityCode": iata,
        "radius": RADIUS,
    }

    # ------------------------------------
    # Acquire hotel results for a location
    # ------------------------------------
    hotels = requests.get(url=AMADEUS_LOCATIONS_ENDPOINT, headers= auth_header, params=request_body_location_search)
    hotels.raise_for_status()
    hotels_breakdown = hotels.json()

    # ----------------------
    # Parse for lowest price
    # ----------------------
    for hotel in hotels_breakdown["data"][:7]:
        time.sleep(2) # Sleep set here due to errors saying too many requests in duration. Prevents this.
        request_body_price = {
            "hotelIds": hotel["hotelId"],
            "checkInDate": date_from,
            "checkOutDate": date_to,
            "adults": PEOPLE_COUNT,
        }
        hotel_price = requests.get(url=AMADEUS_PRICE_ENDPOINT, headers=auth_header, params=request_body_price)
        hotel_price.raise_for_status()
        hotel_price_usable = hotel_price.json()

        # ----------------------------------------------------------------
        # If the price is the lowest, overwrite the old data with the new.
        # ----------------------------------------------------------------
        for price in hotel_price_usable["data"]:
            if price["available"] == True:
                if float(price["offers"][0]["price"]["total"]) < data_return["Hotel Price"]:
                    data_return = {
                        "Hotel ID": price["hotel"]["hotelId"],
                        "Hotel Name": str(price["hotel"]["name"]).title(),
                        "Hotel Price": round(float(price["offers"][0]["price"]["total"]),2),
                        "People": PEOPLE_COUNT,
                }
    # ---------------------------------------------
    # Only return if there's actually a hotel found
    # ---------------------------------------------
    if data_return["Hotel Name"] is not None:
        return data_return
    else:
        return False
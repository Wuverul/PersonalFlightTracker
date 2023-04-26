import flight_search
import os
from twilio.rest import Client
import hotel_search

# -----------------------------------------------------
#                  GLOBAL VALUES
#      Replace these with your own information
#     Note that some are environment variables
# Please configure your environment variables properly
# -----------------------------------------------------
#        This document utilizes the following:
#                    Twilio SMS
# -----------------------------------------------------

TWILIO_APPID = os.environ["TWILIO_APPID"]
TWILIO_AUTH = os.environ["TWILIO_BEARER"]
TWILIO_NUMBER = "+15555555555"
NOTIFY_PHONE = "+15555555555"


# -----------------
# END GLOBAL VALUES
# -----------------

class NotificationManager:
    def __init__(self, input:flight_search.FlightSearch):
        self.data = input.flight_results
        self.notify()

    # ------------------------------------------------------
    # Send SMS for any listings in the Flight Search results
    #          If no results, do not continue.
    # ------------------------------------------------------
    def notify(self):
        client = Client(TWILIO_APPID, TWILIO_AUTH)
        if len(self.data) > 0:
            hotel_access_token = hotel_search.get_token()
            for flight in self.data:
                hotel_info = hotel_search.query(date_from=flight["date_from"],
                                                date_to=flight["date_to"],
                                                city_name=flight["dest_city"],
                                                iata=flight["dest_iata"],
                                                token=hotel_access_token)
                if hotel_info is not False:
                    message = client.messages \
                        .create(
                            body=
                                f'''
                                PRICE ALERT!
                                A round trip to {flight["dest_city"]} is lower than your threshold!
                                Price: ${flight["trip_price"]} Per person
                                {flight["date_from"]} - {flight["date_to"]}                            
                                Book it:                            
                                {flight["link"]}
                                Need a room, too?
                                {hotel_info["Hotel Name"]} has a room for ${hotel_info["Hotel Price"]} for {hotel_info["People"]} adults.
                                ''',
                            from_= TWILIO_NUMBER,
                            to= NOTIFY_PHONE,
                    )
                else:
                    message = client.messages \
                        .create(
                        body=
                        f'''
                             PRICE ALERT!
                             A round trip to {flight["dest_city"]} is lower than your threshold!
                             Price: ${flight["trip_price"]} (USD) (Per person)
                             {flight["date_from"]} - {flight["date_to"]}                            
                             Book it:                            
                             {flight["link"]}
                             We could not, however, find a hotel.
                        ''',
                        from_=TWILIO_NUMBER,
                        to=NOTIFY_PHONE,
                    )



import flight_search
import os
from twilio.rest import Client

TWILIO_APPID = os.environ["TWILIO_APPID"]
TWILIO_AUTH = os.environ["TWILIO_BEARER"]
TWILIO_NUMBER = #"<API NUMBER HERE>"
NOTIFY_PHONE = #"<YOUR NUMBER HERE>"

class NotificationManager:
    def __init__(self, input:flight_search.FlightSearch):
        self.data = input.flight_results
        self.notify()

    def notify(self):
        client = Client(TWILIO_APPID, TWILIO_AUTH)
        if len(self.data) > 0:
            for flight in self.data:
                message = client.messages \
                    .create(
                        body=
                            f'''
                            PRICE ALERT!
                            To {flight["dest_city"]} via {flight["airline"]}!
                            Price: {flight["trip_price"]}
                            {flight["date_from"]} - {flight["date_to"]}                            
                            Book it:                            
                            {flight["link"]}
                            ''',
                        from_= TWILIO_NUMBER,
                        to= NOTIFY_PHONE,
                )


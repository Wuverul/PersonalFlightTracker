Melody's Flight Search!


This program is intended to search for flights for a list of destinations.
The list of destinations is intended to be on a Google Sheet.
It takes in a City Name, IATA code, and a price threshold for your budget.
If a flight is found within the set search duration under that price, it returns it.
It only returns the lowest price.
It then searches for hotels within a set distance of the airport you're landing at.
If it finds a hotel stay in the same timeframe, it returns the hotel name and price.
This program uses this information to send an automated SMS alert to the user.
This text message will include a link to book the flight, and general hotel information.

SAMPLE OUTPUT

          PRICE ALERT!
          A round trip to Seattle is lower than your threshold!
          Price: $285 Per person
          2023-09-03 - 2023-09-12                            
          Book it:                            
          http://<URL-SHORTENER>.com/Kb68bN
          Need a room, too?
          Radisson Hotel Seattle Airport has a room for $734.40 for 2 adults.


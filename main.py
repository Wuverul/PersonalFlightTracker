#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.


import flight_search
import data_manager
import notification_manager

flight_data = data_manager.DataManager()
search_engine = flight_search.FlightSearch()
search_engine.search_engine(flight_data)
notify = notification_manager.NotificationManager(search_engine)

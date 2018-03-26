# Estimate travel departure time using Google APIs

import googlemaps
from datetime import datetime, timedelta

def get_directions(origin, destination, time):
    return gmaps.directions(origin, destination, mode="driving", departure_time=time)

def get_duration(directions, time):
    duration = directions[0]["legs"][0]["duration_in_traffic"]["value"]
    return round(duration, 2)

api_key = 'AIzaSyCdkxrlZ8vXkr4BSAHJJIZKjkqVHDQvlBE'
gmaps = googlemaps.Client(key=api_key)

origin = str(input('Start Address [Roseville, CA]: ') or "Roseville, CA")
destination = str(input('Destination Address [Marriott Marquis, San Francisco]: ') or "Marriott Marquis, Mission Street, San Francisco")
arrival_date = str(input('Arrival Date [04/01/2018]: ') or '04/01/2018')
month, day, year = map(int, arrival_date.split('/'))
arrival_time = str(input('Arrival Time [12:00]: ') or '12:00')
hour, minute = map(int, arrival_time.split(':'))
desired_arrival = datetime(year, month, day, hour, minute)

# Estimate travel duration by getting directions with a departure time equal to the desired arrival time
directions = get_directions(origin, destination, desired_arrival)
estimated_duration = get_duration(directions, desired_arrival)
estimated_departure = desired_arrival - timedelta(seconds=estimated_duration)

# Determine the estimated departure time that produces the desired arrival time
while True:
    directions = get_directions(origin, destination, estimated_departure)    
    delta = timedelta(seconds=get_duration(directions, estimated_departure))
    estimated_arrival = estimated_departure + delta
    if estimated_arrival <= desired_arrival:
        break
    else:
        estimated_departure = estimated_departure - (estimated_arrival - desired_arrival)

print()
print(f'Estimated Departure: {estimated_departure.hour}:{estimated_departure.minute:02d}')
print(f'Estimated Arrival: {estimated_arrival.hour}:{estimated_arrival.minute:02d}')
print(f'Travel Time: {directions[0]["legs"][0]["duration"]["text"]}')
print(f'Distance: {directions[0]["legs"][0]["distance"]["text"]}')

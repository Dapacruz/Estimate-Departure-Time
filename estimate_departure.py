#!/usr/bin/env python3

# Estimate travel departure time using Google APIs

import googlemaps
from datetime import datetime, timedelta

api_key = 'AIzaSyCdkxrlZ8vXkr4BSAHJJIZKjkqVHDQvlBE'
gmaps = googlemaps.Client(key=api_key)

def get_directions(origin, destination, time):
    return gmaps.directions(origin, destination, mode="driving", departure_time=time)

def get_duration(directions):
    return directions[0]["legs"][0]["duration_in_traffic"]["value"]

def get_estimated_departure(origin, destination, desired_arrival):
    directions = get_directions(origin, destination, desired_arrival)
    return desired_arrival - timedelta(seconds=get_duration(directions))

if __name__ == '__main__':
    origin = str(input('Start Address [Roseville, CA]: ') or "Roseville, CA")
    destination = str(input('Destination Address [Marriott Marquis, San Francisco]: ') or "Marriott Marquis, Mission Street, San Francisco")
    arrival_date = str(input('Arrival Date [04/01/2018]: ') or '04/01/2018')
    month, day, year = map(int, arrival_date.split('/'))
    arrival_time = str(input('Arrival Time [10:00]: ') or '10:00')
    hour, minute = map(int, arrival_time.split(':'))
    desired_arrival = datetime(year, month, day, hour, minute)

    # Estimate travel duration by getting directions with a departure time equal to the desired arrival time
    estimated_departure = get_estimated_departure(origin, destination, desired_arrival)

    # Determine the estimated departure time that produces the desired arrival time
    while True:
        directions = get_directions(origin, destination, estimated_departure)    
        delta = timedelta(seconds=get_duration(directions))
        estimated_arrival = estimated_departure + delta
        if estimated_arrival == desired_arrival:
            break
        elif estimated_arrival > desired_arrival:
            estimated_departure = estimated_departure - (estimated_arrival - desired_arrival)
        else:
            estimated_departure = estimated_departure + (desired_arrival - estimated_arrival)

    print(f'\nStart Address: {directions[0]["legs"][0]["start_address"]}')
    print(f'Destination Address: {directions[0]["legs"][0]["end_address"]}')
    print(f'\nEstimated Departure: {estimated_departure.hour}:{estimated_departure.minute:02d}')
    print(f'Estimated Arrival: {estimated_arrival.hour}:{estimated_arrival.minute:02d}')
    print(f'\nTravel Time: {directions[0]["legs"][0]["duration"]["text"]}')
    print(f'Distance: {directions[0]["legs"][0]["distance"]["text"]}')

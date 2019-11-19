#!/usr/bin/env python3

'''
Estimate travel departure time using Google APIs
'''

import argparse
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

def main():
    parser = argparse.ArgumentParser(description='Estimates travel departure time using Google APIs')
    parser.add_argument('-o', '--origin', type=str, help='Start location')
    parser.add_argument('-d', '--destination', type=str, help='End location')
    parser.add_argument('-ad', '--arrival-date', type=str, help='Arrival date')
    parser.add_argument('-at', '--arrival-time', type=str, help='Desired arrival time')
    parser.add_argument('-mi', '--max_iterations', type=int, default=25, help='Max iterations (default is 25)')
    args = parser.parse_args()

    if not args.origin:
        args.origin = str(input('Start Address [Roseville, CA]: ') or "Roseville, CA")
    
    if not args.destination:
        args.destination = str(input('Destination Address [Marriott Marquis, San Francisco]: ') or "Marriott Marquis, Mission Street, San Francisco")
    
    if not args.arrival_date:
        default_arrival_date = (datetime.now() + timedelta(days=1)).strftime('%m/%d/%Y')
        args.arrival_date = str(input(f'Arrival Date [{default_arrival_date}]: ') or default_arrival_date)
    
    if not args.arrival_time:
        args.arrival_time = str(input('Desired Arrival Time [8:00]: ') or '8:00')

    month, day, year = map(int, args.arrival_date.split('/'))
    hour, minute = map(int, args.arrival_time.split(':'))
    desired_arrival = datetime(year, month, day, hour, minute)

    # Estimate travel duration by getting directions with a departure time equal to the desired arrival time
    estimated_departure = get_estimated_departure(args.origin, args.destination, desired_arrival)

    # Determine the estimated departure time that produces the desired arrival time
    iteration = 0
    while iteration <= args.max_iterations:
        iteration += 1
        directions = get_directions(args.origin, args.destination, estimated_departure)
        delta = timedelta(seconds=get_duration(directions))
        estimated_arrival = estimated_departure + delta
        if estimated_arrival.strftime('%H:%M') == desired_arrival.strftime('%H:%M'):
            break
        elif estimated_arrival.strftime('%H:%M') > desired_arrival.strftime('%H:%M'):
            estimated_departure = estimated_departure - (estimated_arrival - desired_arrival)
        else:
            estimated_departure = estimated_departure + (desired_arrival - estimated_arrival)

    print(f'\nStart Address: {directions[0]["legs"][0]["start_address"]}')
    print(f'Destination Address: {directions[0]["legs"][0]["end_address"]}')
    print(f'\nEstimated Departure: {estimated_departure.hour}:{estimated_departure.minute:02d}')
    print(f'Estimated Arrival: {estimated_arrival.hour}:{estimated_arrival.minute:02d}')
    print(f'\nTravel Time: {directions[0]["legs"][0]["duration_in_traffic"]["text"]}')
    print(f'Distance: {directions[0]["legs"][0]["distance"]["text"]}\n')

    # input('Enter to quit')

if __name__ == '__main__':
    main()

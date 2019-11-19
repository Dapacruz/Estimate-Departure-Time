#!/usr/bin/env python3

'''
Estimate travel departure time using Google APIs
'''

import argparse
from datetime import datetime, timedelta
import googlemaps
import json
import os
import sys

def get_directions(gmaps, origin, destination, time):
    return gmaps.directions(origin, destination, mode="driving", departure_time=time)

def get_duration(directions):
    return directions[0]["legs"][0]["duration_in_traffic"]["value"]

def get_estimated_departure(gmaps, origin, destination, desired_arrival):
    directions = get_directions(gmaps, origin, destination, desired_arrival)
    return desired_arrival - timedelta(seconds=get_duration(directions))

def import_saved_settings(settings_path):
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            settings = json.load(f)

        # Check for the existence of settings and add if missing
        changed = False
        if not 'api_key' in settings:
            settings['api_key'] = input('Google Maps API Key: ')
            changed = True
        if changed:
            with open(settings_path, 'w') as f:
                json.dump(settings, f, sort_keys=True, indent=2)
    else:
        settings = {
            'api_key': input('Google Maps API Key: '),
        }
        with open(settings_path, 'w') as f:
            json.dump(settings, f, sort_keys=True, indent=2)
        os.chmod(settings_path, 0o600)

    return settings

def update_saved_settings(settings, settings_path):
    print('\nUpdating saved settings ...\n')
    settings['api_key'] = input(f'New Google Maps API Key [{settings["api_key"]}]: ') or settings['api_key']
    with open(settings_path, 'w') as f:
        json.dump(settings, f, sort_keys=True, indent=2)
    print('\nSettings updated!')

def main():
    parser = argparse.ArgumentParser(description='Estimates travel departure time using Google APIs')
    parser.add_argument('-o', '--origin', type=str, help='Start location')
    parser.add_argument('-d', '--destination', type=str, help='End location')
    parser.add_argument('-ad', '--arrival-date', type=str, help='Arrival date')
    parser.add_argument('-at', '--arrival-time', type=str, help='Desired arrival time')
    parser.add_argument('-k', '--api-key', type=str, help='Google Maps API key')
    parser.add_argument('-mi', '--max_iterations', type=int, default=25, help='Max iterations (default is 25)')
    parser.add_argument('-u', '--update', action='store_true', help='Update saved settings')
    args = parser.parse_args()

    if os.environ.get('USERPROFILE'):
        settings_path = os.path.join(os.environ.get('USERPROFILE'), '.travest-settings.json')
    else:
        settings_path = os.path.join(os.environ.get('HOME'), '.travest-settings.json')
    settings = import_saved_settings(settings_path)

    if args.update:
        update_saved_settings(settings, settings_path)
        sys.exit(0)

    if not args.origin:
        args.origin = str(input('Start Address [Roseville, CA]: ') or "Roseville, CA")
    
    if not args.destination:
        args.destination = str(input('Destination Address [Marriott Marquis, San Francisco]: ') or "Marriott Marquis, Mission Street, San Francisco")
    
    if not args.arrival_date:
        default_arrival_date = (datetime.now() + timedelta(days=1)).strftime('%m/%d/%Y')
        args.arrival_date = str(input(f'Arrival Date [{default_arrival_date}]: ') or default_arrival_date)
    
    if not args.arrival_time:
        args.arrival_time = str(input('Desired Arrival Time [8:00]: ') or '8:00')

    if not args.api_key:
        args.api_key = settings['api_key']
    
    gmaps = googlemaps.Client(key=args.api_key)

    month, day, year = map(int, args.arrival_date.split('/'))
    hour, minute = map(int, args.arrival_time.split(':'))
    desired_arrival = datetime(year, month, day, hour, minute)

    # Estimate travel duration by getting directions with a departure time equal to the desired arrival time
    estimated_departure = get_estimated_departure(gmaps, args.origin, args.destination, desired_arrival)

    # Determine the estimated departure time that produces the desired arrival time
    iteration = 0
    while iteration <= args.max_iterations:
        iteration += 1
        directions = get_directions(gmaps, args.origin, args.destination, estimated_departure)
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

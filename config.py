from train_api.stations import Stations
from train_api.route import Route
import os
import json

def get_route_from_index(idx):
    routes = {0 : Route.RED, 1: Route.BLUE, 2: Route.BROWN, 3: Route.GREEN, 4: Route.ORANGE, 5: Route.PURPLE, 6: Route.PINK, 7: Route.YELLOW}
    return routes[idx]

def prompt_config():
    stops=[]

    while True:
        route_input = input(\
"""
Select Config #:
0: RED
1: BLUE
2: BROWN
3: GREEN
4: ORANGE
5: PURPLE
6: PINK
7: YELLOW
"""
        )
        route_config = get_route_from_index(int(route_input))

        station = Stations()
        stations = station.lookup(route_config)
        print("Select Station(s): ex. 12,5,2")
        for idx, station in enumerate(stations):
            print("%d: %s" % (idx, station['stop_name']))
        stop_input = input().split(',')

        print("Selected Stops: ")
        for stop_idx in stop_input:
            stop = stations[int(stop_idx)]
            print(stop['stop_name'])
            stops.append(stop)

        select_more = input("Do you want to select another train? y/N\n")
        if select_more.lower() == 'y':
            continue
        else:
            break

    print("Selected stops:\n")
    for stop in stops:
        print(stop['stop_name'])
    with open('config.txt', "w") as f:
        json.dump(stops, f)
    return stops

def read_config():
    f = open('config.txt', 'r')
    stops = f.read()
    f.close()
    return json.loads(stops)

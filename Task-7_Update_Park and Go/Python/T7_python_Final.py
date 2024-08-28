import folium
import requests
import json
import pandas as pd
from folium.features import CustomIcon
import time
from IPython.display import display, IFrame
from geopy.distance import geodesic

# Define locations
location1 = [53.381516, 10.021215]   # Car1 Start
location2 = [53.553713, 10.024416]   # Car1 Mid
location5 = [53.639158, 10.053988]   # Car1 Final

location3 = [53.600651, 9.827795]    # Car2 Start
location4 = [53.553713, 10.024416]   # Car2 Mid
location6 = [53.859119, 10.694445]   # Car2 Final
circle_radius = 5000

# OpenRouteService API key
ors_api_key = '5b3ce3597851110001cf62482aa5927220e1482797ca6ea18c66dfa7'

# Create a map
m = folium.Map(location=location2, zoom_start=12)

# Markers
car_icon = CustomIcon('car_icon.png', icon_size=(90, 90))
car_icon2 = CustomIcon('Car_icon2.png', icon_size=(40, 40))
package_icon = CustomIcon('package_icon.png', icon_size=(20, 20))

car_marker = folium.Marker(location1, popup='Seeveta_start', icon=car_icon)
car_marker.add_to(m)
folium.Marker(location2, popup='Hamburg_end').add_to(m)
car_marker2 = folium.Marker(location3, popup='Schenefeld_start', icon=car_icon2)
car_marker2.add_to(m)
folium.Marker(location4, popup='Luebeck_end').add_to(m)
folium.Marker(location5, popup='Berliner Tor').add_to(m)
folium.Marker(location1, popup='Pack', icon=package_icon).add_to(m)

C1_circle = folium.Circle(location1, radius=circle_radius, color='green', fill=True, fill_color='green')
C1_circle.add_to(m)

# Function to get route coordinates using OpenRouteService API
def get_route_coordinates(start, end, api_key):
    url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start[1]},{start[0]}&end={end[1]},{end[0]}"
    response = requests.get(url)
    data = response.json()
    coordinates = [[coord[1], coord[0]] for coord in data['features'][0]['geometry']['coordinates']]
    return coordinates

# Get route coordinates for Car1 and Car2
route1 = get_route_coordinates(location1, location2, ors_api_key)
route2 = get_route_coordinates(location3, location4, ors_api_key)

# Add polylines to the map
folium.PolyLine(route1, color="blue", weight=2.5, opacity=1).add_to(m)
folium.PolyLine(route2, color="red", weight=2.5, opacity=1).add_to(m)

# Function to move car along a route
def move_car(route, car_marker, C1_circle=None):
    for coord in route:
        car_marker.location = coord
        if C1_circle:
            C1_circle.location = coord
        time.sleep(0.02)

# Function to move car to the nearest parking location
def move_to_parking(route, car_marker, color):
    folium.PolyLine(route, color=color, weight=2.5, opacity=1).add_to(m)
    for coord in route:
        car_marker.location = coord
        time.sleep(0.02)

# Function to move car to the final location
def move_to_final(route, car_marker, color):
    folium.PolyLine(route, color=color, weight=2.5, opacity=1).add_to(m)
    for coord in route:
        car_marker.location = coord
        time.sleep(0.02)

# Function to get parking locations using Nominatim API
def get_parking_locations(lat, lon, radius=5000):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q=parking&bounded=1&viewbox={lon-radius/111000},{lat+radius/111000},{lon+radius/111000},{lat-radius/111000}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        parking_locations = [[float(place['lat']), float(place['lon'])] for place in data]
        return parking_locations
    else:
        print(f"Error: Unable to fetch parking locations (status code: {response.status_code})")
        return []

# Function to mark all parking locations inside a given circle
def mark_parking_locations(circle, map_obj):
    parking_locations = get_parking_locations(circle.location[0], circle.location[1], circle_radius)
    
    for location in parking_locations:
        folium.Marker(location, popup='Parking', icon=folium.Icon(color='green')).add_to(m)
    return parking_locations

# Function to find the nearest parking location
def find_nearest_parking(parking_locations, car_location):
    min_distance = float('inf')
    nearest_parking = None
    for location in parking_locations:
        distance = geodesic(car_location, location).meters
        if distance < min_distance:
            min_distance = distance
            nearest_parking = location
            folium.Marker(nearest_parking, popup='Nearest Parking', icon=folium.Icon(color='red')).add_to(m)
    return nearest_parking 

# Function to check if a marker is inside a circle
def is_inside_circle(marker, circle_location, radius):
    distance = geodesic((marker.location[0], marker.location[1]), circle_location).meters
    return distance <= radius

# Loop to move both cars alternately and check for parking locations
nearest_parking = None
for i in range(max(len(route1), len(route2))):
    if i < len(route1):
        move_car([route1[i]], car_marker, C1_circle)
    if i < len(route2):
        move_car([route2[i]], car_marker2)
    
    # Check if both car_marker and car_marker2 are inside the C1_circle
    if is_inside_circle(car_marker2, C1_circle.location, circle_radius):
        # Search for all parking locations inside the circle
        parking_locations = mark_parking_locations(C1_circle, m)
        nearest_parking = find_nearest_parking(parking_locations, car_marker.location)
        time.sleep(4)
        
        if nearest_parking:
            # Get routes to the nearest parking location
            routeP1 = get_route_coordinates(car_marker.location, nearest_parking, ors_api_key)
            routeP2 = get_route_coordinates(car_marker2.location, nearest_parking, ors_api_key)
            
            # Move both cars to the nearest parking location
            move_to_parking(routeP1, car_marker, "black")
            move_to_parking(routeP2, car_marker2, "black")
        else:
            print("No parking locations found.")
        break

# Save the final map as an HTML file
m.save('mapA.html')

if nearest_parking:
    # Get routes to the final locations
    routeF1 = get_route_coordinates(nearest_parking, location5, ors_api_key)
    routeF2 = get_route_coordinates(nearest_parking, location6, ors_api_key)      

    # Move both cars to the final locations
    move_to_final(routeF1, car_marker, "green")
    move_to_final(routeF2, car_marker2, "purple")

    # Save the final map as an HTML file
    m.save('mapB.html')
else:
    print("No nearest parking location found, skipping final move.")
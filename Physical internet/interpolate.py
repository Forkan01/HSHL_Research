import folium
import time
from shapely.geometry import LineString


start_pos1 = (7.4653, 51.5136)  # Dortmund (longitude, latitude)
end_pos1 = (6.7763, 51.2277)    # Dusseldorf (longitude, latitude)
start_pos2 = (7.0131, 51.4556)  # Essen (longitude, latitude)
end_pos2 = (9.4797, 51.3127)    # Kassel (longitude, latitude)


line1 = LineString([start_pos1, end_pos1])
line2 = LineString([start_pos2, end_pos2])


intersection = line1.intersection(line2)

def interpolate(start, end, t):
    return (start[0] + t * (end[0] - start[0]), start[1] + t * (end[1] - start[1]))

map_center = ((start_pos1[1] + end_pos1[1] + start_pos2[1] + end_pos2[1]) / 4,
              (start_pos1[0] + end_pos1[0] + start_pos2[0] + end_pos2[0]) / 4)
mymap = folium.Map(location=map_center, zoom_start=7)

folium.PolyLine(locations=[start_pos1[::-1], end_pos1[::-1]], color='blue').add_to(mymap)
folium.PolyLine(locations=[start_pos2[::-1], end_pos2[::-1]], color='red').add_to(mymap)


if not intersection.is_empty:
    folium.CircleMarker(location=[intersection.y, intersection.x], radius=10, color='green', fill=True).add_to(mymap)


for t in range(0, 101, 5):
    t /= 100
    pos1 = interpolate(start_pos1, end_pos1, t)
    pos2 = interpolate(start_pos2, end_pos2, t)

    folium.CircleMarker(location=pos1[::-1], radius=5, color='blue').add_to(mymap)
    folium.CircleMarker(location=pos2[::-1], radius=5, color='red').add_to(mymap)


    time.sleep(0.1) 


mymap.save("path_animation_final.html")

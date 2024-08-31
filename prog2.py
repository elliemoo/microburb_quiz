import folium
from folium import plugins
from geopy.distance import geodesic

# Coordinates for the locations (example coordinates; replace with actual ones if available)
coordinates = [
    (-37.82457, 144.96340),
    (-37.81399, 144.94125),
    (-37.80076, 144.96245),
    ## we can add more cordinates here
]

# Create a folium map centered around the first coordinate
map_center = coordinates[0]  # Adjust the center as needed
map_folium = folium.Map(location=map_center, zoom_start=13)

# Add markers for each location
for coord in coordinates:
    folium.Marker(location=coord).add_to(map_folium)

# Draw lines between all pairs of locations
for i in range(len(coordinates)):
    for j in range(i + 1, len(coordinates)):
        # Calculate the distance
        distance = geodesic(coordinates[i], coordinates[j]).kilometers

        # Draw the line
        folium.PolyLine(
            locations=[coordinates[i], coordinates[j]],
            color="blue",
            weight=2.5,
            opacity=1,
        ).add_to(map_folium)

        # Optionally, add the distance text
        mid_point = [
            (coordinates[i][0] + coordinates[j][0]) / 2,
            (coordinates[i][1] + coordinates[j][1]) / 2,
        ]
        folium.Marker(
            location=mid_point,
            icon=folium.DivIcon(
                html=f"<div style='font-size: 12pt; color: black;'>{distance:.1f} km</div>"
            ),
        ).add_to(map_folium)

# Save the map to an HTML file
map_folium.save("readable_map.html")

# Display the map in a Jupyter notebook (if running in one)
map_folium

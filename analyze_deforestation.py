import csv

# Country and Year we are looking for
country_name = 'Congo (DRC)'
start_year = 2010

# Initialize variables
total_deforestation_rate = 0
years_count = 0
start_forest_area = 0
end_forest_area = 0
last_year = -1

# Read the CSV
with open('global_deforestation_2000_2025.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Country'] == country_name:
            year = int(row['Year'])
            if year >= start_year:
                total_deforestation_rate += float(row['Annual_Deforestation_Rate'])
                years_count += 1
                
                # Get the earliest forest area (2010)
                if year == start_year:
                    start_forest_area = float(row['Forest_Area_km2'])
                
                # Keep track of the latest forest area
                if year > last_year:
                    last_year = year
                    end_forest_area = float(row['Forest_Area_km2'])

# Calculate average
if years_count > 0:
    avg_rate = total_deforestation_rate / years_count
    total_loss = start_forest_area - end_forest_area
else:
    avg_rate = 0
    total_loss = 0

print(f"Average Annual Deforestation Rate for Congo (DRC) since 2010: {avg_rate:.2f}%")
print(f"Total Forest Area Loss since 2010: {total_loss:,.2f} km2")

# Generate Leaflet Map
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Deforestation Map - Congo (DRC)</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <style>
        #map {{ height: 600px; width: 100%; }}
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
    </style>
</head>
<body>
    <h1>Deforestation in Congo (DRC) since 2010</h1>
    <p><strong>Average Annual Deforestation Rate:</strong> {avg_rate:.2f}%</p>
    <p><strong>Total Forest Area Loss:</strong> {total_loss:,.2f} km2</p>
    <div id="map"></div>
    <script>
        var map = L.map('map').setView([-4.0383, 21.7587], 5);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }}).addTo(map);

        var marker = L.marker([-4.0383, 21.7587]).addTo(map);
        marker.bindPopup("<b>Congo (DRC)</b><br>Avg Deforestation Rate (since 2010): {avg_rate:.2f}%<br>Total Loss: {total_loss:,.2f} km2").openPopup();
    </script>
</body>
</html>
"""

with open('drc_deforestation_map.html', 'w') as f:
    f.write(html_content)

print("Map generated: drc_deforestation_map.html")

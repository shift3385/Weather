import csv
import json

with open('new_weather_historical.json') as f:
    data = json.load(f)

csv_file = "weather_historical_data.csv"

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    header = data[0].keys()
    writer.writerow(header)
    
    for entry in data:
        entry['preciptype'] = ', '.join(entry['preciptype']) if entry['preciptype'] else ''
        writer.writerow(entry.values())

print(f"Data successfully written to {csv_file}")
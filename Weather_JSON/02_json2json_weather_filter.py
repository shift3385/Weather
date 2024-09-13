import json

with open('general_dataset_historical.json') as f:
    json_data = json.load(f)

new_weather_array = []
print(json_data['days'])

for day in json_data['days']:
    new_weather_json = {}
    new_weather_json['datetime'] = day['datetime']
    new_weather_json['temp'] = day['temp']
    new_weather_json['humidity'] = day['humidity']
    new_weather_json['precip'] = day['precip']
    new_weather_json['snow'] = day['snow']
    new_weather_json['pressure'] = day['pressure']
    new_weather_json['preciptype'] = day['preciptype']
    new_weather_json['conditions'] = day['conditions']
    new_weather_json['description'] = day['description']
    
    new_weather_array.append(new_weather_json)

with open('new_weather_historical.json', 'w') as outfile:
    json.dump(new_weather_array, outfile, indent=4)

print("Datos guardados")
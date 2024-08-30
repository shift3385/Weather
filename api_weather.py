import requests
import json

url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Boulder%2C%20CO/2023-01-01/2023-12-31?unitGroup=metric&include=days&key=KWL95D8T3H3LXRZMZYGMHWWHP&contentType=json'
result = requests.get(url)

with open('data.json','w') as file:
    json.dump(result.json(), file)
import requests
import json

API_URL = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc?"


def create_pvgis_api_url(lat: float, lon: float, peak_power: float):
    return f"{API_URL}lat={lat}&lon={lon}&peakpower={peak_power}&startyear=2020&endyear=2020&outputformat=json"


def get_radiation_data(lat, lon, area):
    url = create_pvgis_api_url(lat=lat, lon=lon, peak_power=1.0),
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None

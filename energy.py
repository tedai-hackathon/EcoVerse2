import requests
import json

API_URL = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc?"


def create_pvgis_api_url(lat: float, lon: float):
    return f"{API_URL}lat={lat}&lon={lon}&startyear=2020&endyear=2020&outputformat=json"


def get_radiation_data(coordinates, area):
    url = create_pvgis_api_url(coordinates[0], coordinates[1])
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        hourly_data = data["outputs"]["hourly"]

        return [{"time": data["time"], "Energy (kWh)": data["G(i)"] * area * 0.18 * (1 - 0.14) / 1000} for data in hourly_data]
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None


if __name__ == "__main__":
    data = get_radiation_data((40.767, -7.910), 1)
    print(data)

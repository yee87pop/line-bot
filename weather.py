import requests
import json
def weather_search(location):
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001"
    params = {
        "Authorization": "CWB-0CD62FEF-91F4-407F-B266-2A85D8A8810D",
        "locationName": "{0}".format(location),
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = json.loads(response.text)

        location = data["records"]["location"][0]["locationName"]
        weather = data["records"]["location"][0]["weatherElement"][-1]["elementValue"]
        temprature_low=data["records"]["location"][0]["weatherElement"][-5]["elementValue"]
        temprature_high=data["records"]["location"][0]["weatherElement"][-7]["elementValue"]

    return "{0}今天天氣為{1}，最高溫為{2}，最低溫為{3}".format(location,weather,temprature_high,temprature_low)
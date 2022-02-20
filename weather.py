import requests
import json
def weather_search(location):
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": "CWB-0CD62FEF-91F4-407F-B266-2A85D8A8810D",
        "locationName": "{0}".format(location),
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = json.loads(response.text)

        location = data["records"]["location"][0]["locationName"]
        weather = data["records"]["location"][0]["weatherElement"][0]["time"][2]['parameter']['parameterName']
        rain_percent = data["records"]["location"][0]["weatherElement"][1]["time"][2]['parameter']['parameterName']
        temprature_low=data["records"]["location"][0]["weatherElement"][2]["time"][2]['parameter']['parameterName']
        temprature_high=data["records"]["location"][0]["weatherElement"][4]["time"][2]['parameter']['parameterName']

    return "{0}今天天氣為{1}，降雨機率為{2}，最高溫為{3}，最低溫為{4}".format(location,weather,rain_percent,temprature_high,temprature_low)
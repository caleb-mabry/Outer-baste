import requests
import random
import time

URL = "https://disturbing-azure.cmd.outerbase.io/outerbaste"

def send_temperature(temperature, ambientTemperature, battery):
    payload = {
        "temperature": temperature,
        "ambientTemperature": ambientTemperature,
        "battery": battery
    }
    try:
        response = requests.put(URL, json=payload)
        if response.status_code == 200:
            print(f"Sent Payload: {payload}")
            print(f"Temperature sent: {temperature}")
        else:
            print(f"Failure: {response}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
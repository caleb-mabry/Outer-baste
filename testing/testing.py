import requests
import random
import time

URL = "https://disturbing-azure.cmd.outerbase.io/outerbase-test"

def send_temperature():
    temperature = random.uniform(1, 100)  # Generate a random temperature value between 1 and 100
    payload = {"temperature": temperature}
    try:
        response = requests.put(URL, json=payload)
        if response.status_code == 200:
            print(f"Temperature sent: {temperature}")
        else:
            print(f"Failure: {response}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    while True:
        send_temperature()
        time.sleep(1)  # Wait for 1 second before sending the next request

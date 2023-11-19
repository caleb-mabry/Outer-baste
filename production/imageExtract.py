import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
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

# # Function to capture the screenshot of a specific window
# def screenshot_window():
    
#     image.save('screenshot.png')
#     return image

# # Provide the title (or part of the title) of the window to capture
# window_title = "Your Application Window Title"  # Replace this with your application's title
# screenshot = screenshot_window()

while True:
    screenshot = ImageGrab.grab()
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)  # Convert to OpenCV format
    cropped_image = screenshot_cv[700:900, 1250:2000]  # Example cropping area (adjust as needed)
    
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    _, threshold_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY_INV)

    # Use pytesseract to extract text (digits) from the image
    extracted_text = pytesseract.image_to_string(threshold_image, config='digits --psm 6 -c tessedit_char_whitelist=0123456789')
    print(extracted_text)
    
    tip = int(extracted_text[0:3].strip())
    target = int(extracted_text[3:6].strip())
    # ambient = int(extracted_text[6:].strip())
    send_temperature(tip, 0, 0)
    time.sleep(1)


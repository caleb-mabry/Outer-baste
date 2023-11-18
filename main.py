# import cv2
# import pytesseract
# from PIL import Image
# import cv2
# import pytesseract
# from pytesseract import Output
# import numpy as np

# def main():
#     # Access the webcam (change the index if multiple webcams are connected)
#     cap = cv2.VideoCapture(0)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         # frame = frame[200:400, 350:750 ]
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         thresh = cv2.threshold(gray, 125, 255,cv2.THRESH_BINARY)[1]
#         # resize = cv2.resize(thresh, (1920, 1080), interpolation=cv2.INTER_CUBIC)


#         # thresh = cv2.adaptiveThreshold(gray, 225, cv2.ADAPTIVE_THRESH_MEAN_C,
#         #                             cv2.THRESH_BINARY, 21, 9)
#         custom_config = f'--psm 13 --oem 3'
#         text = pytesseract.image_to_string(thresh, config=custom_config)

#         # Display the frame
#         cv2.imshow('Webcam', thresh)
#         # text = pytesseract.image_to_string(double, config="digits")
#         print("Numbers detected:", text)

#         # HSV_img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#         # h,s,v = cv2.split(HSV_img)
#         # v = cv2.GaussianBlur(v, (1,1), 0)
#         # thresh = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#         # # cv2.imwrite('{}.png'.format(filename),thresh)
#         # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(1, 2))
#         # thresh = cv2.dilate(thresh, kernel)
#         # txt = pytesseract.image_to_string(frame, config="--psm 13 --oem 3 digits")

#         # Perform OCR and extract numbers
#         # numbers = extract_numbers_from_frame(frame)

#         # Exit on pressing 'q'
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

import cv2
from PIL import Image
import numpy as np

"""
 7 segments indexes are:
 0: top,
 1: top left,
 2: top right,
 3: middle,
 4: bottom left
 5: bottom right
 6: bottom
"""
segments = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 1, 0): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9
}


def cv2_2_pil(cv2img, transform=cv2.COLOR_BGR2RGB):
    return Image.fromarray(cv2.cvtColor(cv2img, transform))


def get_digit(img):
    segment_pos = [(12, 3), (3, 14), (26, 14), (11, 26), (2, 38), (24, 39), (8, 50)]
    active = map(lambda x: int(np.count_nonzero(get_dig_sub(img, x[0], x[1], 4, 4)) > 8), segment_pos)

    return segments.get(tuple(active), 'x')


def get_dig_sub(img, x, y, width=36, height=60):
    return img[y:y + height, x:x + width]


def thermo_image_to_temp(img):
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, imthresh = cv2.threshold(imgray, 50, 255, cv2.THRESH_BINARY_INV)
    imthresh = cv2.dilate(imthresh, np.ones((2, 2), np.uint8), iterations=1)
    # cv2_2_pil(imthresh, cv2.COLOR_GRAY2RGB).show()
    dig1 = get_dig_sub(imthresh, 290, 264)
    dig2 = get_dig_sub(imthresh, 329, 264)
    dig3 = get_dig_sub(imthresh, 367, 264)
    return "{}{}.{}°C".format(*map(get_digit, [dig1, dig2, dig3]))


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        image = cv2.imread(frame)
        print(thermo_image_to_temp(image))
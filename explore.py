import numpy as np
import sys
import cv2


def detectColor(img, colorMin, colorMax):
    frame_threshed = cv2.inRange(
        img, colorMin, colorMax)     # Thresholding image
    _, thresh = cv2.threshold(frame_threshed, 127, 255, 0)
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


im = cv2.imread('rubik.png')
im = cv2.bilateralFilter(im, 9, 75, 75)
im = cv2.fastNlMeansDenoisingColored(im, None, 10, 10, 7, 21)
hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)   # HSV image

colors = {
    # Blue
    'blue': (np.array([100, 150, 0], np.uint8), np.array([140, 255, 255], np.uint8), [255, 0, 0]),
    # Yellow
    'yellow': (np.array([20, 100, 100], np.uint8), np.array([30, 255, 255], np.uint8), [0, 255, 0]),
    # Red
    'red': (np.array([0, 100, 100], np.uint8), np.array([10, 255, 255], np.uint8), [0, 0, 255]),
    # White
    'white': (np.array([0, 0, 168], np.uint8), np.array([172, 111, 255], np.uint8), [0, 0, 0]),
    # Green
    'green': (np.array([40, 100, 100], np.uint8), np.array([70, 255, 255], np.uint8), [0, 255, 255]),

}
# HSV color code lower and upper bounds

biggest_y = 0
lowest_y = 99999999
biggest_x = 0
for color_name, color_config in colors.items():
    contours = detectColor(hsv_img, color_config[0], color_config[1])
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w < 100 or h < 100:
            continue

        if y < lowest_y:
            lowest_y = y

        if y >= biggest_y:
            biggest_y = y + h
            print(f"w eh {w}")
            biggest_x = int(x + w / 2)
        print(f"biggest x eh {biggest_x}")
        cv2.rectangle(im, (x, y), (x+w, y+h), color_config[2], 2)

cv2.arrowedLine(im, (biggest_x, lowest_y), (biggest_x,
                biggest_y), (150, 150, 150), 10)

cv2.imshow("Show", im)
cv2.imwrite("extracted.jpg", im)
cv2.waitKey()
cv2.destroyAllWindows()

import numpy as np
import sys
import cv2


def detectColorContours(img, colorMin, colorMax):
    frame_threshed = cv2.inRange(
        img, colorMin, colorMax)     # Thresholding image
    cv2.imwrite(f"frame_threshold{colorMin}.jpg", frame_threshed)
    contours, _ = cv2.findContours(
        frame_threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def filterContours(contours, min_size=100, square_threshold=0.2):
    r = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if abs(w/h - 1) > square_threshold:
            continue

        if w < min_size or h < min_size:
            continue

        r.append((x, y, w, w))
    return r


def drawRects(im, rects, color):
    for rect in rects:
        cv2.rectangle(im, (rect[0], rect[1]),
                      (rect[0]+rect[2], rect[1]+rect[3]), color, 20)


def getAndProcessImage(im):
    new_im = cv2.bilateralFilter(im, 9, 75, 75)
    cv2.imwrite("bilateral_filter.jpg", new_im)
    new_im = cv2.fastNlMeansDenoisingColored(new_im, None, 10, 10, 7, 21)
    cv2.imwrite("fastNlMeansDenoisingColored.jpg", new_im)
    hsv_img = cv2.cvtColor(new_im, cv2.COLOR_BGR2HSV)   # HSV image
    return hsv_img


colors = {
    # Blue
    'blue': (np.array([80, 100, 40], np.uint8), np.array([140, 255, 255], np.uint8), [255, 0, 0]),
    # Yellow
    'yellow': (np.array([20, 100, 100], np.uint8), np.array([30, 255, 255], np.uint8), [0, 255, 255]),
    # Red
    'red': (np.array([0, 100, 100], np.uint8), np.array([10, 255, 255], np.uint8), [0, 0, 255]),
    # White
    'white': (np.array([0, 0, 168], np.uint8), np.array([172, 111, 255], np.uint8), [50, 50, 50]),
    # Green
    'green': (np.array([50, 100, 50], np.uint8), np.array([100, 255, 255], np.uint8), [0, 255, 0]),
}
# HSV color code lower and upper bounds
im = cv2.imread('rubik-hard.png')
hsv_img = getAndProcessImage(im)

for color_name, color_config in colors.items():
    contours = detectColorContours(hsv_img, color_config[0], color_config[1])
    rects = filterContours(contours)
    drawRects(im, rects, color_config[2])

cv2.imwrite("extracted.jpg", im)

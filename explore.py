from distutils.command.config import config
from unittest import result
import numpy as np
import sys
import cv2
import statistics
from game_manager import Game_manager

gm = Game_manager()

colors = {
    # Blue
    'B': (np.array([90, 90, 90], np.uint8), np.array([125, 255, 255], np.uint8), [255, 0, 0]),
    # Yellow
    'Y': (np.array([25, 51, 90], np.uint8), np.array([42, 255, 255], np.uint8), [0, 255, 255]),
    # oRANGE
    'O': (np.array([0, 90, 90], np.uint8), np.array([25, 255, 255], np.uint8), [0, 0, 255]),
    # White
    'W': (np.array([0, 0, 127], np.uint8), np.array([179, 30, 255], np.uint8), [50, 50, 50]),
    # Green
    'G': (np.array([40, 90, 90], np.uint8), np.array([70, 255, 255], np.uint8), [0, 255, 0]),
    # pink
    'R': (np.array([140, 90, 90], np.uint8), np.array([180, 255, 255], np.uint8), [255, 0, 255]),
}
class Square:
    def __init__(self, x, y, w, color):
        self.x = x
        self.y = y
        self.w = w
        self.color = color
    def getDistance(self, square):
        return abs(self.x - square.x) + abs(self.y - square.y)

def detectColorContours(img, colorMin, colorMax):
    frame_threshed = cv2.inRange(
        img, colorMin, colorMax)     # Thresholding image

    #cv2.imwrite(f"before_opening{colorMin}.jpg", frame_threshed)
    # frame_threshed = cv2.morphologyEx(frame_threshed, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)))
    # cv2.imwrite(f"after_opening{colorMin}.jpg", frame_threshed)
    
    contours, _ = cv2.findContours(
        frame_threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def filterContours(contours, min_size=50, square_threshold=0.2):
    results = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if abs(w/h - 1) > square_threshold:
            continue

        if w < min_size or h < min_size:
            continue

        results.append((x, y, w))

    return results

def getBestSquares(squares, mean_treshold=0.2):
    if(len(squares) == 0): return []
    avg_size = statistics.median([r.w for r in squares])
    squares = [r for r in squares if abs(1 - r.w/avg_size) < mean_treshold]

    square_avg_distance = []
    for square in squares:
        square_avg_distance.append((square, [sum([square.getDistance(s) for s in squares])/len(squares)]))

    square_avg_distance.sort(key=lambda x: x[1])
    return [s[0] for s in square_avg_distance[:9]]

def drawRects(im, rects):
    for rect in rects:
        cv2.rectangle(im, (rect.x, rect.y),
                      (rect.x+rect.w, rect.y+rect.w), colors[rect.color][2], 10)


def getAndProcessImage(im):
    new_im = cv2.bilateralFilter(im, 9, 75, 75)
    #cv2.imwrite("bilateral_filter.jpg", new_im)
    new_im = cv2.fastNlMeansDenoisingColored(new_im, None, 10, 10, 7, 21)
    #cv2.imwrite("fastNlMeansDenoisingColored.jpg", new_im)
    hsv_img = cv2.cvtColor(new_im, cv2.COLOR_BGR2HSV)   # HSV image
    return hsv_img

# HSV color code lower and upper bounds

vid = cv2.VideoCapture(0)
fps=0
squares = []
while(True):
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    if(fps==20):
        fps=0
        squares = []

        hsv_img = getAndProcessImage(frame)
        for color_name, color_config in colors.items():
            contours = detectColorContours(hsv_img, color_config[0], color_config[1])
            rects = filterContours(contours)
            squares.extend([Square(r[0],r[1],r[2], color_name) for r in rects])
        squares = getBestSquares(squares)
        
        instruction = gm.getNextMove(squares)
        if(instruction != ""):
            print(instruction)


    drawRects(frame, squares)


    # Display the resulting frame
    cv2.imshow('frame', frame)
    
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    fps+=1

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
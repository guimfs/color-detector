import pandas as pd
import os
import cv2
from helper import run_loader

# Global variables
clicked = False
x_position = 0
y_position = 0
r = 0
g = 0
b = 0

# Images paths
images_list = os.listdir(os.path.join('images'))

# Loading Tkinter to choose your image
selected_image = run_loader(images_list)

# Reading the image from a paste
image_path = os.path.join('images', selected_image)
image = cv2.imread(image_path)

# Getting the image size
height = int(image.shape[0])
width = int(image.shape[1])

# Setting max and min pixels
max_width = 1200
max_height = 700
min_width = 600
min_height = 700

# Resizing the image uploaded
if max_height < height or max_width < width: # For big images
    factor = max_height / height
    if (max_width / width) < factor:
        factor = max_width / width
    image = cv2.resize(image, None, fx=factor, fy=factor, interpolation=cv2.INTER_AREA)
    rec_param = 500

if min_height > height or min_width > width: # For small images
    factor = min_height / height
    if (min_width / width) < factor:
        factor = min_width / width
    image = cv2.resize(image, None, fx=factor, fy=factor, interpolation=cv2.INTER_AREA)
    rec_param = image.shape[1] - 20

# Reading the CSV file (database)
header = ['color', 'color_name', 'hexa', 'r', 'g', 'b']
csv = pd.read_csv('colors.csv', names=header, header=None)

# Click method
def click(event, x, y, flags, param):
    """This method will change the values of global variables when left button on mouse is clicked twice"""
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_position, y_position, clicked
        clicked = True
        x_position = x
        y_position = y
        b, g, r = image[y, x]
        r = int(r)
        g = int(g)
        b = int(b)

# Getting the color method      
def get_color(r, g, b):
    """This method will iterate the color of the pixel"""
    minimum = 10000
    for index in range(len(csv)):
        distance = abs(r - int(csv.loc[index, "r"])) + abs(g - int(csv.loc[index, "g"])) + abs(b - int(csv.loc[index, "b"]))
        if distance <= minimum:
            minimum = distance
            color_name = csv.loc[index, 'color_name']
    return color_name

# Setting the window and event for a mouse callback
cv2.namedWindow('Color detector')
cv2.moveWindow('Color detector', 320, 0)
cv2.setMouseCallback('Color detector', click)

if __name__ == '__main__':
    while True:
        cv2.imshow('Color detector', image)
        if clicked:
            cv2.rectangle(image, (20, 20), (rec_param, 50), (b, g, r), -1)
            identified_color = f'{get_color(r, g, b)}, R = {str(r)}, G = {str(g)}, B = {str(b)}'
            cv2.putText(image, identified_color, (30, 40), 0, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            if (r + g + b) > 600:
                cv2.putText(image, identified_color, (30, 40), 0, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            clicked = False
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()
import cv2
import numpy as np
from skimage.filters import frangi

def detect_circles(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.medianBlur(gray, 11)

    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 20,
                            param1=100, param2=19, minRadius=28, maxRadius=80)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Draw the outer circle
            cv2.circle(gray_blurred, (i[0], i[1]), i[2] + 3, (0, 255, 0), 1)
            # Draw the center of the circle
            # cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

    return circles, gray_blurred



def circle_crop(img, center_x, center_y, radius):

    circle_mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.circle(circle_mask, (center_x, center_y), radius, (255, 255, 255), -1)

    masked_data = cv2.bitwise_and(img, img, mask=circle_mask) 

    return masked_data

def get_raw_red_pixels(img, center_x, center_y, radius, sensitivity=15):

    img_blurred = cv2.medianBlur(img, 7)

    circle_croped_img_blurred = circle_crop(img_blurred, center_x, center_y, radius)

    b, g, r = cv2.split(circle_croped_img_blurred.astype(np.float32))
    redness = r - ((g + b) / 2)
    mask = np.where(redness > sensitivity, 255, 0).astype(np.uint8)
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)



    y_coords, x_coords = np.where(mask == 255)
    raw_points = list(zip(x_coords, y_coords))

    print(f"found {len(raw_points)} pixels")

    circle_croped_img_blurred[mask > 0] = [0, 0, 255]
    cv2.imshow("points", circle_croped_img_blurred)

    return mask, raw_points

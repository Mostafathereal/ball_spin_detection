import cv2
import numpy as np
from utils.camera_utils import load_cam_params
# from utils.cv_utils import detect_circles, find_stitches_from_circle_lab, circle_crop, get_raw_red_pixels, find_contours, detect_baseball_seams_hsv, get_dark_red_pixels, detect_seams_fusion, crop_downsample
from utils.cv_utils import detect_circles, circle_crop, get_raw_red_pixels

# import torch
import kornia as K

cam_param_json_path = "configs/spin_camera_matrix.json"
cam_params = load_cam_params(cam_param_json_path)


# video_path = "data/spin_dataset 2/spin_dataset/raw_spin_video_695d9b0a4899846853793e7d_1767742221.mp4"
video_path = "data/spin_dataset 2/spin_dataset/raw_spin_video_695d23c184c2b7ababb57a8e_1767711685.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

frame_counter = 0
frame_start = 30
while True:
    ret, frame_bgr_np = cap.read()

    torch_bgr_tensor = K.image_to_tensor(frame_bgr_np).to(device="cuda:0")
    torch_rgb_tensor = K.color.bgr_to_rgb(torch_bgr_tensor)


    # frame_copy = frame.copy()
    # cv2.imshow("frame_copy", frame_copy)

    if not ret:
        break

    frame_counter += 1
    if frame_counter < frame_start:
        continue

    circles_list, circles_img = detect_circles(frame_bgr_np)

    if circles_list is not None:
        circle_cropped_img = circle_crop(frame_bgr_np, circles_list[0][0][0], circles_list[0][0][1], circles_list[0][0][2])
        cv2.imshow("circle_cropped_img", circle_cropped_img)
        get_raw_red_pixels(frame_bgr_np, circles_list[0][0][0], circles_list[0][0][1], circles_list[0][0][2])
    cv2.imshow("circles", circles_img)
    cv2.imshow("frame_bgr_np", frame_bgr_np)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

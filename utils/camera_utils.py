import json 
import numpy as np


def load_cam_params(json_path: str) -> dict:
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)

        cam_params = {
            "serial": data.get("serial"),
            "camera_matrix": np.array(data.get("camera_matrix"), dtype=np.float32),
            "dist_coeffs": np.array(data.get("dist_coeffs"), dtype=np.float32),
            "img_shape": np.array(data.get("img_shape"), dtype=np.float32),
            "R": np.array(data.get("R"), dtype=np.float32),
            "tvec": np.array(data.get("tvec"), dtype=np.float32)
        }
        return cam_params

    except Exception as e:
        print("failed json loading: {e}")

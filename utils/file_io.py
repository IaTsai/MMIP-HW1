import numpy as np
from PIL import Image
from pathlib import Path
import json

class FileIO:
    @staticmethod
    def read_raw(filepath, width=512, height=512, dtype=np.uint8):
        """讀取RAW格式影像"""
        with open(filepath, 'rb') as f:
            raw_data = f.read()
        img = np.frombuffer(raw_data, dtype=dtype)
        img = img.reshape((height, width))
        return img

    @staticmethod
    def write_raw(img, filepath):
        """寫入RAW格式影像"""
        img.astype(np.uint8).tofile(filepath)

    @staticmethod
    def read_image(filepath):
        """讀取一般影像格式（JPG, BMP, PNG等）"""
        img = Image.open(filepath)
        if img.mode != 'L':
            img = img.convert('L')
        return np.array(img)

    @staticmethod
    def write_image(img, filepath):
        """寫入一般影像格式"""
        Image.fromarray(img.astype(np.uint8)).save(filepath)

    @staticmethod
    def save_config(config_dict, filepath):
        """儲存設定檔"""
        with open(filepath, 'w') as f:
            json.dump(config_dict, f, indent=2)

    @staticmethod
    def load_config(filepath):
        """載入設定檔"""
        with open(filepath, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_image_info(img):
        """取得影像資訊"""
        info = {
            'shape': img.shape,
            'dtype': str(img.dtype),
            'min': int(img.min()),
            'max': int(img.max()),
            'mean': float(img.mean()),
            'std': float(img.std())
        }
        return info
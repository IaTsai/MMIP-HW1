import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path

class ImageProcessor:
    def __init__(self, data_path="data"):
        self.data_path = Path(data_path)

    # Part A: Image Reading
    def read_raw_image(self, filename, width=512, height=512):
        """讀取RAW格式影像"""
        file_path = self.data_path / filename if not Path(filename).is_absolute() else Path(filename)
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        img = np.frombuffer(raw_data, dtype=np.uint8)
        img = img.reshape((height, width))
        return img

    def read_jpg_image(self, filename):
        """讀取JPG/BMP格式影像"""
        file_path = self.data_path / filename if not Path(filename).is_absolute() else Path(filename)
        img = Image.open(file_path).convert('L')
        img = np.array(img)
        return img

    def read_image(self, filename, width=512, height=512):
        """統一的影像讀取介面"""
        if filename.endswith('.raw'):
            return self.read_raw_image(filename, width, height)
        else:
            return self.read_jpg_image(filename)

    def get_center_pixels(self, img, size=10):
        """取得影像中心10x10像素值"""
        h, w = img.shape
        center_y, center_x = h // 2, w // 2
        start_y = center_y - size // 2
        start_x = center_x - size // 2
        center_pixels = img[start_y:start_y+size, start_x:start_x+size]
        return center_pixels

    # Part B: Image Enhancement Toolkit
    def log_transform(self, img):
        """對數轉換"""
        img_normalized = img / 255.0
        c = 1.0
        log_img = c * np.log(1 + img_normalized)
        log_img = (log_img / log_img.max() * 255).astype(np.uint8)
        return log_img

    def gamma_transform(self, img, gamma=1.0):
        """Gamma轉換"""
        img_normalized = img / 255.0
        gamma_img = np.power(img_normalized, gamma)
        gamma_img = (gamma_img * 255).astype(np.uint8)
        return gamma_img

    def image_negative(self, img):
        """影像負片"""
        return 255 - img

    # Part C: Image Downsampling and Upsampling
    def nearest_neighbor_resize(self, img, new_width, new_height):
        """最近鄰插值法調整影像大小"""
        old_height, old_width = img.shape
        new_img = np.zeros((new_height, new_width), dtype=np.uint8)

        scale_x = old_width / new_width
        scale_y = old_height / new_height

        for i in range(new_height):
            for j in range(new_width):
                src_x = int(j * scale_x)
                src_y = int(i * scale_y)

                src_x = min(src_x, old_width - 1)
                src_y = min(src_y, old_height - 1)

                new_img[i, j] = img[src_y, src_x]

        return new_img

    def bilinear_resize(self, img, new_width, new_height):
        """雙線性插值法調整影像大小"""
        old_height, old_width = img.shape
        new_img = np.zeros((new_height, new_width), dtype=np.uint8)

        scale_x = (old_width - 1) / (new_width - 1) if new_width > 1 else 0
        scale_y = (old_height - 1) / (new_height - 1) if new_height > 1 else 0

        for i in range(new_height):
            for j in range(new_width):
                src_x = j * scale_x
                src_y = i * scale_y

                x1 = int(np.floor(src_x))
                x2 = min(x1 + 1, old_width - 1)
                y1 = int(np.floor(src_y))
                y2 = min(y1 + 1, old_height - 1)

                dx = src_x - x1
                dy = src_y - y1

                value = (1 - dx) * (1 - dy) * img[y1, x1] + \
                        dx * (1 - dy) * img[y1, x2] + \
                        (1 - dx) * dy * img[y2, x1] + \
                        dx * dy * img[y2, x2]

                new_img[i, j] = int(value)

        return new_img
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path
import os

class ImageProcessor:
    def __init__(self):
        self.data_path = Path("data")

    # Part A: Image Reading
    def read_raw_image(self, filename, width=512, height=512):
        """讀取RAW格式影像"""
        file_path = self.data_path / filename
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        img = np.frombuffer(raw_data, dtype=np.uint8)
        img = img.reshape((height, width))
        return img

    def read_jpg_image(self, filename):
        """讀取JPG/BMP格式影像"""
        file_path = self.data_path / filename
        img = Image.open(file_path).convert('L')
        img = np.array(img)
        return img

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
        # 正規化到 [0, 1]
        img_normalized = img / 255.0
        # 加1避免log(0)
        c = 1.0
        log_img = c * np.log(1 + img_normalized)
        # 正規化到 [0, 255]
        log_img = (log_img / log_img.max() * 255).astype(np.uint8)
        return log_img

    def gamma_transform(self, img, gamma=1.0):
        """Gamma轉換"""
        # 正規化到 [0, 1]
        img_normalized = img / 255.0
        # Gamma轉換
        gamma_img = np.power(img_normalized, gamma)
        # 轉回 [0, 255]
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

        # 計算縮放比例
        scale_x = old_width / new_width
        scale_y = old_height / new_height

        for i in range(new_height):
            for j in range(new_width):
                # 找到原圖對應的位置
                src_x = int(j * scale_x)
                src_y = int(i * scale_y)

                # 確保不超出邊界
                src_x = min(src_x, old_width - 1)
                src_y = min(src_y, old_height - 1)

                new_img[i, j] = img[src_y, src_x]

        return new_img

    def bilinear_resize(self, img, new_width, new_height):
        """雙線性插值法調整影像大小"""
        old_height, old_width = img.shape
        new_img = np.zeros((new_height, new_width), dtype=np.uint8)

        # 計算縮放比例
        scale_x = (old_width - 1) / (new_width - 1) if new_width > 1 else 0
        scale_y = (old_height - 1) / (new_height - 1) if new_height > 1 else 0

        for i in range(new_height):
            for j in range(new_width):
                # 找到原圖對應的位置
                src_x = j * scale_x
                src_y = i * scale_y

                # 找到四個鄰近點
                x1 = int(np.floor(src_x))
                x2 = min(x1 + 1, old_width - 1)
                y1 = int(np.floor(src_y))
                y2 = min(y1 + 1, old_height - 1)

                # 計算權重
                dx = src_x - x1
                dy = src_y - y1

                # 雙線性插值
                value = (1 - dx) * (1 - dy) * img[y1, x1] + \
                        dx * (1 - dy) * img[y1, x2] + \
                        (1 - dx) * dy * img[y2, x1] + \
                        dx * dy * img[y2, x2]

                new_img[i, j] = int(value)

        return new_img

    def display_images(self, images, titles, figsize=(15, 10)):
        """顯示多張影像"""
        n = len(images)
        cols = 3
        rows = (n + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        axes = axes.flatten() if n > 1 else [axes]

        for i, (img, title) in enumerate(zip(images, titles)):
            axes[i].imshow(img, cmap='gray')
            axes[i].set_title(title)
            axes[i].axis('off')

        # 隱藏多餘的子圖
        for i in range(n, len(axes)):
            axes[i].axis('off')

        plt.tight_layout()
        return fig

    def save_figure(self, fig, filename):
        """儲存圖片"""
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        fig.savefig(output_dir / filename, dpi=100, bbox_inches='tight')
        plt.close(fig)

def main():
    # 初始化影像處理器
    processor = ImageProcessor()

    # 建立輸出資料夾
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    print("=" * 50)
    print("HW1: Digital Image Processing")
    print("=" * 50)

    # Part A: Image Reading
    print("\n[Part A] Image Reading")
    print("-" * 30)

    # 讀取RAW影像
    raw_files = ['lena.raw', 'goldhill.raw', 'peppers.raw']
    raw_images = []
    for file in raw_files:
        img = processor.read_raw_image(file)
        raw_images.append(img)
        print(f"讀取 {file}: shape={img.shape}, dtype={img.dtype}")

        # 取得並顯示中心10x10像素
        center = processor.get_center_pixels(img)
        print(f"{file} 中心10x10像素值:")
        print(center)
        print()

    # 讀取JPG/BMP影像
    jpg_files = ['boat.bmp', 'baboon.bmp', 'F16.bmp']
    jpg_images = []
    for file in jpg_files:
        img = processor.read_jpg_image(file)
        jpg_images.append(img)
        print(f"讀取 {file}: shape={img.shape}, dtype={img.dtype}")

        # 取得並顯示中心10x10像素
        center = processor.get_center_pixels(img)
        print(f"{file} 中心10x10像素值:")
        print(center)
        print()

    # 顯示所有原始影像
    all_images = raw_images + jpg_images
    all_titles = [f"RAW: {f}" for f in raw_files] + [f"BMP: {f}" for f in jpg_files]
    fig = processor.display_images(all_images, all_titles)
    processor.save_figure(fig, "part_a_original_images.png")

    # Part B: Image Enhancement
    print("\n[Part B] Image Enhancement")
    print("-" * 30)

    # 對每張影像進行增強處理
    for idx, (img, name) in enumerate(zip(all_images, raw_files + jpg_files)):
        print(f"\n處理影像: {name}")

        # Log transform
        log_img = processor.log_transform(img)

        # Gamma transform (使用不同的gamma值)
        gamma_05 = processor.gamma_transform(img, gamma=0.5)
        gamma_15 = processor.gamma_transform(img, gamma=1.5)
        gamma_22 = processor.gamma_transform(img, gamma=2.2)

        # Image negative
        negative_img = processor.image_negative(img)

        # 顯示結果
        enhanced_images = [img, log_img, gamma_05, gamma_15, gamma_22, negative_img]
        enhanced_titles = [
            f"Original: {name}",
            "Log Transform",
            "Gamma (γ=0.5)",
            "Gamma (γ=1.5)",
            "Gamma (γ=2.2)",
            "Negative"
        ]

        fig = processor.display_images(enhanced_images, enhanced_titles)
        processor.save_figure(fig, f"part_b_enhancement_{idx}_{name.split('.')[0]}.png")

    # Part C: Image Downsampling and Upsampling
    print("\n[Part C] Image Downsampling and Upsampling")
    print("-" * 30)

    # 使用 Lena 影像進行測試
    test_img = raw_images[1]  # 使用 goldhill.raw

    # 測試案例
    test_cases = [
        ("512x512 -> 128x128", (128, 128)),
        ("512x512 -> 32x32", (32, 32)),
        ("32x32 -> 512x512", (512, 512)),
        ("512x512 -> 1024x512", (1024, 512)),
        ("128x128 -> 256x512", (256, 512))
    ]

    for case_name, (new_w, new_h) in test_cases:
        print(f"\n測試: {case_name}")

        # 如果是從32x32開始，先降採樣到32x32
        if "32x32 ->" in case_name:
            source_img = processor.bilinear_resize(test_img, 32, 32)
        elif "128x128 ->" in case_name:
            source_img = processor.bilinear_resize(test_img, 128, 128)
        else:
            source_img = test_img

        # 使用兩種方法調整大小
        nn_img = processor.nearest_neighbor_resize(source_img, new_w, new_h)
        bilinear_img = processor.bilinear_resize(source_img, new_w, new_h)

        # 顯示結果
        if source_img.shape[0] < 100:  # 如果原圖太小，放大顯示
            display_source = processor.nearest_neighbor_resize(source_img,
                                                              min(source_img.shape[0]*4, 512),
                                                              min(source_img.shape[1]*4, 512))
        else:
            display_source = source_img

        resize_images = [display_source, nn_img, bilinear_img]
        resize_titles = [
            f"Source ({source_img.shape[1]}x{source_img.shape[0]})",
            f"Nearest Neighbor ({new_w}x{new_h})",
            f"Bilinear ({new_w}x{new_h})"
        ]

        fig = processor.display_images(resize_images, resize_titles, figsize=(15, 5))
        case_filename = case_name.replace(" ", "_").replace("->", "to").replace("x", "")
        processor.save_figure(fig, f"part_c_resize_{case_filename}.png")

    print("\n" + "=" * 50)
    print("所有處理完成！結果已儲存至 output/ 資料夾")
    print("=" * 50)

if __name__ == "__main__":
    main()
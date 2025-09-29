#!/usr/bin/env python3
"""
多模態影像處理系統 - 主程式
整合各次作業的影像處理功能
"""

import sys
from pathlib import Path
import argparse

from core import ImageProcessor
from utils import Visualizer, FileIO

def hw1_demo():
    """執行HW1的展示功能"""
    processor = ImageProcessor()
    visualizer = Visualizer()

    print("=" * 50)
    print("HW1: Digital Image Processing Demo")
    print("=" * 50)

    # 讀取測試影像
    test_images = {
        'lena.raw': processor.read_raw_image('lena.raw'),
        'goldhill.raw': processor.read_raw_image('goldhill.raw'),
        'boat.bmp': processor.read_jpg_image('boat.bmp')
    }

    for name, img in test_images.items():
        print(f"\n處理影像: {name}")
        print(f"Shape: {img.shape}, Type: {img.dtype}")

        # 展示各種影像增強
        enhanced = {
            'Original': img,
            'Log Transform': processor.log_transform(img),
            'Gamma (0.5)': processor.gamma_transform(img, 0.5),
            'Gamma (2.2)': processor.gamma_transform(img, 2.2),
            'Negative': processor.image_negative(img)
        }

        fig = visualizer.display_images(
            list(enhanced.values()),
            list(enhanced.keys()),
            figsize=(15, 8)
        )
        visualizer.save_figure(fig, f"demo_{name.split('.')[0]}_enhanced.png")

        # 展示縮放功能
        resized = {
            'Original (512x512)': img,
            'Downsampled (128x128)': processor.nearest_neighbor_resize(img, 128, 128),
            'Bilinear (256x256)': processor.bilinear_resize(img, 256, 256)
        }

        fig = visualizer.display_images(
            list(resized.values()),
            list(resized.keys()),
            figsize=(12, 4)
        )
        visualizer.save_figure(fig, f"demo_{name.split('.')[0]}_resized.png")

    print("\n展示完成！結果已儲存至 output/ 資料夾")

def main():
    parser = argparse.ArgumentParser(description='多模態影像處理系統')
    parser.add_argument('--hw', type=int, choices=[1, 2, 3],
                        help='選擇要執行的作業 (1, 2, or 3)')
    parser.add_argument('--demo', action='store_true',
                        help='執行展示模式')
    parser.add_argument('--input', type=str,
                        help='輸入影像路徑')
    parser.add_argument('--output', type=str, default='output',
                        help='輸出資料夾路徑')

    args = parser.parse_args()

    if args.demo:
        if args.hw == 1 or args.hw is None:
            hw1_demo()
        elif args.hw == 2:
            print("HW2 功能尚未實作")
        elif args.hw == 3:
            print("HW3 功能尚未實作")
    elif args.input:
        # 處理單一影像
        processor = ImageProcessor()
        visualizer = Visualizer(args.output)

        # 讀取影像
        if args.input.endswith('.raw'):
            img = processor.read_raw_image(args.input)
        else:
            img = processor.read_jpg_image(args.input)

        print(f"已讀取影像: {args.input}")
        print(f"影像大小: {img.shape}")

        # 顯示影像資訊
        info = FileIO.get_image_info(img)
        print(f"影像統計: min={info['min']}, max={info['max']}, "
              f"mean={info['mean']:.2f}, std={info['std']:.2f}")

        # 執行基本處理
        processed = {
            'Original': img,
            'Enhanced (Log)': processor.log_transform(img),
            'Enhanced (Gamma)': processor.gamma_transform(img, 1.5)
        }

        fig = visualizer.display_images(
            list(processed.values()),
            list(processed.keys())
        )
        output_name = Path(args.input).stem + "_processed.png"
        visualizer.save_figure(fig, output_name)
        print(f"結果已儲存至: {args.output}/{output_name}")
    else:
        print("多模態影像處理系統")
        print("-" * 30)
        print("使用方式:")
        print("  python main.py --demo          # 執行展示")
        print("  python main.py --hw 1 --demo   # 執行HW1展示")
        print("  python main.py --input image.bmp  # 處理單一影像")
        print("\n可用功能:")
        print("  - HW1: 影像讀取、點運算、縮放")
        print("  - HW2: (待實作)")
        print("  - HW3: (待實作)")

if __name__ == "__main__":
    main()
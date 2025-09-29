import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

class Visualizer:
    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def display_images(self, images, titles, figsize=(15, 10)):
        """顯示多張影像"""
        n = len(images)
        cols = 3
        rows = (n + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=figsize)

        if n == 1:
            axes = [axes]
        elif rows == 1:
            pass
        else:
            axes = axes.flatten()

        for i, (img, title) in enumerate(zip(images, titles)):
            if n == 1:
                ax = axes[0]
            else:
                ax = axes[i]
            ax.imshow(img, cmap='gray')
            ax.set_title(title)
            ax.axis('off')

        if n > 1:
            for i in range(n, len(axes)):
                axes[i].axis('off')

        plt.tight_layout()
        return fig

    def save_figure(self, fig, filename):
        """儲存圖片"""
        fig.savefig(self.output_dir / filename, dpi=100, bbox_inches='tight')
        plt.close(fig)

    def plot_histogram(self, img, title="Histogram"):
        """繪製直方圖"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        ax1.imshow(img, cmap='gray')
        ax1.set_title("Image")
        ax1.axis('off')

        ax2.hist(img.ravel(), bins=256, range=[0, 256], color='black', alpha=0.7)
        ax2.set_title(title)
        ax2.set_xlabel("Pixel Value")
        ax2.set_ylabel("Frequency")
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def compare_images(self, img1, img2, title1="Original", title2="Processed"):
        """比較兩張影像"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        ax1.imshow(img1, cmap='gray')
        ax1.set_title(title1)
        ax1.axis('off')

        ax2.imshow(img2, cmap='gray')
        ax2.set_title(title2)
        ax2.axis('off')

        plt.tight_layout()
        return fig
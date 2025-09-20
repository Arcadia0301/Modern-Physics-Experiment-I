import numpy as np
import matplotlib.pyplot as plt
import re

# 两个文件
files = [
    "vac/merged/Merged_Pos270mm_Vac.txt",
    "air/merged/Merged_Pos270mm_Air.txt"
]

# 同色系，深色和浅色
colors = ["tab:brown", "#D2B48C"]  # 深红和浅红

plt.figure(figsize=(8, 6))

for fname, color in zip(files, colors):
    data = np.loadtxt(fname)
    x = data[:, 0]
    y = data[:, 1]

    # 提取标签，括号显示
    match = re.search(r'Pos(\d+)mm_(\w+)', fname)
    if match:
        label = f"{match.group(1)} mm ({match.group(2)})"
    else:
        label = fname.split(".")[0]

    # 绘制散点
    plt.scatter(x, y, color=color, s=8, alpha=0.8, label=label)

    # 找 x > 50 的最大值点
    mask = x > 50
    if np.any(mask):
        x_filtered = x[mask]
        y_filtered = y[mask]
        max_idx = np.argmax(y_filtered)
        x_peak = x_filtered[max_idx]
        y_peak = y_filtered[max_idx]
        print(f"{label} peak x = {x_peak}")  # 输出 x 坐标

        # 空心峰值点，用同色系边框
        plt.scatter(x_peak, y_peak,
                    facecolors='white', edgecolors=color, s=15, linewidths=1.5, zorder=5)

plt.legend(fontsize=14)
plt.xlabel("X", fontsize=18)
plt.ylabel("N", fontsize=18)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.tight_layout()
plt.show()

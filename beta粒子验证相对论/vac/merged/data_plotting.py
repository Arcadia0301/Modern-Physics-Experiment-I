import numpy as np
import matplotlib.pyplot as plt
import re

# 文件列表
files = [
    "Merged_Pos150mm_Vac.txt",
    "Merged_Pos170mm_Vac.txt",
    "Merged_Pos190mm_Vac.txt",
    "Merged_Pos220mm_Vac.txt",
    "Merged_Pos250mm_Vac.txt",
    "Merged_Pos270mm_Vac.txt"
]

colors = ["tab:blue", "tab:orange", "tab:green",
          "tab:red", "tab:purple", "tab:brown"]

plt.figure(figsize=(10, 6))

for fname, color in zip(files, colors):
    data = np.loadtxt(fname)
    x = data[:, 0]
    y = data[:, 1]

    # 提取标签
    match = re.search(r'Pos(\d+)mm', fname)
    label = match.group(1) + " mm" if match else fname.split(".")[0]

    # 绘制普通散点
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

        # 画空心峰值点
        plt.scatter(x_peak, y_peak,
                    facecolors='white', edgecolors=color, s=15, linewidths=1.5, zorder=5)

plt.ylim(0, 160)  # 设置纵坐标范围
plt.legend(fontsize=14)
plt.xlabel("X", fontsize=18)
plt.ylabel("N", fontsize=18)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.tight_layout()
plt.show()

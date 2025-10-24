import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from matplotlib import font_manager as fm

# ===== 1. 中文字体 =====
font_path = '/System/Library/Fonts/STHeiti Medium.ttc'
my_font = fm.FontProperties(fname=font_path, size=16)

# ===== 2. 读取数据 =====
filename = "2300017787/2300017787_Cs_Co_far.txt"   # ← 换成你的文件路径
n = np.loadtxt(filename)                            # 文件只有一列：计数 n
x = np.arange(1, len(n) + 1)                       # 道址 x = 1, 2, ..., 1024

# ===== 3. 样条平滑拟合 =====
x_smooth = np.linspace(x.min(), x.max(), 300)
spline = make_interp_spline(x, n, k=3)
n_smooth = spline(x_smooth)

# ===== 4. 绘图 =====
plt.figure(figsize=(10, 6))

# 数据点
plt.scatter(x, n, color='#20B2AA', s=30, alpha=0.8, label='测量数据', zorder=3)

# 平滑曲线
plt.plot(x_smooth, n_smooth, color='#007BA7', linewidth=2.2, label='拟合曲线')

# ===== 5. 手动指定灰色虚线峰值 =====
manual_peaks = [39, 148, 450, 793, 898]
gray_ns = []

for x_peak in manual_peaks:
    plt.axvline(x=x_peak, color='gray', linestyle='--', linewidth=1, alpha=1, dashes=(8,6))
    # 插值获取对应的 n
    n_val = np.interp(x_peak, x_smooth, n_smooth)
    gray_ns.append(n_val)

# 输出灰色虚线峰值及对应计数
print("灰色虚线峰值及对应计数：")
for i, (x_val, n_val) in enumerate(zip(manual_peaks, gray_ns), 1):
    print(f"峰 {i}: x = {x_val}, n ≈ {n_val:.1f}")

# ===== 坐标轴与标题 =====
plt.xlabel('道址 x', fontproperties=my_font, fontsize=18)
plt.ylabel('计数 n (个)', fontproperties=my_font, fontsize=18)
plt.legend(prop=my_font, loc='upper right')
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
plt.show()
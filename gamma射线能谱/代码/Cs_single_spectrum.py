import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from matplotlib import font_manager as fm
from scipy.signal import find_peaks

# ===== 1. 加载中文字体 =====
font_path = '/System/Library/Fonts/STHeiti Medium.ttc'
my_font = fm.FontProperties(fname=font_path, size=16)

# ===== 2. 读取数据 =====
filename = "2300017787/Cs_single_spectrum.txt"
data = np.loadtxt(filename, skiprows=1)
E_g = data[:, 0]
n = data[:, 1]

# ===== 3. 升序排序 =====
sort_idx = np.argsort(E_g)
E_g = E_g[sort_idx]
n = n[sort_idx]

# ===== 4. 样条平滑拟合 =====
E_smooth = np.linspace(E_g.min(), E_g.max(), 500)
spline = make_interp_spline(E_g, n, k=3)
n_smooth = spline(E_smooth)

# ===== 5. 找局部峰值（高度超过20%总峰值） =====
peaks, _ = find_peaks(n_smooth)
threshold = 0.25 * np.max(n_smooth)  # 高度阈值
peaks = peaks[n_smooth[peaks] > threshold]  # 只保留高度超过阈值的峰
peak_Es = E_smooth[peaks]
peak_ns = n_smooth[peaks]

# ===== 输出每个峰值 =====
print("峰值列表 (E_g, n):")
for E_peak, n_peak in zip(peak_Es, peak_ns):
    print(f"{E_peak:.3f} V, {n_peak:.1f}")

# ===== 输出最后一个峰的半高全宽 (FWHM) =====
last_peak_idx = peaks[-1]
peak_height = n_smooth[last_peak_idx]
half_height = peak_height / 2

# 找左右半高点索引
left_idx = np.where(n_smooth[:last_peak_idx] <= half_height)[0]
left_idx = left_idx[-1] if len(left_idx) > 0 else 0

right_idx = np.where(n_smooth[last_peak_idx:] <= half_height)[0]
right_idx = right_idx[0] + last_peak_idx if len(right_idx) > 0 else len(n_smooth)-1

FWHM = E_smooth[right_idx] - E_smooth[left_idx]
print(f"\n最后一个峰半高全宽 FWHM: {FWHM:.3f} V")

# ===== 6. 绘图 =====
plt.figure(figsize=(10, 6))

# 散点
plt.scatter(E_g, n, color='#5894c8', s=30, alpha=0.8, label='测量数据', zorder=3)

# 拟合曲线
plt.plot(E_smooth, n_smooth, color='#1E90FF', linewidth=2, label='拟合曲线')

# 局部峰值虚线（淡蓝色）
for x in peak_Es:
    plt.axvline(x=x, color='gray', linestyle='--', linewidth=1, alpha=1, dashes=(8, 6))

# ===== 在绘图中画最后一个峰的FWHM =====
# 半高水平线
plt.hlines(half_height, E_smooth[left_idx]-0.5, E_smooth[right_idx]+0.5,
           colors='green', linestyles='--', linewidth=2)

# 坐标轴与标题（中文）
plt.xlabel('阈值 $E_g$ (V)', fontproperties=my_font, fontsize=18)
plt.ylabel('计数 $n$ (个)', fontproperties=my_font, fontsize=18)

# 图例
plt.legend(prop=my_font, loc='upper right')
plt.ylim(bottom=None, top=19000)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
plt.show()
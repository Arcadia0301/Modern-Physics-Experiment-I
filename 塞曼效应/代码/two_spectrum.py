import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# ---------- 读取第一个文件 ----------
filename1 = "I_5A_pi.txt"
data1 = np.loadtxt(filename1)
pressure1 = data1[:, 0]
intensity1 = data1[:, 1]
idx1 = np.argsort(pressure1)
pressure1 = pressure1[idx1]
intensity1 = intensity1[idx1]

# ---------- 读取第二个文件 ----------
filename2 = "I_5A_sigma.txt"
data2 = np.loadtxt(filename2)
pressure2 = data2[:, 0]
intensity2 = data2[:, 1]
idx2 = np.argsort(pressure2)
pressure2 = pressure2[idx2]
intensity2 = intensity2[idx2]

# ---------- 样条拟合 ----------
pressure_dense1 = np.linspace(pressure1.min(), pressure1.max(), 1000)
spline1 = make_interp_spline(pressure1, intensity1, k=3)
intensity_smooth1 = spline1(pressure_dense1)

pressure_dense2 = np.linspace(pressure2.min(), pressure2.max(), 1000)
spline2 = make_interp_spline(pressure2, intensity2, k=3)
intensity_smooth2 = spline2(pressure_dense2)

# ---------- 纵向偏移 ----------
shift = 500  # 第二条曲线向上移动的值
intensity_smooth2_shifted = intensity_smooth2 + shift

# ---------- 绘图 ----------
plt.figure(figsize=(12,6))

# 绘制两条曲线
plt.plot(pressure_dense2, intensity_smooth2_shifted, color='#2E5AA7', linestyle='-', linewidth=3, label=r'$\sigma$ component (shifted)')
plt.plot(pressure_dense1, intensity_smooth1, color='#f7aa58', linestyle='-', linewidth=3, label=r'$\pi$ component')
# 绘制 shift 的水平线
plt.axhline(y=shift, color='grey', linestyle='--', linewidth=1.5, label=f'Shift = {shift}')

# ⬇⬇ 强制 x、y 轴从 0 开始 ⬇⬇
plt.xlim(left=0, right=3800)
plt.ylim(bottom=0, top=max(intensity_smooth1.max(), intensity_smooth2_shifted.max())*1.4)

plt.xlabel("Pressure (a.u.)", fontsize=16)
plt.ylabel("Intensity (a.u.)", fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize=16, loc='upper right')
plt.tight_layout()
plt.show()
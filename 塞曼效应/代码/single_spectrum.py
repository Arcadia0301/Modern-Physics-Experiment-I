import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# ---------- 读取文件 ----------
filename = "I_0A.txt"
data = np.loadtxt(filename)

pressure = data[:, 0]
intensity = data[:, 1]

# 按横轴排序
idx = np.argsort(pressure)
pressure = pressure[idx]
intensity = intensity[idx]

# ---------- 样条拟合 ----------
pressure_dense = np.linspace(pressure.min(), pressure.max(), 1000)
spline = make_interp_spline(pressure, intensity, k=3)
intensity_smooth = spline(pressure_dense)

# ---------- 绘图 ----------
plt.figure(figsize=(12,6))

# 散点图 (如需要)
# plt.scatter(pressure, intensity, s=20, label='Raw Data')

plt.plot(pressure_dense, intensity_smooth, color='#046B38', linestyle='-', linewidth=3, label='B=0.0 T')

# ⬇⬇ 强制 x、y 轴从 0 开始 ⬇⬇
plt.xlim(left=0, right=3800)
plt.ylim(bottom=0, top=1900)

plt.xlabel("Pressure (a.u.)", fontsize=16)
plt.ylabel("Intensity (a.u.)", fontsize=16)
# plt.title("B=0 T", fontsize=20)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize=16, loc = 'upper right')
plt.tight_layout()
plt.show()
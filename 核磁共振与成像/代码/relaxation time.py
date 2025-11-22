import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

def load_txt(filename):
    data = np.loadtxt(filename)
    t = data[:, 0]
    s = data[:, 1]

    # ---- 按时间升序排列 ----
    idx = np.argsort(t)
    t = t[idx]
    s = s[idx]

    return t, s

# 读取并自动排序
t1, s1 = load_txt("cuso4_0.5_T1.txt")
t2, s2 = load_txt("cuso4_0.5_T2.txt")

# --- 平滑处理 ---
def smooth_curve(x, y):
    # x 和 y 已经在 load_txt 中排好序，这里可不再排序
    spline = make_interp_spline(x, y, k=3)
    x_new = np.linspace(x.min(), x.max(), 1000000)
    y_new = spline(x_new)
    return x_new, y_new

x1_smooth, y1_smooth = smooth_curve(t1, s1)
x2_smooth, y2_smooth = smooth_curve(t2, s2)

# ---------------- 绘图 ----------------
plt.figure(figsize=(10, 6))

# 散点
plt.scatter(t1, s1, color='green', s=20)
plt.scatter(t2, s2, color='blue', s=20)

# 平滑曲线
plt.plot(x1_smooth, y1_smooth, color='green', linewidth=2, label='longitudinal relaxation time T1')
plt.plot(x2_smooth, y2_smooth, color='blue', linewidth=2, label='transverse relaxation time T2')

plt.xscale("log")  # 横坐标对数

# 字体大小设置
plt.xlabel("Time (ms)", fontsize=16)
plt.ylabel("Signal magnitude (a.u.)", fontsize=16)
plt.title("0.5% CuSO4 Solution", fontsize=18)
plt.legend(fontsize=14, loc='upper left')
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()
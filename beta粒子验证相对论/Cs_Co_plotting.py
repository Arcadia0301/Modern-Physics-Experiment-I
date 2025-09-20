import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess

# 文件名
filename = "Cs.txt"

# 读取数据
data = np.loadtxt(filename)
x = data[:, 0]
y = data[:, 1]

# 定义不同x区间对应的frac
frac_values = np.zeros_like(x)
frac_values[x < 112] = 0.015
frac_values[(x >= 112) & (x < 180)] = 0.01
frac_values[x >= 180] = 0.05

# 自定义局部 LOWESS
smoothed = np.zeros_like(y)
for i, xi in enumerate(x):
    f = frac_values[i]
    y_fit = lowess(y, x, frac=f, it=0, return_sorted=False)
    smoothed[i] = y_fit[i]

# 绘图
fig, ax = plt.subplots(figsize=(8/1.2, 6/1.2))

# 散点和拟合线
ax.scatter(x, y, color='skyblue', s=6, alpha=1)
ax.plot(x, smoothed, color='blue', linewidth=2)

# 标红特定点
highlight_x = [47,153]
for hx in highlight_x:
    mask = x == hx
    ax.scatter(x[mask], y[mask], color='orange', s=10, zorder=5)

# 坐标轴标签和标题
ax.set_xlabel("X", fontsize=18)
ax.set_ylabel("N", fontsize=18)

# 坐标轴刻度字体大小
ax.tick_params(axis='both', which='major', labelsize=14)

plt.tight_layout()
plt.show()

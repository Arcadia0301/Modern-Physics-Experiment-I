import numpy as np
import matplotlib.pyplot as plt

# 四个点
x_points = np.array([271, 306, 47, 153])
y_points = np.array([1173.237, 1332.501, 184.323, 661.660])

# 线性拟合
coeff = np.polyfit(x_points, y_points, 1)
a, b = coeff

# 相关系数 r
r_matrix = np.corrcoef(x_points, y_points)
r = r_matrix[0, 1]

# 拟合直线
x_fit = np.linspace(min(x_points)-10, max(x_points)+10, 100)
y_fit = a * x_fit + b

# 绘图
fig, ax = plt.subplots(figsize=(8/1.2, 6/1.2))

# 空心白圈散点
ax.scatter(x_points, y_points, s=80, facecolors='white', edgecolors='black', linewidths=1.5, label='Data points')

# 红色拟合线
ax.plot(x_fit, y_fit, color='red', linewidth=2, label='Linear fit')

# 坐标轴标签和标题
ax.set_xlabel("N", fontsize=18)
ax.set_ylabel("E (keV)", fontsize=18)

# 坐标轴刻度字体大小
ax.tick_params(axis='both', which='major', labelsize=14)


plt.tight_layout()
plt.show()

print(f"Linear fit: y = {a:.4f} * x + {b:.4f}")
print(f"Correlation coefficient r = {r:.4f}")

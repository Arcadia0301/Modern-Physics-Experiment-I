import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 实验数据
T = np.array([289.81, 293.68, 299.58, 303.70, 309.24, 314.56])  # K
I = np.array([1.614, 2.423, 3.673, 5.450, 7.951, 11.470]) * 1e-6  # A
V_mean = 160.18e-3  # V

# 物理常数
q = 1.602e-19
k = 1.381e-23
Ae = 2.83e-3  # cm^2

# 纵坐标和横坐标
y = np.log(I / T**2)
x = 1000 / T

# 线性回归 - 获取斜率和截距的标准误
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
# std_err 是斜率的标准误，需要计算截距的标准误

n = len(x)
x_mean = np.mean(x)
Sxx = np.sum((x - x_mean)**2)
s_err = np.sqrt(np.sum((y - (slope*x + intercept))**2) / (n-2))

# 正确的标准误计算
slope_err = std_err  # linregress返回的就是斜率标准误
intercept_err = s_err * np.sqrt(1/n + x_mean**2 / Sxx)

print(f"斜率 m = {slope:.3f} ± {slope_err:.3f}")
print(f"截距 b = {intercept:.3f} ± {intercept_err:.3f}")

# 计算物理参数
n = 1.304  # 理想因子
phi_b = -slope * k / q * 1000 + V_mean / n
phi_b_err = slope_err * k / q * 1000

Astar = np.exp(intercept) / Ae
# A** 的误差传递
Astar_err = Astar * intercept_err  # d(A**)/A** = d(intercept)

print(f"肖特基势垒高度 φ_b = {phi_b:.4f} ± {phi_b_err:.4f} eV")
print(f"有效理查逊常数 A** = {Astar:.2f} ± {Astar_err:.2f} A/cm²·K²")
print(f"R² = {r_value**2:.5f}")

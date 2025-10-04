import numpy as np
import matplotlib.pyplot as plt

filename = "exp2.txt"

dVdI_list = []
one_over_I_list = []
T_list = []

# 读取数据
with open(filename, "r") as f:
    for _ in range(2):
        f.readline()  # 跳过表头
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 5:
            try:
                T_val = float(parts[2])
                dVdI_val = float(parts[3])
                one_over_I_val = float(parts[4])
                T_list.append(T_val)
                dVdI_list.append(dVdI_val)
                one_over_I_list.append(one_over_I_val)
            except ValueError:
                continue

T_arr = np.array(T_list)
dVdI_arr = np.array(dVdI_list)
one_over_I_arr = np.array(one_over_I_list)

# 温度平均值
T_mean = np.mean(T_arr)
print(f"温度平均值 = {T_mean:.2f} K")

# 去掉无效值
mask = (~np.isnan(one_over_I_arr)) & (~np.isnan(dVdI_arr)) & (one_over_I_arr != 0)
x = one_over_I_arr[mask]
y = dVdI_arr[mask]

# ===========================
# 手动线性拟合 + 正确的斜率和截距不确定度
# ===========================
n = len(x)
x_mean = np.mean(x)
y_mean = np.mean(y)

# 斜率和截距
slope = np.sum((x - x_mean)*(y - y_mean)) / np.sum((x - x_mean)**2)
intercept = y_mean - slope * x_mean

# 残差标准差
residuals = y - (slope*x + intercept)
s_err = np.sqrt(np.sum(residuals**2)/(n-2))

# 标准误
slope_err = s_err / np.sqrt(np.sum((x - x_mean)**2))
intercept_err = s_err * np.sqrt(1/n + x_mean**2 / np.sum((x - x_mean)**2))

# R^2
r_squared = np.corrcoef(x, y)[0,1]**2

# ===========================
# 绘图
# ===========================
plt.figure(figsize=(6,5))
plt.scatter(x, y, color='black', label='Data')
plt.xlabel("1/I (1/A)", fontsize=16)
plt.ylabel("dV/dI (Ω)", fontsize=16)

# 拟合直线
x_fit = np.linspace(np.min(x), np.max(x), 100)
y_fit = slope*x_fit + intercept
plt.plot(x_fit, y_fit, color='red', label='Linear fit')

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(False)
plt.legend()
plt.tight_layout()
plt.show()

# ===========================
# 输出结果
# ===========================
print("拟合直线方程: dV/dI = slope * (1/I) + intercept")
print(f"slope = {slope:.5f} ± {slope_err:.5f} V/A^2")
print(f"intercept = {intercept:.5f} ± {intercept_err:.5f} Ω")
print(f"皮尔逊 r^2 = {r_squared:.5f}")

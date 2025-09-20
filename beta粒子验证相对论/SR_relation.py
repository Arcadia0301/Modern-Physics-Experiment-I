import matplotlib.pyplot as plt
import numpy as np

# 提取的实验数据点
pc_exp = np.array([0.81 , 0.99 , 1.17 , 1.44 , 1.71 , 1.89])  # MeV
Ek_exp = np.array([0.402, 0.558, 0.740, 0.994, 1.254, 1.425])  # MeV
Ek_exp2 = np.array([0.382, 0.570, 0.727, 0.962, 1.176, 1.362])  # MeV

# 创建理论曲线的Ek值范围
Ek_theory = np.linspace(0, 3, 100)  # MeV

# 相对论理论曲线: pc = sqrt((Ek + 0.511)^2 - 0.511^2)
pc_relativistic = np.sqrt((Ek_theory + 0.511)**2 - 0.511**2)

# 经典理论曲线: pc = sqrt(1.022 * Ek)
pc_classical = np.sqrt(1.022 * Ek_theory)

# 创建图形
plt.figure(figsize=(8, 6))

# 绘制实验数据点（白色空心点）
plt.plot(pc_exp, Ek_exp, 'ro', markersize=6, markeredgewidth=2, 
         markeredgecolor='red')

# plt.plot(pc_exp, Ek_exp2, 'wo', markersize=6, markeredgewidth=2, 
 #        markeredgecolor='black')

# 绘制相对论理论曲线（红色实线）
plt.plot(pc_relativistic, Ek_theory, 'r-', linewidth=2.5)

# 绘制经典理论曲线（蓝色虚线）
plt.plot(pc_classical, Ek_theory, 'b--', linewidth=2.5)

# 设置图表属性
plt.xlabel('pc (MeV)', fontsize=18)
plt.ylabel('$E_k$ (MeV)', fontsize=18)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True, alpha=0.3)

# 设置坐标轴范围
plt.xlim(0, 2.5)
plt.ylim(0, 3)

# 显示图形
plt.tight_layout()
plt.show()

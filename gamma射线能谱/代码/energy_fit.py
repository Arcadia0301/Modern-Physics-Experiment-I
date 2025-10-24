import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from scipy.stats import pearsonr

# ===== 1. 加载中文字体 =====
font_path = '/System/Library/Fonts/STHeiti Medium.ttc'  # macOS 系统字体
my_font = fm.FontProperties(fname=font_path, size=16)
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# ===== 2. 输入实验数据 =====
E_g = np.array([1.084, 3.569, 6.137, 6.956])   # 阈值电压 (V)
E_gamma = np.array([0.184, 0.662, 1.173, 1.332])  # 光子能量 (MeV)

# ===== 3. 拟合能量刻度关系 Eγ = G * Eg + E0 =====
coeffs = np.polyfit(E_g, E_gamma, 1)
G, E0 = coeffs
E_fit = np.poly1d(coeffs)

print(f"拟合结果：Eγ = {G:.4f} * Eg + {E0:.4f}")

# ===== 4. 计算皮尔逊相关系数 r =====
r, p_value = pearsonr(E_gamma, E_fit(E_g))
print(f"皮尔逊相关系数 r^2 = {r**2:.6f}, p值 = {p_value:.4e}")

# ===== 5. 生成拟合曲线 =====
E_g_fit = np.linspace(min(E_g) - 0.2, max(E_g) + 0.2, 200)
E_gamma_fit = E_fit(E_g_fit)

# ===== 6. 绘图 =====
plt.figure(figsize=(8, 6))

# 黑色实心点（实验数据）
plt.scatter(E_g, E_gamma, color='black', s=70, label='测量数据')

# 红色拟合线
plt.plot(E_g_fit, E_gamma_fit, color='red', linewidth=2, label='线性拟合')

# ===== 7. 坐标轴与标签 =====
plt.xlabel('阈值 $E_g$ (V)', fontproperties=my_font, fontsize=18)
plt.ylabel('光子能量 $E_{\\gamma}$ (MeV)', fontproperties=my_font, fontsize=18)

# ===== 8. 图例与显示范围 =====
plt.legend(prop=my_font, fontsize=14)
plt.xlim(0, 7.5)
plt.ylim(bottom=0, top=1.5)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)


plt.tight_layout()
plt.show()
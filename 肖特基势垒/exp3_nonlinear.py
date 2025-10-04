import numpy as np
from scipy.optimize import newton, curve_fit
import matplotlib.pyplot as plt

# =========================
# 实验数据
# =========================
T_list = np.array([289.81, 293.68, 299.58, 303.70, 309.24, 314.56])  # K
I_list = np.array([1.614, 2.423, 3.673, 5.450, 7.951, 11.470]) * 1e-6  # μA -> A

# 使用电压平均值
V_mean = np.mean([160.23, 160.38, 160.10, 160.13, 160.18, 160.26]) * 1e-3  # mV -> V

# 固定参数
Ae = 2.83e-3  # cm^2
n = 1.304
R = 3.1 # Ω

q = 1.602176634e-19
k = 1.380649e-23

# =========================
# 隐式肖特基 I-V 模型（用平均电压）
# =========================
def diode_IV_avgV(T_array, phi_b, Astar):
    I_out = []
    for T_i in T_array:
        Is = Ae * Astar * T_i**2 * np.exp(-q*phi_b/(k*T_i))
        # 定义方程 f(I)=0
        def f(I):
            return I - Is*(np.exp(q*(V_mean - I*R)/(n*k*T_i))-1)
        I0 = Is * np.exp(q * V_mean / (n * k * T_i)-1)  # 固定初值
        try:
            I_sol = newton(f, I0, maxiter=1000, tol=1e-12)
        except RuntimeError:
            # 如果Newton法失败，使用近似解
            I_sol = Is * np.exp(q*V_mean/(n*k*T_i))
        I_out.append(I_sol)
    return np.array(I_out)

# =========================
# 拟合
# =========================
p0 = [0.8, 45]  # 修正初值: phi_b ≈ 0.8 eV, A** ≈ 100 A/cm^2·K^2
popt, pcov = curve_fit(diode_IV_avgV, T_list, I_list, p0=p0, maxfev=5000)
phi_b_fit, Astar_fit = popt
phi_b_err, Astar_err = np.sqrt(np.diag(pcov))

print(f"拟合结果:")
print(f"q*phi_b = {phi_b_fit:.4f} eV ± {phi_b_err:.4f} eV")
print(f"A** = {Astar_fit:.2f} A/cm^2·K^2 ± {Astar_err:.2f} A/cm^2·K^2")

# =========================
# 绘图
# =========================
plt.figure(figsize=(6,5))
plt.scatter(T_list, I_list*1e6, color='black', label='实验数据')  # μA
T_fit = np.linspace(min(T_list), max(T_list), 200)
I_fit = diode_IV_avgV(T_fit, phi_b_fit, Astar_fit)*1e6  # μA
plt.plot(T_fit, I_fit, 'red', label='拟合曲线')
plt.xlabel('T (K)', fontsize=16)
plt.ylabel('I (μA)', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(False)

plt.tight_layout()
plt.show()

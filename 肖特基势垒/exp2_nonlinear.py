import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 常数
q = 1.602e-19  # C
k = 1.381e-23  # J/K
T = 299.81     # K

# 定义模型 (通过牛顿迭代解 I)
def diode_eq(V, I0, n, R):
    I = np.zeros_like(V)
    for j in range(len(V)):
        I_guess = 1e-6
        for _ in range(100):
            f = I_guess - I0*(np.exp(q*(V[j]-I_guess*R)/(n*k*T)) - 1)
            df = 1 - I0*np.exp(q*(V[j]-I_guess*R)/(n*k*T)) * (-q*R/(n*k*T))
            I_guess -= f/df
        I[j] = I_guess
    return I

# 清理文件: 找到第一行包含数字的地方
def load_data(fname):
    lines = []
    with open(fname, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            # 至少两列，且第一列能转成数字
            if len(parts) >= 2:
                try:
                    float(parts[0]); float(parts[1])
                    lines.append(line)
                except ValueError:
                    continue
    return np.loadtxt(lines)

# 读取数据
data = load_data("exp2.txt")
I_exp = data[:,0] * 1e-6  # µA -> A
V_exp = data[:,1] * 1e-3  # mV -> V

# 拟合
popt, pcov = curve_fit(diode_eq, V_exp, I_exp, p0=[1e-12, 1.5, 10])
perr = np.sqrt(np.diag(pcov))

I0, n, R = popt
I0_err, n_err, R_err = perr

print(f"I0 = {I0:.3e} ± {I0_err:.3e} A")
print(f"n  = {n:.3f} ± {n_err:.3f}")
print(f"R  = {R:.3f} ± {R_err:.3f} Ω")

# 绘图
plt.figure(figsize=(6,5))
plt.scatter(V_exp*1e3, I_exp*1e6, label="Data", color="black")  # µA
V_fit = np.linspace(min(V_exp), max(V_exp), 200)
I_fit = diode_eq(V_fit, *popt)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.plot(V_fit*1e3, I_fit*1e6, label="Fit", color="red")

plt.xlabel("V (mV)", fontsize=16)
plt.ylabel("I (µA)", fontsize=16)
plt.tight_layout()
plt.show()

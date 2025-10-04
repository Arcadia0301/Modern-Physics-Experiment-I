import matplotlib.pyplot as plt
import numpy as np

filename = "IV.txt"

I, V, T = [], [], []

# 读取文件
with open(filename, "r") as f:
    for _ in range(2):  # 跳过表头
        f.readline()
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 3:
            try:
                i_val = float(parts[0])
                v_val = float(parts[1])
                t_val = float(parts[2])
                I.append(i_val)
                V.append(v_val)
                T.append(t_val)
            except ValueError:
                continue

I = np.array(I)
V = np.array(V)
T = np.array(T)

# 只选择 V<0 的部分
I_negV = I[V<0]
V_negV = V[V<0]

# 绘图
plt.figure(figsize=(4.5,3.5))
plt.plot(V_negV, I_negV, 'o-', color='red', label='V<0', markersize=6, linewidth=1.5)


plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(False)
plt.tight_layout()
plt.show()

# 温度平均值
if len(T) > 0:
    T_mean = np.mean(T)
    print(f"温度的平均值为: {T_mean:.2f} K")

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

# 分离 V 正负
I_posV = I[V>0]
V_posV = V[V>0]
I_negV = I[V<0]
V_negV = V[V<0]

# 绘图
plt.figure(figsize=(6,5))
plt.plot(V_posV, I_posV, 'o-', color='blue', markersize=4)
plt.plot(V_negV, I_negV, 'o-', color='red', markersize=4)

plt.xlabel("V (mV)")
plt.ylabel("I (μA)")

# 设置坐标轴标签字体大小
plt.xlabel("V (mV)", fontsize=14)
plt.ylabel("I (μA)", fontsize=14)

# 设置刻度字体大小
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.grid(False)
plt.tight_layout()
plt.show()

# 温度平均值
if len(T) > 0:
    T_mean = np.mean(T)
    print(f"温度的平均值为: {T_mean:.2f} K")

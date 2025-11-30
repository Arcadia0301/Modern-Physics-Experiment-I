import numpy as np

# 峰值数据
peak_data = {
    1: (161.79, 459.98), 2: (239.14, 572.40), 3: (316.48, 433.78), 4: (393.82, 512.18),
    5: (467.64, 267.91), 6: (520.38, 104.00), 7: (552.02, 136.05), 8: (762.95, 128.04),
    9: (847.32, 296.26), 10: (917.63, 488.26), 11: (991.46, 464.47), 12: (1068.80, 583.54),
    13: (1142.62, 440.08), 14: (1223.48, 520.43), 15: (1297.31, 273.12), 16: (1350.04, 108.00),
    17: (1381.68, 136.00), 18: (1592.61, 132.34), 19: (1676.98, 300.04), 20: (1747.29, 499.85),
    21: (1821.12, 472.07), 22: (1898.46, 588.39), 23: (1972.29, 443.97), 24: (2049.63, 520.32),
    25: (2098.84, 232.00), 26: (2123.45, 272.03), 27: (2176.19, 108.00), 28: (2183.22, 112.36),
    29: (2204.31, 136.03), 30: (2422.27, 132.02), 31: (2443.36, 116.40), 32: (2499.61, 300.33),
    33: (2573.44, 496.29), 34: (2643.75, 472.15), 35: (2724.61, 588.25), 36: (2794.92, 448.07),
    37: (2875.77, 519.92), 38: (2946.08, 272.01), 39: (3002.33, 108.01), 40: (3033.97, 136.00),
    41: (3237.87, 128.11), 42: (3262.48, 116.40), 43: (3318.73, 296.25), 44: (3392.55, 492.40),
    45: (3466.38, 472.23), 46: (3543.72, 588.38)
}

# 子峰对应关系
subpeak_mapping = {
    1: [8, 18, 30],
    2: [9, 19, 32],
    3: [10, 20, 33],
    4: [11, 21, 34],
    5: [12, 22, 35],  # 参考峰
    6: [13, 23, 36],
    7: [14, 24, 37],
    8: [15, 26, 38],
    9: [17, 29, 40]
}

# 本底信号
background = 48

print(f"扣除本底信号: {background}\n")

# 计算扣除本底后的子峰5平均强度作为归一化基准
subpeak5_y = [peak_data[peak_num][1] - background for peak_num in subpeak_mapping[5]]
subpeak5_avg = np.mean(subpeak5_y)
normalization_factor = 4.0 / subpeak5_avg  # 将子峰5归一化为4

print(f"子峰5扣除本底后平均强度: {subpeak5_avg:.2f}")
print(f"归一化因子: {normalization_factor:.6f}")
print(f"目标: 子峰5强度归一化为 4.0\n")

# 计算扣除本底并归一化后的强度
normalized_results = {}
for subpeak_num, peak_indices in subpeak_mapping.items():
    # 扣除本底信号
    y_values_bg_corrected = [peak_data[peak_num][1] - background for peak_num in peak_indices]
    original_y_values = [peak_data[peak_num][1] for peak_num in peak_indices]

    # 归一化
    normalized_y = [y * normalization_factor for y in y_values_bg_corrected]
    avg_normalized = np.mean(normalized_y)
    std_normalized = np.std(normalized_y)

    normalized_results[subpeak_num] = {
        'original_values': original_y_values,
        'bg_corrected_values': y_values_bg_corrected,
        'normalized_values': normalized_y,
        'average': avg_normalized,
        'std': std_normalized,
        'original_avg': np.mean(original_y_values),
        'bg_corrected_avg': np.mean(y_values_bg_corrected)
    }

# 输出扣除本底并归一化后的结果
print("各子峰扣除本底并归一化强度 (以子峰5强度为4):")
print("子峰序号 | 原始强度 | 扣本底强度 | 归一化强度 | 平均值 | 标准差")
print("-" * 80)
for subpeak_num in sorted(normalized_results.keys()):
    data = normalized_results[subpeak_num]
    orig_vals = [f"{y:6.1f}" for y in data['original_values']]
    bg_vals = [f"{y:6.1f}" for y in data['bg_corrected_values']]
    norm_vals = [f"{y:6.3f}" for y in data['normalized_values']]

    print(
        f"子峰 {subpeak_num}  | {orig_vals[0]} {orig_vals[1]} {orig_vals[2]} | {bg_vals[0]} {bg_vals[1]} {bg_vals[2]} | {norm_vals[0]} {norm_vals[1]} {norm_vals[2]} | {data['average']:6.3f} | {data['std']:5.3f}")

# 验证子峰5的归一化结果
print(f"\n验证子峰5归一化结果:")
print(f"原始强度: {[peak_data[peak_num][1] for peak_num in subpeak_mapping[5]]}")
print(f"扣本底后: {subpeak5_y}")
print(f"归一化后: {[y * normalization_factor for y in subpeak5_y]}")
print(f"归一化后平均值: {np.mean([y * normalization_factor for y in subpeak5_y]):.3f} (应为4.000)")

# 输出归一化后的相对强度
print(f"\n归一化后的相对强度分布:")
print("子峰序号 | 归一化强度 | 相对于子峰5")
print("-" * 40)
for subpeak_num in sorted(normalized_results.keys()):
    data = normalized_results[subpeak_num]
    relative_percent = data['average'] / 4.0 * 100
    print(f"子峰 {subpeak_num}  |   {data['average']:6.3f}   |    {relative_percent:5.1f}%")
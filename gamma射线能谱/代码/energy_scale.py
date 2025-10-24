import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from scipy.signal import find_peaks
from matplotlib import font_manager as fm

# ===== 1. 中文字体 =====
font_path = '/System/Library/Fonts/STHeiti Medium.ttc'
my_font = fm.FontProperties(fname=font_path, size=13)

# ===== 2. 四组数据 =====
data_list = [
    {  # 137Cs 反散射峰
        'E_g': np.array([3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8]),
        'n': np.array([2699, 5161, 11672, 19435, 21174, 11958, 3706]),
        'label': r'$^{137}$Cs 0.184 MeV反散射峰',
        'color_light': '#a6cee3',  # 浅蓝
        'color_dark': '#1f78b4'  # 深蓝
    },
    {  # 137Cs 光电峰
        'E_g': np.array([0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]),
        'n': np.array([5747, 6242, 7113, 7490, 6768, 6172, 5740]),
        'label': r'$^{137}$Cs 0.184 MeV光电峰',
        'color_light': '#b2df8a',  # 浅绿
        'color_dark': '#33a02c'  # 深绿
    },
    {  # 60Co 光电峰 1
        'E_g': np.array([5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4]),
        'n': np.array([5670, 6929, 8273, 9652, 9371, 7286, 4846]),
        'label': r'$^{60}$Co 1.173 MeV光电峰',
        'color_light': '#fb9a99',  # 浅红
        'color_dark': '#e31a1c'  # 深红
    },
    {  # 60Co 光电峰 2
        'E_g': np.array([6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3]),
        'n': np.array([4259, 5655, 6818, 6886, 5443, 3515, 1854]),
        'label': r'$^{60}$Co 1.332 MeV光电峰',
        'color_light': '#fdbf6f',  # 浅橙
        'color_dark': '#ff7f00'  # 深橙
    }
]

# ===== 3. 绘图 =====
plt.figure(figsize=(8, 6))

for data in data_list:
    E_g = data['E_g']
    n = data['n']

    # 升序排序
    sort_idx = np.argsort(E_g)
    E_g = E_g[sort_idx]
    n = n[sort_idx]

    # 样条拟合
    E_smooth = np.linspace(E_g.min(), E_g.max(), 500)
    spline = make_interp_spline(E_g, n, k=3)
    n_smooth = spline(E_smooth)

    # 绘制散点（不在图例中出现）
    plt.scatter(E_g, n, color=data['color_light'], s=40, alpha=1,
                label=None, edgecolors='none', zorder=3)

    # 绘制拟合曲线（在图例中出现）
    plt.plot(E_smooth, n_smooth, color=data['color_dark'], linewidth=2,
             label=data['label'])

    # 找峰值并画灰色虚线，同时输出峰值坐标
    peaks, _ = find_peaks(n_smooth)
    if len(peaks) > 0:
        peak_Es = E_smooth[peaks]
        peak_ns = n_smooth[peaks]
        for E_peak, n_peak in zip(peak_Es, peak_ns):
            plt.axvline(x=E_peak, color='gray', linestyle='--', linewidth=1, alpha=1, dashes=(8, 6))
            print(f"{data['label']} 峰值: E_g = {E_peak:.3f} V, n = {n_peak:.1f}")


# 坐标轴与标题
plt.xlabel('阈值 $E_g$ (V)', fontproperties=my_font, fontsize=18)
plt.ylabel('计数 $n$ (个)', fontproperties=my_font, fontsize=18)

plt.legend(prop=my_font, fontsize=8, loc='upper right')
plt.ylim(top=25000)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
plt.show()
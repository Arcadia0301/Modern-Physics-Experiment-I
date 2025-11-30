import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from scipy.signal import find_peaks

# ----------- Read txt file -----------
filename = "I_5A.txt"  # Replace with your filename
data = np.loadtxt(filename)
x = data[:, 0]
y = data[:, 1]

# ----------- Data sorting -----------
idx = np.argsort(x)
x = x[idx]
y = y[idx]

# ----------- Smooth curve -----------
x_smooth = np.linspace(x.min(), x.max(), 1000)
spline = make_interp_spline(x, y, k=3)  # Cubic spline
y_smooth = spline(x_smooth)

# ----------- Find peaks (maxima only) -----------
# Use height parameter to ensure only peaks above threshold are found
peaks_idx, properties = find_peaks(y_smooth, height=100)  # height=100 ensures y>100

x_peaks = x_smooth[peaks_idx]
y_peaks = y_smooth[peaks_idx]

# Output coordinates
print("Peak coordinates (x, y):")
for i, (xp, yp) in enumerate(zip(x_peaks, y_peaks), start=1):
    print(f"Peak {i}: ({xp:.2f}, {yp:.2f})")

print(f"\nTotal {len(x_peaks)} maxima found")

# ----------- Plotting -----------
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'o', alpha=0.3, label="Raw data", markersize=4)
plt.plot(x_smooth, y_smooth, 'b-', label="Smooth curve", linewidth=1.5)
plt.scatter(x_peaks, y_peaks, color='red', s=50, zorder=5, label="Detected maxima")

# Add labels to peaks
for i, (xp, yp) in enumerate(zip(x_peaks, y_peaks), start=1):
    plt.text(xp, yp + np.max(y_peaks)*0.05, f"{i}", fontsize=10,
             ha='center', va='bottom', color='blue', weight='bold')

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Maxima Detection (y > 100)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
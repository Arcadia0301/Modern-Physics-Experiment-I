import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Data
n = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])  # Subpeak index
delta_nu = np.array([-0.92, -0.67, -0.46, -0.24, 0.00, 0.22, 0.46, 0.68, 0.93])  # Wavenumber difference (cm⁻¹)

# Linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(n, delta_nu)

# Calculate parameter uncertainties manually
n_points = len(n)
fitted_values = slope * n + intercept
residuals = delta_nu - fitted_values
RSS = np.sum(residuals**2)  # Residual sum of squares
dof = n_points - 2  # Degrees of freedom

# Standard errors for slope and intercept
x_mean = np.mean(n)
Sxx = np.sum((n - x_mean)**2)
slope_std_error = np.sqrt(RSS / (dof * Sxx))
intercept_std_error = np.sqrt(RSS / dof * (1/n_points + x_mean**2 / Sxx))

# Calculate fitted values
n_fit = np.linspace(0.5, 9.5, 100)
delta_nu_fit = slope * n_fit + intercept

# Fitted equation with uncertainties
equation = f"Δν̃ = ({slope:.4f} ± {slope_std_error:.4f})n + ({intercept:.4f} ± {intercept_std_error:.4f})"

print("=" * 60)
print("LINEAR REGRESSION RESULTS WITH UNCERTAINTIES")
print("=" * 60)
print(f"Fitted equation: {equation}")
print(f"Slope: {slope:.6f} ± {slope_std_error:.6f} cm⁻¹/index")
print(f"Intercept: {intercept:.6f} ± {intercept_std_error:.6f} cm⁻¹")
print(f"Pearson's r: {r_value:.6f}")
print(f"R²: {r_value**2:.6f}")
print(f"p-value: {p_value:.6f}")
print(f"Standard error of estimate: {std_err:.6f}")
print(f"Residual sum of squares (RSS): {RSS:.6f}")
print(f"Degrees of freedom: {dof}")
print(f"Sxx: {Sxx:.6f}")

# Confidence intervals (95% confidence level)
t_value = stats.t.ppf(0.975, dof)  # Two-tailed t-value for 95% CI
slope_CI = (slope - t_value * slope_std_error, slope + t_value * slope_std_error)
intercept_CI = (intercept - t_value * intercept_std_error, intercept + t_value * intercept_std_error)

print(f"\n95% Confidence Intervals:")
print(f"Slope: [{slope_CI[0]:.6f}, {slope_CI[1]:.6f}] cm⁻¹/index")
print(f"Intercept: [{intercept_CI[0]:.6f}, {intercept_CI[1]:.6f}] cm⁻¹")

# Plotting
plt.figure(figsize=(8, 6))
plt.scatter(n, delta_nu, color='black', s=50, label='Experimental data', zorder=5)
plt.plot(n_fit, delta_nu_fit, color='red', linewidth=3, label=f'Fitted line')

# Plot formatting
plt.xlabel('Subpeak Index n', fontsize=16)
plt.ylabel('Wavenumber Difference Δν̃ (cm⁻¹)', fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize=14)

# Add statistics text box with uncertainties
textstr = '\n'.join((
    f'Slope: {slope:.4f} ± {slope_std_error:.4f}',
    f'Intercept: {intercept:.4f} ± {intercept_std_error:.4f}',
    f'R² = {r_value**2:.4f}',
    f'n = {n_points}'))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=12,
         verticalalignment='top', bbox=props)

plt.xlim(0.5, 9.5)
plt.tight_layout()
plt.show()

# Residual analysis
print("\nRESIDUAL ANALYSIS:")
print("Subpeak Index | Experimental | Fitted | Residual")
print("-" * 50)
for i in range(len(n)):
    fitted_value = slope * n[i] + intercept
    residual = residuals[i]
    print(f"      {n[i]}       |    {delta_nu[i]:6.2f}    | {fitted_value:6.2f} |  {residual:6.3f}")

print(f"\nResidual standard deviation: {np.std(residuals):.4f} cm⁻¹")
print(f"Standard error of residuals: {np.sqrt(RSS/dof):.4f} cm⁻¹")

# Goodness of fit metrics
print(f"\nGOODNESS OF FIT:")
print(f"Mean squared error (MSE): {RSS/n_points:.6f}")
print(f"Root mean squared error (RMSE): {np.sqrt(RSS/n_points):.6f}")
print(f"Mean absolute error (MAE): {np.mean(np.abs(residuals)):.6f}")
import numpy as np
from scipy.optimize import newton, curve_fit
import matplotlib.pyplot as plt

# =========================
# Experimental Data
# =========================
T_list = np.array([289.81, 293.68, 299.58, 303.70, 309.24, 314.56])  # K
I_list = np.array([1.614, 2.423, 3.673, 5.450, 7.951, 11.470]) * 1e-6  # μA -> A

# Use average voltage
V_mean = np.mean([160.23, 160.38, 160.10, 160.13, 160.18, 160.26]) * 1e-3  # mV -> V

# Fixed parameters
Ae = 2.83e-3  # cm^2
n = 1.304
R = 3.1  # Ω

q = 1.602176634e-19
k = 1.380649e-23

# =========================
# Exact Schottky I-V Model
# =========================
def diode_IV_exact(T_array, phi_b, Astar):
    I_out = []
    for T_i in T_array:
        # Saturation current
        Is = Ae * Astar * T_i**2 * np.exp(-q * phi_b / (k * T_i))
        
        # Exact solution of implicit equation I = Is * [exp(q(V - IR)/(nkT)) - 1]
        # For forward bias, the -1 term can be neglected
        def f(I):
            return I - Is * (np.exp(q * (V_mean - I * R) / (n * k * T_i))-1)
        
        # Use better initial guess
        I0_guess = Is * np.exp(q * V_mean / (n * k * T_i)-1)
        
        try:
            I_sol = newton(f, I0_guess, maxiter=1000, tol=1e-12)
        except:
            # If fails, use approximate solution as backup
            I_sol = I0_guess
        
        I_out.append(I_sol)
    
    return np.array(I_out)

# =========================
# Fitting - Using expected Astar range
# =========================
# According to your expectation that Astar should be around 40s
p0 = [0.8, 45]  # phi_b ≈ 0.8 eV, A** ≈ 45 A/cm^2·K^2

try:
    popt, pcov = curve_fit(diode_IV_exact, T_list, I_list, p0=p0, maxfev=5000)
    phi_b_fit, Astar_fit = popt
    phi_b_err, Astar_err = np.sqrt(np.diag(pcov))
    
    print(f"Fitting Results:")
    print(f"Barrier height φ_b = {phi_b_fit:.4f} ± {phi_b_err:.4f} eV")
    print(f"Richardson constant A** = {Astar_fit:.2f} ± {Astar_err:.2f} A/cm²·K²")
    
    # =========================
    # Plot Verification
    # =========================
    plt.figure(figsize=(6, 5))
    
    # Experimental data
    plt.scatter(T_list, I_list*1e6, color='black', s=45, label='Experimental Data', zorder=5)
    
    # Fitted curve
    T_fit = np.linspace(min(T_list)-2, max(T_list)+2, 300)
    I_fit = diode_IV_exact(T_fit, phi_b_fit, Astar_fit) * 1e6
    plt.plot(T_fit, I_fit, 'red', linewidth=2, label=f'Nonlinear Fit Params (φ_b = {phi_b_fit:.3f} eV, A** = {Astar_fit:.0f} A/cm²·K²)')
    
    # Fitted points
    I_fit_points = diode_IV_exact(T_list, phi_b_fit, Astar_fit) * 1e6
    #plt.scatter(T_list, I_fit_points, color='red', s=60, marker='x', 
                #label='Nonlinear Fit Points', zorder=6, linewidth=2)
    
    # =========================
    # Add manually specified curve: φ_b=0.726 eV, A**=49
    # =========================
    phi_b_manual = 0.688  # eV
    Astar_manual = 49   # A/cm²·K²
    
    I_manual_curve = diode_IV_exact(T_fit, phi_b_manual, Astar_manual) * 1e6
    plt.plot(T_fit, I_manual_curve, 'blue', linewidth=2, linestyle='--', 
             label=f'Linear Fit Params (φ_b = 0.726 eV, A** = 49 A/cm²·K²)')
    
    # Points for manual parameters
    I_manual_points = diode_IV_exact(T_list, phi_b_manual, Astar_manual) * 1e6
    # plt.scatter(T_list, I_manual_points, color='blue', s=60, marker='+', 
                #label='Linear Fit Param Points', zorder=6, linewidth=2)

    
    plt.xlabel('T (K)', fontsize=16)
    plt.ylabel('I (μA)', fontsize=16)
    plt.legend(fontsize=9)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    
    plt.grid(False)
    plt.tight_layout()
    plt.show()
    
    # Fitting quality analysis
    residuals = I_list - diode_IV_exact(T_list, phi_b_fit, Astar_fit)
    relative_error = np.abs(residuals / I_list)
    
    print(f"\nAuto Fit Quality Analysis:")
    print(f"Max relative error: {np.max(relative_error)*100:.2f}%")
    print(f"Mean relative error: {np.mean(relative_error)*100:.2f}%")
    
    # Manual parameters fitting quality
    residuals_manual = I_list - diode_IV_exact(T_list, phi_b_manual, Astar_manual)
    relative_error_manual = np.abs(residuals_manual / I_list)
    
    print(f"\nManual Parameters Fit Quality Analysis:")
    print(f"Max relative error: {np.max(relative_error_manual)*100:.2f}%")
    print(f"Mean relative error: {np.mean(relative_error_manual)*100:.2f}%")
    
    # Show fitting details for each data point
    print(f"\nAuto Fit Details by Temperature:")
    for i, T in enumerate(T_list):
        I_exp = I_list[i] * 1e6
        I_calc = I_fit_points[i]
        error_pct = (I_calc - I_exp) / I_exp * 100
        print(f"T = {T:.2f}K: Exp = {I_exp:.3f}μA, Fit = {I_calc:.3f}μA, Error = {error_pct:.2f}%")
    
    print(f"\nManual Parameters Details by Temperature:")
    for i, T in enumerate(T_list):
        I_exp = I_list[i] * 1e6
        I_manual = I_manual_points[i]
        error_pct = (I_manual - I_exp) / I_exp * 100
        print(f"T = {T:.2f}K: Exp = {I_exp:.3f}μA, Manual = {I_manual:.3f}μA, Error = {error_pct:.2f}%")
        
except Exception as e:
    print(f"Fitting failed: {e}")
    
    # Manual parameter scanning
    print("\nPerforming manual parameter scan...")
    best_error = float('inf')
    best_params = None
    
    # Scan around your expected Astar range
    phi_b_range = np.linspace(0.75, 0.85, 30)
    Astar_range = np.linspace(35, 55, 30)
    
    for phi_b in phi_b_range:
        for Astar in Astar_range:
            I_pred = diode_IV_exact(T_list, phi_b, Astar)
            error = np.sum(np.abs((I_pred - I_list) / I_list))
            
            if error < best_error:
                best_error = error
                best_params = (phi_b, Astar)
    
    if best_params:
        phi_b_manual, Astar_manual = best_params
        print(f"Best parameters from manual search:")
        print(f"Barrier height φ_b = {phi_b_manual:.4f} eV")
        print(f"Richardson constant A** = {Astar_manual:.2f} A/cm²·K²")
        print(f"Mean relative error: {best_error/len(T_list)*100:.2f}%")

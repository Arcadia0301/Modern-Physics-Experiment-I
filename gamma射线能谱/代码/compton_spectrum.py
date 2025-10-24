import numpy as np
import matplotlib.pyplot as plt

# Constants
m_e_c2 = 511.0  # keV

# Different alpha values
alphas = [0.5, 1.0, 1.5, 2.0]

theta = np.linspace(1e-4, np.pi-1e-4, 2000)  # scattering angles

plt.figure(figsize=(10,8))

for alpha in alphas:
    E_gamma = alpha * m_e_c2

    # Scattered photon energy
    E_gamma_prime = E_gamma / (1 + alpha * (1 - np.cos(theta)))

    # Compton electron kinetic energy
    E_c = E_gamma - E_gamma_prime

    # Klein-Nishina differential cross-section (a.u.)
    d_sigma_dOmega = (E_gamma_prime/E_gamma)**2 * (
        E_gamma_prime/E_gamma + E_gamma/E_gamma_prime - np.sin(theta)**2
    )

    # Jacobian dΩ/dE_c
    dEcdtheta = E_gamma * alpha * np.sin(theta) / (1 + alpha*(1-np.cos(theta)))**2
    dOmegadE = 2 * np.pi * np.sin(theta) / dEcdtheta

    # Differential cross-section vs E_c
    d_sigma_dE = d_sigma_dOmega * dOmegadE

    # Insert origin (E_c=0, dσ/dE=0)
    E_c_plot = np.insert(E_c, 0, 0)
    d_sigma_plot = np.insert(d_sigma_dE, 0, 0)

    # Plot curve
    line, = plt.plot(E_c_plot, d_sigma_plot, lw=2, label=fr'$\alpha$={alpha:.1f}, $E_\gamma$={E_gamma:.0f} keV')

    # Fill area under the curve with matching color
    plt.fill_between(E_c_plot, 0, d_sigma_plot, color=line.get_color(), alpha=0.2)

    # Compton edge
    E_edge = (2*alpha/(1+2*alpha))*E_gamma
    plt.axvline(E_edge, color='gray', linestyle='--', alpha=0.6)

# Set axes to start from 0
plt.xlim(left=0)
plt.ylim(bottom=0)

# Labels and title with larger font
plt.xlabel("$E_c$ (keV)", fontsize=22)
plt.ylabel("d$\sigma$/d$E_c$ (a.u.)", fontsize=22)


# Increase tick size
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

plt.legend(fontsize=18)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

import numpy as np

from src.topology import (
    compute_lower_band_states,
    compute_link_variables,
    compute_chern_number
)


def analytic_berry_curvature(kx, ky, m):
    dx = np.sin(kx)
    dy = np.sin(ky)
    dz = m + np.cos(kx) + np.cos(ky)

    numerator = (
        np.sin(kx)**2 * np.cos(ky)
        + np.sin(ky)**2 * np.cos(kx)
        + dz * np.cos(kx) * np.cos(ky)
    )

    d_norm = np.sqrt(dx**2 + dy**2 + dz**2)

    return numerator / (2 * d_norm**3)


def convergence_check():
    grid_sizes = [20, 40, 80]
    mass_values = [-3.0, -1.0, 1.0, 3.0]

    print("--- Chern Number Convergence ---")
    print(f"{'N':<8}" + "".join(f"m={m:<10}" for m in mass_values))

    for N in grid_sizes:
        results = []

        for m in mass_values:
            _, _, states = compute_lower_band_states(N, m)

            Ux, Uy = compute_link_variables(states)
            C, _ = compute_chern_number(Ux, Uy)

            results.append(C)

        print(f"{N:<8}" + "".join(f"{C:<14.8f}" for C in results))

    print("\n--- Berry Curvature Convergence (m=-1) ---")

    for N in grid_sizes:
        _, _, states = compute_lower_band_states(N, -1.0)

        Ux, Uy = compute_link_variables(states)
        _, flux = compute_chern_number(Ux, Uy)

        dk = 2 * np.pi / N

        # Plaquette beginning at k = (0, 0)
        i = j = N // 2

        omega_num = flux[i, j] / dk**2

        # Compare with analytic curvature at its center
        omega_exact = analytic_berry_curvature(
            dk / 2, dk / 2, -1.0
        )

        error = abs(omega_num - omega_exact)

        print(
            f"N={N}: numerical={omega_num:.8f}, "
            f"analytic={omega_exact:.8f}, "
            f"error={error:.8e}"
        )


if __name__ == "__main__":
    convergence_check()

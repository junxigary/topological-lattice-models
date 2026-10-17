
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from chern_model import chern_model_hamiltonian


# Project configuration
N = 80
project_root = Path(__file__).resolve().parent.parent
figure_dir = project_root / "figures"
figure_dir.mkdir(exist_ok=True)


# 2D Brillouin zone
k_values = np.linspace(-np.pi, np.pi, N, endpoint=False)
KX, KY = np.meshgrid(k_values, k_values, indexing="ij")


def plot_band_structure(m=-1.0):
    """
    Plot the two energy bands of the QWZ model.
    """

    E_lower = np.zeros((N, N))
    E_upper = np.zeros((N, N))

    for i in range(N):
        for j in range(N):

            kx = KX[i, j]
            ky = KY[i, j]

            H = chern_model_hamiltonian(kx, ky, m)
            energies = np.linalg.eigvalsh(H)

            E_lower[i, j] = energies[0]
            E_upper[i, j] = energies[1]

    gap = np.min(E_upper - E_lower)

    print(f"m = {m}")
    print(f"Minimum bulk gap = {gap:.6f}")

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_surface(KX, KY, E_upper, cmap="autumn", alpha=0.85)
    ax.plot_surface(KX, KY, E_lower, cmap="winter", alpha=0.85)

    ax.set_xlabel(r"$k_x$")
    ax.set_ylabel(r"$k_y$")
    ax.set_zlabel("Energy")
    ax.set_title(f"QWZ Band Structure (m = {m})")

    plt.tight_layout()
    plt.savefig(figure_dir / "qwz_bands_m_minus1.png", dpi=300)


def plot_bulk_gap():
    """
    Scan m and compute the global minimum band gap.
    """

    m_values = np.linspace(-4, 4, 401)
    gaps = []

    for m in m_values:

        dx = np.sin(KX)
        dy = np.sin(KY)
        dz = m + np.cos(KX) + np.cos(KY)

        # Analytical eigenvalues E = +/- |d|
        energies = np.sqrt(dx**2 + dy**2 + dz**2)

        gap = np.min(2 * energies)
        gaps.append(gap)

    gaps = np.array(gaps)

    # Check selected values
    for m_test in [-3, -2, -1, 0, 1, 2, 3]:
        idx = np.argmin(np.abs(m_values - m_test))
        print(f"m = {m_test:2d}, gap = {gaps[idx]:.6f}")

    # Plot
    plt.figure(figsize=(9, 5.5))

    plt.plot(m_values, gaps, linewidth=2,
             label="Numerical bulk gap")

    for mc in [-2, 0, 2]:
        plt.axvline(mc, color="gray", linestyle="--", alpha=0.6)

    plt.scatter([-2, 0, 2], [0, 0, 0],
                color="red", zorder=5,
                label="Gap closing points")

    plt.xlabel("Model parameter m")
    plt.ylabel("Minimum bulk gap")
    plt.title("QWZ Model: Bulk Gap vs. m")

    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(figure_dir / "qwz_bulk_gap.png", dpi=300)


if __name__ == "__main__":

    plot_band_structure(m=-1.0)
    plot_bulk_gap()

    plt.show()


import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from src.strip_geometry import build_strip_hamiltonian


def plot_edge_spectrum(Nx=40, Nk=121, m=-1.0):

    ky_values = np.linspace(-np.pi, np.pi, Nk)

    all_ky = []
    all_energies = []
    all_edge_weights = []

    edge_cells = 6

    for ky in ky_values:

        # Construct strip Hamiltonian
        H = build_strip_hamiltonian(ky, m, Nx)

        # Diagonalize
        energies, eigenvectors = np.linalg.eigh(H)

        # Probability at each x position
        probabilities = np.abs(eigenvectors)**2

        # Sum over the two internal components
        probabilities = probabilities.reshape(Nx, 2, 2*Nx)
        probabilities_x = np.sum(probabilities, axis=1)

        # Probability concentrated near both boundaries
        left_weight = np.sum(
            probabilities_x[:edge_cells, :], axis=0
        )

        right_weight = np.sum(
            probabilities_x[-edge_cells:, :], axis=0
        )

        edge_weight = left_weight + right_weight

        all_ky.extend([ky] * len(energies))
        all_energies.extend(energies)
        all_edge_weights.extend(edge_weight)

    all_ky = np.array(all_ky)
    all_energies = np.array(all_energies)
    all_edge_weights = np.array(all_edge_weights)

    # Plot all energy eigenvalues
    fig, ax = plt.subplots(figsize=(8, 6))

    scatter = ax.scatter(
        all_ky,
        all_energies,
        c=all_edge_weights,
        cmap="viridis",
        vmin=0,
        vmax=1,
        s=6,
        rasterized=True
    )

    fig.colorbar(
        scatter,
        ax=ax,
        label="Edge probability weight"
    )

    ax.set_xlabel(r"$k_y$")
    ax.set_ylabel("Energy E")
    ax.set_title(f"QWZ Strip Edge Spectrum (m={m})")

    ax.set_xlim(-np.pi, np.pi)
    ax.set_xticks(
        [-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
        [r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"]
    )

    ax.grid(alpha=0.2)

    output = Path("figures")
    output.mkdir(exist_ok=True)

    fig.savefig(
        output / f"qwz_edge_spectrum_m{m}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()




if __name__ == "__main__":
    plot_edge_spectrum(Nx=40, Nk=121, m=-1.0)

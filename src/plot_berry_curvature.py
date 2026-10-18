
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from src.topology import (
    compute_lower_band_states,
    compute_link_variables,
    compute_chern_number,
)


def plot_berry_curvature(N, m):

    # Step 1: Compute lower-band eigenvectors
    k_grid, energies, states = compute_lower_band_states(N, m)

    # Step 2: Compute link variables
    Ux, Uy = compute_link_variables(states)

    # Step 3: Compute Berry flux and Chern number
    C, berry_flux = compute_chern_number(Ux, Uy)

    # Step 4: Convert Berry flux to curvature
    dk = 2 * np.pi / N
    berry_curvature = berry_flux / dk**2

    # Step 5: Plot
    fig, ax = plt.subplots(figsize=(7, 6))

    image = ax.imshow(
        berry_curvature.T,
        origin="lower",
        extent=[-np.pi, np.pi, -np.pi, np.pi],
        cmap="RdBu_r",
        aspect="equal"
    )

    fig.colorbar(image, ax=ax, label="Berry curvature")

    ax.set_xlabel(r"$k_x$")
    ax.set_ylabel(r"$k_y$")
    ax.set_title(f"Berry Curvature (m={m}, C={C:.2f})")

    # Save figure
    output = Path("figures")
    output.mkdir(exist_ok=True)

    fig.savefig(
        output / f"berry_curvature_m{m}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


if __name__ == "__main__":
    plot_berry_curvature(N=80, m=-1.0)
    plot_berry_curvature(N=80, m=3.0)


import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from src.topology import (
    compute_lower_band_states,
    compute_link_variables,
    compute_chern_number
)


def plot_chern_phase_diagram(N=40):

    # Step 1: Define mass parameter range
    m_values = np.linspace(-3, 3, 121)
    chern_values = []

    # Gap-closing points
    critical_points = [-2.0, 0.0, 2.0]

    # Step 2: Compute Chern number for each m
    for m in m_values:

        if any(np.isclose(m, mc) for mc in critical_points):
            chern_values.append(np.nan)
            continue

        _, _, states = compute_lower_band_states(N, m)

        Ux, Uy = compute_link_variables(states)

        C, _ = compute_chern_number(Ux, Uy)

        chern_values.append(C)

    chern_values = np.array(chern_values)

    # Step 3: Plot the phase diagram
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        m_values,
        chern_values,
        ".-",
        color="navy",
        markersize=4,
        linewidth=1.5,
        label="Numerical Chern number"
    )

    for mc in critical_points:
        ax.axvline(
            mc,
            color="red",
            linestyle="--",
            alpha=0.6
        )

    ax.set_xlabel("Mass parameter m")
    ax.set_ylabel("Chern number C")
    ax.set_title("QWZ Model: Chern Number Phase Diagram")

    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_yticks([-1, 0, 1])
    ax.set_ylim(-1.3, 1.3)

    ax.grid(alpha=0.3)
    ax.legend()

    # Step 4: Save figure
    output = Path("figures")
    output.mkdir(exist_ok=True)

    fig.savefig(
        output / "chern_phase_diagram.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    # Step 5: Print selected results
    print("\n--- Chern Number Verification ---")

    for m in [-3.0, -1.0, 1.0, 3.0]:
        idx = np.argmin(np.abs(m_values - m))
        print(f"m = {m:+.1f}, C = {chern_values[idx]:.6f}")


if __name__ == "__main__":
    plot_chern_phase_diagram(N=40)

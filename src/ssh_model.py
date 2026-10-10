
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


FIGURE_DIR = Path(__file__).resolve().parent.parent / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def ssh_bloch_hamiltonian(k, t1, t2):
    H = np.array([
        [0, -(t1 + t2 * np.exp(-1j * k))],
        [-(t1 + t2 * np.exp(1j * k)), 0]
    ], dtype=complex)

    return H


def analytical_energies(k, t1, t2):
    energy = np.sqrt(
        t1**2 + t2**2 + 2 * t1 * t2 * np.cos(k)
    )

    return np.array([-energy, energy])


def compute_bands(k_values, t1, t2):
    energies = []

    for k in k_values:
        H = ssh_bloch_hamiltonian(k, t1, t2)
        eigenvalues, _ = np.linalg.eigh(H)
        energies.append(eigenvalues)

    return np.array(energies)


def plot_ssh_bands(k_values):
    ratios = [0.2, 1.0, 2.0]
    t2 = 1.0

    fig, axes = plt.subplots(
        1, 3, figsize=(15, 4.5),
        sharey=True
    )

    for ax, ratio in zip(axes, ratios):
        t1 = ratio * t2
        energies = compute_bands(k_values, t1, t2)

        ax.plot(
            k_values,
            energies[:, 0],
            label="Lower band",
            color="royalblue",
            linewidth=2
        )

        ax.plot(
            k_values,
            energies[:, 1],
            label="Upper band",
            color="darkorange",
            linewidth=2
        )

        ax.axhline(
            0,
            color="gray",
            linestyle="--",
            linewidth=0.8
        )

        ax.set_title(f"$t_1/t_2 = {ratio:.1f}$")
        ax.set_xlabel("$k$")
        ax.set_ylabel("Energy")

        ax.set_xticks([-np.pi, 0, np.pi])
        ax.set_xticklabels(["$-\\pi$", "0", "$\\pi$"])

        ax.set_ylim(-3.2, 3.2)

        ax.grid(alpha=0.3)
        ax.legend()

    fig.suptitle(
        "SSH Model: Bulk Band Structure",
        fontsize=14
    )

    fig.tight_layout()

    fig.savefig(
        FIGURE_DIR / "ssh_band_structures.png",
        dpi=300
    )

    plt.show()
    plt.close(fig)


def minimum_band_gap(t1, t2, k_values):
    energies = compute_bands(k_values, t1, t2)

    gaps = energies[:, 1] - energies[:, 0]

    return np.min(gaps)


def plot_gap_vs_ratio(k_values):
    t2 = 1.0
    ratios = np.linspace(0.0, 2.0, 201)

    numerical_gaps = []
    analytical_gaps = []

    for ratio in ratios:
        t1 = ratio * t2

        numerical_gap = minimum_band_gap(
            t1, t2, k_values
        )

        analytical_gap = 2 * abs(t1 - t2)

        numerical_gaps.append(numerical_gap)
        analytical_gaps.append(analytical_gap)

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(
        ratios,
        numerical_gaps,
        label="Numerical gap",
        color="royalblue",
        linewidth=2
    )

    ax.plot(
        ratios,
        analytical_gaps,
        "--",
        label="Analytical gap",
        color="darkorange",
        linewidth=1.5
    )

    ax.axvline(
        1.0,
        color="red",
        linestyle=":",
        label="Gap closing: $t_1=t_2$"
    )

    ax.set_xlabel("$t_1/t_2$")
    ax.set_ylabel("Minimum direct band gap")

    ax.set_title(
        "SSH Model: Band Gap Closing and Reopening"
    )

    ax.legend()
    ax.grid(alpha=0.3)

    fig.tight_layout()

    fig.savefig(
        FIGURE_DIR / "ssh_gap_vs_ratio.png",
        dpi=300
    )

    plt.show()
    plt.close(fig)


def verify_ssh_model(k_values):
    parameter_sets = [
        (0.2, 1.0),
        (1.0, 1.0),
        (2.0, 1.0)
    ]

    for t1, t2 in parameter_sets:
        maximum_error = 0.0
        maximum_hermiticity_error = 0.0

        for k in k_values:
            H = ssh_bloch_hamiltonian(k, t1, t2)

            numerical, _ = np.linalg.eigh(H)
            analytical = analytical_energies(k, t1, t2)

            error = np.max(
                np.abs(numerical - analytical)
            )

            hermiticity_error = np.max(
                np.abs(H - H.conj().T)
            )

            maximum_error = max(
                maximum_error, error
            )

            maximum_hermiticity_error = max(
                maximum_hermiticity_error,
                hermiticity_error
            )

        numerical_gap = minimum_band_gap(
            t1, t2, k_values
        )

        analytical_gap = 2 * abs(t1 - t2)

        print(f"\nt1/t2 = {t1/t2:.2f}")

        print(
            "Maximum eigenvalue error: "
            f"{maximum_error:.3e}"
        )

        print(
            "Maximum Hermiticity error: "
            f"{maximum_hermiticity_error:.3e}"
        )

        print(
            "Minimum numerical gap: "
            f"{numerical_gap:.6f}"
        )

        print(
            "Analytical gap: "
            f"{analytical_gap:.6f}"
        )

        assert maximum_error < 1e-10
        assert maximum_hermiticity_error < 1e-10

        assert np.isclose(
            numerical_gap,
            analytical_gap,
            atol=1e-10
        )


if __name__ == "__main__":
    k_values = np.linspace(
        -np.pi, np.pi, 401
    )

    print("=== SSH Bloch Hamiltonian ===")

    H = ssh_bloch_hamiltonian(
        k=0,
        t1=1.0,
        t2=2.0
    )

    print(H)

    eigenvalues, eigenvectors = np.linalg.eigh(H)

    print("\nEigenvalues:")
    print(eigenvalues)

    print("\nEigenvectors:")
    print(eigenvectors)

    print("\n=== Numerical Verification ===")
    verify_ssh_model(k_values)

    print("\nGenerating band structure figures...")
    plot_ssh_bands(k_values)

    print("\nGenerating band gap figure...")
    plot_gap_vs_ratio(k_values)

    print("\nWeek 3 SSH bulk calculations completed.")

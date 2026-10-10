
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



def ssh_open_hamiltonian(N, t1, t2):
    H = np.zeros((2 * N, 2 * N), dtype=float)

    for i in range(2 * N - 1):
        hopping = t1 if i % 2 == 0 else t2

        H[i, i + 1] = -hopping
        H[i + 1, i] = -hopping

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


def verify_ssh_edge_states():
    N = 40
    t2 = 1.0

    for t1 in [0.5, 1.5]:
        H = ssh_open_hamiltonian(N, t1, t2)

        energies, states = np.linalg.eigh(H)

        indices = np.argsort(np.abs(energies))[:2]

        print(f"\nt1/t2 = {t1/t2:.2f}")
        print("Two eigenvalues closest to zero:")
        print(energies[indices])

        print("Hermiticity check:")
        print(np.allclose(H, H.conj().T))


def plot_ssh_edge_states():
    N = 40
    t1 = 0.5
    t2 = 1.0

    H = ssh_open_hamiltonian(N, t1, t2)

    energies, states = np.linalg.eigh(H)

    indices = np.argsort(np.abs(energies))[:2]

    site_indices = np.arange(1, 2 * N + 1)

    fig, axes = plt.subplots(
        2, 1, figsize=(9, 6),
        sharex=True
    )

    for ax, j in zip(axes, indices):
        probability = np.abs(states[:, j]) ** 2

        ax.bar(
            site_indices,
            probability,
            width=0.8,
            color="royalblue"
        )

        ax.set_ylabel(r"$|\psi_n|^2$")
        ax.set_title(
            f"Near-zero state: E = {energies[j]:.3e}"
        )
        ax.grid(alpha=0.3)

    axes[-1].set_xlabel("Site index")

    fig.suptitle(
        "SSH Model: Near-Zero-Energy Edge States"
    )

    fig.tight_layout()

    fig.savefig(
        FIGURE_DIR / "ssh_edge_states.png",
        dpi=300
    )

    plt.show()
    plt.close(fig)



def plot_localized_edge_states():
    N = 40
    t1 = 0.5
    t2 = 1.0

    H = ssh_open_hamiltonian(N, t1, t2)

    energies, states = np.linalg.eigh(H)

    indices = np.argsort(np.abs(energies))[:2]

    V = states[:, indices]

    positions = np.arange(1, 2 * N + 1)

    X_edge = V.conj().T @ (positions[:, None] * V)

    _, rotation = np.linalg.eigh(X_edge)

    localized_states = V @ rotation

    left_state = localized_states[:, 0]
    right_state = localized_states[:, 1]

    fig, axes = plt.subplots(
        2, 1, figsize=(9, 6),
        sharex=True
    )

    for ax, psi, title in zip(
        axes,
        [left_state, right_state],
        ["Left Edge State", "Right Edge State"]
    ):
        probability = np.abs(psi) ** 2

        ax.bar(
            positions,
            probability,
            width=0.8,
            color="royalblue"
        )

        ax.set_title(title)
        ax.set_ylabel(r"$|\psi_n|^2$")
        ax.grid(alpha=0.3)

        average_position = np.sum(
            positions * probability
        )

        print(
            f"{title}: <X> = {average_position:.4f}"
        )

        print(
            f"Normalization = {np.sum(probability):.6f}"
        )

    axes[-1].set_xlabel("Site index")

    fig.suptitle(
        "SSH Model: Localized Edge Modes"
    )

    fig.tight_layout()

    fig.savefig(
        FIGURE_DIR / "ssh_localized_edge_states.png",
        dpi=300
    )

    plt.show()
    plt.close(fig)


def calculate_winding_number(t1, t2):
    if np.isclose(abs(t1), abs(t2)):
        raise ValueError("Winding number undefined at gap closing.")

    k_values = np.linspace(-np.pi, np.pi, 1001)

    q = t1 + t2 * np.exp(1j * k_values)

    phases = np.angle(q)
    unwrapped_phases = np.unwrap(phases)

    winding = (
        unwrapped_phases[-1] - unwrapped_phases[0]
    ) / (2 * np.pi)

    return winding


def plot_ssh_winding():
    k_values = np.linspace(-np.pi, np.pi, 1001)

    ratios = [0.5, 1.0, 1.5]
    t2 = 1.0

    fig, axes = plt.subplots(
        1, 3, figsize=(15, 4.5)
    )

    for ax, ratio in zip(axes, ratios):
        t1 = ratio * t2

        dx = t1 + t2 * np.cos(k_values)
        dy = t2 * np.sin(k_values)

        ax.plot(
            dx, dy,
            color="royalblue",
            linewidth=2
        )

        ax.scatter(
            0, 0,
            color="red",
            s=60,
            label="Origin",
            zorder=5
        )

        ax.scatter(
            t1, 0,
            color="darkorange",
            marker="x",
            s=70,
            label="Circle center"
        )

        for j in [150, 450, 750]:
            ax.annotate(
                "",
                xy=(dx[j + 1], dy[j + 1]),
                xytext=(dx[j - 10], dy[j - 10]),
                arrowprops=dict(
                    arrowstyle="->",
                    color="royalblue",
                    lw=2
                )
            )

        if np.isclose(t1, t2):
            title = "Gap closing: winding undefined"
        else:
            winding = calculate_winding_number(t1, t2)
            title = f"Winding number = {winding:.0f}"

        ax.set_title(
            f"$t_1/t_2={ratio:.1f}$\n{title}"
        )

        ax.axhline(0, color="gray", linewidth=0.7)
        ax.axvline(0, color="gray", linewidth=0.7)

        ax.set_xlabel("$d_x(k)$")
        ax.set_ylabel("$d_y(k)$")

        ax.set_aspect("equal")
        ax.set_xlim(-1.7, 2.7)
        ax.set_ylim(-1.4, 1.4)

        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)

    fig.suptitle(
        "SSH Model: Winding Number and Topological Phases",
        fontsize=14
    )

    fig.tight_layout()

    fig.savefig(
        FIGURE_DIR / "ssh_winding.png",
        dpi=300
    )

    plt.show()
    plt.close(fig)


def plot_ssh_obc_spectrum():
    N = 40
    t2 = 1.0
    ratios = np.linspace(0.0, 2.0, 161)

    edge_sites = 6
    edge_threshold = 0.25

    all_energies = []
    all_weights = []

    for ratio in ratios:
        t1 = ratio * t2

        H = ssh_open_hamiltonian(N, t1, t2)
        energies, states = np.linalg.eigh(H)

        probability = np.abs(states) ** 2

        weights = (
            np.sum(probability[:edge_sites, :], axis=0)
            + np.sum(probability[-edge_sites:, :], axis=0)
        )

        all_energies.append(energies)
        all_weights.append(weights)

    all_energies = np.array(all_energies)
    all_weights = np.array(all_weights)

    gap_half = t2 * np.abs(ratios - 1.0)

    within_gap = (
        np.abs(all_energies)
        < gap_half[:, None] - 1e-9
    )

    edge_mask = (
        (ratios[:, None] < 1.0)
        & within_gap
        & (all_weights > edge_threshold)
    )

    x_all = np.repeat(ratios, 2 * N)
    y_all = all_energies.ravel()

    x_edge = np.broadcast_to(
        ratios[:, None],
        all_energies.shape
    )[edge_mask]

    y_edge = all_energies[edge_mask]
    w_edge = all_weights[edge_mask]

    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(9, 9),
        gridspec_kw={"height_ratios": [1, 1.1]}
    )

    for ax in [ax1, ax2]:
        ax.scatter(
            x_all,
            y_all,
            color="#929BA8",
            s=1.0,
            alpha=0.19,
            rasterized=True,
            linewidths=0,
            label="All OBC eigenenergies"
        )

        scatter = ax.scatter(
            x_edge,
            y_edge,
            c=w_edge,
            cmap="plasma",
            vmin=0,
            vmax=1,
            s=18,
            linewidths=0,
            zorder=5,
            label="In-gap edge-localized states"
        )

        ax.plot(
            ratios,
            gap_half,
            "--",
            color="black",
            linewidth=1.1,
            label="Bulk band edges"
        )

        ax.plot(
            ratios,
            -gap_half,
            "--",
            color="black",
            linewidth=1.1
        )

        ax.axvline(
            1.0,
            color="firebrick",
            linestyle=":",
            linewidth=1,
            label="Bulk transition"
        )

        ax.axhline(
            0,
            color="gray",
            linestyle=":",
            linewidth=0.8
        )

        ax.set_ylabel("Energy (t2 = 1)")
        ax.grid(alpha=0.15)

    ax1.set_title(
        "SSH Open-Chain Spectrum (80 Sites)"
    )
    ax1.set_xlim(0, 2)
    ax1.set_ylim(-3.15, 3.15)
    ax1.legend(loc="upper left", fontsize=8)

    ax2.set_title("Zoom Near Zero Energy")
    ax2.set_xlim(0, 1.2)
    ax2.set_ylim(-0.35, 0.35)
    ax2.set_xlabel(r"$t_1/t_2$")

    cbar = fig.colorbar(
        scatter,
        ax=[ax1, ax2],
        pad=0.025,
        fraction=0.025
    )

    cbar.set_label(
        "Edge probability weight (left/right 6 sites)"
    )

    fig.subplots_adjust(
        hspace=0.28,
        right=0.87,
        left=0.1,
        top=0.94,
        bottom=0.09
    )

    fig.savefig(
        FIGURE_DIR / "ssh_obc_spectrum_edge_colored.png",
        dpi=300
    )

    plt.show()
    plt.close(fig)


def verify_edge_splitting():
    N = 40
    t2 = 1.0

    ratios = [0.5, 0.7, 0.8, 0.9]

    print("\n=== Edge-State Energy Splitting ===")

    for rho in ratios:
        t1 = rho * t2

        H = ssh_open_hamiltonian(N, t1, t2)
        energies = np.linalg.eigvalsh(H)

        numerical = np.min(np.abs(energies))

        analytical = (
            t2 * (1 - rho**2) * rho**N
            / (1 - rho**(2*N))
        )

        relative_error = (
            abs(numerical - analytical)
            / analytical
        )

        print(
            f"ratio={rho:.1f} | "
            f"numerical={numerical:.6e} | "
            f"approx={analytical:.6e} | "
            f"relative error={relative_error:.3e}"
        )







if __name__ == "__main__":

    def edge_weight(state, edge_sites=6):
        probability = np.abs(state) ** 2

        left_weight = np.sum(probability[:edge_sites])
        right_weight = np.sum(probability[-edge_sites:])

        return left_weight + right_weight
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

    print("\n=== Week 4: SSH Edge States ===")

    verify_ssh_edge_states()

    print("\nGenerating edge-state figures...")
    plot_ssh_edge_states()

    print("\n=== Localized SSH Edge States ===")

    plot_localized_edge_states()

    print("\n=== SSH Winding Numbers ===")

    for ratio in [0.5, 1.5]:
        winding = calculate_winding_number(ratio, 1.0)
        print(f"t1/t2 = {ratio:.1f}, winding = {winding:.6f}")

    print("\nGenerating SSH winding trajectories...")
    plot_ssh_winding()

    print("\nGenerating OBC energy spectrum...")
    plot_ssh_obc_spectrum()

    verify_edge_splitting()

    print("\nWeek 4 edge-state calculations completed.")

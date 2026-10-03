import os
import numpy as np
import matplotlib.pyplot as plt


def build_open_chain(N, t=1.0, epsilon=0.0):
    H = np.zeros((N, N))

    for n in range(N):
        H[n, n] = epsilon

    for n in range(N - 1):
        H[n, n + 1] = -t
        H[n + 1, n] = -t

    return H

def build_periodic_chain(N, t=1.0, epsilon=0.0):
    H = build_open_chain(N, t, epsilon)

    H[0, N - 1] = -t
    H[N - 1, 0] = -t

    return H


def solve_chain(H):
    energies, states = np.linalg.eigh(H)
    return energies, states


def analytical_open_chain_energies(N, t=1.0, epsilon=0.0):
    j = np.arange(1, N + 1)

    energies = (
        epsilon
        - 2 * t * np.cos(j * np.pi / (N + 1))
    )

    return energies

def analytical_periodic_chain_energies(N, t=1.0, epsilon=0.0, a=1.0):
    m = np.arange(N)
    k = 2 * np.pi * m / (N * a)

    k = (k + np.pi / a) % (2 * np.pi / a) - np.pi / a

    energies = epsilon - 2 * t * np.cos(k * a)

    return k, energies


def save_finite_chain_figures():
    sizes = [5, 20, 100]
    t = 1.0
    a = 1.0

    os.makedirs("figures", exist_ok=True)

    k_cont = np.linspace(0, np.pi / a, 500)
    E_cont = -2 * t * np.cos(k_cont * a)

    for N in sizes:
        H = build_open_chain(N, t)
        energies, _ = solve_chain(H)

        j = np.arange(1, N + 1)
        k = j * np.pi / ((N + 1) * a)

        plt.figure()

        plt.plot(
            k_cont,
            E_cont,
            label="Analytical band"
        )

        plt.plot(
            k,
            energies,
            "o",
            markersize=5,
            label=f"N = {N}"
        )

        plt.xlabel("k")
        plt.ylabel("Energy")
        plt.title(f"Open Tight-Binding Chain: N = {N}")
        plt.legend()

        filename = f"figures/open_chain_N{N}.png"

        plt.savefig(
            filename,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print(f"Saved {filename}")

def save_periodic_band_figure(N=20, t=1.0, a=1.0):
    os.makedirs("figures", exist_ok=True)

    # Continuous band
    k_cont = np.linspace(-np.pi / a, np.pi / a, 500)
    E_cont = -2 * t * np.cos(k_cont * a)

    # Allowed discrete k values
    m = np.arange(N)
    k = 2 * np.pi * m / (N * a)

    # Fold into first Brillouin zone
    k = (k + np.pi / a) % (2 * np.pi / a) - np.pi / a

    # Energies at allowed k
    E_k = -2 * t * np.cos(k * a)

    # Sort by k for cleaner plotting
    order = np.argsort(k)
    k = k[order]
    E_k = E_k[order]

    plt.figure()

    plt.plot(
        k_cont,
        E_cont,
        label="Continuous band"
    )

    plt.plot(
        k,
        E_k,
        "o",
        markersize=5,
        label=f"Allowed k values, N = {N}"
    )

    plt.xlabel("k")
    plt.ylabel("Energy")
    plt.title("Periodic Tight-Binding Chain")
    plt.legend()

    filename = f"figures/periodic_chain_N{N}.png"

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved {filename}")

def save_hopping_comparison_figure():
    os.makedirs("figures", exist_ok=True)

    a = 1.0
    k = np.linspace(-np.pi / a, np.pi / a, 500)

    t_values = [0.5, 1.0, 2.0]

    plt.figure()

    for t in t_values:
        E = -2 * t * np.cos(k * a)

        plt.plot(
            k,
            E,
            label=f"t = {t}"
        )

    plt.xlabel("k")
    plt.ylabel("Energy")
    plt.title("Effect of Hopping Strength on Band Structure")
    plt.legend()

    filename = "figures/hopping_strength_comparison.png"

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved {filename}")

def save_lattice_spacing_comparison_figure():
    os.makedirs("figures", exist_ok=True)

    t = 1.0
    a_values = [0.5, 1.0, 2.0]

    plt.figure()

    for a in a_values:
        k = np.linspace(
            -np.pi / a,
            np.pi / a,
            500
        )

        E = -2 * t * np.cos(k * a)

        plt.plot(
            k,
            E,
            label=f"a = {a}"
        )

    plt.xlabel("k")
    plt.ylabel("Energy")
    plt.title("Effect of Lattice Spacing on Band Structure")
    plt.legend()

    filename = "figures/lattice_spacing_comparison.png"

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved {filename}")


if __name__ == "__main__":
    N = 5
    t = 1.0
    epsilon = 0.0

    H = build_open_chain(N, t, epsilon)
    energies, states = solve_chain(H)
    analytical_energies = analytical_open_chain_energies(
        N,
        t,
        epsilon
    )

    print("Hamiltonian:")
    print(H)

    print("\nNumerical energies:")
    print(energies)

    print("\nAnalytical energies:")
    print(analytical_energies)

    print("\nGround-state eigenvector:")
    print(states[:, 0])

    print("\nCheck H psi = E psi:")
    psi0 = states[:, 0]
    E0 = energies[0]

    print("H psi:")
    print(H @ psi0)

    print("E psi:")
    print(E0 * psi0)

    H_periodic = build_periodic_chain(N, t, epsilon)

    print("\nPeriodic-chain Hamiltonian:")
    print(H_periodic)

    H_periodic = build_periodic_chain(N, t, epsilon)
    periodic_energies, periodic_states = solve_chain(H_periodic)

    k_periodic, analytical_periodic_energies = (
    analytical_periodic_chain_energies(
        N,
        t,
        epsilon
    )
)

    print("\nPeriodic numerical energies:")
    print(periodic_energies)

    print("\nAllowed k values in first Brillouin zone:")
    print(np.sort(k_periodic))

    print("\nPeriodic analytical energies:")
    print(np.sort(analytical_periodic_energies))

    print("\nNumerical and analytical energies agree:")
    print(
    np.allclose(
        periodic_energies,
        np.sort(analytical_periodic_energies)
    )
)

    #save_finite_chain_figures()
    save_periodic_band_figure()
    save_hopping_comparison_figure()
    save_lattice_spacing_comparison_figure()
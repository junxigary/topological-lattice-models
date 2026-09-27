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

    save_finite_chain_figures()
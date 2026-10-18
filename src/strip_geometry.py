
import numpy as np


def build_strip_hamiltonian(ky, m, Nx=40):

    # Pauli matrices
    sigma_x = np.array([
        [0, 1],
        [1, 0]
    ], dtype=complex)

    sigma_y = np.array([
        [0, -1j],
        [1j, 0]
    ], dtype=complex)

    sigma_z = np.array([
        [1, 0],
        [0, -1]
    ], dtype=complex)

    # Onsite block
    A = (
        np.sin(ky) * sigma_y
        + (m + np.cos(ky)) * sigma_z
    )

    # Nearest-neighbor hopping block
    T = (sigma_z - 1j * sigma_x) / 2

    # Full strip Hamiltonian
    H = np.zeros((2 * Nx, 2 * Nx), dtype=complex)

    for x in range(Nx):

        start = 2 * x
        H[start:start+2, start:start+2] = A

        if x < Nx - 1:
            next_start = 2 * (x + 1)

            H[start:start+2, next_start:next_start+2] = T

            H[next_start:next_start+2, start:start+2] = T.conj().T

    return H


if __name__ == "__main__":

    Nx = 40
    ky = 0.0
    m = -1.0

    H = build_strip_hamiltonian(ky, m, Nx)

    print("Hamiltonian shape:", H.shape)

    print("Hermitian:",
          np.allclose(H, H.conj().T))

    energies, eigenvectors = np.linalg.eigh(H)

    print("Minimum absolute energy:",
          np.min(np.abs(energies)))

    print("Number of near-zero states:",
          np.sum(np.abs(energies) < 1e-8))

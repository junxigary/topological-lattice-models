
import numpy as np


def chern_model_hamiltonian(kx, ky, m):
    """
    Qi-Wu-Zhang model Bloch Hamiltonian.

    Parameters
    ----------
    kx, ky : float
        Crystal momenta.
    m : float
        Model parameter.

    Returns
    -------
    H : np.ndarray
        2x2 Hermitian Hamiltonian.
    """

    dx = np.sin(kx)
    dy = np.sin(ky)
    dz = m + np.cos(kx) + np.cos(ky)

    H = np.array([
        [dz, dx - 1j * dy],
        [dx + 1j * dy, -dz]
    ], dtype=complex)

    return H


if __name__ == "__main__":

    # Test at a generic momentum point
    kx = 0.7
    ky = 1.2
    m = -1.0

    H = chern_model_hamiltonian(kx, ky, m)

    # Check 1: Hermiticity
    assert np.allclose(H, H.conj().T)
    print("Hermiticity: PASSED")

    # Check 2: Numerical vs analytical eigenvalues
    numerical = np.linalg.eigvalsh(H)

    dx = np.sin(kx)
    dy = np.sin(ky)
    dz = m + np.cos(kx) + np.cos(ky)

    energy = np.sqrt(dx**2 + dy**2 + dz**2)
    analytical = np.array([-energy, energy])

    assert np.allclose(numerical, analytical)
    print("Eigenvalue comparison: PASSED")

    print("Numerical:", numerical)
    print("Analytical:", analytical)


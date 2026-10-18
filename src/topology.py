
import numpy as np
from src.chern_model import chern_model_hamiltonian


def compute_lower_band_states(N, m):
    # Step 1: Discretize the Brillouin zone
    k_grid = np.linspace(
        -np.pi, np.pi, N, endpoint=False
    )

    # Step 2: Initialize arrays
    lower_states = np.zeros((N, N, 2), dtype=complex)
    lower_energies = np.zeros((N, N))

    # Step 3: Diagonalize H(kx, ky) at every k point
    for i, kx in enumerate(k_grid):
        for j, ky in enumerate(k_grid):
            H = chern_model_hamiltonian(kx, ky, m)

            eigenvalues, eigenvectors = np.linalg.eigh(H)

            lower_energies[i, j] = eigenvalues[0]
            lower_states[i, j] = eigenvectors[:, 0]

    return k_grid, lower_energies, lower_states


def compute_link_variables(lower_states):
    N = lower_states.shape[0]

    Ux = np.zeros((N, N), dtype=complex)
    Uy = np.zeros((N, N), dtype=complex)

    for i in range(N):
        for j in range(N):
            # Current eigenvector
            u = lower_states[i, j]

            # Neighboring eigenvectors (periodic boundaries)
            u_x = lower_states[(i + 1) % N, j]
            u_y = lower_states[i, (j + 1) % N]

            # Overlaps
            overlap_x = np.vdot(u, u_x)
            overlap_y = np.vdot(u, u_y)

            # Check for vanishing overlaps
            if abs(overlap_x) < 1e-12 or abs(overlap_y) < 1e-12:
                raise ValueError("Overlap too small. Try a finer grid.")

            # Normalize to unit complex numbers
            Ux[i, j] = overlap_x / abs(overlap_x)
            Uy[i, j] = overlap_y / abs(overlap_y)

    return Ux, Uy


def compute_chern_number(Ux, Uy):
    N = Ux.shape[0]

    berry_flux = np.zeros((N, N))

    for i in range(N):
        for j in range(N):
            # Periodic neighboring indices
            next_i = (i + 1) % N
            next_j = (j + 1) % N

            # Plaquette product (counterclockwise)
            W = (
                Ux[i, j]
                * Uy[next_i, j]
                * np.conj(Ux[i, next_j])
                * np.conj(Uy[i, j])
            )

            # Gauge-invariant Berry flux
            berry_flux[i, j] = -np.angle(W)

    # Sum over the Brillouin zone
    C = np.sum(berry_flux) / (2 * np.pi)

    return C, berry_flux




if __name__ == "__main__":
    N = 20
    m = -1.0

    k_grid, energies, states = compute_lower_band_states(N, m)

    # Numerical checks at k = (0, 0)
    i = N // 2
    j = N // 2

    u = states[i, j]
    E = energies[i, j]
    H = chern_model_hamiltonian(k_grid[i], k_grid[j], m)

    print("k-grid shape:", k_grid.shape)
    print("Energies shape:", energies.shape)
    print("States shape:", states.shape)

    print("Lower-band energy at (0,0):", E)
    print("Lower-band eigenvector:", u)
    print("Normalization:", np.vdot(u, u))

    # Verify H|u> = E|u>
    print("Eigenvalue equation valid:",
          np.allclose(H @ u, E * u))

    
    # Stage 2: Compute link variables
    Ux, Uy = compute_link_variables(states)

    print("\n--- Stage 2: Link Variables ---")
    print("Ux shape:", Ux.shape)
    print("Uy shape:", Uy.shape)

    print("Ux magnitude close to 1:",
          np.allclose(np.abs(Ux), 1.0))

    print("Uy magnitude close to 1:",
          np.allclose(np.abs(Uy), 1.0))

    print("Ux at (10,10):", Ux[10, 10])
    print("Uy at (10,10):", Uy[10, 10])

    # Check periodic boundary indexing
    print("Periodic x-link magnitude:", abs(Ux[N-1, 10]))


    # Stage 3: Compute Chern number
    C, berry_flux = compute_chern_number(Ux, Uy)

    print("\n--- Stage 3: Chern Number ---")
    print("Berry flux shape:", berry_flux.shape)
    print("Numerical Chern number:", C)
    print("Nearest integer:", round(C))

    # Stage 4: Gauge invariance test

    rng = np.random.default_rng(42)

    # Generate a random phase at every k-point
    phases = rng.uniform(-np.pi, np.pi, size=(N, N))

    # Apply gauge transformation to each eigenvector
    transformed_states = states * np.exp(1j * phases)[:, :, None]

    # Recompute link variables and Chern number
    Ux_new, Uy_new = compute_link_variables(transformed_states)
    C_new, berry_flux_new = compute_chern_number(Ux_new, Uy_new)

    print("\n--- Stage 4: Gauge Invariance Test ---")
    print("Original Chern number:", C)
    print("Transformed Chern number:", C_new)

    print("Chern number unchanged:",
          np.allclose(C, C_new))

    print("Berry flux unchanged:",
          np.allclose(berry_flux, berry_flux_new))

    print("Max Berry flux difference:",
          np.max(np.abs(berry_flux - berry_flux_new)))



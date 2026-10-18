import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from src.strip_geometry import build_strip_hamiltonian
from src.topology import (
    compute_lower_band_states,
    compute_link_variables,
    compute_chern_number,
)

FIGURES = Path('figures')
FIGURES.mkdir(exist_ok=True)


def plot_edge_localization(Nx=40, ky=np.pi / 6, m=-1.0, edge_cells=6):
    H = build_strip_hamiltonian(ky, m, Nx)
    energies, vectors = np.linalg.eigh(H)
    prob = np.abs(vectors.reshape(Nx, 2, 2 * Nx)) ** 2
    prob = prob.sum(axis=1)

    left_weights = prob[:edge_cells, :].sum(axis=0)
    right_weights = prob[-edge_cells:, :].sum(axis=0)
    left_idx = int(np.argmax(left_weights))
    right_idx = int(np.argmax(right_weights))

    assert left_idx != right_idx
    assert left_weights[left_idx] > 0.95
    assert right_weights[right_idx] > 0.95
    assert np.isclose(energies[left_idx], np.sin(ky), atol=1e-8)
    assert np.isclose(energies[right_idx], -np.sin(ky), atol=1e-8)

    x = np.arange(1, Nx + 1)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, prob[:, left_idx], 'o-', ms=3,
            label=f'Left edge (E={energies[left_idx]:+.3f})')
    ax.plot(x, prob[:, right_idx], 'o-', ms=3,
            label=f'Right edge (E={energies[right_idx]:+.3f})')
    ax.set(xlabel='Unit cell x', ylabel='Probability P(x)',
           title=f'QWZ Edge-State Localization (m={m}, ky=pi/6)')
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    filename = FIGURES / 'qwz_edge_localization_m-1.0.png'
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)

    print('\n--- Edge Localization ---')
    print(f'Left edge:  E={energies[left_idx]:+.6f}, P_left={left_weights[left_idx]:.6f}')
    print(f'Right edge: E={energies[right_idx]:+.6f}, P_right={right_weights[right_idx]:.6f}')
    print('Saved:', filename)


def compute_strip_spectrum(Nx, Nk, m, edge_cells=6):
    ky_values = np.linspace(-np.pi, np.pi, Nk, endpoint=False)
    energy_grid = np.empty((Nk, 2 * Nx))
    weight_grid = np.empty((Nk, 2 * Nx))

    for j, ky in enumerate(ky_values):
        H = build_strip_hamiltonian(ky, m, Nx)
        energies, vectors = np.linalg.eigh(H)
        prob = (np.abs(vectors)**2).reshape(Nx, 2, 2 * Nx).sum(axis=1)
        energy_grid[j] = energies
        weight_grid[j] = (
            prob[:edge_cells, :].sum(axis=0)
            + prob[-edge_cells:, :].sum(axis=0)
        )

    return ky_values, energy_grid, weight_grid


def plot_phase_comparison(Nx=40, Nk=120):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), constrained_layout=True)
    for ax, m, C in zip(axes, [-1.0, 3.0], [1, 0]):
        ky, energies, weights = compute_strip_spectrum(Nx, Nk, m)
        scatter = ax.scatter(
            np.repeat(ky, 2 * Nx), energies.ravel(),
            c=weights.ravel(), cmap='viridis', vmin=0, vmax=1,
            s=5, rasterized=True,
        )
        ax.set_title(f'm={m:g}, bulk C={C:+d}')
        ax.set_xlabel(r'$k_y$')
        ax.set_ylabel('Energy E')
        ax.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi],
                      [r'$-\pi$', r'$-\pi/2$', '0', r'$\pi/2$', r'$\pi$'])
        ax.set_xlim(-np.pi, np.pi)
        ax.set_ylim((-3.25, 3.25) if m == -1.0 else (-5.25, 5.25))
        ax.grid(alpha=0.2)

    fig.colorbar(scatter, ax=axes, label='Edge probability weight')
    filename = FIGURES / 'qwz_edge_spectrum_comparison.png'
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print('Saved:', filename)


def run_checks(Nx=40):
    print('\n--- Week 7 Numerical Checks ---')
    ky = np.pi / 6
    for m, expected_C in [(-1.0, 1), (3.0, 0)]:
        H = build_strip_hamiltonian(ky, m, Nx)
        assert H.shape == (2 * Nx, 2 * Nx)
        assert np.allclose(H, H.conj().T)
        _, _, states = compute_lower_band_states(40, m)
        Ux, Uy = compute_link_variables(states)
        C, _ = compute_chern_number(Ux, Uy)
        assert np.isclose(C, expected_C, atol=1e-8)
        print(f'm={m:+.1f}: Hermitian=True, bulk C={C:+.6f}')

    trivial_energies = np.linalg.eigvalsh(build_strip_hamiltonian(0, 3.0, Nx))
    assert np.min(np.abs(trivial_energies)) > 1.0
    print('Trivial strip has no near-zero modes at ky=0: True')
    print('All checks passed.')


if __name__ == '__main__':
    plot_edge_localization()
    plot_phase_comparison()
    run_checks()

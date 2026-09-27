# Topological Lattice Models

A computational study of energy spectra, topological phase transitions,
and boundary states in quantum lattice models.

## Project Roadmap

1. One-dimensional tight-binding model
2. SSH model
3. Topological invariants and edge states
4. Two-dimensional Chern insulator
5. Bulk-edge correspondence

## Week 1: Finite Open Tight-Binding Chain

The first stage of this project studies a one-dimensional finite
tight-binding chain with nearest-neighbour hopping.

The Hamiltonian is

\[
H =
-t \sum_n
\left(
|n\rangle \langle n+1|
+
|n+1\rangle \langle n|
\right).
\]

For a chain of \(N\) sites with open boundary conditions, the numerical
eigenvalues obtained using NumPy agree with the analytical result

\[
E_j =
-2t
\cos
\left(
\frac{j\pi}{N+1}
\right),
\qquad
j=1,\dots,N.
\]

As the number of lattice sites increases, the allowed energy levels
become increasingly dense and approach the continuous tight-binding
dispersion relation

\[
E(k) = -2t\cos(ka).
\]

This stage verifies the connection between finite-system eigenvalues
and the bulk energy band.

## Current Status

Week 1 completed:
- constructed finite open-chain Hamiltonians
- numerically diagonalized Hermitian Hamiltonians
- verified eigenvalues and eigenvectors
- compared numerical and analytical spectra
- visualized the finite-size approach to the energy band
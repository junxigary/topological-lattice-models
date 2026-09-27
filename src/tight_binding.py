import numpy as np
N = 5
t = 1.0
epsilon = 0.0
H = np.zeros((N, N))
for n in range(N):
    H[n, n] = epsilon
for n in range(N - 1):
    H[n, n + 1] = -t
    H[n + 1, n] = -t
print("Hamiltonian:")
print(H)

energies, states = np.linalg.eigh(H)

print("\nEnergies:")
print(energies)

print("\nGround-state eigenvector:")
print(states[:, 0])

psi0 = states[:, 0]
E0 = energies[0]

print("\nCheck H psi = E psi:")
print("H psi:")
print(H @ psi0)

print("E psi:")
print(E0 * psi0)
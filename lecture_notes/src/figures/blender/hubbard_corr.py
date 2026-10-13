"""Exact <S_0 . S_j> in the half-filled ground state of Eq. (hub3) on an open chain, for figure 3.4.

The ground state is a singlet (Lieb's theorem), so <S_0 . S_j> = 3 <S^z_0 S^z_j>, and only the
diagonal S^z correlator is needed. Nearest-neighbor hopping on an open chain moves no electron past
another of the same spin, so no fermionic sign appears.
"""
import itertools

import numpy as np


def correlations(L=6, U=4.0, t=1.0):
    half = L // 2
    ups = [sum(1 << i for i in c) for c in itertools.combinations(range(L), half)]
    basis = [(u, d) for u in ups for d in ups]
    idx = {b: k for k, b in enumerate(basis)}
    H = np.zeros((len(basis), len(basis)))
    for k, (u, d) in enumerate(basis):
        for i in range(L):
            H[k, k] += U * (((u >> i) & 1) - 0.5) * (((d >> i) & 1) - 0.5)
        for i in range(L - 1):
            for spin in (0, 1):
                s = (u, d)[spin]
                if ((s >> i) & 1) != ((s >> (i + 1)) & 1):
                    s2 = s ^ (1 << i) ^ (1 << (i + 1))
                    b2 = (s2, d) if spin == 0 else (u, s2)
                    H[idx[b2], k] += -t
    w, v = np.linalg.eigh(H)
    g = v[:, 0] ** 2
    sz = np.array([[(((u >> i) & 1) - ((d >> i) & 1)) / 2 for i in range(L)] for u, d in basis])
    return [3 * float(np.sum(g * sz[:, 0] * sz[:, j])) for j in range(L)], float(np.sum(g * sz[:, 0]))


if __name__ == '__main__':
    c, m = correlations()
    print('m_0 =', round(m, 6), ' <S0.Sj> =', [round(x, 4) for x in c])

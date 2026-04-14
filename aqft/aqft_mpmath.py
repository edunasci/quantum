#!/usr/bin/env -S python3 -u 
## carrega bibliotecas
import matplotlib
matplotlib.use('Agg') 

import qiskit
import Crypto
import decimal

from decimal import *

from datetime import datetime
from Crypto.Util import number
from Crypto.Random import random
import matplotlib.pyplot as plt
import numpy as np
import mpmath
from mpmath import mp
import math

from fractions import Fraction

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

print(f'qiskit.__version__={qiskit.__version__}')
print(f'numpy.__version__={np.__version__}')
print(f'decimal.__version__={decimal.__version__}')
print(f'Crypto.__version__={Crypto.__version__}')
print(f'mpmath.__version__={mpmath.__version__}')

mp.dps=100

def normalize(psi):
    norm = mp.sqrt(sum(abs(a)**2 for a in psi))
    return [a / norm for a in psi]


def apply_hadamard(psi, qubit, n):
    """Apply H to qubit"""
    new_psi = psi.copy()
    N = len(psi)

    for i in range(N):
        if ((i >> qubit) & 1) == 0:
            j = i | (1 << qubit)

            a = psi[i]
            b = psi[j]

            new_psi[i] = (a + b) / mp.sqrt(2)
            new_psi[j] = (a - b) / mp.sqrt(2)

    return new_psi

def apply_cp(psi, control, target, theta):
    """Apply controlled phase"""
    new_psi = psi.copy()
    N = len(psi)

    for i in range(N):
        if ((i >> control) & 1) and ((i >> target) & 1):
            new_psi[i] *= mp.exp(1j * theta)

    return new_psi

# -----------------------------------
# AQFT dagger (your exact structure)
# -----------------------------------
def aqft_dagger_state(psi, L, m):
    psi = psi.copy()

    for j in range(L):
        start_k = max(0, j - m + 1)
        # controlled phase rotations
        for k in range(start_k, j):
            angle = -mp.pi / (2 ** (j - k))
            psi = apply_cp(psi, k, j, angle)

        # Hadamard
        psi = apply_hadamard(psi, j, L)

    return psi

def iqft_state(psi, L):
    return aqft_dagger_state(psi, L, m=L)



# -----------------------------------
# Probabilities
# -----------------------------------
def probabilities(psi):
    return [abs(a)**2 for a in psi]


def define_initial_state_for_order(r: int, L: int ):
    """
    Estado do registrador de fase após phase kickback e antes da IQFT/AQFT:
    (1/sqrt(2^L)) sum_x exp(2πi phi x) |x>
    """
    v_exp = np.vectorize(mp.exp)
    M = 2 ** L
    amps = np.array([mp.mpc(0)]*M)
    for i in range(r):
        phi = mp.mpc(i)/mp.mpc(r)
        amps += v_exp(2j * mp.pi * phi * np.arange(M)) / mp.sqrt(M)
    #amps /= r  # Normaliza o vetor de estado
    return amps

def bit_reverse(x: int, nbits: int) -> int:
    out = 0
    for _ in range(nbits):
        out = (out << 1) | (x & 1)
        x >>= 1
    return out

def aqft_example(N, a, r, p, q):
    L = int(mp.log(N, 2)) + 1
    phi = (1/r)
    M = 2 ** L

    print(f"Exemplo: N={N}, a={a}, r={r}, p={p}, q={q}, L={L}, phi=2*pi*{phi:.16f}")

    # Example: |011>
    #psi = [mp.mpc(0) for _ in range(M)]
    #psi[3] = mp.mpc(1)
    psi = define_initial_state_for_order(r, L)
    psi = normalize(psi)

    # IQFT
    psi_iqft = iqft_state(psi, L)
    prob_iqft = probabilities(psi_iqft)
    print("IQFT probabilities:")
    for i, p in enumerate(prob_iqft):
        print(f'{i:0{L}b}: {float(p):.16f}')
    print(f'total probability: {float(sum(prob_iqft)):.16f} ')
    print(f'')

    # AQFT with truncation m=5
    psi_aqft = aqft_dagger_state(psi, L, m=5)
    prob_aqft = probabilities(psi_aqft)
    print("\nAQFT probabilities (m=5):")
    for i, p in enumerate(prob_aqft):
        print(f'{i:0{L}b}: {float(p):.16f}')
    print(f'total probability: {float(sum(prob_aqft)):.16f} ')
    print(f'')

    error = sum(mp.fabs(prob_iqft[i] - prob_aqft[i]) for i in range(len(prob_iqft)))
    print(f"\nTotal error (L1 norm): {float(error):.16f}")
    print(f'')

    i=0
    for probs in [prob_iqft, prob_aqft]:
        reordered_probs = np.zeros_like(probs)
        for y, p in enumerate(probs):
            reordered_probs[bit_reverse(y, L)] = p
    
        ys = np.arange(len(reordered_probs))
        peak_y = np.argmax(reordered_probs)
        peak_value = np.max(reordered_probs)

        plt.figure()
        plt.stem(ys, reordered_probs)
        plt.xlabel("Y")
        plt.ylabel("Probability")
        plt.title(f"Frequency Spectrum - max at y={peak_y} {peak_y:0{L}b} ({float(peak_value):.6f})")
        plt.vlines(peak_y, 0, peak_value,colors='r', linestyles='dashed', label='Peak')
        plt.savefig(f'img/probability_mpmath_{i}_L_{L}.png')
        #plt.show()
        i+=1
    return

# -----------------------------------
# Example
# -----------------------------------
if __name__ == "__main__":

    #aqft_example(N=15, a=8, r=4, p=3, q=5)
    #aqft_example(N=21, a=11, r=6, p=7, q=3)
    aqft_example(N=29737, a=9094, r=14690, p=131, q=227)


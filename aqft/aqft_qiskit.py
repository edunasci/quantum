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
from mpmath import mp, psi
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


def aqft_dagger(L: int, m: int) -> QuantumCircuit:
    """
    AQFT inversa truncada em L qubits.
    Mantém apenas rotações controladas até distância m.
    Para m >= L, coincide com a IQFT usual (sem swaps explícitos, mas com
    correção de bit-reversal na leitura).
    ### Original function using QISKIT
    """
    qc = QuantumCircuit(L, name=f"AQFT†(L={L},m={m})")
    # Implementação padrão da IQFT sem swaps finais
    for j in range(L):
        # rotações controladas truncadas
        start_k = max(0, j - m + 1)
        for k in range(start_k, j):
            angle = -np.pi / (2 ** (j - k))
            qc.cp(angle, k, j)
        qc.h(j)
    return qc

def normalize(psi):
    norm = np.sqrt(sum(abs(a)**2 for a in psi))
    return [a / norm for a in psi]

def define_initial_state_for_order(r: int, L: int ) -> Statevector:
    """
    Estado do registrador de fase após phase kickback e antes da IQFT/AQFT:
    (1/sqrt(2^L)) sum_x exp(2πi phi x) |x>
    """
    M = 2 ** L
    """
    amps = np.zeros(M, dtype=complex)
    for i in range(r):
        phi = i/r
        amps += np.exp(2j * np.pi * phi * np.arange(M)) / np.sqrt(M)
    amps = normalize(amps)
    """
    phi=1/r
    amps = np.zeros(M, dtype=complex)
    for i in range(1, r+1):
        phi = i/r
        amps += np.exp(2j * np.pi * phi * np.arange(M)) / np.sqrt(M)
    amps /= r
    return Statevector(amps)

def bit_reverse(x: int, nbits: int) -> int:
    out = 0
    for _ in range(nbits):
        out = (out << 1) | (x & 1)
        x >>= 1
    return out

def reorder_probabilities(probs, L):
    reordered_probs = np.zeros_like(probs)
    for y, p in enumerate(probs):
        reordered_probs[bit_reverse(y, L)] = p
    return reordered_probs

def aqft_example(N, a, r, p, q, L=None, m=5):
    if L is None:
        L = (int(math.log2(N))+1)*2+1
    phi = ((1)/r)
    m=5
    # gera AQFT† para diferentes m
    print(f"Exemplo: N={N}, a={a}, r={r}, p={p}, q={q}, L={L}, phi=2*pi*{phi:.16f}")

    print (f'Circuito AQFT† - qiskit - L={L}, m={m}:')
    # IQFT
    qc = aqft_dagger(L, L)
    sv_initial = define_initial_state_for_order(r, L)
    sv_final = sv_initial.evolve(qc)
    prob_iqft = sv_final.probabilities()
    #prob_iqft = reorder_probabilities(prob_iqft, L) 
    print("IQFT probabilities:")

    peak_prob = 0
    expected_peak = np.round(np.arange(2**L/r,2**L,2**L/r)).astype(int)
    for i, p in enumerate(prob_iqft):
        print(f'{i:0{L}b} ({i}): {float(p):.16f}')
        if i in expected_peak:
            peak_prob += p
            
    print(f'total probability: {float(sum(prob_iqft)):.16f} ')
    print(f'expected peaks at: {expected_peak} with total probability {float(peak_prob):.16f}')
    print(f'')


    # AQFT with truncation m
    qc = aqft_dagger(L, m)
    sv_initial = define_initial_state_for_order(r, L)
    sv_final = sv_initial.evolve(qc)
    prob_aqft = sv_final.probabilities()
    #prob_aqft = reorder_probabilities(prob_aqft, L) 
    print(f"AQFT probabilities (m={m}):")
    
    peak_prob = 0
    expected_peak = np.round(np.arange(2**L/r,2**L,2**L/r)).astype(int)
    for i, p in enumerate(prob_aqft):
        print(f'{i:0{L}b} ({i}): {float(p):.16f}')
        if i in expected_peak:
            peak_prob += p
    print(f'total probability: {float(sum(prob_aqft)):.16f} ')
    print(f'expected peaks at: {expected_peak} with total probability {float(peak_prob):.16f}')
    print(f'')


    error = sum(mp.fabs(prob_iqft[i] - prob_aqft[i]) for i in range(len(prob_iqft)))
    print(f"\nTotal error (L1 norm): {float(error):.16f}")
    print(f'')

    i=0
    for probs in [prob_iqft, prob_aqft]:
        ys = np.arange(len(probs))
        peak_y = np.argmax(probs)
        peak_value = np.max(probs)
        plt.figure()
        plt.stem(ys, probs)
        plt.xlabel("Y")
        plt.ylabel("Probability")
        plt.title(f"Frequency Spectrum - max at y={peak_y} {peak_y:0{L}b} ({float(peak_value):.6f})")
        plt.vlines(peak_y, 0, peak_value,colors='r', linestyles='dashed', label='Peak')
        plt.savefig(f'img/probability_qiskit_{'IQFT' if i == 0 else 'AQFT'}_L_{L}.png')
        #plt.show()
        i+=1
    return

if __name__ == "__main__":
    aqft_example(N=21, a=11, r=6, p=7, q=3, L=8, m=5)
    #aqft_example(N=15, a=8, r=4, p=3, q=5)
    #aqft_example(N=29737, a=9094, r=14690, p=131, q=227)
    #aqft_example(N=26123, a=10452, r=516, p=151, q=173)

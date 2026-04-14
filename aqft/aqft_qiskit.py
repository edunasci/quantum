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
    norm = mp.sqrt(sum(abs(a)**2 for a in psi))
    return [a / norm for a in psi]

def define_initial_state_for_order(r: int, L: int ) -> Statevector:
    """
    Estado do registrador de fase após phase kickback e antes da IQFT/AQFT:
    (1/sqrt(2^L)) sum_x exp(2πi phi x) |x>
    """
    M = 2 ** L
    amps = np.zeros(M, dtype=complex)
    for i in range(r):
        phi = i/r
        amps += np.exp(2j * np.pi * phi * np.arange(M)) / np.sqrt(M)
    amps = normalize(amps)
    #amps /= r  # Normaliza o vetor de estado
    #phi = 1/r
    #amps += np.exp(2j * np.pi * phi * np.arange(M)) / np.sqrt(M)
    return Statevector(amps)

def define_initial_state_for_phase_estimation(phi: float, L: int ) -> Statevector:
    """
    Estado do registrador de fase após phase kickback e antes da IQFT/AQFT:
    (1/sqrt(2^L)) sum_x exp(2πi phi x) |x>
    """
    M = 2 ** L
    amps = np.exp(2j * np.pi * phi * np.arange(M)) / np.sqrt(M)
    return Statevector(amps)

def bit_reverse(x: int, nbits: int) -> int:
    out = 0
    for _ in range(nbits):
        out = (out << 1) | (x & 1)
        x >>= 1
    return out

def aqft_example(N, a, r, p, q):
    L = int(math.log2(N))+1
    phi = ((1)/r)
        
    # gera AQFT† para diferentes m
    print(f"Exemplo: N={N}, a={a}, r={r}, p={p}, q={q}, L={L}, phi=2*pi*{phi:.16f}")
    for m in [L,5]:
        qc = aqft_dagger(L, m)
        print (f'Circuito AQFT† - L={L}, m={m}:')
        #fig = qc.draw('mpl')
        #fig.suptitle(f'AQFT† - L={L}, m={m}', fontsize=16)
        #fig.savefig(f'img/aqft_dagger_L_{L}_m_{m}.png')

        #sv_initial = define_initial_state_for_phase_estimation(phi, L)
        sv_initial = define_initial_state_for_order(r, L)
        #print(f'{sv_initial}')

        sv_final = sv_initial.evolve(qc)
        #print(f'{sv_final}')

        probs = sv_final.probabilities()
        print("probabilities:")
        for i, p in enumerate(probs):
            #print(i, p)
            print(f'{i:0{L}b}: {p:.16f}')
        print(f'total probability: {sum(probs):.16f} ')
        print(f'')


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
        plt.title(f"Frequency Spectrum - max at y={peak_y} {peak_y:0{L}b} ({peak_value:.6f})")
        plt.vlines(peak_y, 0, peak_value,colors='r', linestyles='dashed', label='Peak')
        plt.savefig(f'img/probability_qiskit_L_{L}_m_{m}.png')
        #plt.show()
        
    return

#aqft_example(N=15, a=8, r=4, p=3, q=5)
#aqft_example(N=21, a=11, r=6, p=7, q=3)
aqft_example(N=29737, a=9094, r=14690, p=131, q=227)
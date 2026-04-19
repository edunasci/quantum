#!/usr/bin/env -S python3 -u 
"""
usage:precisiontest.ipynb

options:

description:
    This notebook contains code to test the precision libraries in python and determine the impact on our research. 

"""

## carrega bibliotecas
import qiskit
import Crypto
import decimal

from decimal import *

from datetime import datetime
from Crypto.Util import number
from Crypto.Random import random
import matplotlib.pyplot as plt
import numpy as np
import mpmath as mp
import math

from fractions import Fraction

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


print(f'qiskit.__version__={qiskit.__version__}')
print(f'numpy.__version__={np.__version__}')
print(f'decimal.__version__={decimal.__version__}')
print(f'Crypto.__version__={Crypto.__version__}')
print(f'mpmath.__version__={mp.__version__}')

# 2^4097 +-= 10^1233 -- 1500 digits
getcontext().prec = 1500
mp.mp.dps = 1500

# sin / cos / exp differencies from pi/2 to pi/2**1024

def print_results(denominator, x, sin_x, cos_x, exp_x, _x_minus_sin_x, _1_minus_cos_x, _1_minus_exp_x):
    print("denominator: ")
    [print(f'   2**{2**i:<5}: {denominator[i]}') for i in range(len(denominator))]
    print("x: ")
    [print(f'pi/2**{2**i:<5}: {x[i]}') for i in range(len(x))]
    print("sin(x): ")
    [print(f'sin(pi/2**{2**i:<5}):   {sin_x[i]}') for i in range(len(sin_x))]
    print("cos(x): ")
    [print(f'cos(pi/2**{2**i:<5}):   {cos_x[i]}') for i in range(len(cos_x))]
    print("exp(x): ")
    [print(f'exp(pi/2**{2**i:<5}):   {exp_x[i]}') for i in range(len(exp_x))]
    print("x - sin(x): ")
    [print(f'x-sin(pi/2**{2**i:<5}):   {_x_minus_sin_x[i]}') for i in range(len(_x_minus_sin_x))]
    print("1 - cos(x): ")
    [print(f'1-cos(pi/2**{2**i:<5}):   {_1_minus_cos_x[i]}') for i in range(len(_1_minus_cos_x))]
    print("1 - exp(x): ")
    [print(f'1-exp(pi/2**{2**i:<5}):   {_1_minus_exp_x[i]}') for i in range(len(_1_minus_exp_x))]


def get_results_Decimal(max_i=13):
     denominator = 2**(np.array([Decimal(2)**i for i in range(max_i)]))
     x = Decimal(np.pi) / denominator
     sin_x = np.array([Decimal(math.sin(float(xi))) for xi in x])
     cos_x = np.array([Decimal(math.cos(float(xi))) for xi in x])
     exp_x = np.array([Decimal(math.exp(float(xi))) for xi in x])
     _x_minus_sin_x = x - sin_x
     _1_minus_cos_x = 1 - cos_x
     _1_minus_exp_x = 1 - exp_x
     return (denominator, x, sin_x, cos_x, exp_x, _x_minus_sin_x, _1_minus_cos_x, _1_minus_exp_x)

def get_results_float64(max_i=13):
    denominator = 2**(np.array([np.float64(2)**i for i in range(max_i)]))
    x = np.float64(np.pi) / denominator
    sin_x = np.sin(x)
    cos_x = np.cos(x)
    exp_x = np.exp(x)
    _x_minus_sin_x = x - sin_x
    _1_minus_cos_x = 1 - cos_x
    _1_minus_exp_x = 1 - exp_x
    return (denominator, x, sin_x, cos_x, exp_x, _x_minus_sin_x, _1_minus_cos_x, _1_minus_exp_x)

def get_results_float128(max_i=13):
    denominator = 2**(np.array([np.float128(2)**i for i in range(max_i)]))
    x = np.float128(np.pi) / denominator
    sin_x = np.sin(x)
    cos_x = np.cos(x)
    exp_x = np.exp(x)
    _x_minus_sin_x = x - sin_x
    _1_minus_cos_x = 1 - cos_x
    _1_minus_exp_x = 1 - exp_x
    return (denominator, x, sin_x, cos_x, exp_x, _x_minus_sin_x, _1_minus_cos_x, _1_minus_exp_x)

def get_results_mp(max_i=13):
    denominator = 2**(np.array([mp.mpf(2)**i for i in range(max_i)]))
    x = mp.mp.pi / denominator
    sin_x = np.array([mp.mp.sin(float(xi)) for xi in x])
    cos_x = np.array([mp.mp.cos(float(xi)) for xi in x])
    exp_x = np.array([mp.mp.exp(float(xi)) for xi in x])
    _x_minus_sin_x = x - sin_x
    _1_minus_cos_x = 1 - cos_x
    _1_minus_exp_x = 1 - exp_x
    return (denominator, x, sin_x, cos_x, exp_x, _x_minus_sin_x, _1_minus_cos_x, _1_minus_exp_x)

def precision_test():
    print('Calculating sin, cos and exp for x = pi/2**i, i=0..12 - using float64')
    print('')
    denominator, x, sin_x, cos_x, exp_x, _x_minus_sin_x, _1_minus_cos_x, _1_minus_exp_x = get_results_float64()
    print_results(denominator, x, sin_x, cos_x, exp_x, _x_minus_sin_x, _1_minus_cos_x, _1_minus_exp_x)

    if hasattr(np, "float128"):
        print('')
        print('')
        print('Calculating sin, cos and exp for x = pi/2**i, i=0..12 - using float128')
        print('')
        denominator, x, sin_x, cos_x, exp_x, _x_minus_sin_x, _1_minus_cos_x, _1_minus_exp_x = get_results_float128()
        print_results(denominator, x, sin_x, cos_x, exp_x, _x_minus_sin_x, _1_minus_cos_x, _1_minus_exp_x)

    print('')
    print('')
    print('Calculating sin, cos and exp for x = pi/2**i, i=0..12 - using Decimal with 1500 digits of precision')
    print('')
    denominator, x, sin_x, cos_x, exp_x, _x_minus_sin_x, _1_minus_cos_x, _1_minus_exp_x = get_results_Decimal()
    print_results(denominator, x, sin_x, cos_x, exp_x, _x_minus_sin_x, _1_minus_cos_x, _1_minus_exp_x)

    print('')
    print('')
    print('Calculating sin, cos and exp for x = pi/2**i, i=0..12 - using mpmath with 1500 digits of precision')
    print('')
    denominator, x, sin_x, cos_x, exp_x, _x_minus_sin_x, _1_minus_cos_x, _1_minus_exp_x = get_results_mp()
    print_results(denominator, x, sin_x, cos_x, exp_x, _x_minus_sin_x, _1_minus_cos_x, _1_minus_exp_x)

    print('')
    print('Done.')
    
if __name__ == "__main__":
    precision_test()
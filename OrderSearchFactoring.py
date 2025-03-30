#!/usr/bin/env -S python3 -u 
"""
usage: ordersearch.py [-h] [-b BITS] [-m MAXORDER]

options:
  -h, --help            show this help message and exit
  -b BITS, --bits BITS  Enter "bits" to define the size of "p", "q" in bits
  -m MAXORDER, --maxorder MAXORDER
                        Enter "maxorder" to define maximum order for the search

"""
__author__      = 'Eduardo Marsola do Nascimento'
__copyright__   = 'Copyright 2025-02-16'
__credits__     = ''
__license__     = 'MIT'
__version__     = '1.00'
__maintainer__  = ''
__email__       = ''
__status__      = 'Production'
__printdebug__  = False

from decimal import *
from datetime import datetime
from Crypto.Util import number
from Crypto.Random import random
import matplotlib.pyplot as plt
import numpy as np
import argparse

global C
C = Decimal(0)

def getnumberorder( a, N, maxorder ):
    global C
    if maxorder == None:
        maxorder = N+1
    result = Decimal(1)
    i = Decimal(1)
    while i < Decimal(maxorder):
        #print(f'i={i}, a={a}, maxorder={maxorder}, result={result} (C={C})') if __printdebug__ or (i%1000000)==0 else None
        C += 1
        result = (result * a)%N
        if result==Decimal(1):
            return i
        i += 1
    return None

def factorize( N ):
    global C
    C=Decimal(0)
    print(f'*** Factorizing N = {N} ***')    
    print(f'')
    if N == None:
        print(f'Nothing to do')
        return
    R = {}
    root_N = N.sqrt()
    floor_root_N = root_N.to_integral_value(ROUND_FLOOR)
    max_q = (root_N*Decimal(2).sqrt()).to_integral_value(ROUND_FLOOR)
    floor_root_4_N = root_N.sqrt().to_integral_value(ROUND_FLOOR)
    floor_root_8_N = root_N.sqrt().sqrt().to_integral_value(ROUND_FLOOR)
    print(f'floor_root_N = {floor_root_N}')
    print(f'max_q = {max_q}')
    print(f'floor_root_4_N = {floor_root_4_N}')
    print(f'')
    i = Decimal(0)
    a = max_q
    while( a > floor_root_N):
        i += 1
        r = getnumberorder( a, N, 2*floor_root_4_N)
        print(f'i={i}, a={a:8}, r={r} (C={C})') # if __printdebug__ or (i%1000)==0 else None
        if r != None:
            print(f'if N={N} and a={a}, then N%a={N%a}, r={r} (C={C})')
            if (r%2) != 0:
                a -= floor_root_4_N
                continue
            p_candidate = pow( a, r//2, N)
            R[f'{a:16}'] = r
            print(f'p_candidate = {p_candidate}')
            print(f'q_candidate = {N/p_candidate}')
        a -= 1
    return

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('-N','--n_to_factorize', help='Enter "N" to be factored', type=Decimal, default=None)
    args = parser.parse_args()
    N = args.n_to_factorize
    factorize(N)
    
if __name__ == '__main__':
    # track execution time
    startTime=datetime.now()
    print(f'Start: {startTime.replace(microsecond=0)}\n\n')
    main()
    # track execution time
    finishTime=datetime.now()
    print( f'\nStart: {startTime.replace(microsecond=0)}, Finish:{finishTime.replace(microsecond=0)}, Running Time: {finishTime-startTime}')


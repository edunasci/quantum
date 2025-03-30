#!/usr/bin/env -S python3 -u 
"""
usage: classicalFactoring.py [-h] [-n N_TO_FACTORIZE]

options:
  -h, --help            show this help message and exit
  -n, --n_to_factorize N_TO_FACTORIZE
                        Enter "n" to be factored
"""
__author__      = 'Eduardo Marsola do Nascimento'
__copyright__   = 'Copyright 2025-03-30'
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
import math

def getPQ(N=16, limit=0.8):
    while True:
        p = number.getPrime(N)
        q = number.getPrime(N)
        p,q = min(p,q),max(p,q)
        if p/q < limit:
            return p,q,N

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('-N','--N_bits_size_of_n', help='Enter "N" number of bits to generate "n"', type=int, default=40)
    args = parser.parse_args()
    N = args.N_bits_size_of_n
    p,q,N1 = getPQ(N//2)
    n = p*q
    print(f'n={n} ({N} bits), p={p}, q={q}, (p+q)/2={(p+q)/2}')
    
if __name__ == '__main__':
    # track execution time
    startTime=datetime.now()
    print(f'Start: {startTime.replace(microsecond=0)}\n\n')
    main()
    # track execution time
    finishTime=datetime.now()
    print( f'\nStart: {startTime.replace(microsecond=0)}, Finish:{finishTime.replace(microsecond=0)}, Running Time: {finishTime-startTime}')

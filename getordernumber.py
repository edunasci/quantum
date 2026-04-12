#!/usr/bin/env python3
"""
primeplot.py - primeplot examples and test
"""
__author__      = 'Eduardo Marsola do Nascimento'
__copyright__   = 'Copyright 2023-09-22'
__credits__     = ''
__license__     = 'MIT'
__version__     = '1.00'
__maintainer__  = ''
__email__       = ''
__status__      = 'Production'
__printdebug__  = True

from decimal import *
from datetime import datetime
from Crypto.Util import number
from Crypto.Random import random
import matplotlib.pyplot as plt
import numpy as np
import argparse

def getGCD( a, N ):
    GCD = 1
    for i in range(min(a,N),0,-1):
        #print(f'i={i}, GCD={GCD}')
        if (a%i)==0 and (N%i)==0:
            GCD = i
            #print(f'GCD={GCD}')
            break
    return GCD

def getZ_star_N( N ):
    Z_star_N = []
    for a in range(1,N): 
        if getGCD(a,N)==1:
            Z_star_N += [a]
    return Z_star_N

<<<<<<< HEAD
<<<<<<< HEAD
def getnumberorder( a, n, maxorder=None ):
    a = a % n
    if a == 0:
        return None
    if maxorder == None:
        maxorder = n
    m=1
    i=1
    while i<=maxorder:
        m = (m*a)%n
        print(f'a={a}, i={i}, n={n}, (a**i%n)=m={m}') if __printdebug__ and i%1000==0 else None
        if m==1:
            print(f'a={a}, i={i}, n={n}, (a**i%n)=m={m}') if __printdebug__ else None
            return i
        i += 1
=======
=======
>>>>>>> 0772ea1cd680708d0ba8e65898cc4d8c3892f7c8
def getnumberorder( a, N, maxorder ):
    if maxorder == None:
        maxorder = N
    m=1
    for i in range(1,maxorder):
        print(f'a={a}, i={i}, N={N}, a**i%N={a**i%N}') if __printdebug__ else None
        m = (m*a)%N
        if m==1:
            return i
<<<<<<< HEAD
>>>>>>> 0772ea1cd680708d0ba8e65898cc4d8c3892f7c8
=======
>>>>>>> 0772ea1cd680708d0ba8e65898cc4d8c3892f7c8
    return None

def print_Z_star_N_orders( N, maxorder ):
    Z_star_N = getZ_star_N( N )
    print(f'for N={N} Z^*_N = {Z_star_N}')
    if maxorder != None:
        print(f'maxorder = {maxorder}')
    for a in Z_star_N:
        if a==1:
            continue
        r = getnumberorder( a, N, maxorder )
        if r != None:
            print(f'if N={N} and a={a}, then r={r}')
    return

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('-N','--number', help='Enter N to define the number group Z_star_N', type=int, default=9)
    parser.add_argument('-r','--maxorder', help='Enter maxorder to test the number group on Z_star_N', type=int, default=None)
    args = parser.parse_args()
    N  = args.number
    maxorder  = args.maxorder
    print_Z_star_N_orders( N, maxorder )

if __name__ == '__main__':
    # track execution time
    startTime=datetime.now()
    print(f'Start: {startTime.replace(microsecond=0)}\n\n')
    main()
    # track execution time
    finishTime=datetime.now()
    print( f'\nStart: {startTime.replace(microsecond=0)}, Finish:{finishTime.replace(microsecond=0)}, Running Time: {finishTime-startTime}')


#!/usr/bin/env python3
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

def getPQ(N=16, limit=0.8):
    while True:
        p = number.getPrime(N)
        q = number.getPrime(N)
        p,q = min(p,q),max(p,q)
        if p/q < limit:
            return p,q,N

def simpleGraph(filename, title, type, data, ylabel, xlabel ):
    dpi = 120
    figsize = (6,6)
    plt.ioff()
    plt.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    plt.title(title)
    if type == 'line':
        ax.plot(data.keys(), data.values())
    else:
        ax.bar( data.keys(), data.values())
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.grid()
    plt.savefig(f'img/{filename}')
    plt.show() if __printdebug__ else None
    plt.close('all')
    return

def getnumberorder( a, N, maxorder ):
    global C
    if maxorder == None:
        maxorder = N+1
    result = Decimal(1)
    for i in np.arange(Decimal(1),Decimal(maxorder)):
        C += 1
        result = (result * a)%N
        if result==Decimal(1):
            return i
    return None

def print_orders( b, maxorder ):
    p,q,N = getPQ(N=b)
    N=p*q
    global C
    C=Decimal(0)
    print(f'*** Finding orders for Z*_N ***')
    print(f'')
    print(f'Parameters: bits={b}, p={p}, q={q}, N={N}, maxorder={maxorder}')
    print(f'')
    R = {}
    orders_of_N = {}
    for a in np.arange(Decimal(2**b),Decimal(N),Decimal(2**b)):
        if a==Decimal(1):
            continue
        r = getnumberorder( a, N, maxorder )
        print(f'i={a/2**b:8}, a={a:8}, r={r}') if __printdebug__ else None
        if r != None:
            R[f'{a:16}'] = r
            print(f'if N={N} and a={a}, then N%a={N%a}, r={r} (C={C})')
            if f'{r:8}' in orders_of_N:
                orders_of_N[f'{r:8}'] +=1
            else:
                orders_of_N[f'{r:8}'] =1
    orders_of_N = dict(sorted(orders_of_N.items()))
    print(f'')
    for r in orders_of_N.keys():
        print(f'r={r}, frequency={orders_of_N[r]}')
    print(f'')
    print(f'R={R}')
    print(f'')
    print(f'N={N}, total_r = {len(orders_of_N)}, sum(frequency)={sum(orders_of_N.values())}, N-sum(frequency)={N-sum(orders_of_N.values())}')
    simpleGraph( f'grafico_frequencia_de_ordem_para_{N}',f'frequencia de ordem r para N={N}','bar',orders_of_N, ylabel='Ocorrências', xlabel='Ordem')
    simpleGraph( f'grafico_tendencia_de_ordem_para_{N}',f'tendencia de ordem r para N={N}','line',R, ylabel='Ordem', xlabel='a')
    return

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--bits', help='Enter "bits" to define the size of "p", "q" in bits', type=int, default=10)
    parser.add_argument('-m','--maxorder', help='Enter "maxorder" to define maximum order for the search', type=int, default=None)
    args = parser.parse_args()
    bits = args.bits
    maxorder = args.maxorder
    print_orders( bits, maxorder )

if __name__ == '__main__':
    # track execution time
    startTime=datetime.now()
    print(f'Start: {startTime.replace(microsecond=0)}\n\n')
    main()
    # track execution time
    finishTime=datetime.now()
    print( f'\nStart: {startTime.replace(microsecond=0)}, Finish:{finishTime.replace(microsecond=0)}, Running Time: {finishTime-startTime}')


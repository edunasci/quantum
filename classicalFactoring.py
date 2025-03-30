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

def factorize( n ):
    getcontext().prec=100
    root_n = Decimal(n).sqrt()
    floor_root_n=root_n.to_integral_value(ROUND_FLOOR)
    print(f'n={n}')
    print(f'root_n={root_n}')
    print(f'floor_root_n={floor_root_n}')
    filename = f'log/results_factoring_{n}.txt'
    with open(filename,'a') as f:
        time0=datetime.now()
        i=1
        f.write(f'Starting at {time0.replace(microsecond=0)} (i={i}) - factoring {n}\n')
        while True:
            pq_mean = floor_root_n+i
            diff=((pq_mean)**2-n).sqrt()
            if i%2**20==0:
                text = (f'i={i:5d}, runningtime={datetime.now()-time0}, pq_mean={pq_mean}, diff={diff:5.6f},q(candidate)={floor_root_n+i+diff}')
                f.write(text+'\n')
                f.flush()
            if diff == diff.to_integral_value(ROUND_FLOOR):
                text = (f'i={i:5d}, runningtime={datetime.now()-time0}, pq_mean={pq_mean}, diff={diff:5.6f},q(calculated)={floor_root_n+i+diff}')
                f.write(text+'\n')
                text=(f'math.log(i,2)={math.log(i,2)}, math.log(diff,2)={math.log(diff,2)}')
                f.write(text+'\n')
                f.flush()
                if n%(floor_root_n+i+diff)==0:
                    break
            i +=1
        q=floor_root_n+i+diff
        p=n//q
        text = (f'####\nn={n}, p={p}, q={q}, p*q={p*q}, n-(p*q)={n-(p*q)}\n####')
        f.write(text+'\n')
        f.flush()
        print(text)
        time1=datetime.now()
        text = (f'Finish at {time1.replace(microsecond=0)} - Elapsed Time: {time1-time0} (i={i}) - factoring {n}\n')
        f.write(text+'\n')
        print(text)
 
def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--n_to_factorize', help='Enter "n" to be factored', type=Decimal)
    args = parser.parse_args()
    n = args.n_to_factorize
    if n == None:
        print(f'Nothing to do')
        return
    else:
        factorize(n)
    
if __name__ == '__main__':
    # track execution time
    startTime=datetime.now()
    print(f'Start: {startTime.replace(microsecond=0)}\n\n')
    main()
    # track execution time
    finishTime=datetime.now()
    print( f'\nStart: {startTime.replace(microsecond=0)}, Finish:{finishTime.replace(microsecond=0)}, Running Time: {finishTime-startTime}')

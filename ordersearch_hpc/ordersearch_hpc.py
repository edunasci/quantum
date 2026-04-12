#!/usr/bin/env python3
"""
usage: ordersearch_hpc.py [-h] [-b BITS] [-m MAXORDER] [-t MAXTASKS] [-s SAMPLES] [-r REPEAT]

options:
  -h, --help            show this help message and exit
  -b BITS, --bits BITS  Enter "bits" to define the size of "p", "q" in bits
  -m MAXORDER, --maxorder MAXORDER
            Enter "maxorder" to define maximum order for the search
"""
__author__      = 'Eduardo Marsola do Nascimento'
__copyright__   = 'Copyright 2025-12-29'
__credits__     = ''
__license__     = 'MIT'
__version__     = '1.00'
__maintainer__  = ''
__email__       = 'eduardo.marsola@estudante.ufscar.br'
__status__      = 'Production'
__printdebug__  = False

import socket
import math
import time
from datetime import datetime
from Crypto.Util import number
from Crypto.Random import random
import numpy as np
import argparse
import os
from mpi4py import MPI

def gen_pqn(bits=32, limit=0.8):
    tries = 0
    while tries < 10000:
        tries += 1
        p = number.getPrime(bits//2)
        q = number.getPrime(bits//2)
        p,q = min(p,q),max(p,q)
        n = p*q
        if p/q < limit:
            return p,q,n
    print(f"Failed to generate p and q with {bits} bits after {tries} tries.")
    return 1,1,1

def find_orders_smp(bits, maxorder):
    nstatus = 100_000_000
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    rankStartTime=datetime.now()
    print(f'Rank {rank:3}/{size:3} - Start: {rankStartTime.replace(microsecond=0)}'
          f' host {socket.gethostname()} - (PID {os.getpid()})')
    if rank == 0:
        p,q,n = gen_pqn(bits=bits, limit=0.8)
        a = random.StrongRandom().randint(2, n-1) if p!= 1 else 1
        print(f"Rank {rank:3} - Generated n={n} (p={p}, q={q}) with {math.log2(n)} bits.")
        step = pow(a,size,n)
        data = []
        for i in range(1,size+1):
            data += [[p,q,n,a,pow(a,i,n),step]]
    else:
        data = None
    my_data = comm.scatter(data, root=0)
    print(f"Rank {rank:3} recebeu {my_data}")
    # Cada rank gera um resultado
    p,q,n,a,x,step = my_data
    if maxorder == None or maxorder > n:
        maxorder = n
    solved = x==1
    r = rank+1
    print(f"Rank {rank:3} - solved={solved}, start r={r}, a={a}, n={n}, a**r (mod n)={x}")
    while not solved:
        x = (x * step) % n
        r += size
        if r > maxorder:
            r = 0
            break
        if (r//size)%nstatus==0 or x==1:
            rankStatusTime=datetime.now()
            print(f'Status Rank={rank:3}: {rankStatusTime.replace(microsecond=0)} - {(r//size)//nstatus},'
                  f' r={r}, a={a}, n={n}, a**r (mod n)={x}, Elapsed Time: {rankStatusTime-rankStartTime}')
            solved = comm.allreduce(x==1, op=MPI.LOR)
    if x==1:
        print(f"Rank {rank} found order {r}")
    order = comm.reduce(r if x==1 else 0, op=MPI.MAX, root=0)
    comm.Barrier()
    MPI.Finalize()
    if rank == 0:
        print(f'p={p}, q={q}, n={n}, a={a}, order={order}')
        with open(f"results_n_{n}_p_{p}_q_{q}_a_{a}_order_{order}.txt", "w") as f:
            f.write(f'p={p}, q={q}, n={n}, a={a}, order={order}\n')
    rankFinishTime=datetime.now()
    print(f'Rank {rank} - Start: {rankStartTime.replace(microsecond=0)} - Finish: {rankFinishTime.replace(microsecond=0)} - Running Time: {rankFinishTime-rankStartTime}')

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--bits', help='Enter "bits" to define the size of "n"', type=int, default=32)
    parser.add_argument('-m','--maxorder', help='Enter "maxorder" to define maximum order for the search', type=int, default=None)
    args = parser.parse_args()
    maxorder = args.maxorder
    bits = args.bits
    find_orders_smp( bits, maxorder)
    
if __name__ == '__main__':
    main()
    

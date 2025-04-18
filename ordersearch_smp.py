#!/usr/bin/env python3
"""
usage: ordersearch_smp.py [-h] [-b BITS] [-m MAXORDER] [-t MAXTASKS]

options:
  -h, --help            show this help message and exit
  -b, --bits BITS       Enter "bits" to define the size of "p", "q" in bits
  -m, --maxorder MAXORDER
                        Enter "maxorder" to define maximum order for the search
  -t, --maxtasks MAXTASKS
                        Enter "maxtasks" to define the maximum number of tasks running in parallel
"""
__author__      = 'Eduardo Marsola do Nascimento'
__copyright__   = 'Copyright 2025-04-18'
__credits__     = ''
__license__     = 'MIT'
__version__     = '1.00'
__maintainer__  = ''
__email__       = ''
__status__      = 'Production'
__printdebug__  = True
#__printdebug__  = False

import multiprocessing
import time
from datetime import datetime
from Crypto.Util import number
from Crypto.Random import random
import numpy as np
import argparse

#from decimal import *
#import matplotlib.pyplot as plt

def getPQ(bits=16, limit=0.8):
    while True:
        p = number.getPrime(bits)
        q = number.getPrime(bits)
        p,q = min(p,q),max(p,q)
        if p/q < limit:
            return p,q

def getnumberorder_smp( a, n, maxorder, csvfile, order_frequency, running_tasks, lock ):
    with lock:
        running_tasks.value += 1
        print(f"Started task {a}, running tasks: {running_tasks.value}") if __printdebug__ else None
    if maxorder == None:
        maxorder = n+1
    result = 1
    r = 1
    while r <= maxorder:
        result = (result * a)%n
        if result==1:
            break
        r += 1
    with lock:
        running_tasks.value -= 1
        if not r in order_frequency:
            order_frequency[r] = 0
        order_frequency[r] += 1
        csvfile.write(f'{a},{r}\n')
        csvfile.flush() 
        print(f"Finished task {a}, running tasks: {running_tasks.value}") if __printdebug__ else None
    return
        
def find_orders_smp( bits, maxorder, maxtasks ):
    # preparing multiprocessing
    global num_tasks, manager, lock, running_tasks
    manager = multiprocessing.Manager()
    order_frequency = manager.dict()
    lock = multiprocessing.Lock()  # To prevent race conditions
    running_tasks = multiprocessing.Value('i', 0)  # 'i' = integer
    processes = []
    #    
    p,q = getPQ(bits=bits)
    n=p*q
    print(f'')
    print(f'*** Finding orders for Z*_N ***')
    print(f'')
    print(f'Parameters: bits={bits}, p={p}, q={q}, N={n}, maxorder={maxorder}')
    print(f'')
    csvfile = open(f'data/orders_n_{n}_p_{p}_q_{q}.csv','w')
    csvfile.write('a,order\n')
    csvfile.flush() 
    R = {}
    orders_of_N = {}
    a=2
    while a<n:
        ## if a contains a factor of N, skip it
        if a%p == 0 or a%q == 0:
            a += 1
            continue
        ## Check if any process has finished
        for process in processes:
            if not process.is_alive():
                processes.remove(process)
        while running_tasks.value >= maxtasks:
            print(f"Waiting for a task to finish, running tasks: {running_tasks.value}") if __printdebug__ else None
            time.sleep(0.1)  # if maxtask reachead, wait for a task to finish before starting a new one
        ## Start a new process
        process = multiprocessing.Process(target=getnumberorder_smp, args=(a, n, maxorder, csvfile, order_frequency, running_tasks, lock))
        process.start()
        processes.append(process)
        a += 1
    # Wait for all processes to finish
    for process in processes:
        process.join()
    csvfile.close()
    csvfile = open(f'data/orders_frequency_n_{n}_p_{p}_q_{q}.csv','w')
    csvfile.write('order,frequency\n')
    for r in order_frequency.keys():
        csvfile.write(f'{r},{order_frequency[r]}\n')
    csvfile.flush() 
    return

def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--bits', help='Enter "bits" to define the size of "p", "q" in bits', type=int, default=5)
    parser.add_argument('-m','--maxorder', help='Enter "maxorder" to define maximum order for the search', type=int, default=None)
    parser.add_argument('-t','--maxtasks', help='Enter "maxtasks" to define the maximum number of tasks running in parallel', type=int, default=8)
    args = parser.parse_args()
    bits = args.bits
    maxorder = args.maxorder
    maxtasks = args.maxtasks
    find_orders_smp( bits, maxorder, maxtasks )

if __name__ == '__main__':
    # track execution time
    startTime=datetime.now()
    print(f'Start: {startTime.replace(microsecond=0)}\n\n')
    main()
    # track execution time
    finishTime=datetime.now()
    print( f'\nStart: {startTime.replace(microsecond=0)}, Finish:{finishTime.replace(microsecond=0)}, Running Time: {finishTime-startTime}')


#!/usr/bin/env python3
from datetime import datetime
import socket
import os
from mpi4py import MPI

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    rankStartTime=datetime.now()
    print(f'Rank {rank:3}/{size:3} - Start: {rankStartTime.replace(microsecond=0)}'
          f' host {socket.gethostname()} - (PID {os.getpid()})')
    
if __name__ == '__main__':
    main()
    

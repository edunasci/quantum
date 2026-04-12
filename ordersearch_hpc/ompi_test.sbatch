#!/bin/bash
#SBATCH --job-name=ordersearch_mpi
#SBATCH --partition=normal
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=1
#SBATCH --time=12:00:00
#SBATCH --mem=1G
#SBATCH --output=results_%j.out
#SBATCH --error=results_%j.err
#SBATCH --mail-user=eduardo.marsola@estudante.ufscar.br
#SBATCH --mail-type=ALL

set -eE
umask 077

module purge
module load singularity
module load gnu9
module load pmix
module load openmpi4

echo "Job iniciado em $(date)"
echo "Nós alocados:"
scontrol show hostnames $SLURM_JOB_NODELIST

echo "ID do Job: $SLURM_JOB_ID"
echo "Número de nós: $SLURM_NNODES"
echo "Número de tarefas: $SLURM_NTASKS"
echo "Tarefas por nó: $SLURM_NTASKS_PER_NODE"
echo "Diretório de trabalho: $SLURM_SUBMIT_DIR" 

# OPENMPI
# Diretórios
WORKDIR=$SLURM_SUBMIT_DIR
mpirun singularity exec \
    --bind $WORKDIR/ompi_test.py:/opt/ordersearch_hpc/ompi_test.py \
    ~/ordersearch_hpc/ubuntu_ompi_python.sif \
    python /opt/ordersearch_hpc/ompi_test.py

echo "Execução finalizada, copiando resultados para a nuvem..."

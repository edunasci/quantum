#!/bin/bash
#SBATCH --job-name=ordersearch_mpi
#SBATCH --partition=normal
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=20
#SBATCH --time=12:00:00
#SBATCH --mem=1G
#SBATCH --output=results_%j.out
#SBATCH --error=results_%j.err
#SBATCH --mail-user=eduardo.marsola@estudante.ufscar.br
#SBATCH --mail-type=ALL

set -eE

module purge
module load singularity
module load gnu9
module load openmpi4

echo "Job iniciado em $(date)"
echo "Nós alocados:"
scontrol show hostnames $SLURM_JOB_NODELIST

echo "ID do Job: $SLURM_JOB_ID"
echo "Número de nós: $SLURM_NNODES"
echo "Número de tarefas: $SLURM_NTASKS"
echo "Tarefas por nó: $SLURM_NTASKS_PER_NODE"
echo "Diretório de trabalho: $SLURM_SUBMIT_DIR" 

# Diretórios
WORKDIR=$SLURM_SUBMIT_DIR
RESULTS_DIR=$WORKDIR/results_$SLURM_JOB_ID
mkdir -p $RESULTS_DIR


# Executa MPI
mpirun singularity exec \
    --bind $WORKDIR/ordersearch_hpc.py:/opt/ordersearch_hpc/ordersearch_hpc.py \
    --bind $RESULTS_DIR:/opt/ordersearch_hpc/data \
    ~/ordersearch_hpc/ubuntu_ompi_python.sif \
    python /opt/ordersearch_hpc/ordersearch_hpc.py -b 40

echo "Execução finalizada, copiando resultados para a nuvem..."

mv results*txt $RESULTS_DIR

# Upload para Google Drive (ou outro remote)
rclone copy $RESULTS_DIR gdrive:/projects/ordersearch_hpc_results

echo "Upload concluído em $(date)"

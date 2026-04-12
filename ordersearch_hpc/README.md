# useful commands
## install singularity
sudo apt update -y && sudo apt install singularity-container -y

## verify singularity version
singularity --version

# build the container
singularity build -f ersearch.simg ordersearch.def
sudo singularity build Singularity.simg Singularity

# create the container:
sudo singularity build ubuntu_ompi_python.sif ubuntu_ompi_python.def


# rodando o batch
sbatch --test-only ordersearch_hpc.sbatch
sbatch ordersearch_hpc.sbatch
squeue -u $USER
#scontrol show job 123456
#scancel 123456


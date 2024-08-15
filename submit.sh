#!/bin/bash
#PBS -V
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=1:00:00
#PBS -q debug
#PBS -A QuantumDS
#PBS -N workflow
#PBS -l filesystems=home:eagle

module purge
module use /soft/modulefiles
module load conda
module load PrgEnv-nvhpc nvhpc cudatoolkit-standalone/11.8.0
module load cray-hdf5
module load cray-fftw


module list
conda activate pynta_env

export MPICH_GPU_SUPPORT_ENABLED=0
export EXE=/soft/applications/quantum_espresso/7.3.1-nvhpc23.1-libxc610/bin/pw.x

ldd $EXE >& exe.ld

cd $PBS_O_WORKDIR
#d /lus/eagle/projects/catalysis_aesp/raymundohe/testPyntaMultiNode
echo $PBS_O_WORKDIR

echo " ===================================  TEST  ===================================="
echo "          JobId  : $PBS_JOBID"
echo "Running on host  : `hostname`"
echo "Running on nodes : `cat $PBS_NODEFILE`"
echo "numactl -H"
numactl -H
echo " ===================================  TEST  ===================================="

export OMP_NUM_THREADS=1
export OMP_PLACES=threads
export OMP_PROC_BIND=spread
#export OMP_DISPLAY_AFFINITY=true

echo -n " Starting  :"
date

cat $PBS_NODEFILE  > nodes.txt


myhost=()
nproc=0
while IFS= read -r line
do
  myhost+=($line)
  ((nproc=nproc+1))

done < $PBS_NODEFILE

for host in "${myhost[@]}"
do
        pbs_tmrsh $host /bin/bash -c 'echo "node = `hostname`"'
done

echo `pwd`


#python3  runPynta.py
python3  test_OPT2.py

echo " ===================================  DONE  ===================================="
echo -n " Finishing :"
date

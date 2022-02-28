.. _hpc-setup:


Setting up VeloxChem on a HPC cluster
=====================================

.. objectives::

   - Learn how to use the VeloxChem module on Dardel.

.. keypoints::

   - VeloxChem and its Python dependencies are installed in a virtual environment.


Dardel (PDC)
^^^^^^^^^^^^

`Dardel <https://www.pdc.kth.se/hpc-services/computing-systems/about-dardel-1.1053338>`_
is a Cray XE system at `PDC <https://www.pdc.kth.se/>`_.

VeloxChem is available as a module on Dardel::

  $ module load PDC/21.11
  $ module load veloxchem/1.0dev

Example submission script::

  #!/bin/bash

  #SBATCH -J myjob
  #SBATCH -t 01:00:00
  #SBATCH -p main
  #SBATCH -A edu22.veloxchem
  #SBATCH --reservation velox-lab1

  #SBATCH --nodes=1
  #SBATCH --ntasks-per-node=8

  module load PDC/21.11
  module load veloxchem/1.0dev

  export OMP_NUM_THREADS=16
  export OMP_PLACES=cores

  job=porphyrin
  srun vlx ${job}.inp ${job}.out

.. note::

   There are two ways to log in to Dardel.

   - If you have a SUPR account, you can choose to log in using SSH key pairs.
     See `How to login in with SSH keys
     <https://www.pdc.kth.se/support/documents/login/ssh_login.html>`_

   - If you don't have a SUPR account, or do not know what SUPR is, you can
     log in using a Kerberos ticket. See `How to Login with kerberos
     <https://www.pdc.kth.se/support/documents/login/login.html>`_


Exercise
^^^^^^^^

The purpose of the exercise is to check that your VeloxChem can run a simple
calculation.  You can test with the `cpp.inp
<https://gitlab.com/veloxchem/veloxchem/-/raw/master/docs/inputs/cpp.inp>`_
file.

- On Dardel::

    salloc -N 1 --ntasks-per-node 8 -t 00:20:00 -p main -A edu22.veloxchem --reservation velox-lab1
    module load PDC/21.11 veloxchem/1.0dev
    export OMP_NUM_THREADS=16
    export OMP_PLACES=cores
    wget https://gitlab.com/veloxchem/veloxchem/-/raw/master/docs/inputs/cpp.inp
    srun vlx cpp.inp
    exit

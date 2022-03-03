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

   - There are two ways to log in to Dardel.

     - If you have a SUPR account, you can choose to log in using SSH key pairs.
       See `How to login in with SSH keys
       <https://www.pdc.kth.se/support/documents/login/ssh_login.html>`_

     - If you don't have a SUPR account, or do not know what SUPR is, you can
       log in using a Kerberos ticket. See `How to Login with kerberos
       <https://www.pdc.kth.se/support/documents/login/login.html>`_

   - The time allocation for the workshop is ``edu22.veloxchem``

     - For the first day we can use the reservation ``velox-lab1``

     - For the second day we can use the reservation ``velox-lab2``


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


.. _linrsp-analysis:

Script for analyzing singlet excitations from linear response output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from pathlib import Path
   import numpy as np
   import h5py
   import sys

   out_file = Path(sys.argv[1])
   rsp_file = out_file.with_suffix('.rsp.solutions.h5')

   # threshold for priting excitations

   coef_thresh = 0.1

   # read output file for number of occupied and virtual orbitals

   nocc, n_ao = None, None
   n_lindep = 0

   with out_file.open('r') as f_out:
       for line in f_out:
           if 'Number of alpha electrons   :' in line:
               nocc = int(line.split(':')[1].split()[0])
           if 'Contracted Basis Functions :' in line:
               n_ao = int(line.split(':')[1].split()[0])
           if 'Removed' in line and 'linearly dependent vectors' in line:
               n_lindep = int(line.split('Removed')[1].split()[0])

   n_mo = n_ao - n_lindep
   nvir = n_mo - nocc
   n_ov = nocc * nvir

   # read hdf5 file for excitations

   hf = h5py.File(str(rsp_file), 'r')
   keys = list(hf.keys())

   state = 0
   while True:
       state += 1
       key = f'S{state}'
       if key not in keys:
           break
       array = np.array(hf.get(key))
       assert array.size == n_ov * 2

       excitations = []
       de_excitations = []

       for i in range(nocc):
           for a in range(nvir):
               ia = i * nvir + a
               exc_coef = array[ia]
               de_exc_coef = array[n_ov + ia]

               homo = f'HOMO-{nocc-1-i}' if i != nocc - 1 else 'HOMO'
               lumo = f'LUMO+{a}' if a != 0 else 'LUMO'

               if abs(exc_coef) > coef_thresh:
                   excitations.append((
                       abs(exc_coef),
                       f'{homo:<8s} -> {lumo:<8s} {exc_coef:10.4f}',
                   ))

               if abs(de_exc_coef) > coef_thresh:
                   de_excitations.append((
                       abs(de_exc_coef),
                       f'{homo:<8s} <- {lumo:<8s} {de_exc_coef:10.4f}',
                   ))

       print(f'S{state}:')
       for exc in sorted(excitations, reverse=True):
           print('  ', exc[1])
       for de_exc in sorted(de_excitations, reverse=True):
           print('  ', de_exc[1])

   hf.close()

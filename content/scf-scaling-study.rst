.. _scf-scaling-study:


Scaling study: self-consistent field calculations
=================================================

.. objectives::

   - Learn how to run a self-consistent field (SCF) calculation.

.. keypoints::

   - Run a SCF calculation.
   - Perform scaling test of the SCF calculation.


In this exercise we will run self-consistent field (SCF) calculations
of zinc-porphyrin and oligomers of guanine.

An SCF calculation consists essentially of three parts:

#. Initial guess for the density matrix :math:`\mathbf{D}`,
#. Formation of the Fock matrix:

   .. math::

      F_{\mu\nu} = h_{\mu\nu} + \sum_{\kappa\lambda} \left[ 2(\mu\nu|\kappa\lambda) - (\mu\kappa|\nu\lambda) \right]D_{\lambda\kappa}

   by assembling one-electron:

   .. math::

      h_{\mu\nu} =
      \left\langle
      \chi_{\mu}
      \left| -\frac{1}{2}\nabla^{2} -\sum_{A=1}^{N_\mathrm{at}} \frac{Z_{A}}{|\mathbf{R}_A - \mathbf{r}|} \right|
      \chi_{\nu}
      \right\rangle

   and two-electron integrals:

   .. math::

      (\mu\nu|\kappa\lambda) =
      \left\langle
      \chi_{\mu}(\mathbf{r})\chi_{\nu}(\mathbf{r})
      \left| \frac{1}{|\mathbf{r} - \mathbf{r}^{\prime}|} \right|
      \chi_{\kappa}(\mathbf{r}^{\prime})\chi_{\lambda}(\mathbf{r}^{\prime})
      \right\rangle

#. Diagonalization of Fock matrix and formation of new density matrix.

While the last step formally scales with the *third power* of the dimension of
the Fock matrix, it is usually the formation of the matrix itself in step 2
that is the most time-consuming.
The formation of the Fock matrix and in particular the computation of the
electron-repulsion integrals (ERIs) are natural targets for code optimization
and parallelization.

.. figure:: img/rh-scf.svg
   :align: center
   :scale: 80%

   A schematic view of the SCF algorithm. The formation of the Fock matrix is
   the most time-consuming step in the algorithm.

VeloxChem adopts a **hybrid MPI+OpenMP** parallelization strategy to achieve
efficient Fock builds:

- We spread the workload across multiple **nodes** using the `message passing
  interface (MPI) <https://en.wikipedia.org/wiki/Message_Passing_Interface>`_.
  In this context, a node might be a machine in a blade, a socket, or a NUMA
  domain.
- On each node, we spawn multiple **threads** using `OpenMP
  <https://en.wikipedia.org/wiki/OpenMP>`_. All threads share the memory space
  on the node.

In contrast, the first and third steps are carried out using OpenMP threading on
a single MPI process. [*]_

In this exercise, we want to explore three aspects of the SCF code in VeloxChem:

#. Its **strong scaling**: how does the time-to-solution change for a fixed-size
   problem using an increasing number of workers?  We will use a zinc-porphyrin
   system for this investigation.
#. Its **weak scaling**: how does the time-to-solution change when both the
   workload and the number of workers increase? Note that the workload of an
   SCF calculation increases nonlinearly with respect to the number of basis 
   functions. We will use a series of guanine oligomers for this purpose.
#. How do MPI and OpenMP settings affect the performance of SCF calculation on
   a single node?

Systems and input files
-----------------------

Below is the input file for SCF calculation of zinc porphyrin and guanine oligomers.
You can read more about the VeloxChem input keywords in
`this page <https://veloxchem.org/docs/keywords.html>`_.

The ``timing`` input option in the SCF section will print out a detailed
breakdown of the time spent within each task of every SCF iteration:

.. literalinclude:: inputs/zn-ph.inp
   :emphasize-lines: 9-11
   :lines: 1-16

Zinc porphyrin
  You can download the full input file with:

  .. code-block:: shell

     wget https://raw.githubusercontent.com/ENCCS/veloxchem-hpc/main/content/inputs/zn-ph.inp

  .. raw:: html

     <div style="height: 400px; width: 600px; position: relative;" class='viewer_3Dmoljs' data-href='_static/zn-ph.xyz' data-type='xyz' data-backgroundcolor='0xffffff' data-style='stick'></div>

Guanine oligomers
  You can download the full input files with:

  .. code-block:: shell

     wget https://raw.githubusercontent.com/ENCCS/veloxchem-hpc/main/content/inputs/g{1,2,3,4}.inp

  .. raw:: html

     <div style="height: 400px; width: 600px; position: relative;" class='viewer_3Dmoljs' data-href='_static/g4.xyz' data-type='xyz' data-backgroundcolor='0xffffff' data-style='stick'></div>

Using the SLURM scheduler
~~~~~~~~~~~~~~~~~~~~~~~~~

Dardel, as virtually all modern HPC clusters, uses `SLURM
<https://slurm.schedmd.com/overview.html>`_ as its job scheduler.

A sample submission script:

.. code-block:: shell
   :linenos:
   :emphasize-lines: 4,5,9-10,15-16

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

- **Line 4** sets the limit on the total runtime of the job allocation.
- **Line 5** specifies which *partition* to be used. `Check here
  <https://www.pdc.kth.se/support/documents/run_jobs/job_scheduling.html#dardel-partitions>`_
  for the partitions available on Dardel.
- **Lines 9 and 10** request computational resources:

  - each node consists of **two** AMD EPYC 7742 CPUs, since nodes are
    dual-socket on Dardel.
  - on each node, we spawn 8 MPI ranks: 4 per socket, since ``numactl
    --hardware`` showed that each socket is in NPS-4 configuration.

  Thus 8 is the number of MPI ranks which will be used in the calculation.
- **Line 15** tells to use 16 OpenMP threads on each MPI rank. This ensures
  full usage of all cores in the given NUMA domain/MPI rank.
- Finally, **line 16** specifies that threads should be mapped to the cores.

This sample script will use a single node on Dardel:

.. math::

   \text{1 node} \times \text{8 MPI ranks per node} \times \text{16 OpenMP threads per rank} = \text{128 cores on a node}

Exercise
--------

We are going to plot speedup (or scaled speedup) with respect to the number of
nodes used. VeloxChem prints out the total execution time at the end of each
output file:

.. code-block:: text

   !========================================================================================================================!
   !                               VeloxChem execution completed at Wed Mar  2 10:51:14 2022.                               !
   !========================================================================================================================!
   !                                          Total execution time is 111.56 sec.                                           !
   !========================================================================================================================!

With the ``timing`` option set to ``yes`` in the input file, you will also get a
detailed breakdown of timings in each SCF iteration:

.. code-block:: text

   Timing (in sec)
   ---------------
                         FockBuild          ERI   CompEnergy     FockDiag
   Iteration 1                3.12         3.12         0.04         0.44
   Iteration 2                3.50         3.50         0.04         0.48
   Iteration 3                3.50         3.50         0.04         0.52
   Iteration 4                3.88         3.88         0.04         0.55
   Iteration 5                3.88         3.88         0.04         0.58
   Iteration 6                3.87         3.87         0.04         0.63
   Iteration 7                3.88         3.88         0.04         0.68
   Iteration 8                3.87         3.87         0.04         0.74
   Iteration 9                3.88         3.87         0.04         0.79
   Iteration 10               3.88         3.88         0.04         0.79
   Iteration 11               3.88         3.88         0.04         0.81
   Iteration 12               3.87         3.87         0.04         0.81
   Iteration 13               3.87         3.87         0.04         0.81
   Iteration 14               3.87         3.87         0.04         0.81
   Iteration 15               3.87         3.87         0.04         0.80
   Iteration 16               3.88         3.88         0.04         0.81
   Iteration 17               3.87         3.87         0.04         0.81
   Iteration 18               3.87         3.87         0.04         0.84
   Iteration 19               3.88         3.88         0.04         0.82
   Iteration 20               3.87         3.87         0.04


.. tabs::

   .. tab:: Strong scaling: zinc porphyrin

      #. Run the zinc porphyrin example on 1, 2, 3 and 4 nodes.
         Use 8 MPI ranks per node and 16 OpenMP threads per rank.
      #. Gather total execution times from the output files and plot the speedup
         against the number of nodes.
      #. Gather the breakout of timings per SCF iteration from the output files.
         Plot the speedup of ``FockBuild`` with respect to the
         number of nodes.

   .. tab:: Weak scaling: guanine oligomers

      #. Run the guanine monomer (``g1.inp``), dimer (``g2.inp``), trimer
         (``g3.inp``), and tetramer (``g4.inp``) on 1, 2, 3, and 4 nodes,
         respectively.
         Use 8 MPI ranks per node and 16 OpenMP threads per rank.
      #. Gather total execution times from the output files and plot the
         computational cost (taking into account number of nodes) against 
         the number of basis functions. Use logarithm scale on both axes.
      #. Gather the breakout of timings per SCF iteration from the output files.
         Plot the computational cost of ``FockBuild`` with respect to the number
         of basis functions.

   .. tab:: MPI+OpenMP usage

      Run the zinc porphyrin example:

      #. Compare the total execution time and the timings for ``FockBuild``
         obtained using:

         - 1 node, 8 MPI ranks, 16 OpenMP threads
         - 1 node, 2 MPI ranks, 64 OpenMP threads

           .. code-block:: shell

              #SBATCH --nodes=1
              #SBATCH --ntasks-per-node=2
              #SBATCH --cpus-per-task=128  # 64x2 because of SMT

              export OMP_NUM_THREADS=64
              export OMP_PLACES=cores

         Both calculation setups use one full node on Dardel, but they are not
         equally efficient. What might make it so?

.. callout:: Plotting your results

   You can adapt this sample script.

   .. code-block:: python

      import numpy as np
      import plotly.graph_objs as go

      # insert your data!
      nnodes = np.array([1, 2, 3, 4])

      # insert your data!
      timings = np.array([1, 2, 3, 4])
      speedup = timings[0] / timings

      fig = go.Figure()

      fig.add_trace(
          go.Scatter(
              name=f"SCF",
              x=nnodes,
              y=speedup,
              mode="lines+markers",
              hovertemplate="~%{y:.2f}x<extra></extra>",
          )
      )

      fig.update_layout(
          title="SCF Speedup",
          xaxis_title="Number of nodes",
          yaxis_title="Speedup",
          height=500,
          width=600,
      )

.. [*] MPI processes are usually also called ranks.

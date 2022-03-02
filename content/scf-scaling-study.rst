.. _scf-scaling-study:


Scaling study: self-consistent field calculation
================================================

.. objectives::

   - Learn how to run a self-consistent field (SCF) calculation.

.. keypoints::

   - Run a SCF calculation.
   - Perform scaling test of the SCF calculation.


Introduction
------------

In this exercise we will run self-consistent field (SCF) calculations
of zinc-porphyrin and oligomers of guanine.

An SCF calculation consists of three parts: 1) initial guess for density matrix,
2) formation of Fock matrix, and 3) diagonalization of Fock matrix and formation
of new density matrix. Step 2 usually takes most of the time and is therefore the
natural target for code optimization. In VeloxChem, efficient Fock build is achieved
by means of hybrid MPI/OpenMP parallelization. Steps 1 and 3, on the other hand,
are carried out on a single MPI process with OpenMP parallelization.

In this exercise, we'll examine the scaling of SCF calculation using two examples.
The first example is zinc-porphyrin that can be used for strong scaling, see :ref:`amdahl`.
The second example is guanine oligomer that can be use for weak scaling, see :ref:`gustafson`.

Input files
-----------

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

Guanine monomer, dimer, trimer and tetramer
  You can download the full input files with:

  .. code-block:: shell

     wget https://raw.githubusercontent.com/ENCCS/veloxchem-hpc/main/content/inputs/g{1,2,3,4}.inp

  .. raw:: html

     <div style="height: 400px; width: 400px; position: relative;" class='viewer_3Dmoljs' data-href='_static/g4.xyz' data-type='xyz' data-backgroundcolor='0xffffff' data-style='stick'></div>


Exercise
--------

- Zinc porphyrin

    Run the zinc porphyrin example on 1, 2, 3 and 4 nodes.
    Plot the speedup with respect to the number of nodes.

- Guanine oligomer

    Run guanine monomer, dimer, trimer and tetramer on 1, 2, 3 and 4 nodes,
    respectively. Plot the computational cost with respect to the number of
    basis functions.

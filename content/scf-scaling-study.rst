.. _scf-scaling-study:


Scaling study: self-consistent field calculation
================================================

.. objectives::

   - Learn how to run a self-consistent field (SCF) calculation.

.. keypoints::

   - Run a SCF calculation.
   - Perform scalability test of the SCF calculation.


Introduction
------------

In this exercise we will run self-consisten field (SCF) calculations
of zinc-porphyrin and oligomers of guanine.

An SCF calculation consists of three parts: 1) initial guess for density matrix,
2) formation of Fock matrix, and 3) diagonalization of Fock matrix and formation
of new density matrix. Step 2 usually takes most of the time and is therefore the
natural target for code optimization. In VeloxChem, efficient Fock build is achieved
by means of hybrid MPI/OpenMP parallelization. Steps 1 and 3, on the other hand,
are carried out on a single MPI process with OpenMP parallelization.

In this exercise, we'll examine the scaling of SCF calculation using two examples.
The first example is zinc-porphyrin that can be used for strong scaling.
The second example is guanine oligomer that can be use for weak scaling.

Input file
----------

Below is the input file for SCF calculation of zinc porphyrin and guanine oligomers.
You can read more about the VeloxChem input keywords in
`this page <https://veloxchem.org/docs/keywords.html>`_.

- Zinc porphyrin

.. literalinclude:: inputs/porphyrin.inp
   :emphasize-lines: 9-12

- Guanine monomer, dimer, trimer and tetramer

.. literalinclude:: inputs/g1.inp

.. literalinclude:: inputs/g2.inp

.. literalinclude:: inputs/g3.inp

.. literalinclude:: inputs/g4.inp


Exercise
--------

- Zinc porphyrin

    Run the zinc porphyrin example on 1, 2, 3 and 4 nodes.
    Plot the speedup with respect to the number of nodes.

- Guanine oligomer

    Run guanine monomer, dimer, trimer and tetramer on 1, 2, 3 and 4 nodes,
    respectively. Plot the computational cost with respect to the number of
    basis functions.

.. _linrsp-scaling-study:


Scaling study: excitation energies with linear response
=======================================================

.. objectives::

   - Learn how to run a linear response calculation for excitation energies.

.. keypoints::

   - Run a linear response calculation for excitation energies.
   - Perform scaling test of the linear response calculation.


Introduction
------------

In this exercise we will run linear response calculation for excitation energies,
using the same examples as in the SCF exercises.

Input file
----------

Below is the input file for linear response calculation of zinc porphyrin.
You can read more about the VeloxChem input keywords in
`this page <https://veloxchem.org/docs/keywords.html>`_.

- Zinc porphyrin

.. literalinclude:: inputs/zn-ph-linrsp.inp


Exercise
--------

- Zinc porphyrin

    Run the zinc porphyrin example on 2, 4, 6 and 8 nodes.
    Plot the speedup with respect to the number of nodes.

- Guanine oligomer

    Run guanine monomer, dimer, trimer and tetramer on 2, 4, 6 and 8 nodes,
    respectively. Plot the computational cost with respect to the number of
    basis functions.

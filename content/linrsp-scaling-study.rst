.. _linrsp-scaling-study:


Scaling study: excitation energies with linear response
=======================================================

.. objectives::

   - Learn how to run a linear response calculation for excitation energies.

.. keypoints::

   - Run a linear response calculation for excitation energies.
   - Perform scaling test of the linear response calculation.


In this exercise we will run linear response calculation for excitation
energies, using the same examples as in the SCF exercises.

We aim to solve the following *generalized* eigenvalue problem:

.. math::

   \begin{equation}
    \begin{pmatrix}
      \mathbf{A} & \mathbf{B} \\
      \mathbf{B}^{*} & \mathbf{A}^{*}
    \end{pmatrix}
    \begin{pmatrix}
      \mathbf{X}_{n} \\
      \mathbf{Y}_{n}
    \end{pmatrix}
    =
    \omega_{n}
    \begin{pmatrix}
      \mathbf{1} & \mathbf{0} \\
      \mathbf{0} & -\mathbf{1}
    \end{pmatrix}
  \begin{pmatrix}
    \mathbf{X}_{n} \\
    \mathbf{Y}_{n}
  \end{pmatrix}.
  \end{equation}

The eigenvalues :math:`\omega_{n}` are the excitation energies.

The :math:`\mathbf{A}` and :math:`\mathbf{B}` matrices appearing on the left-hand side are
the blocks of the molecular electronic Hessian:

.. math::

   \begin{equation}
   \begin{aligned}
   A_{aibj} &= \delta_{ij}f_{ab} - \delta_{ab}f_{ij} + (ai|jb) - (ab|ji) \\
   B_{aibj} &= (ai|bj) - (aj|ib) \\
   \end{aligned}
   \end{equation}

whose dimensionality is :math:`(OV)^{2}`, with :math:`O` and :math:`V` the
number of occupied and virtual molecular orbitals, respectively.
This prevents *explicit* formation of the full Hessian, and subspace iteration
methods need to be used to extract the first few roots.
In such methods, the eigenvectors :math:`\begin{pmatrix} \mathbf{X}_{n} \\ \mathbf{Y}_{n} \end{pmatrix}` are expanded in a subspace of trial vectors,
whose dimensionality is much lower than that of the full eigenproblem.
The Hessian is projected down to this subspace where conventional full
diagonalization algorithms can be applied. The subspace is augmented with new
trial vectors, until a suitable convergence criterion is met.
The efficiency of the subspace solver is determined by the first half-projection
of the Hessian in the trial subspace, that is, by the efficiency of the routines
performing the matrix-vector products.
In VeloxChem, these routines are implemented as the construction of multiple
Fock matrices in which the ERIs are contracted with perturbed density matrices.

Systems and input files
-----------------------

We will re-use the same systems as for the SCF scaling study.
As detailed in `this page <https://veloxchem.org/docs/keywords.html>`_, we add a response task to the input to calculate 5 excited states:

.. literalinclude:: inputs/zn-ph-linrsp.inp
   :lines: 1-3

.. literalinclude:: inputs/zn-ph-linrsp.inp
   :lines: 9-13

We can set the ``timing`` option in the response section as well, in order to obtain a detailed breakdown of the time spent within each task in the calculation.

You can download the full input files with:

.. code-block:: shell

   wget https://raw.githubusercontent.com/ENCCS/veloxchem-hpc/main/content/inputs/zn-ph-linrsp.inp
   wget https://raw.githubusercontent.com/ENCCS/veloxchem-hpc/main/content/inputs/g{1,2,3,4}-linrsp.inp

Exercise
--------

.. tabs::

   .. tab:: Strong scaling: zinc porphyrin

      #. Run the zinc porphyrin example on 2, 4, 6, and 8 nodes.
         Use 8 MPI ranks per node and 16 OpenMP threads per rank.
      #. Gather total execution times from the output files and plot the speedup
         against the number of nodes.

   .. tab:: Scaling of linear response: guanine oligomers

      #. Run the guanine monomer (``g1.inp``), dimer (``g2.inp``), trimer
         (``g3.inp``), and tetramer (``g4.inp``) on 2, 4, 6, and 8 nodes,
         respectively.
         Use 8 MPI ranks per node and 16 OpenMP threads per rank.
      #. Gather total execution times from the output files and plot the 
         computational cost (taking into account number of nodes) 
         against the number of basis functions. Use logarithm on both axes.


.. callout:: Plotting your results

   You can launch a `MyBinder instance
   <https://mybinder.org/v2/gh/ENCCS/veloxchem-hpc/main?urlpath=lab%2Ftree%2Fcontent%2Fnotebooks>`_
   to analyze your results in a Jupyter notebook.  You can adapt this sample
   script.

   .. code-block:: python

      import numpy as np
      import plotly.graph_objects as go
      from scipy import stats

      # insert your data!
      nnodes = np.array([1, 2, 3, 4])

      # insert your data!
      timings = np.array([1, 0.6, 0.4, 0.35])
      speedup = timings[0] / timings

      fig = go.Figure()

      fig.add_trace(
          go.Scatter(
              name=f"SCF",
              x=nnodes,
              y=speedup,
              mode="markers",
              hovertemplate="~%{y:.2f}x<extra></extra>",
          )
      )

      # generate linear fit
      slope, intercept, r_value, p_value, std_err = stats.linregress(nnodes, speedup)
      line = slope * nnodes + intercept

      fig.add_trace(
          go.Scatter(
              x=nnodes,
              y=line,
              mode="lines",
              name=f"Fit: y = {slope:.3f}x + {intercept:.3f}",
          )
      )

      fig.update_layout(
          title="SCF Speedup",
          xaxis_title="Number of nodes",
          yaxis_title="Speedup",
          height=500,
          width=600,
      )

      fig.show()

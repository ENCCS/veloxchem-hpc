.. _linrsp-scaling-study:


Scaling study: excitation energies with linear response
=======================================================

.. objectives::

   - Learn how to run a linear response calculation for excitation energies.

.. keypoints::

   - Run a linear response calculation for excitation energies.
   - Perform scaling test of the linear response calculation.


In this exercise we will run linear response calculations for excitation
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

      #. Gather execution times of linear response from the output 
         files and plot the speedup against the number of nodes.

         .. code-block:: shell

            grep 'Linear response converged' zn-ph-linrsp.out

      #. Gather the breakout of timings per linear response iteration 
         from the output files. Plot the speedup of ``ERI`` with 
         respect to the number of nodes.

   .. tab:: Scaling of linear response: guanine oligomers

      #. Run the guanine monomer (``g1.inp``), dimer (``g2.inp``), trimer
         (``g3.inp``), and tetramer (``g4.inp``) on 2, 4, 6, and 8 nodes,
         respectively.
         Use 8 MPI ranks per node and 16 OpenMP threads per rank.

      #. Gather execution times of linear response from the output files 
         and plot the computational cost (taking into account number of 
         nodes) against the number of basis functions. Use logarithm on 
         both axes.

         .. code-block:: shell

            grep 'Linear response converged' g?-linrsp.out

      #. Gather the breakout of timings per linear response iteration from 
         the output files. Plot the computational cost of ``ERI`` with 
         respect to the number of basis functions.

   .. tab:: Analysis of linear response output

      #. Extract important excitations from linear response output files.
         Use the python script from :ref:`this page <linrsp-analysis>`.

         .. code-block:: shell

            ml PDC/21.11 Anaconda3/2021.05 vim/8.2
            python3 analyze_response_output.py zn-ph.out


.. callout:: Plotting your results

   You can launch a `MyBinder instance
   <https://mybinder.org/v2/gh/ENCCS/veloxchem-hpc/main?urlpath=lab%2Ftree%2Fcontent%2Fnotebooks>`_
   to analyze your results in a Jupyter notebook.  You can adapt this sample
   script.

   .. code-block:: python

      # example script for strong scaling

      import numpy as np
      import plotly.graph_objects as go

      # insert your data!
      nnodes = np.array([1, 2, 3, 4])

      # insert your data!
      timings = np.array([10, 6, 4.5, 4])
      speedup = timings[0] / timings

      fig = go.Figure()

      fig.add_trace(
          go.Scatter(
              name=f"Linear response",
              x=nnodes,
              y=speedup,
              mode="lines+markers",
              hovertemplate="~%{y:.2f}x<extra></extra>",
          )
      )

      fig.update_layout(
          title="Linear response speedup",
          xaxis_title="Number of nodes",
          yaxis_title="Speedup",
          height=500,
          width=600,
      )

      fig.show()


   .. code-block:: python

      # example script for scaling of linear response

      import numpy as np
      import plotly.graph_objects as go
      from scipy import stats

      # insert your data!
      nbfs = np.array([258, 516, 774, 1032])

      # insert your data!
      nnodes = np.array([1, 2, 3, 4])

      # insert your data!
      timings = np.array([3.5, 8, 15, 26])
      cost = timings * nnodes

      log_x = np.log(nbfs)
      log_y = np.log(cost)

      # generate linear fit
      slope, intercept, r_value, p_value, std_err = stats.linregress(log_x, log_y)
      fit_y = np.exp(slope * log_x + intercept)

      fig = go.Figure()

      fig.add_trace(
          go.Scatter(
              x=nbfs,
              y=fit_y,
              mode="lines",
              name=f"O(N^{slope:.3f})",
          )
      )

      fig.add_trace(
          go.Scatter(
              name="Linear response",
              x=nbfs,
              y=cost,
              mode="markers",
          )
      )

      fig.update_layout(
          title="Scaling of linear response",
          xaxis_title="Number of basis functions",
          yaxis_title="Computational cost",
          height=500,
          width=600,
      )

      fig.update_xaxes(type="log")
      fig.update_yaxes(type="log")

      fig.show()

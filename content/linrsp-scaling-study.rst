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

   .. tab:: Weak scaling: guanine oligomers

      #. Run the guanine monomer (``g1.inp``), dimer (``g2.inp``), trimer
         (``g3.inp``), and tetramer (``g4.inp``) on 2, 4, 6, and 8 nodes,
         respectively.
         Use 8 MPI ranks per node and 16 OpenMP threads per rank.
      #. Gather total execution times from the output files and plot the 
         computational cost (taking into account number of nodes) 
         against the number of basis functions. Use logarithm on both axes.


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
              name=f"Excitation energies",
              x=nnodes,
              y=speedup,
              mode="lines+markers",
              hovertemplate="~%{y:.2f}x<extra></extra>",
          )
      )

      fig.update_layout(
          title="Excitation energies speedup",
          xaxis_title="Number of nodes",
          yaxis_title="Speedup",
          height=500,
          width=600,
      )

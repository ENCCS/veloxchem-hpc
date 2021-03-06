.. _x-ray-cpp:


Complex polarization propagator in the X-ray region
===================================================

.. objectives::

   - Learn how to run a complex polarization propagator (CPP) calculation.

.. keypoints::

   - Run a CPP calculation.
   - Plot the absorption spectrum.
   - Perform scalability test of the CPP calculation.

Introduction
------------

In this exercise we will use an efficient implementation of the complex
polarization propagator approach (CPP) to compute the near-edge X-ray
absorption fine-structure spectrum of free-base porphyrin.

Conventional response theory solves a generalized eigenvalue problem and
provides excitation energies starting from the lowest excited states. It is therefore
impractical to study spectral regions with high density-of-states. The CPP
approach introduces a damping term which, from a purely computational
perspective, removes the singularities of the response functions at resonance
frequencies. The damped response theory can be applied to any frequency region
of interest. You may read more in `this paper <https://pubs.acs.org/doi/10.1021/ct500114m>`_ :cite:`Kauczor2014-vg`

The CPP solver in VeloxChem will solve multiple frequencies simultaneously. The
complex response equations for a given frequency can be expressed in terms of a
coupled set of linear equations for a real symmetric matrix


.. math::

   \begin{pmatrix}
    E^{[2]} & -\omega S^{[2]}  & \gamma S^{[2]}  & 0 \\
    -\omega S^{[2]} & E^{[2]} & 0 & \gamma S^{[2]} \\
    \gamma S^{[2]} & 0 & -E^{[2]} &\omega S^{[2]} \\
    0 & \gamma S^{[2]}  & \omega S^{[2]} & -E^{[2]}
   \end{pmatrix}
   \begin{pmatrix}
   X^R_g\\
   X^R_u\\
   X^I_u\\
   X^I_g
   \end{pmatrix} =
   \begin{pmatrix}
   G^R_g\\
   G^R_u\\
   -G^I_u\\
   -G^I_g
   \end{pmatrix}

Here, :math:`\omega` is the frequency, :math:`\gamma` is the damping parameter, :math:`E^{[2]}`
and :math:`S^{[2]}` are the Hessian and metric matrices, respectively, and :math:`G` is the
gradient vector. The :math:`R`/:math:`I` superscripts denote real/imaginary components,
while the :math:`g`/:math:`u` subscripts denote *gerade*/*ungerade* symmetry.


System: free-base porphyrin
---------------------------

.. raw:: html

   <div style="height: 400px; width: 600px; position: relative;" class='viewer_3Dmoljs' data-href='_static/porphyrin.xyz' data-type='xyz' data-backgroundcolor='0xffffff' data-style='stick'></div>


Input file
----------

Below is the input file for a CPP calculation of free-base porphyrin.
You can read more about the VeloxChem input keywords in
`this page <https://veloxchem.org/docs/keywords.html>`_.

.. literalinclude:: inputs/porphyrin.inp
   :emphasize-lines: 9-12

You can download it with:

.. code-block:: shell

   wget https://raw.githubusercontent.com/ENCCS/veloxchem-hpc/main/content/inputs/porphyrin.inp

You can set the ``timing`` keyword in the response group if you
want to look at a breakdown of the total time by specific sub-tasks in the
calculation.

Exercise
--------

- Submit a job

    Runs the above example on 2 nodes.
    On Dardel this will take around 2 minutes.

- Plot and analyse the spectrum

    The absorption spectrum will be printed at the end of the output file.
    Compare this to the results provided in `this Jupyter notebook on MyBinder
    <https://mybinder.org/v2/gh/ENCCS/veloxchem-hpc/main?urlpath=lab%2Ftree%2Fcontent%2Fnotebooks%2Fcpp_analysis%2Fvlx_cpp.ipynb>`_,
    where analysis of polarization dependence and the association of features
    to chemically unique atoms is also available. Results for a smaller system
    (vinylfluoride) are also available.
    
- Investigate strong scalability for the CPP workload

    Run the CPP calculation on different number of nodes.
    Plot the speedup with respect to the number of nodes.


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

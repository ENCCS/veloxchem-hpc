.. _exciton:


Exciton calculation
===================

.. objectives::

   - Learn how to run an *ab initio* exciton model calculation.

.. keypoints::

   - Run an *ab initio* exciton model calculation.
   - Plot the UV-Vis absorption and ECD spectra.
   - Analyze the character of the excitations.

Introduction
------------

In this exercise we will use an *ab initio* exciton model to compute
the UV-Vis absorption and electronic ciruclar dichroism (ECD) of
oligothiophene self-assembly.

The Frenkel exciton model describes the electronic structure of
multi-chromophoric system by dividing the system into subgroups.
It has been most successful in the weak-coupling limit where
the excitons are localized on inidividual chromophores.
The *ab initio* exciton model expands the Frenkel exciton model by
taking into account charge-transfer between the chromophores, and
is therefore more useful for studies of singly excited states.
You may read more in `this paper <https://pubs.acs.org/doi/abs/10.1021/acs.jctc.7b00171>`_
:cite:`Li2017-eq`.

In the exciton model, the Hamiltonian adopts the following matrix form

.. math::

   \mathbf{H} =
   \sum_I^N E_I |\phi_I\rangle \langle \phi_I| +
   \sum_{I \ne J}^N V_{IJ} |\phi_I\rangle \langle \phi_J|

where :math:`N` is the total number of excited states, :math:`\phi_I` is
the :math:`I`-th excitonic basis function, and :math:`E` and :math:`V` are the
excitation energies and couplings, respectively.
Diagonalization of the Hamiltonian gives the eigenvalues and
eigenvectors for the excited states.

System: oligothiophene self-assembly
------------------------------------

.. raw:: html

   <div style="height: 400px; width: 600px; position: relative;" class='viewer_3Dmoljs' data-href='_static/hexamer.xyz' data-type='xyz' data-backgroundcolor='0xffffff' data-style='stick'></div>


Input file
----------

Below is the input file for *ab initio* exciton model calculation of oligothiophene
self-assembly. You can read more about the input keywords in
`this page <https://docs.veloxchem.org/inputs/keywords.html#the-exciton-group>`_.

.. literalinclude:: inputs/hexamer.inp
   :emphasize-lines: 9-15

Exercise
--------

- Submit a job

    Runs the above example.
    On Dardel this calculation takes around 10 minutes on
    2 nodes. You can choose to run on more nodes.

- Plot the spectrum

    The excitation energies, oscillator strengths, and rotatory strengths will be
    printed at the end of the output file.
    You can plot the UV-Vis and ECD spectra by line broadening using e.g.
    `Gaussian function <https://en.wikipedia.org/wiki/Gaussian_function>`_.

    .. code-block:: python

       import numpy as np
       import plotly.graph_objects as go

       def gaussian(x, y, xmin, xmax, xstep, sigma):
           """Gaussian broadening function

           Call: xi,yi = gaussian(energies, intensities, start energy, end energy, energy step, gamma)
           """

           xi = np.arange(xmin, xmax, xstep)
           yi = np.zeros_like(xi)

           for _x, _y in zip(x, y):
               yi += _y * np.exp( -(xi - _x)**2 / (2 * sigma**2))

           return xi, yi

       # insert your data!
       exc_ene = np.array([2.8, 3.0, 3.1, 3.15])

       # insert your data!
       osc_str = np.array([0.3, 0.1, 1.0, 0.2])

       x0, y0 = gaussian(exc_ene, osc_str, 2.5, 3.4, 0.01, 0.1)

       fig = go.Figure()

       fig.add_trace(
           go.Scatter(
               x=x0,
               y=y0,
               mode="lines",
               name="absorption",
           )
       )

       fig.update_layout(
           title="Absorption",
           xaxis_title="Excitation energy",
           yaxis_title="",
           height=500,
           width=600,
       )

       fig.show()

- Examine the character of the excitations

    The character of the excitations will be printed at the end of the output
    file. Find out the characters of the important excitations.

    Notation:

    - ``LE 5e(3)`` stands for the 3rd locally excited state (S3) on monomer 5.

    - ``CT 3+(H0)4-(L0)`` stands for charge transfer from HOMO of monomer
      3 to LUMO of monomer 4.

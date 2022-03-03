.. _ntos:


Natural transition orbitals
===========================

.. objectives::

   - Learn how to generate cube files for natural transition orbitals (NTOs).

.. keypoints::

   - Generate cube files for NTOs.
   - Compare the number of NTOs with the number of important excitations.
   - Visualize selected cube files for NTOs.

Introduction
------------

In this exercise we will generate NTO cube files for visualizing
exitations.
NTOs are given by singular value decomposition (SVD) of single particle
transition density matrix **T**

.. math::

   \begin{equation}
     U S V^{\dagger} = T
   \end{equation}

where **S** is diagonal matrix and **U** and **V** are unitary transformation
matrices. Transformation of orbital sets by **U** and **V** makes it more
straightforward to interpret the excitations. The square of the diagonal 
elements of **S** reflect the importance of the associated particle-hole 
excitations.
You can read more about NTOs in `this paper
<https://aip.scitation.org/doi/abs/10.1063/1.1558471>`_ :cite:`Martin2003-rl`

System: BPVB
------------

.. raw:: html

   <div style="height: 400px; width: 600px; position: relative;" class='viewer_3Dmoljs' data-href='_static/bpvb.xyz' data-type='xyz' data-backgroundcolor='0xffffff' data-style='stick'></div>


Input file
----------

Below is the input file for generating NTO cube files.
You can read more about the input keywords in
`this page <https://veloxchem.org/docs/keywords.html>`_.

.. literalinclude:: inputs/bpvb.inp
   :emphasize-lines: 9-13

Exercise
--------

- Submit a job

    Runs the above example. On Dardel this calculation takes several minutes
    on 4 nodes.

- Compare number of NTOs with number of important excitations

    Use the python script in :ref:`this page <linrsp-analysis>`
    to extract important excitations from output files.

    .. code-block:: shell

       ml PDC/21.11 Anaconda3/2021.05 vim/8.2
       python3 analyze_response_output.py bpvb.out

- Visualize the cube files. You can launch a `MyBinder instance
  <https://mybinder.org/v2/gh/ENCCS/veloxchem-hpc/main?urlpath=lab%2Ftree%2Fcontent%2Fnotebooks>`_
  to look at your NTOs in a Jupyter notebook. Once instance has started up, you
  can upload your cube files to it and use py3Dmol (already installed) as
  follows:

  .. code-block:: python

     import py3Dmol as p3d

     # generate view
     v = p3d.view(width=400, height=400)

     # to show the molecular geometry, we read it from a XYZ file
     v.addModel(h2o_xyz, "xyz")
     v.setStyle({'stick':{}})

     # we read in the cube file we uploaded (might take a bit of time, depending on the filesize)
     with open("HOMO.cube", "r") as f:
         cube = f.read()

     # negative lobe
     v.addVolumetricData(cube, "cube", {"isoval": -0.02, "color": "blue", "opacity": 0.75})
     # positive lobe
     v.addVolumetricData(cube, "cube", {"isoval": 0.02, "color": "red", "opacity": 0.75})

     v.show()

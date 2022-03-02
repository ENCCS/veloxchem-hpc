.. _ntos:


Natural transition orbitals
===========================

.. objectives::

   - Learn how to generate cube files for natural transition orbitals (NTOs)
     and detachment/attachment densities.

.. keypoints::

   - Generate cube files for NTOs.
   - Generate cube files for detachment/attachment densities.

Introduction
------------

In this exercise we will generate cube files for visualizing
exitations. In particular, natural transition orbitals (NTOs) and
detachment/attachment densities will be visualized.

System: BPVB
------------

.. raw:: html

   <div style="height: 400px; width: 600px; position: relative;" class='viewer_3Dmoljs' data-href='_static/bpvb.xyz' data-type='xyz' data-backgroundcolor='0xffffff' data-style='stick'></div>


Input file
----------

Below is the input file for generating NTOs and detachment/attachment
densities.
You can read more about the input keywords in
`this page <https://veloxchem.org/docs/keywords.html>`_.

.. literalinclude:: inputs/bpvb.inp
   :emphasize-lines: 9-14

Exercise
--------

- Submit a job

    Runs the above example. On Dardel this calculation takes several minutes
    on 4 nodes.

- Visualize the cube files


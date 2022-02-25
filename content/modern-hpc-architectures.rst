.. _modern-hpc-architectures:


Modern HPC architectures
========================


.. objectives::

   - WRITE ME


.. keypoints::

   - WRITE ME

Moore's law [*]_
----------------

The number of transistors in a dense integrated circuit doubles about every two years.
More transistors means smaller size of a single element, so higher core frequency can be achieved.
However, power consumption scales as frequency in third power, so the growth in the core frequency has slowed down significantly.
Higher performance of a single node has to rely on its more complicated structure and still can be achieved with SIMD, branch prediction, etc.


.. chart:: charts/microprocessor-trend-data.json

   The evolution of microprocessors. The number of transistors per chip
   increases every 2 years or so. However, it can no longer be exploited by the
   core frequency due to power consumption limits. Before 2000, the increase in
   the single core clock frequency was the major source of performance increase.
   Mid-2000 mark a transition towards multi-core processors. [*]_

Achieving performance has been based on two main strategies over the years:

- Increase the single processor performance:
- More recently, increase the number of physical cores.

.. [*] This section is adapted, with permission, from the training material for the `ENCCS CUDA workshop <https://enccs.github.io/CUDA/1.01_GPUIntroduction/#exposing-parallelism>`_.
.. [*] The data in this plot is collected by Karl Rupp and made available on: https://github.com/karlrupp/microprocessor-trend-data

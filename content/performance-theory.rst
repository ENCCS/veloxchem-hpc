.. _performance-theory:


Performance theory
==================


.. objectives::

   - WRITE ME


.. keypoints::

   - WRITE ME



Speedup:

.. math::

   \mathrm{speedup} = \frac{T_{1}}{T_{P}}

.. todo::

   - absolute vs relative speedup


Efficiency:

.. math::

   \mathrm{efficiency} = \frac{\mathrm{speedup}}{P} = \frac{T_{1}}{PT_{P}}


Split :math:`T_{1}` into serial and parallel work:

.. math::

   T_{1} = W_{\mathrm{ser}} + W_{\mathrm{par}}

then we have:

.. math::

   T_{P} \geq W_{\mathrm{ser}} + \frac{W_{\mathrm{par}}}{P}

because parallelization is not perfect and/or the algorithm might introduce some overhead.

.. chart:: charts/amdahl-speedup.json

   WRITE ME!

.. chart:: charts/amdahl-efficiency.json

   WRITE ME!

For a more comprehensive discussion, consult:
McCool, M.; Robison, A.; Reinders, J. *Structured Parallel Programming: Patterns for Efficient Computation* :cite:`McCool2012-tx`

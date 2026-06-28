Getting started
===============

Quickstart
---------

Follow the instructions in the project README for running the simulation and tests. In short:

.. code-block:: sh

   python -m src.main

Configuration
-------------

Edit `config/config.json` to tweak intervals, thresholds, and output logfile path. For tests and CI, prefer injecting a deterministic config or using the `tmp_path` fixture in pytest.

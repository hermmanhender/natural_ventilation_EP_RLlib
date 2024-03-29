.. eprllib documentation master file, created by
   sphinx-quickstart on Fri Mar 22 15:18:05 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to eprllib's documentation!
===================================

This repository provides a set of methods to establish the computational loop of EnergyPlus within a Markov Decision Process (MDP), treating it as a multi-agent environment compatible with RLlib. The main goal is to offer a simple configuration of EnergyPlus as a standard environment for experimentation with Deep Reinforcement Learning.

Installation
------------

To install EnergyPlusRL, simply use pip:

```
pip install eprllib
```

Key Features
------------

* Integration of EnergyPlus and RLlib: This package facilitates setting up a Reinforcement Learning environment using EnergyPlus as the base, allowing for experimentation with energy control policies in buildings.
* Simplified Configuration: To use this environment, you simply need to provide a configuration in the form of a dictionary that includes state variables, metrics, actuators (which will also serve as agents in the environment), and other optional features.
* Flexibility and Compatibility: EnergyPlusRL easily integrates with RLlib, a popular framework for Reinforcement Learning, enabling smooth setup and training of control policies for actionable elements in buildings.

Usage
-----

1. Import the package into your Python script.
2. Define your environment configuration in a dictionary, specifying state variables, metrics, actuators, and other relevant features as needed. (See Documentation section to know all the parameters).
3. Configure RLlib for training control policies using the EnergyPlusRL environment.
4. Execute the training of your Reinforcement Learning model and evaluate the results obtained.


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

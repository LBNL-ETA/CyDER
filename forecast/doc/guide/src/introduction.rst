.. highlight:: rest

.. _introduction:

Introduction
============

This user guide explains how to install and use the CyDER photovoltaic (PV) forecasting module.
The forecasting module is a software package written in C which allows
users to predict future Photovoltaic generation values from historical data.
The algorithm uses a Nonlinear Autoregressive Exogenous (NARX) neural network model.
This neural network can be trained with historical PV data and potentially other
independent time-series such as weather or surrounding PV generation. Once
the network is trained it can then be used for prediction of future values.
We use the Fast Artifical Neural Network Library (`FANN http://leenissen.dk/`)
to develop this neural network model.

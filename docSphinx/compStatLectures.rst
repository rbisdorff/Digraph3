.. meta::
   :description: Documentation of the Digraph3 collection of python3 modules for algorithmic decision theory
   :keywords: Algorithmic Decision Theory, Outranking Digraphs, MIS and kernels, Multiple Criteria Decision Support, Bipolar-valued Epistemic Logic

Computational Statistics Lectures
=================================
:Author: Raymond Bisdorff, Emeritus Professor of Applied Mathematics and Computer Science, University of Luxembourg
:Url: https://rbisdorff.github.io/
:Copyright: R. Bisdorff |location_link3| 2013-2023

Introduction
------------

From 2007 to 2011 the Algorithmic Decision Theory COST Action IC0602, coordinated by Alexis Tsoukiàs, gathered researchers coming from different fields such as *Decision Theory*, *Discrete Mathematics*, *Theoretical Computer Science* and *Artificial Intelligence* in order to improve decision support in the presence of **massive data bases**, **combinatorial structures**, **partial** and/or **uncertain information** and **distributed**, possibly **interoperating decision makers**.

A positive result a.o. of this COST action was the organisation from 2010 to 2020 of a Semester Course on |location_link4| at the *University of Luxembourg* in the context of its **Master in Information and Computer Science**.

Below are gathered 2x2 reduced copies of the presentation slides for 8 Lectures from the Winter Semester 2019.

Lectures
--------

L1. `Generating random numbers for simulations <_static/1-randomNumbers-2x2.pdf>`_
    1. On numbers "chosen at random", computer generated random numbers and multiple recursive random number generators over *F2*

    2. Recommendations and traps to watch for with home brewed generators

    3. Combining random number generators and testing randomness

L2. `Introduction to statistical computing <_static/2-intro-R-2x2.pdf>`_ 
    1. On generating simulation data with Python and exploring simulation data with *gretl*. Getting started with *R*. Introducing *R* objects: vectors, matrices, lists, data frames. Reading CSV data files into data frames

    2. Doing linear algebra in *R*. Constructing matrix objects, matrix operations and inversion, solving linear systems, eigen-values and -vectors, singular value decomposition, Choleski and QR decompositions

    3. Principal component analysis (PCA) and discrete Markov chain simulating

L3. `Continuous Random Variables <_static/3-randVarGen-2x2.pdf>`_
    1. Probability distributions in *R*-core, simulating a continuous uniform random distribution, the spectral test for random number generators
       
    2. Simulating random variables by a continuous inverse transform, standard exponential law based generators

    3. The Gaussian random variables, important properties, simulating Gaussian random variables

L4. `Simulating from Discrete Random Variables <_static/4-randDiscrVarGen-2x2.pdf>`_
    1. Simulating Bernoulli and Binomial random variables. The CLT for binomial distributions

    2. Simulating a Poisson random variable and Poisson processes with exponential time intervals

    3. Simulating Gamma variables, integer alpha parameter and the sum rule for Gamma Variables

L5. `Simulating from arbitrary empirical random distributions <_static/5-QuantileEstimation-2x2.pdf>`_
    1. Single pass estimation of arbitrary quantiles: computing sample quantiles, quantiles via selecting algorithms, tracking the *M*-largest element in a single pass

    2. Computing quantiles from binned data: equally binned observation data, linear integration formulas, regular binned data quantiles

    3. Incremental quantiles estimation with the IQ-agent: using the IQ-agent for Monte-Carlo simulations

L6. `Two distributions, are they of the same kind? <_static/6-chiSquareTest-2x2.pdf>`_
    1. Comparing statistical distributions: methodological approach and statistical tests

    2. Comparing histograms: Chi-square test against a known distribution, comparing two binned data sets, testing uniform randomness

    3. Comparing continuous distributions with the  Kolmogorov-Smirnov test

L7. `On Averaging <_static/7-averaging-2x2.pdf>`_
    1. The benefit from averaging: the law of large numbers, estimating distribution parameters, how to reduce noise

    2. Convergence of the averaging: Convergence of the mean for a standard Gaussian, and if there are outliers? Non convergence of a Cauchy mean
       
    3. Comparing two empiric means: robustness of the *t* statistic, estimating *t* statistics, Monte Carlo simulation of the *H0* rejection

L8. `Accept-Reject Simulation Methods <_static/8-acceptReject-2x2.pdf>`_
    1. Classical Monte Carlo Integration: principles and applications
       
    2. Accept-reject simulation methods

    3. Accept-reject simulation applications: pi estimation, Box-Muller transform, Ratio-Of-Uniforms method
 

.. |location_link1| raw:: html

   <a href="https://rbisdorff.github.io/" target="_blank">https://rbisdorff.github.io/</a>

.. |location_link3| raw:: html

   <a href="_static/digraph3_copyright.html" target="_blank">&copy;</a>

.. |location_link4| raw:: html

   <a href="http://hdl.handle.net/10993/37870" target="_blank">Computational Statistics</a>

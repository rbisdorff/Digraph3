.. meta::
   :description: Documentation of the Digraph3 collection of python3 modules for algorithmic decision theory
   :keywords: Algorithmic Decision Theory, Outranking Digraphs, MIS and kernels, Multiple Criteria Decision Aid

Documentation of the Digraph3 Python resources
==============================================
:Author: Raymond Bisdorff, Emeritus Professor of Computer Science and Applied Mathematics
:Version: |version|
:Url: https://rbisdorff.github.io/
:Copyright: R. Bisdorff |location_link3| 2013-2021

.. image:: introDoc2.png
    :width: 500pt
    :align: center

.. _Documents:

Contents
--------

1. `Tutorials <tutorial.html>`_

    .. raw:: html

       <small><i>Start here</i></small>
   
2. `Reference manual <techDoc.html>`_

    .. raw:: html

       <small><i>Technical documentation and source code of all modules</i></small>
   
3. `Advanced topics <pearls.html>`_

    .. raw:: html
   
       <small><i>Pearls of bipolar-valued epistemic logic</i></small>
   
4. `Algorithimc Decision Theory Lectures <adtLectures.html>`_

    .. raw:: html

       <small><i>2x2 reduced copies of the presentation slides</i></small>

5. `Archives <digraph3Archives.html>`_

    .. raw:: html

       <small><i>Historical case studies and example graphs</i></small>


Indices and tables
``````````````````

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Introduction-label:

Introduction
````````````

|
|      *This documentation is dedicated to*
|      *our late colleague and dear friend*
|                  Marc ROUBENS
|

The *Digraph3 documentation*, available on the `Read The Docs <https://readthedocs.org/>`_ site: |location_link1|, describes the Python3 resources for implementing decision aid algorithms in the context of a **bipolar-valued outranking** approach ([BISD-15]_, [BISD-00]_). These computing resources are useful in the field of `Algorithmic Decision Theory <https://www.lamsade.dauphine.fr/~projet_cost/ALGORITHMIC_DECISION_THEORY/ALGORITHMIC_DECISION_THEORY.html>`_ and more specifically in *outranking* based **Multiple Criteria Decision Aid** (MCDA). They provide practical tools for a Master Course on |location_link4| tought at the University of Luxembourg.

The documentation contains, first, a set of tutorials introducing the main objects like **digraphs**, **outranking digraphs** and **performance tableaux**. There is also a tutorial provided on **undirected graphs**. Some tutorials are problem oriented and show how to compute the *winner of an election*, how to build a *best choice recommendation*, or *how to linearly rank or rate* with multiple incommensurable performance criteria. Other tutorials concern more specifically operational aspects of computing **maximal independent sets** (MISs) and **kernels** in graphs and digraphs. The tutorial about *split*, *interval* and *permutation graphs* is inspired by *Martin Golumbic* 's book on *Algorithmic Graph Theory and Perfect Graphs* ([GOLU-04]_). We also provide a tutorial on *tree graphs* and *spanning forests*.

   .. toctree:: tutorial
      :maxdepth: 2

The second Section concerns the **extensive reference manual** of the collection of provided Python3 modules, classes and methods. The main classes in this collection are the :py:class:`digraphs.Digraph` overall root class, the :py:class:`perfTabs.PerformanceTableau` class and the :py:class:`outrankingDigraphs.BipolarOutrankingDigraph` class. The technical documentation also provides insight into the complete source code of all modules, classes and methods.

  .. toctree:: techDoc
     :maxdepth: 2
		
The third Section exhibits some pearls of **bipolar-valued epistemic logic** that enrich the Digraph3 resources. These short texts illustrate well the very computational benefit one may get when working in a bipolar-valued logical framework. And, more specifically, the essential part the *logically neutral* **undeterminate** value is judiciously playing therein.  

   .. toctree:: pearls
      :maxdepth: 2

The fourth section provides 2x2-reduced notes of the author's lectures on **Algorithmic Decision Theory** given at the University of Luxembourg during Spring 2020.

   .. toctree:: adtLectures
      :maxdepth: 2

		 
The last section gathers **historical case studies** with example digraphs compiled before 2006 and concerning the early development of the Digraph3 collection of python3 modules for implementing tools and methods for enumerating *non isomorphic maximal independent sets* in undirected graphs and computing *dominant digraph kernels*. 

   .. toctree:: digraph3Archives
      :maxdepth: 2


References
``````````
.. [BISD-15] R. Bisdorff, L.C. Dias, P. Meyer, V. Mousseau and M. Pirlot (Eds.) (2015). *Evaluation and decision models with multiple criteria: Case studies*. Springer-Verlag Berlin Heidelberg, International Handbooks on Information Systems, `ISBN 978-3-662-46815-9 <https://link.springer.com/book/10.1007/978-3-662-46816-6>`_, 643 pages (see http://hdl.handle.net/10993/23698).

.. [BISD-00] R. Bisdorff (2000). "Logical foundation of fuzzy preferential systems with application to the Electre decision aid methods", *Computers and Operations Research*, 27: 673-687 (downloadable `PDF file 159.1kB <http://hdl.handle.net/10993/23724>`_)

.. [GOLU-04] M. Ch. Golumbic (2004), *Agorithmic Graph Theory and Perfect Graphs* 2nd Ed., Annals of Discrete Mathematics 57, Elsevier.


.. |location_link1| raw:: html

   <a href="https://digraph3.readthedocs.io/en/latest/" target="_blank">https://digraph3.readthedocs.io/en/latest/</a>

.. |location_link3| raw:: html

   <a href="_static/digraph3_copyright.html" target="_blank">Copyright</a>

.. |location_link4| raw:: html

   <a href="http://hdl.handle.net/10993/37933" target="_blank">Algorithmic Decision Theory</a>




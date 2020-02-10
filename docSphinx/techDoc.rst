Technical Reference of the Digraph3 modules
===========================================
:Author: Raymond Bisdorff, Emeritus Professor, University of Luxembourg
:Version: Revision: Python 3.7
:Copyright: `R. Bisdorff <_static/digraph3_copyright.html>`_ 2013-2020

.. contents:: Table of Contents
	:depth: 1
	:local:	    

.. _Technical-label:

Installation
------------

**Dowloading the Digraph3 resources**

Three download options are given:

1. Either (easiest under Linux or Mac OS-X), by using a git client and cloning from github.com::

     ...$ git clone https://github.com/rbisdorff/Digraph3

2. Or from sourceforge.net::
  
     ...$ git clone https://git.code.sf.net/p/digraph3/code Digraph3
     
3. Or, with a browser access,  download and extract the latest distribution zip archive either, from the `github link above <https://github.com/rbisdorff/Digraph3>`_  or, from the `sourceforge page <https://sourceforge.net/projects/digraph3/>`_ .

On Linux or Mac OS, ..$ cd to the extracted <Digraph3> directory::

     ../Digraph3$ make install

installs (with sudo !!) the Digraph3 modules in the current running python environment. Pythhon 3.5 (or later) environment is recommended. Whereas::

     ../Digraph3$ make installVenv
          
installs the Digraph3 modules in an activated virtual python environment.
     
If the **cython** (https://cython.org/) C-compiled modules for Big Data applications are required, it is necessary to previously install the Cython package in the running Python environment::

     ...$ pip3.5+ install cython

It is recommended to run a nose test suite::
    
     .../Digraph3$ make tests

Test results are stored in the <Digraph3/test> directory. Notice, the python3 nose package is required::

      ...$ pip3 install nose
      .../Digraph3$ make verboseTests

runs a verbose (with stdout not captured) nose test suite::

     ../Digraph3$ make pTests

runs the nose test suite in multiple processing mode when the GNU `parallel <https://www.gnu.org/software/parallel/>`_ shell tool is installed and multiple cores are detected.

**Dependencies**

* To be fully functional, the Digraph3 resources mainly need the `graphviz <https://graphviz.org>`_ tools and the `R statistics resources <https://www.r-project.org>`_ to be installed.
* When exploring digraph isomorphisms, the `nauty <https://www.cs.sunysb.edu/~algorith/implement/nauty/implement.shtml>`_ isomorphism testing program is required.
* Two specific criteria and actions clustering methods of the `OutrankingDigraph <techDoc.html#outrankingDigraphs.OutrankingDigraph>`_ class furthermore require the *calmat* matrix computing resource to be installed (see the calmat directory in Digraph3 resources)::

     ../Digraph3/calmat$ less README

.. _Modules-organisation-label:

Organisation of the Digraph3 modules
------------------------------------

The Digraph3 source code is split into several interdependent modules of which the ``digraphs`` module is the master module.

Basic modules
.............

* :ref:`digraphs-label`  
     Main part of the Digraph3 source code with the root `Digraph
     <techDoc.html#digraphs.Digraph>`_ class.

     .. inheritance-diagram:: digraphs
     
* :ref:`graphs-label`
     Resources for handling undirected graphs with the root `Graph
     <techDoc.html#graphs.Graph>`_ class and a brigde to the
     ``digraphs`` module resources.

     .. inheritance-diagram:: graphs
     
* :ref:`perfTabs-label`
     Tools for handling multiple criteria performance tableaux with
     root `PerformanceTableau
     <techDoc.html#perfTabs.PerformanceTableau>`_ class.

     .. inheritance-diagram:: perfTabs
     
* :ref:`outrankingDigraphs-label`
     Root module for handling outranking digraphs with the abstract root :py:class:`outrankingDigraphs.OutrankingDigraph` classs and the main
     `BipolarOutrankingDigraph
     <techDoc.html#outrankingDigraphs.BipolarOutrankingDigraph>`_
     class. Notice that the outrankingDigraph class defines a hybrid object type, inheriting conjointly from the Digraph class *and* the PerformanceTableau class.

     .. inheritance-diagram:: outrankingDigraphs.BipolarOutrankingDigraph

* :ref:`votingProfiles-label` 
     Classes and methods for handling voting ballots and computing election results
     with main `LinearVotingProfile
     <techDoc.html#votingProfiles.LinearVotingProfile>`_ class.

     .. inheritance-diagram:: votingProfiles.LinearVotingProfile
     

Various Random generators
.........................

* :ref:`randomDigraphs-label` 
     Various implemented random digraph models.

     .. inheritance-diagram:: randomDigraphs

* :ref:`randomPerfTabs-label` 
     Various implemented random performance tableau models.

     .. inheritance-diagram:: randomPerfTabs

* :ref:`randomNumbers-label` 
     Additional random number generators, not available in the
     standard python random.py library.

     .. inheritance-diagram:: randomNumbers

Handling big data
.................

* :ref:`performanceQuantiles-label` 
     Incremental representation of large performance tableaux via
     binned cumulated density functions per criteria. Depends on the
     :py:mod:`randomPerfTabs` module.   

     .. inheritance-diagram:: performanceQuantiles  

* :ref:`sparseOutrankingDigraphs-label` 
     Sparse implementation design for large bipolar outranking digraphs (order
     > 1000);

     .. inheritance-diagram:: sparseOutrankingDigraphs.PreRankedOutrankingDigraph    

Cythonized modules
..................

* :ref:`cythonized-label` 
     Cythonized C implementation for handling big performance tableaux
     and bipolar outranking digraphs (order
     > 1000).

Sorting, rating and ranking tools
.................................

* :ref:`sortingDigraphs-label`
     Additional tools for solving sorting problems with the root :py:class:`sortingDigraphs.SortingDigraph` class and the main
     `QuantilesSortingDigraph <techDoc.html#sortingDigraphs.QuantilesSortingDigraph>`_
     class;

     .. inheritance-diagram:: sortingDigraphs.SortingDigraph
     
* :ref:`linearOrders-label` 
     Additional tools for solving linearly ranking problems with the
     root `LinearOrder <techDoc.html#linearOrders.LinearOrder>`_
     class;

     .. inheritance-diagram:: linearOrders
     
* :ref:`transitiveDigraphs-label` 
     Additional tools for solving pre-ranking problems with
     root `TransitiveDigraph <techDoc.html#transitiveDigraphs.TransitiveDigraph>`_ class.

     .. inheritance-diagram:: transitiveDigraphs

Miscellaneous tools
...................

* :ref:`digraphsTools-label` 
     Various generic methods and tools for handling digraphs.

* :ref:`xmcda-label` 
     Methods and tools for handling XMCDA encoded performance tableaux and digraphs.
     
* :ref:`arithmetics-label` 
     Some common methods and tools for computing with integer numbers.

.. toctree::
   :maxdepth: 2

.. _digraphs-label:

digraphs module
---------------

A tutorial with coding examples is available here: :ref:`Digraphs-Tutorial-label`

.. automodule:: digraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _randomDigraphs-label:

randomDigraphs module
---------------------

.. automodule:: randomDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _graphs-label:

graphs module
-------------

A tutorial with coding examples is available here: :ref:`Graphs-Tutorial-label`

.. automodule:: graphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _perfTabs-label:

perfTabs module
---------------

.. automodule:: perfTabs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _performanceQuantiles-label:

performanceQuantiles module
---------------------------

.. automodule:: performanceQuantiles
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _randomPerfTabs-label:
      
randomPerfTabs module
---------------------

A tutorial with coding examples is available here: :ref:`RandomPerformanceTableau-Tutorial-label`

.. automodule:: randomPerfTabs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _outrankingDigraphs-label:

outrankingDigraphs module
-------------------------

A tutorial with coding examples is available here: :ref:`OutrankingDigraphs-Tutorial-label`

.. automodule:: outrankingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _xmcda-label:

xmcda module
------------

.. automodule:: xmcda
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _sparseOutrankingDigraphs-label:

sparseOutrankingDigraphs module
-------------------------------

.. automodule:: sparseOutrankingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _sortingDigraphs-label:

sortingDigraphs module
----------------------

A tutorial with coding examples for solving multi-criteria rating problems is available here: :ref:`Rating-Tutorial-label`


.. automodule:: sortingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _votingProfiles-label:

votingProfiles module
---------------------

A tutorial with coding examples is available here: :ref:`LinearVoting-Tutorial-label`

.. automodule:: votingProfiles
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _linearOrders-label:

linearOrders module
-------------------

A tutorial with coding examples is available here: :ref:`LinearVoting-Tutorial-label`

.. automodule:: linearOrders
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _transitiveDigraphs-label:

transitiveDigraphs module
-------------------------

.. automodule:: transitiveDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _randomNumbers-label:

randomNumbers module
--------------------

.. automodule:: randomNumbers
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _digraphsTools-label:

digraphsTools module
--------------------

.. automodule:: digraphsTools
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _arithmetics-label:

arithmetics module
------------------

.. automodule:: arithmetics
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _cythonized-label:

Cythonized modules for big digraphs
-----------------------------------

The following modules are compiled C-extensions using the Cython pre-compiler. No Python code source is provided for inspection. To distinguish them from the corresponding pure Python modules, a c- prefix is used.

.. _cRandPerfTabs-label:

cRandPerfTabs module
....................

.. automodule:: cRandPerfTabs
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _cIntegerOutrankingDigraphs-label:

cIntegerOutrankingDigraphs module
.................................

.. automodule:: cIntegerOutrankingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _cIntegerSortingDigraphs-label:

cIntegerSortingDigraphs module
..............................

.. automodule:: cIntegerSortingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _cSparseIntegerOutrankingDigraphs-label:

cSparseIntegerOutrankingDigraphs module
.......................................

.. automodule:: cSparseIntegerOutrankingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Tutorials
---------

* `Tutorial <tutorial.html>`_



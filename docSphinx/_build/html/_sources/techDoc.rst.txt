.. meta::
   :description: Documentation of the Digraph3 collection of python3 modules for algorithmic decision theory
   :keywords: Algorithmic Decision Theory, Outranking Digraphs, MIS and kernels, Multiple Criteria Decision Aid, Bipolar-valued Epistemic Logic


Technical Reference of the Digraph3 modules
===========================================

:Author: Raymond Bisdorff, Emeritus Professor of Computer Science and Applied Mathematics, University of Luxembourg
:Url: https://rbisdorff.github.io/
:Version: |version| (release: |release|)
:Copyright: `R. Bisdorff <_static/digraph3_copyright.html>`_ 2013-2024

	    

.. only:: html

   :New:

        - In order to explore potential run time accelerations with CUDA on GPUs, a new cythonized **cnpBipolarDigraphs** module with a numpy integer array implementation of the bipolar-valued characteristic valuation has been added to the cythonized collection of Digraph3 modules.
	
        - Following a Python 3.12 recommendation, all multiprocessing resources have been refactored to use by default, instead of the traditional *fork*, the safer *spawn* threading start method. As a consequence, main program code of multiprocessing Digraph3 Python scripts must now start with a *__name__=='__main__'* test in order to avoid its recursive execution in each started thread (see the :py:mod:`multiprocessing` module).

        - A :py:mod:`pairings` module for solving **fair intergroup** and **intragroup pairing** problems

        - A :py:mod:`dynamicProgramming` module for solving **dynamic programming** problems

        - The :py:meth:`digraphsTools.computeSequenceAlignment` method implements the *Needlemann* % *Wunsch* dynamic programming algorithm for computing DNA *sequence alignments*

**Preface**

It is necessary to mention that the Digraph3 Python resources do not provide a professional Python software library. The collection of Python modules was not built following any professional software development methodology. The design of classes and methods was kept as simple and elementary as was opportune for the author. Sophisticated and cryptic overloading of classes, methods and variables is more or less avoided all over. A simple copy, paste and ad hoc customisation development strategy was generally preferred. As a consequence, the Digraph3 modules keep a large part of independence.

Furthermore, the development of the Digraph3 modules being spread over two decades, the programming style did evolve with growing experience and the changes and enhancement coming up with the ongoing new releases first, of the standard Python2,  and later of the standard Python3 libraries. The backward compatibility requirements necessarily introduced so with time different notation and programming techniques.

.. note:: Two deviating features from the usually recommended Python source coding style must be mentioned. We do not use only lowercase function names and avoid all underscore separators because of *Latex* editing problems. Same rule is applied to variable names, except Boolean method parameters --like *Debug* or *Comments*-- where we prefer using semiotic names starting with an uppercase letter.
	  
.. _Contents-Table-label:

.. contents:: Table of Contents
	:depth: 1
	:local:

.. _Technical-label:

Installation
------------

**Dowloading the Digraph3 resources**

Three download options are given:

1. Recommended: With a browser access, download and extract the latest distribution zip archive either, from

   https://github.com/rbisdorff/Digraph3  or, from

   https://sourceforge.net/projects/digraph3/


2. By using a git client and cloning either, from github.com::

     ...$ git clone https://github.com/rbisdorff/Digraph3

3. Or, from sourceforge.net::
  
     ...$ git clone https://git.code.sf.net/p/digraph3/code Digraph3
     

On Linux or Mac OS, ..$ *cd* to the extracted <Digraph3> directory. From Python3.10.4 on, the *distutils* package and the direct usage of *setup.py* are deprecated. The instead recommended installation via the *pip* module is provided with::

     ../Digraph3$ make installPip

This *make* command  launches in fact a *${PYTHON} -m pip -v install --upgrade --scr = .* command that installs the Digraph3 modules in the running virtual environment (recommended option) or the user's local *site-packages* directory. A system wide installation is possible with prefixing the *make installPip* commad with *sudo*. As of Python 3.11, it is necessary to previously install the *wheel* package ( ...$ python3.11 -m pip install wheel).

For earlier Python3 version::

     ../Digraph3$ make installVenv
          
installs the Digraph3 modules in an activated virtual Python environment (the Python recommended option), or in the user's local python3 *site-packages*. 

Whereas::

     ../Digraph3$ make install

installs (with *sudo ${PYTHON} setup.py*) the Digraph3 modules system wide in the current running python environment. Python 3.8 (or later) environment is recommended (see the makefile for adapting to your *PYTHON* make constant). 

If the **cython** (https://cython.org/) C-compiled modules for Big Data applications are required, it is necessary to previously install the *cython* package and, if not yet installed, the *wheel*  package in the running Python environment::

     ...$ python3 -m pip install cython wheel

It is recommended to run a test suite::
    
     .../Digraph3$ make tests

Test results are stored in the <Digraph3/test/results> directory. Notice that the python3 *pytest* package is therefore required::

      ...$ python3 -m pip install pytest pytest-xdist

A verbose (with stdout not captured) pytest suite may be run as follows::
      
      .../Digraph3$ make verboseTests

Individual module *pytest* suites are also provided (see the makefile), like the one for the :py:mod:`outrankingDigraphs` module::

     ../Digraph3$ make outrankingDigraphsTests

When the GNU `parallel <https://www.gnu.org/software/parallel/>`_ shell tool is installed and multiple processor cores are detected, the tests may be executed in multiprocessing mode::

       ../Digraph3$ make pTests

If the *pytest-xdist* package is installed (see above), it is also possible to set as follws a number of pytests to be run in parallel (see the *makefile*)::

       ../Digraph3$ make tests JOBS="-n 8"

The *pytest* module is by default ignoring Python run time warnings. It is possible to activate default warnings as follows (see the *makefile*)::

       ../Digraph3$ make tests PYTHON="python3 -Wd"

**Dependencies**

* To be fully functional, the Digraph3 resources mainly need the `graphviz <https://graphviz.org>`_ tools and the `R statistics resources <https://www.r-project.org>`_ to be installed.
* When exploring digraph isomorphisms, the `nauty <https://www.cs.sunysb.edu/~algorith/implement/nauty/implement.shtml>`_ isomorphism testing program is required.

.. _Modules-organisation-label:

Organisation of the Digraph3 modules
------------------------------------

The Digraph3 source code is split into several interdependent modules of which the *digraphs.py* module is the master module.

Basic modules
.............

* :ref:`digraphs-label`  
     Main part of the Digraph3 source code with the generic root `Digraph
     <techDoc.html#digraphs.Digraph>`_ class.

     .. inheritance-diagram:: digraphs
	:parts: 1
     
* :ref:`graphs-label`
     Resources for handling undirected graphs with the generic root `Graph
     <techDoc.html#graphs.Graph>`_ class and a brigde to the
     :py:mod:`digraphs` module resources.

     .. inheritance-diagram:: graphs
	:parts: 1
     
* :ref:`perfTabs-label`
     Tools for handling multiple criteria performance tableaux with the generic 
     root `PerformanceTableau
     <techDoc.html#perfTabs.PerformanceTableau>`_ class.

     .. inheritance-diagram:: perfTabs
	:parts: 1
     
* :ref:`outrankingDigraphs-label`
     Root module for handling outranking digraphs with the abstract generic root :py:class:`~outrankingDigraphs.OutrankingDigraph` classs and the main
     `BipolarOutrankingDigraph
     <techDoc.html#outrankingDigraphs.BipolarOutrankingDigraph>`_
     class. Notice that the outrankingDigraph class defines a hybrid object type, inheriting conjointly from the :py:class:`~digraphs.Digraph` class *and* the :py:class:`~perfTabs.PerformanceTableau` class.

     .. inheritance-diagram:: outrankingDigraphs
	:top-classes: outrankingDigraphs.outrankingDigraph, outrankingDigraphs.BipolarOutrankingDigraph
	:parts: 1

* :ref:`votingProfiles-label` 
     Classes and methods for handling voting ballots and computing election results
     with main `LinearVotingProfile
     <techDoc.html#votingProfiles.LinearVotingProfile>`_ class.

     .. inheritance-diagram:: votingProfiles
	:top-classes: votingProfiles.VotingProfile
	:parts: 1
     
* :ref:`pairings-label` 
     Classes and methods for computing fair pairings solutions
     with abstract generic root :py:class:`~pairings.Pairing` class.

     .. inheritance-diagram:: pairings
	:top-classes: pairings.Pairing
	:parts: 1

* :ref:`dynamicProgramming-label` 
     Classes and methods for solving dynamic programming problems
     with generic root :py:class:`~dynamicProgramming.DynamicProgrammingDigraph` class.

     .. inheritance-diagram:: dynamicProgramming
	:parts: 1

Various Random generators
.........................

* :ref:`randomDigraphs-label` 
     Various implemented random digraph models.

     .. inheritance-diagram:: randomDigraphs
	:parts: 1

* :ref:`randomPerfTabs-label` 
     Various implemented random performance tableau models.

     .. inheritance-diagram:: randomPerfTabs
	:parts: 1

* :ref:`randomNumbers-label` 
     Additional random number generators, not available in the
     standard python random.py library.

     .. inheritance-diagram:: randomNumbers
	:parts: 1

Handling big data
.................

* :ref:`performanceQuantiles-label` 
     Incremental representation of large performance tableaux via
     binned cumulated density functions per criteria. Depends on the
     :py:mod:`randomPerfTabs` module.   

     .. inheritance-diagram:: performanceQuantiles
        :parts: 1

* :ref:`sparseOutrankingDigraphs-label` 
     Sparse implementation design for large bipolar outranking digraphs (order
     > 1000);

     .. inheritance-diagram:: sparseOutrankingDigraphs
	:top-classes: sparseOutrankingDigraphs.SparseOutrankingDigraph
	:parts: 1

* :ref:`mpOutrankingDigraphs-label`
     New variable start-methods based multiprocessing construction of genuine bipolar-valued outranking digraphs.

     .. inheritance-diagram:: mpOutrankingDigraphs
	:top-classes: outrankingDigraphs.BipolarOutrankingDigraph
	:parts: 1

* :ref:`cythonized-label` 
     Cythonized C implementation for handling big performance tableaux
     and bipolar outranking digraphs (order > 1000).

     :ref:`cRandPerfTabs-label`
	  Integer and float valued C version of the :py:mod:`randomPerfTabs` module

     :ref:`cIntegerOutrankingDigraphs-label`
	  Integer and float valued C version of the
	  :py:class:`~outrankingDigraphs.BipolarOutrankingDigraph` class

     :ref:`cIntegerSortingDigraphs-label`
	  Integer and float valued C version of the :py:class:`~sortingDigraphs.QuantilesSortingDigraph` class

     :ref:`cSparseIntegerOutrankingDigraphs-label`
	  Integer and float valued C version of sparse outranking digraphs.

     :ref:`cnpBipolarDigraphs-label`
	  New numpy integer arrays implemented bipolar outrankingDigraphs.

Sorting, rating and ranking tools
.................................

* :ref:`ratingDigraphs-label`
     Tools for solving relative and absolute rating problems with the abstract generic root :py:class:`~ratingDigraphs.RatingDigraph` class;

     .. inheritance-diagram:: ratingDigraphs
	:top-classes: ratingDigraphs.RatingDigraph
	:parts: 1

* :ref:`sortingDigraphs-label`
     Additional tools for solving sorting problems with the generic root :py:class:`~sortingDigraphs.SortingDigraph` class and the main
     `QuantilesSortingDigraph <techDoc.html#sortingDigraphs.QuantilesSortingDigraph>`_
     class;

     .. inheritance-diagram:: sortingDigraphs
	:top-classes: sortingDigraphs.SortingDigraph
	:parts: 1
     
* :ref:`linearOrders-label` 
     Additional tools for solving linearly ranking problems with the
     abstract generic root `LinearOrder <techDoc.html#linearOrders.LinearOrder>`_
     class;

     .. inheritance-diagram:: linearOrders
	:top-classes: linearOrders.LinearOrder
	:parts: 1
     
* :ref:`transitiveDigraphs-label` 
     Additional tools for solving pre-ranking problems with abstract
     generic root `TransitiveDigraph <techDoc.html#transitiveDigraphs.TransitiveDigraph>`_ class.

     .. inheritance-diagram:: transitiveDigraphs
        :top-classes: transitiveDigraphs.TransitiveDigraph
	:parts: 1

Miscellaneous tools
...................

* :ref:`digraphsTools-label` 
     Various generic methods and tools for handling digraphs.

* :ref:`arithmetics-label` 
     Some common methods and tools for computing with integer numbers.

..  * :ref:`xmcda-label` 
     Methods and tools for handling XMCDA encoded performance tableaux and digraphs.
     

.. toctree::
   :maxdepth: 2

-------------

.. _digraphs-label:

digraphs module
---------------

A tutorial with coding examples is available here: :ref:`Digraphs-Tutorial-label`

**Inheritance Diagram**

.. inheritance-diagram:: digraphs
   :parts: 1

.. automodule:: digraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _randomDigraphs-label:

randomDigraphs module
---------------------

**Inheritance Diagram**

.. inheritance-diagram:: randomDigraphs
   :parts: 1

.. automodule:: randomDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _perfTabs-label:

perfTabs module
---------------

**Inheritance Diagram**

.. inheritance-diagram:: perfTabs
   :parts: 1

.. automodule:: perfTabs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _randomPerfTabs-label:
      
randomPerfTabs module
---------------------

A tutorial with coding examples is available here: :ref:`RandomPerformanceTableau-Tutorial-label`

**Inheritance Diagram**

.. inheritance-diagram:: randomPerfTabs
   :parts: 1

.. automodule:: randomPerfTabs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _outrankingDigraphs-label:

outrankingDigraphs module
-------------------------

A tutorial with coding examples is available here: :ref:`OutrankingDigraphs-Tutorial-label`

**Inheritance Diagram**

.. inheritance-diagram:: outrankingDigraphs
   :top-classes: outrankingDigraphs.outrankingDigraph, outrankingDigraphs.BipolarOutrankingDigraph
   :parts: 1

.. automodule:: outrankingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _mpOutrankingDigraphs-label:

mpOutrankingDigraphs module
---------------------------

**Inheritance Diagram**

.. inheritance-diagram:: mpOutrankingDigraphs
   :top-classes: outrankingDigraphs.BipolarOutrankingDigraph
   :parts: 1

.. automodule:: mpOutrankingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

-------------

.. _ratingDigraphs-label:

ratingDigraphs module
----------------------

**Inheritance Diagram**

.. inheritance-diagram:: ratingDigraphs
   :top-classes: ratingDigraphs.RatingDigraph
   :parts: 1

.. automodule:: ratingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _sortingDigraphs-label:

sortingDigraphs module
----------------------

A tutorial with coding examples for solving multi-criteria rating problems is available here: :ref:`QuantilesRating-Tutorial-label`

**Inheritance Diagram**

.. inheritance-diagram:: sortingDigraphs
   :top-classes: sortingDigraphs.SortingDigraph
   :parts: 1

.. automodule:: sortingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _sparseOutrankingDigraphs-label:

sparseOutrankingDigraphs module
-------------------------------

**Inheritance Diagram**

.. inheritance-diagram:: sparseOutrankingDigraphs
   :top-classes: sparseOutrankingDigraphs.SparseOutrankingDigraph
   :parts: 1

.. automodule:: sparseOutrankingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _performanceQuantiles-label:

performanceQuantiles module
---------------------------

**Inheritance Diagram**

.. inheritance-diagram:: performanceQuantiles
   :parts: 1

.. automodule:: performanceQuantiles
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _votingProfiles-label:

votingProfiles module
---------------------

**Inheritance Diagram**

.. inheritance-diagram:: votingProfiles
   :top-classes: votingProfiles.VotingProfile
   :parts: 1

A tutorial with coding examples is available here: :ref:`LinearVoting-Tutorial-label`

.. automodule:: votingProfiles
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _linearOrders-label:

linearOrders module
-------------------

A tutorial with coding examples is available here: :ref:`Ranking-Tutorial-label`

**Inheritance Diagram**

.. inheritance-diagram:: linearOrders
   :top-classes: linearOrders.LinearOrder
   :parts: 1

.. automodule:: linearOrders
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _dynamicProgramming-label:

dynamicProgramming module
-------------------------

**Inheritance Diagram**

.. inheritance-diagram:: dynamicProgramming
   :top-classes: transitiveDigraphs.TransitiveDigraph			 
   :parts: 1

.. automodule:: dynamicProgramming
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _transitiveDigraphs-label:

transitiveDigraphs module
-------------------------

**Inheritance Diagram**

.. inheritance-diagram:: transitiveDigraphs
   :top-classes: transitiveDigraphs.TransitiveDigraph
   :parts: 1

.. automodule:: transitiveDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _graphs-label:

graphs module
-------------

A tutorial with coding examples is available here: :ref:`Graphs-Tutorial-label`

**Inheritance Diagram**

.. inheritance-diagram:: graphs
   :parts: 1

.. automodule:: graphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _pairings-label:

pairings module
---------------

**Inheritance Diagram**

.. inheritance-diagram:: pairings
   :parts: 1

Two tutorials with coding examples are provided: :ref:`Fair-InterGroup-Pairings-label` and :ref:`Fair-IntraGroup-Pairings-label`

.. automodule:: pairings
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _randomNumbers-label:

randomNumbers module
--------------------

**Inheritance Diagram**

.. inheritance-diagram:: randomNumbers
   :parts: 1

.. automodule:: randomNumbers
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _digraphsTools-label:

digraphsTools module
--------------------

.. automodule:: digraphsTools
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

.. _arithmetics-label:

arithmetics module
------------------

.. automodule:: arithmetics
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _xmcda-label:

xmcda module
------------

.. automodule:: xmcda
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _cythonized-label:

Cythonized modules for big digraphs
-----------------------------------

The following modules are compiled C-extensions using the Cython pre-compiler. No Python code source is provided for inspection. To distinguish them from the corresponding pure Python modules, a c- prefix is used. 

     :ref:`cRandPerfTabs-label`
	  Integer and float valued C version of the :py:mod:`randomPerfTabs` module

     :ref:`cIntegerOutrankingDigraphs-label`
	  Integer and float valued C version of the
	  :py:class:`~outrankingDigraphs.BipolarOutrankingDigraph` class

     :ref:`cIntegerSortingDigraphs-label`
	  Integer and float valued C version of the :py:class:`~sortingDigraphs.QuantilesSortingDigraph` class

     :ref:`cSparseIntegerOutrankingDigraphs-label`
	  Integer and float valued C version of sparse outranking digraphs.

     :ref:`cnpBipolarDigraphs-label`
	  New C version of bipolar outranking digraphs with a numpy integer array implemented characteristic valuation.
	  

A tutorial with coding examples is available here: :ref:`HPC-Tutorial-label`.

.. note::

   These cythonized modules, specifically designed for being run on HPC clusters (see https://hpc.uni.lu), are starting with *Threading=True* their multiprocessing threads by default with the *spawn* start method. The main program code of Python scripts using these modules must therefore be protected with the *__name__=="__main__"* test from recursive re-execution. The threading start method is actually configurable with the *StartMethod* parameter: *spawn*, *forkserver* or *fork*. The latter is not safe --especially on not Linux systems-- and may result in dead locks and hence return partial or false results. 

.. _cnpBipolarDigraphs-label:

cnpBipolarDigraphs module
.........................

**Inheritance Diagram**

.. inheritance-diagram:: cnpBipolarDigraphs
   :top-classes: cnpBipolarDigraphs.npDigraph,cRandPerfTabs.cPerformanceTableau
   :parts: 1

.. automodule:: cnpBipolarDigraphs
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _cRandPerfTabs-label:

cRandPerfTabs module
....................

**Inheritance Diagram**

.. inheritance-diagram:: cRandPerfTabs
   :top-classes: cRandPerfTabs.cPerformanceTableau
   :parts: 1

.. automodule:: cRandPerfTabs
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _cIntegerOutrankingDigraphs-label:

cIntegerOutrankingDigraphs module
.................................

.. inheritance-diagram:: cIntegerOutrankingDigraphs
   :top-classes: cRandPerfTabs.cPerformanceTableau, 
   :parts: 1

.. automodule:: cIntegerOutrankingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _cIntegerSortingDigraphs-label:

cIntegerSortingDigraphs module
..............................

.. inheritance-diagram:: cIntegerSortingDigraphs
   :top-classes: cRandPerfTabs.cPerformanceTableau
   :parts: 1

.. automodule:: cIntegerSortingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

.. _cSparseIntegerOutrankingDigraphs-label:

cSparseIntegerOutrankingDigraphs module
.......................................

**Inheritance Diagram**

.. inheritance-diagram:: cSparseIntegerOutrankingDigraphs
   :top-classes: cSparseIntegerOutrankingDigraphs.SparseIntegerDigraph
   :parts: 1

.. automodule:: cSparseIntegerOutrankingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Table of Contents <Contents-Table-label>`

-------------

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



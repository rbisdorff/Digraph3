Tutorial of the Digraph resources!
=================================================
:Author: Raymond Bisdorff, University of Luxembourg FSTC/CSC
:Version: $Revision: Python 3.3+$
:Copyright: R. Bisdorff 2014


.. toctree::
   :maxdepth: 2


.. _Tutorial-label:

Using the Digraph3 modules
--------------------------

Simple execution will show a list of results concerning a randomly generated digraph. To make directly executable the code source, you will have to adapt, the case given, the first line of the source code accordingly to your Python3 installation directory. 

See the http://www.python.org/doc in case of troubles. 

Example::

	[$Home/Digraph3]...$python3 digraphs.py
	****************************************************
	* Python digraphs module                           *
	* $Revision: 1.18 $                               *
	* Copyright (C) 2006-2007 University of Luxembourg *
	* The module comes with ABSOLUTELY NO WARRANTY     *
	* to the extent permitted by the applicable law.   *
	* This is free software, and you are welcome to    *
	* redistribute it if it remains free software.     *
	****************************************************
	*-------- Testing classes and methods -------
	==>> Testing RandomDigraph() class instantiation 
	*----- show detail -------------*
	Digraph          : randomDigraph
	*---- Actions ----*
	['1', '2', '3', '4', '5']
	*---- Characteristic valuation domain ----*
	{'med': Decimal("0.5"), 'min': Decimal("0"), 'max': Decimal("1.0")}
	* ---- Relation Table -----
	 S   |  '1',  '2',  '3',  '4',  '5',  
	-----|------------------------------------------------------------
	 '1' |  0.00  0.00  0.00  1.00  0.00 
	 '2' |  0.00  0.00  1.00  1.00  1.00 
	 '3' |  1.00  1.00  0.00  1.00  1.00 
	 '4' |  0.00  1.00  1.00  0.00  1.00 
	 '5' |  0.00  1.00  0.00  0.00  0.00 
	*--- Connected Components ---*
	1: ['1', '2', '3', '4', '5']
	Neighborhoods:
	Neighborhoods:
	  Gamma     :
	'1': in => set(['3']), out => set(['4'])
	'2': in => set(['3', '4', '5']), out => set(['3', '4', '5'])
	'3': in => set(['2', '4']), out => set(['1', '2', '4', '5'])
	'4': in => set(['1', '2', '3']), out => set(['2', '3', '5'])
	'5': in => set(['2', '3', '4']), out => set(['2'])
	  Not Gamma :
	'1': in => set(['2', '4', '5']), out => set(['2', '3', '5'])
	'2': in => set(['1']), out => set(['1'])
	'3': in => set(['1', '5']), out => set([])
	'4': in => set(['5']), out => set(['1'])
	'5': in => set(['1']), out => set(['1', '3', '4'])
	*------------------*
	If you see this line all tests were passed successfully :-)
	Enjoy !
	*************************************
	* R.B. May 2014               *
	* $Revision: 1.600+$                *
	*************************************

Working with the :code:`graphs` module
......................................

A genuine simple graph without loops and multiple limks instance consists in:

    1. the vertices: a dictionary of vertices with 'name' and 'shortname' attributes,
    2. the edges: a dictionary with frozensets of pairs of vertices as entries carrying a bipolar-valued attribute characterising the link between them ( -1 means no limk, +1 means a link, 0 models missing information).
    3. the valuation domain, a dictionary with three entries: the minimum, the median and the maximum characteristic value.
     
Example python3 session:
    >>> from graphs import Graph
    >>> g = Graph(numberOfVertices=7,edgeProbability=0.5)
    >>> g.showShort()
    *----- show short --------------*
    Name             : 'tempGraph'
    Vertices         :  ['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7']
    Valuation domain :  {'med': 0, 'max': 1, 'min': -1}
    Gamma function   : 
    v1 -> ['v5']
    v2 -> ['v4', 'v6', 'v3']
    v3 -> ['v2']
    v4 -> ['v5', 'v2', 'v7']
    v5 -> ['v4', 'v6', 'v1']
    v6 -> ['v5', 'v2']
    v7 -> ['v4']
    >>> g.save(fileName='tutorialGraph')

The saved Graph instance named :code:`tutorialGraph.py` is encoded in python3 as follows::

	# Graph instance saved in Python format
	vertices = {
	'v1': {'shortName': 'v1', 'name': 'random vertex'},
	'v2': {'shortName': 'v2', 'name': 'random vertex'},
	'v3': {'shortName': 'v3', 'name': 'random vertex'},
	'v4': {'shortName': 'v4', 'name': 'random vertex'},
	'v5': {'shortName': 'v5', 'name': 'random vertex'},
	'v6': {'shortName': 'v6', 'name': 'random vertex'},
	'v7': {'shortName': 'v7', 'name': 'random vertex'},
	}
	valuationDomain = {'min':-1,'med':0,'max':1}
	edges = {
	frozenset(['v1','v2']) : -1, 
	frozenset(['v1','v3']) : -1, 
	frozenset(['v1','v4']) : -1, 
	frozenset(['v1','v5']) : 1, 
	frozenset(['v1','v6']) : -1, 
	frozenset(['v1','v7']) : -1, 
	frozenset(['v2','v3']) : 1, 
	frozenset(['v2','v4']) : 1, 
	frozenset(['v2','v5']) : -1, 
	frozenset(['v2','v6']) : 1, 
	frozenset(['v2','v7']) : -1, 
	frozenset(['v3','v4']) : -1, 
	frozenset(['v3','v5']) : -1, 
	frozenset(['v3','v6']) : -1, 
	frozenset(['v3','v7']) : -1, 
	frozenset(['v4','v5']) : 1, 
	frozenset(['v4','v6']) : -1, 
	frozenset(['v4','v7']) : 1, 
	frozenset(['v5','v6']) : 1, 
	frozenset(['v5','v7']) : -1, 
	frozenset(['v6','v7']) : -1, 
	}

The stored graph can be recalled and plotted with the generic :code:`exportGraphViz` method as follows::

	>>> g = Graph('tutorialGraph')
	>>> g.exportGraphViz()
	*---- exporting a dot file dor GraphViz tools ---------*
	Exporting to tutorialGraph.dot
	fdp -Tpng tutorialGraph.dot -o tutorialGraph.png

.. image:: tutorialGraph.png
   :width: 400 px
   :align: center

A 3-coloring of the tutorial graph may be computed and plotted as follows::

	>>> g = Graph('tutorialGrah')
	>>> qc = Q_Coloring(g)
	Running a Gibbs Sampler for 42 step !
	The q-coloring with 3 colors is feasible !!
	>>> qc.showConfiguration()
	v5 lightblue
	v3 gold
	v7 gold
	v2 lightblue
	v4 lightcoral
	v1 gold
	v6 lightcoral
	>>> qc.exportGraphViz('tutorial-3-coloring')
	*---- exporting a dot file for GraphViz tools ---------*
	Exporting to tutorial-3-coloring.dot
	fdp -Tpng tutorial-3-coloring.dot -o tutorial-3-coloring.png

.. image:: tutorial-3-coloring.png
   :width: 400 px
   :align: center

Special classes of graphs, like nXm rectangular or triangular grid graphs are available in the :code:`graphs` module.

For more information and more code examples look into the technical documentation of the :ref:`graphs-label`
module.

Back to the :ref:`Introduction-label`

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* :ref:`Introduction-label`




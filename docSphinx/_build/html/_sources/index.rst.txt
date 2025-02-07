.. meta::
   :description: Documentation of the Digraph3 collection of python3 modules for algorithmic decision theory
   :keywords: Algorithmic Decision Theory, Outranking Digraphs, MIS and kernels, Multiple Criteria Decision Aid, Bipolar-valued Epistemic Logic

.. |location_link1| raw:: html

   <a href="https://digraph3.readthedocs.io/en/latest/" target="_blank">https://digraph3.readthedocs.io/en/latest/</a>

.. |location_link3| raw:: html

   <a href="_static/digraph3_copyright.html" target="_blank">&copy;</a>

.. |location_link4| raw:: html

   <a href="http://hdl.handle.net/10993/37933" target="_blank">Algorithmic Decision Theory</a>

Python resources for Algorithmic Decision Theory
================================================

Wecome! This is the documentation for the **Digraph3** *Python* programming resources.

:Author: Raymond Bisdorff, Emeritus Professor of Applied Mathematics and Computer Science, University of Luxembourg
:Url: https://rbisdorff.github.io/
:Version: |version| (release: |release|)
:Copyright: R. Bisdorff |location_link3| 2013-2024

.. image:: introDoc2.png
    :width: 500pt
    :align: center

.. toctree::
   :hidden:
   :numbered:
   :maxdepth: 2

   tutorial
   techDoc
   pearls
   adtLectures
   compStatLectures
   digraph3Archives
   errataList
   
.. _Documents:

Parts of the documentation
..........................
:New:

   - The documentation of the :py:mod:`arithmetics` module has been reviewed and a bipolar {-1,0,1} encoding of *Bachet* numbers has been added by the way (see the :py:class:`arithmetics.BachetNumber` class).
     
   - The tutorial on :ref:`Computing a best choice recommendation <Rubis-Tutorial-label>` has been thoroughly reviewed and upgraded
          
   - A tutorial on :ref:`using the Digraph3 HPC resources <HPC-Ranking-Tutorial-label>` for ranking several millions of multicriteria performance records via big sparse outranking digraphs
	
   - A :py:mod:`pairings` module for solving pairing problems illustrated with two tutorials on computing **fair** :ref:`intergroup<Fair-InterGroup-Pairings-label>` and :ref:`intragroup<Fair-IntraGroup-Pairings-label>` pairing solutions

   - :ref:`Condorcet's 1785 critical perspective on the simple plurality voting rule <Condorcet-Tutorial-label>`
     
   - :ref:`On characterizing bipolar-valued outranking digraphs <Sufficiency-Tutorial-label>`
     
   - :ref:`Consensus quality of the bipolar-valued outranking relation <Outranking-Consensus-Tutorial-label>`


#. `Tutorials <tutorial.html>`_

    .. raw:: html

       <small><i>Start here</i></small>
   
#. `Reference manual <techDoc.html>`_

    .. raw:: html

       <small><i>Technical documentation and source code of all Digraph3 modules</i></small>

#. `Pearls of bipolar-valued epistemic logic <pearls.html>`_

    .. raw:: html

       <small><i>Advanced theoretical and computational topics</i></small>
   
#. `Digraph3 Book <http://hdl.handle.net/10993/48296>`_

    .. raw:: html

       <a href="https://doi.org/10.1007/978-3-030-90928-4" target="_blank"><img src="_static/bookCover.png" width="240" alt="Springer ISOR 324 Book cover"/></a>
       <br>
       <a href="_static/examples.zip"><small><i>Example files</i> (zip archive, 236.4kB)</small></a>
       <br>
       <a href="errataList.html" target="_blank"><small><i>Errata List</i></small></a>

#. `Algorithimc Decision Theory Lectures <adtLectures.html>`_

    .. raw:: html

       <small><i>2x2 reduced copies of the presentation slides</i></small>

#. `Computational Statistics Lectures <compStatLectures.html>`_

    .. raw:: html

       <small><i>2x2 reduced copies of the presentation slides</i></small>

#. `Archives <digraph3Archives.html>`_

    .. raw:: html

       <small><i>Historical case studies and example graphs</i></small>


**Indices and search results**

#. `General Index <genindex.html>`_

    .. raw:: html

       <small><i>All classes, functions and terms</i></small>
  
#. `Module Index <py-modindex.html>`_

    .. raw:: html

       <small><i>Quick access to all the</i> <b>Digraph3</b> <i>modules</i></small>
  
#. `Search page <search.html>`_

    .. raw:: html

       <small><i>Results of current search request</i></small>

.. role:: raw-html(raw)
   :format: html

.. _Introduction-label:

Introduction
............

     |    *This documentation is dedicated to*
     |    *our colleague and dear friend*
     |    *the late Prof.* Marc ROUBENS

The *Digraph3 documentation*, available on the `Read The Docs <https://readthedocs.org/>`_ site: |location_link1|, describes the Python3 resources for implementing decision algorithms via **bipolar-valued outranking** digraphs [:raw-html:`<a class="reference internal" href="#Bisdorff-2022" id="id1"><span>1</span></a>`]. These computing resources are useful in the field of `Algorithmic Decision Theory <https://www.lamsade.dauphine.fr/~projet_cost/ALGORITHMIC_DECISION_THEORY/ALGORITHMIC_DECISION_THEORY.html>`_ and more specifically in the field of **Multiple-Criteria Decision Aiding** [:raw-html:`<a class="reference internal" href="#Bisdorff-2015" id="id2"><span>2</span></a>`]. They provide practical tools for a Master Course on |location_link4| taught at the University of Luxembourg.
      
The documentation contains, first, a set of tutorials introducing the main objects like **digraphs**, **outranking digraphs** and **performance tableaux**. There is also a tutorial provided on **undirected graphs**. Some tutorials are problem oriented and show how to compute the **winner of an election**, how to build a **best choice recommendation**, or **how to linearly rank or rate** with multiple incommensurable performance criteria. The tutorial about **split**, **interval** and **permutation graphs** is inspired by *Martin Golumbic* 's book on *Algorithmic Graph Theory and Perfect Graphs* [:raw-html:`<a class="reference internal" href="#Golumbic-2004" id="id3"><span>3</span></a>`]. We also provide a tutorial on **tree graphs** and **spanning forests**. Recently added, the reader may find two tutorials on **fairly** solving **inter**-, respectively **intragroup pairing** problems. 

The second Section concerns the **extensive reference manual** of the collection of provided Python3 modules, classes and methods. The main classes in this collection are the :py:class:`digraphs.Digraph` overall root class, the :py:class:`perfTabs.PerformanceTableau` class and the :py:class:`outrankingDigraphs.BipolarOutrankingDigraph` class. The technical documentation also provides insight into the complete source code of all modules, classes and methods.

The third Section exhibits some pearls of **bipolar-valued epistemic logic** that enrich the Digraph3 resources. These short topics illustrate well the very computational benefit one may get when working in a bipolar-valued logical framework. And, more specifically, the essential part the *logically neutral* **undeterminate** value is judiciously playing therein.  

The fourth and fifth sections provide 2x2-reduced notes of the author's lectures on **Algorithmic Decision Theory** and **Computational Statistics** given at the University of Luxembourg in Autumn 2019 and Spring 2020.

The last section gathers **historical case studies** with example digraphs compiled before 2006 and concerning the early development of tools and methods for enumerating *non isomorphic maximal independent sets* in undirected graphs and computing *digraph kernels*. 

.. _Bibliography-label:

.. **References**

.. raw:: html

    <p class="rubric" id="bibliography-label">References</p>
    <div role="list" class="citation-list">
    <div class="citation" id="Bisdorff-2022" role="doc-biblioentry">
    <span class="label"><span class="fn-bracket">[</span><a role="doc-backlink" href="#id1">1</a><span class="fn-bracket">]</span></span>
    <p>Bisdorff (Feb 2022). <em>Algorithmic Decision Making with Python Resources: From multicriteria performance records to decision algorithms via bipolar-valued outranking digraphs</em>. Springer Verlag Heidelberg, International Series in Operations Research &amp; Management Science ISOR 324, ISBN 978-3-030-90927-2, xli, 346 pages (see <a class="reference external" href="https://doi.org/10.1007/978-3-030-90928-4">https://doi.org/10.1007/978-3-030-90928-4</a>).</p>
    </div>
    <div class="citation" id="Bisdorff-2015" role="doc-biblioentry">
    <span class="label"><span class="fn-bracket">[</span><a role="doc-backlink" href="#id2">2</a><span class="fn-bracket">]</span></span>
    <p>Bisdorff, L.C. Dias, P. Meyer, V. Mousseau and M. Pirlot (Eds.) (2015). <em>Evaluation and decision models with multiple criteria: Case studies</em>. Springer-Verlag Berlin Heidelberg, International Handbooks on Information Systems, <a class="reference external" href="https://link.springer.com/book/10.1007/978-3-662-46816-6">ISBN 978-3-662-46815-9</a>, 643 pages.</p>
    </div>
    <div class="citation" id="Golumbic-2004" role="doc-biblioentry">
    <span class="label"><span class="fn-bracket">[</span><a role="doc-backlink" href="#id3">3</a><span class="fn-bracket">]</span></span>
    <p>Ch. Golumbic (2004), <em>Algorithmic Graph Theory and Perfect Graphs</em> 2nd Ed., Annals of Discrete Mathematics 57, Elsevier.</p>
    </div>
    </div>

.. .. [BISD-22i] R. Bisdorff (Feb 2022). *Algorithmic Decision Making with Python Resources: From multicriteria performance records to decision algorithms via bipolar-valued outranking digraphs*. Springer Verlag Heidelberg, International Series in Operations Research & Management Science ISOR 324, ISBN 978-3-030-90927-2, xli, 346 pages (see https://doi.org/10.1007/978-3-030-90928-4).
	     
.. .. [BISD-15i] R. Bisdorff, L.C. Dias, P. Meyer, V. Mousseau and M. Pirlot (Eds.) (2015). *Evaluation and decision models with multiple criteria: Case studies*. Springer-Verlag Berlin Heidelberg, International Handbooks on Information Systems, `ISBN 978-3-662-46815-9 <https://link.springer.com/book/10.1007/978-3-662-46816-6>`_, 643 pages.

.. .. [GOLU-04i] M. Ch. Golumbic (2004), *Agorithmic Graph Theory and Perfect Graphs* 2nd Ed., Annals of Discrete Mathematics 57, Elsevier.

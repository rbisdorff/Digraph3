Digraph3 Archives
=================

:Author: *Raymond BISDORFF*, Emeritus Professor of Applied Mathematics and Computer Science, University of Luxembourg
:Url: https://rbisdorff.github.io/
:Copyright: `R. Bisdorff <_static/digraph3_copyright.html>`_ 2013-2023

**Introduction**

The *Digraph3 Archives* gather historical case studies and example digraphs compiled before 2006 and concerning the early development of python modules implementing tools and methods of the *Rubis decision aiding* approach (see [BISD-2008]_).

A first collection of pages is devoted to the problem of enumerating *non isomorphic kernels* in symmetric digraphs like the *Petersen*, the *Coxeter* and the *Chvátal* graph for instance (see :ref:`IsomorphicMIS-Tutorial-label`). A second collection concerns the early development of the *Rubis best choice algorithm* (see :ref:`Rubis-Tutorial-label`). And, a third collection finally illustrates the concepts of *hyperkernels* and *prekernels* in digraphs (see :ref:`Kernel-Tutorial-label`).

More than 15 years later now, the historical discussions and illustrations of outranking digraphs, with potential best choice recommendations, appear rather confuse and controversial. It is worthwhile noticing that the concept of *outranking digraph* has meanwhile become much more accurate both, from a *logical* as well as, from an *epistemic* perspective (see [BISD-2013]_).

In our present terms, the *outranking concept* is indeed modelled as a *hybrid* object. On the one hand, it is a *bipolar-valued digraph* object, modelling pairwise outranking *relations* between potential *decision alternatives*. On the other hand, the same concept models *preferential situations*, observed between decision alternatives that are assessed on *multiple incommensurable performance criteria*, as gathered in what we call a *performance tableau* object.

Such bipolar-valued outranking digraphs are specifically characterised by the fact that they verify a *strong completeness* property and the *coduality principle*, i.e. *not outranking* situations necessarily correspond to the corresponding *strictly outranked* situations. Contrary, hence, to the historical outranking digraph examples shown below, we nowadays model a potential *incomparability* situation not via the absence of an outranking, but as an *indeterminate* situation (see :ref:`CopingMissing-Data-label`). With this more accurate epistemic modelling, the *strict outranking kernel* concept gains great effectiveness for computing best choice recommendations from a given outranking digraph (see :ref:`Kernel-Tutorial-label`).     

-------------------

.. raw:: html
	 
   <h3><a href="_static/GraphDataSets/index.html" target="_blank"><b>Link to the Digraph3 Archives</b></a></h3>

**References**   
   
.. [BISD-2008] Bisdorff R., Meyer P. and Roubens M.(2008) "RUBIS: a bipolar-valued outranking method for the choice problem". 4OR, *A Quarterly Journal of Operations Research* Springer-Verlag, Volume 6,  Number 2 pp. 143-165. (Online) Electronic version: DOI: 10.1007/s10288-007-0045-5 (downloadable preliminary version `PDF file 271.5Kb <_static/HyperKernels.pdf>`_).

.. [BISD-2013] Bisdorff R. (2013) "On Polarizing Outranking Relations with Large Performance Differences" *Journal of Multi-Criteria Decision Analysis* (Wiley) **20**:3-12 (downloadable preprint `PDF file 403.5 Kb <_static/MCDA-10-0059-PrePeerReview.pdf>`_).

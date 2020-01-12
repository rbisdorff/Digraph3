Extraction of minimal dominant choices
by reduction of X to minimal dominating sets
R. Bisdorff, April 2005               
--------------------------------------
direct neighbors :  {'3_1': (set(['2_1', '4_1', '3_2']), set(['2_1', '4_1', '3_2'])), '3_2': (set(['3_1', '4_2', '6_2']), set(['3_1', '4_2', '6_2'])), '6_1': (set(['5_1', '1_1', '6_2']), set(['5_1', '1_1', '6_2'])), '6_2': (set(['5_2', '3_2', '6_1']), set(['5_2', '3_2', '6_1'])), '2_1': (set(['3_1', '2_2', '1_1']), set(['3_1', '2_2', '1_1'])), '2_2': (set(['2_1', '1_2', '5_2']), set(['2_1', '1_2', '5_2'])), '5_2': (set(['2_2', '5_1', '6_2']), set(['2_2', '5_1', '6_2'])), '5_1': (set(['5_2', '4_1', '6_1']), set(['5_2', '4_1', '6_1'])), '1_2': (set(['4_2', '2_2', '1_1']), set(['4_2', '2_2', '1_1'])), '1_1': (set(['2_1', '6_1', '1_2']), set(['2_1', '6_1', '1_2'])), '4_2': (set(['4_1', '3_2', '1_2']), set(['4_1', '3_2', '1_2'])), '4_1': (set(['3_1', '4_2', '5_1']), set(['3_1', '4_2', '5_1']))}
not direct neighbors :  {'3_1': (set(['3_1', '6_1', '6_2', '2_2', '5_2', '5_1', '1_2', '1_1', '4_2']), set(['3_1', '6_1', '6_2', '2_2', '5_2', '5_1', '1_2', '1_1', '4_2'])), '3_2': (set(['3_2', '6_1', '2_1', '2_2', '5_2', '5_1', '1_2', '1_1', '4_1']), set(['3_2', '6_1', '2_1', '2_2', '5_2', '5_1', '1_2', '1_1', '4_1'])), '6_1': (set(['3_1', '3_2', '6_1', '2_1', '2_2', '5_2', '1_2', '4_2', '4_1']), set(['3_1', '3_2', '6_1', '2_1', '2_2', '5_2', '1_2', '4_2', '4_1'])), '6_2': (set(['3_1', '6_2', '2_1', '2_2', '5_1', '1_2', '1_1', '4_2', '4_1']), set(['3_1', '6_2', '2_1', '2_2', '5_1', '1_2', '1_1', '4_2', '4_1'])), '2_1': (set(['3_2', '6_1', '6_2', '2_1', '5_2', '5_1', '1_2', '4_2', '4_1']), set(['3_2', '6_1', '6_2', '2_1', '5_2', '5_1', '1_2', '4_2', '4_1'])), '2_2': (set(['3_1', '3_2', '6_1', '6_2', '2_2', '5_1', '1_1', '4_2', '4_1']), set(['3_1', '3_2', '6_1', '6_2', '2_2', '5_1', '1_1', '4_2', '4_1'])), '5_2': (set(['3_1', '3_2', '6_1', '2_1', '5_2', '1_2', '1_1', '4_2', '4_1']), set(['3_1', '3_2', '6_1', '2_1', '5_2', '1_2', '1_1', '4_2', '4_1'])), '5_1': (set(['3_1', '3_2', '6_2', '2_1', '2_2', '5_1', '1_2', '1_1', '4_2']), set(['3_1', '3_2', '6_2', '2_1', '2_2', '5_1', '1_2', '1_1', '4_2'])), '1_2': (set(['3_1', '3_2', '6_1', '6_2', '2_1', '5_2', '5_1', '1_2', '4_1']), set(['3_1', '3_2', '6_1', '6_2', '2_1', '5_2', '5_1', '1_2', '4_1'])), '1_1': (set(['3_1', '3_2', '6_2', '2_2', '5_2', '5_1', '1_1', '4_2', '4_1']), set(['3_1', '3_2', '6_2', '2_2', '5_2', '5_1', '1_1', '4_2', '4_1'])), '4_2': (set(['3_1', '6_1', '6_2', '2_1', '2_2', '5_2', '5_1', '1_1', '4_2']), set(['3_1', '6_1', '6_2', '2_1', '2_2', '5_2', '5_1', '1_1', '4_2'])), '4_1': (set(['3_2', '6_1', '6_2', '2_1', '2_2', '5_2', '1_2', '1_1', '4_1']), set(['3_2', '6_1', '6_2', '2_1', '2_2', '5_2', '1_2', '1_1', '4_1']))}
Connected Components:
1: set(['3_1', '3_2', '6_1', '6_2', '2_1', '2_2', '5_2', '5_1', '1_2', '1_1', '4_2', '4_1'])

--------------------------------------

connected component : set(['3_1', '3_2', '6_1', '6_2', '2_1', '2_2', '5_2', '5_1', '1_2', '1_1', '4_2', '4_1'])

------------------
    Iterations    
1 ------------
Minimal dominant choice:  frozenset(['3_1', '4_2', '2_2', '6_1'])
Minimal absorbent choice:  frozenset(['3_1', '4_2', '2_2', '6_1'])
Minimal dominant choice:  frozenset(['3_1', '5_2', '6_1', '1_2'])
Minimal absorbent choice:  frozenset(['3_1', '5_2', '6_1', '1_2'])
Minimal dominant choice:  frozenset(['3_1', '5_2', '6_1', '4_2'])
Minimal absorbent choice:  frozenset(['3_1', '5_2', '6_1', '4_2'])
Minimal dominant choice:  frozenset(['3_1', '5_1', '6_2', '1_1', '4_2', '2_2'])
Minimal absorbent choice:  frozenset(['3_1', '5_1', '6_2', '1_1', '4_2', '2_2'])
Minimal dominant choice:  frozenset(['3_1', '5_1', '1_2', '6_2'])
Minimal absorbent choice:  frozenset(['3_1', '5_1', '1_2', '6_2'])
Minimal dominant choice:  frozenset(['3_1', '5_2', '1_1', '4_2'])
Minimal absorbent choice:  frozenset(['3_1', '5_2', '1_1', '4_2'])
2 ------------
Minimal dominant choice:  frozenset(['5_2', '3_2', '1_2', '2_1', '4_1', '6_1'])
Minimal absorbent choice:  frozenset(['5_2', '3_2', '1_2', '2_1', '4_1', '6_1'])
Minimal dominant choice:  frozenset(['4_1', '2_2', '3_2', '6_1'])
Minimal absorbent choice:  frozenset(['4_1', '2_2', '3_2', '6_1'])
Minimal dominant choice:  frozenset(['2_1', '5_1', '3_2', '1_2'])
Minimal absorbent choice:  frozenset(['2_1', '5_1', '3_2', '1_2'])
Minimal dominant choice:  frozenset(['2_2', '3_2', '5_1', '1_1'])
Minimal absorbent choice:  frozenset(['2_2', '3_2', '5_1', '1_1'])
Minimal dominant choice:  frozenset(['4_1', '2_2', '3_2', '1_1'])
Minimal absorbent choice:  frozenset(['4_1', '2_2', '3_2', '1_1'])
Minimal dominant choice:  frozenset(['5_2', '4_1', '3_2', '1_1'])
Minimal absorbent choice:  frozenset(['5_2', '4_1', '3_2', '1_1'])
3 ------------
Minimal dominant choice:  frozenset(['4_2', '2_1', '6_1', '5_2'])
Minimal absorbent choice:  frozenset(['4_2', '2_1', '6_1', '5_2'])
4 ------------
Minimal dominant choice:  frozenset(['4_2', '2_1', '5_1', '6_2'])
Minimal absorbent choice:  frozenset(['4_2', '2_1', '5_1', '6_2'])
Minimal dominant choice:  frozenset(['2_1', '5_1', '1_2', '6_2'])
Minimal absorbent choice:  frozenset(['2_1', '5_1', '1_2', '6_2'])
Minimal dominant choice:  frozenset(['2_1', '4_1', '1_2', '6_2'])
Minimal absorbent choice:  frozenset(['2_1', '4_1', '1_2', '6_2'])
Minimal dominant choice:  frozenset(['2_2', '4_1', '6_2', '1_1'])
Minimal absorbent choice:  frozenset(['2_2', '4_1', '6_2', '1_1'])
5 ------------
6 ------------
7 ------------
8 ------------
9 ------------
10 ------------
11 ------------
12 ------------
------------------
    Statistics    
------------------
  Global results  
== >>  frozenset(['2_2', '4_1', '6_2', '1_1'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['5_2', '3_2', '1_2', '2_1', '4_1', '6_1'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['4_1', '2_2', '3_2', '1_1'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['3_1', '5_2', '6_1', '1_2'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['3_1', '5_2', '1_1', '4_2'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['4_2', '2_1', '5_1', '6_2'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['3_1', '5_1', '6_2', '1_1', '4_2', '2_2'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['2_2', '3_2', '5_1', '1_1'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['4_1', '2_2', '3_2', '6_1'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['3_1', '5_1', '1_2', '6_2'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['4_2', '2_1', '6_1', '5_2'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['5_2', '4_1', '3_2', '1_1'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['2_1', '4_1', '1_2', '6_2'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['2_1', '5_1', '3_2', '1_2'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['2_1', '5_1', '1_2', '6_2'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['3_1', '4_2', '2_2', '6_1'])
independance: 2 ; dominance: 2 ; absorbancy: 2

== >>  frozenset(['3_1', '5_2', '6_1', '4_2'])
independance: 2 ; dominance: 2 ; absorbancy: 2


Time needed: 0.01 ; History length:  195
---- end component ----


--- end of components ----
******************
* allkernels.py  *
* R.B. June 2005 *
******************

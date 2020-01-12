/* exemple ROY de Lausanne  */
actionset([a, b, c]).

evaluationdomain:-
asserta((valuationdomain(V) :- fd_domain(V, 0, 100))).

relation(a, a, 100):- !.
relation(a, b, 0):- !.
relation(a, c, 100):- !.
relation(b, a, 55):- !.
relation(b, b, 100):- !.
relation(b, c, 100):- !.
relation(c, a, 55):- !.
relation(c, b, 55):- !.
relation(c, c, 100):- !.

/* ------------  resultat
Bipolar ranking of relation : roylausorig
choices : 

    Initial kernels =[[[45,100,0]]]
    1 best choice  : [b]([100])

        Initial kernels =[[[100]]]
        2 best choice  : [a]([100])
        residual class : [a](50)

        Terminal kernels =[[[100]]]
        residual class : [a](50)
        2 worst choice  : [a]([100])

    Terminal kernels =[[[0,0,100]]]
    1 worst choice  : [c]([100])
*-------------------------------------------*/

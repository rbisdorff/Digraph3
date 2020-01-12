/* exemple 4 On Good Choices  */
/* Roy-Bouysso p.383 */
actionset([a1, a2, a3, a4, a5, a6, a7, a8, a9]).

evaluationdomain:-
asserta((valuationdomain(V) :- fd_domain(V, 0, 100))).

relation(a1, a1, 100):- !.
relation(a2, a1, 69):- !.
relation(a3, a1, 62):- !.
relation(a4, a1, 69):- !.
relation(a5, a1, 0):- !.
relation(a6, a1, 0):- !.
relation(a7, a1, 77):- !.
relation(a8, a1, 45):- !.
relation(a9, a1, 12):- !.

relation(a1, a2, 72):- !.
relation(a2, a2, 100):- !.
relation(a3, a2, 92):- !.
relation(a4, a2, 85):- !.
relation(a5, a2, 0):- !.
relation(a6, a2, 0):- !.
relation(a7, a2, 57):- !.
relation(a8, a2, 21):- !.
relation(a9, a2, 18):- !.

relation(a1, a3, 67):- !.
relation(a2, a3, 87):- !.
relation(a3, a3, 100):- !.
relation(a4, a3, 79):- !.
relation(a5, a3, 0):- !.
relation(a6, a3, 0):- !.
relation(a7, a3, 30):- !.
relation(a8, a3, 17):- !.
relation(a9, a3, 6):- !.

relation(a1, a4, 79):- !.
relation(a2, a4, 72):- !.
relation(a3, a4, 85):- !.
relation(a4, a4, 100):- !.
relation(a5, a4, 0):- !.
relation(a6, a4, 0):- !.
relation(a7, a4, 59):- !.
relation(a8, a4, 21):- !.
relation(a9, a4, 17):- !.

relation(a1, a5, 92):- !.
relation(a2, a5, 92):- !.
relation(a3, a5, 92):- !.
relation(a4, a5, 100):- !.
relation(a5, a5, 100):- !.
relation(a6, a5, 95):- !.
relation(a7, a5, 87):- !.
relation(a8, a5, 67):- !.
relation(a9, a5, 74):- !.

relation(a1, a6, 74):- !.
relation(a2, a6, 64):- !.
relation(a3, a6, 77):- !.
relation(a4, a6, 72):- !.
relation(a5, a6, 0):- !.
relation(a6, a6, 100):- !.
relation(a7, a6, 92):- !.
relation(a8, a6, 27):- !.
relation(a9, a6, 0):- !.

relation(a1, a7, 69):- !.
relation(a2, a7, 0):- !.
relation(a3, a7, 21):- !.
relation(a4, a7, 24):- !.
relation(a5, a7, 0):- !.
relation(a6, a7, 42):- !.
relation(a7, a7, 100):- !.
relation(a8, a7, 27):- !.
relation(a9, a7, 0):- !.

relation(a1, a8, 25):- !.
relation(a2, a8, 27):- !.
relation(a3, a8, 79):- !.
relation(a4, a8, 8):- !.
relation(a5, a8, 0):- !.
relation(a6, a8, 0):- !.
relation(a7, a8, 79):- !.
relation(a8, a8, 100):- !.
relation(a9, a8, 48):- !.

relation(a1, a9, 5):- !.
relation(a2, a9, 67):- !.
relation(a3, a9, 59):- !.
relation(a4, a9, 4):- !.
relation(a5, a9, 0):- !.
relation(a6, a9, 0):- !.
relation(a7, a9, 9):- !.
relation(a8, a9, 64):- !.
relation(a9, a9, 100):- !.






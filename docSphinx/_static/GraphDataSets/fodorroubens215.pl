actionset([vwgc, r9gt, gsax, p305, tahg, audi, r18g, alfa]).

evaluationdomain:-
asserta((valuationdomain(V) :- fd_domain(V, 0, 100))).

/* concordance and discordance Rubens & Fodor 215 */
relation(vwgc, vwgc, 0):- !.
relation(vwgc, r9gt,  75):- !.
relation(vwgc, gsax,  70):- !.
relation(vwgc, p305,  62):- !.
relation(vwgc, tahg,  0):- !.
relation(vwgc, audi,  0):- !.
relation(vwgc, r18g,  0):- !.
relation(vwgc, alfa,  0):- !.

relation(r9gt, vwgc,  76):- !.
relation(r9gt, r9gt, 0):- !.
relation(r9gt, gsax,  90):- !.
relation(r9gt, p305,  100):- !.
relation(r9gt, tahg,  82):- !.
relation(r9gt, audi,  82):- !.
relation(r9gt, r18g,  82):- !.
relation(r9gt, alfa,  80):- !.

relation(gsax, vwgc,  70):- !.
relation(gsax, r9gt,  86):- !.
relation(gsax, gsax, 0):- !.
relation(gsax, p305,  100):- !.
relation(gsax, tahg,  100):- !.
relation(gsax, audi,  46):- !.
relation(gsax, r18g,  80):- !.
relation(gsax, alfa,  91):- !.

relation(p305, vwgc,  64):- !.
relation(p305, r9gt,  65):- !.
relation(p305, gsax,  94):- !.
relation(p305, p305, 0):- !.
relation(p305, tahg,  88):- !.
relation(p305, audi,  22):- !.
relation(p305, r18g,  94):- !.
relation(p305, alfa,  74):- !.

relation(tahg, vwgc,  33):- !.
relation(tahg, r9gt,  57):- !.
relation(tahg, gsax,  93):- !.
relation(tahg, p305,  100):- !.
relation(tahg, tahg, 0):- !.
relation(tahg, audi,  0):- !.
relation(tahg, r18g,  80):- !.
relation(tahg, alfa,  86):- !.

relation(audi, vwgc,  0):- !.
relation(audi, r9gt,  73):- !.
relation(audi, gsax,  64):- !.
relation(audi, p305,  92):- !.
relation(audi, tahg,  76):- !.
relation(audi, audi, 0):- !.
relation(audi, r18g,  96):- !.
relation(audi, alfa,  80):- !.

relation(r18g, vwgc,  0):- !.
relation(r18g, r9gt,  63):- !.
relation(r18g, gsax,  73):- !.
relation(r18g, p305,  85):- !.
relation(r18g, tahg,  82):- !.
relation(r18g, audi,  70):- !.
relation(r18g, r18g, 0):- !.
relation(r18g, alfa,  81):- !.

relation(alfa, vwgc,  0):- !.
relation(alfa, r9gt,  60):- !.
relation(alfa, gsax,  64):- !.
relation(alfa, p305,  60):- !.
relation(alfa, tahg,  77):- !.
relation(alfa, audi,  0):- !.
relation(alfa, r18g,  0):- !.
relation(alfa, alfa, 0):- !.


/* ---------- resultat 
Bipolar ranking of relation : voitures
choices : 

    Initial kernels =[[[24,76,24,24,24,24,24,24]]]
    1 best choice  : [r9gt]([76])

        Initial kernels =[[[30,30,30,70,30,30]]]
        2 best choice  : [r18g]([70])

            Initial kernels =[[[64,36,36,36],[36,36,64,36]]]
            3 best choice  : [p305,audi]([64,64])

            Terminal kernels =[[[36,64,36,36],[36,36,36,64]]]
            3 worst choice  : [vwgc,gsax]([64,64])

        Terminal kernels =[[[31,31,31,31,69,31]]]
        2 worst choice  : [tahg]([69])

    Terminal kernels =[[[26,26,26,26,26,26,26,74]]]
    1 worst choice  : [alfa]([74])
*/

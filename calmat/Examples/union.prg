rem "union de deux vecteurs booléens"
rem "union.prg vec_1 vec_2 vec_3 dimension"
load %1 a 1 %4
load %2 b 1 %4
c = a | b
print a
print b
print c
save c %3
end

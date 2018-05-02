rem ok
load matr.dat a 5 5
c = a ¨ a
d = a ¨ c
while c < d
d = c ¨ c
endwhile
rem " la relation d est la "
rem " fermeture transitive de "
rem " la relation a"
save a con:
save c con:
save d con:
end

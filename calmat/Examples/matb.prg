rem ok
load matb.prn a 4 4
load matb1.prn b 4 4
c = ( a À b )
d = (c À c)
while c < d
d = c À c
endwhile
rem " la relation d est la "
rem " fermeture transitive de "
rem " la relation c = ( a À b)"
save a con:
save b con:
save c con:
save d con:
end

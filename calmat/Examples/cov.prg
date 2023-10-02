load examples/covt.mat a 4 4
b = cent_red(a)
print b
c =   (`b * b)
print c
c = 0.25 c
save c cov.mat
end

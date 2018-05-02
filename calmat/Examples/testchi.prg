load can79_84.prn a 13 4
b = a * `a
dist_fact b
load mat_diag.prn a 13 13
tridiag a
load val_prop.prn a 13 2
save a valcan.prn
load can79_84.prn a 13 4
b = `a * a
dist_fact b
load mat_diag.prn a 4 4
tridiag a
end

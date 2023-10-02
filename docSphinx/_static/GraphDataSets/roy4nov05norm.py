##########################################
# generating outranking graphs from a    #
# a given performance tableau            #
# standard concordance and non veto      #
# R. Bisdorff January 2006               #
##########################################
# standard outranking graph from  <module 'roy4nov05' from '/home/bisi/Current/NewPythonConcordance/roy4nov05.pyc'>
actionset = [
'a',
'b',
'c',
'd',
]
valuationdomain = {'min':0.0, 'med':50.0, 'max':100.0}
relation = {
'a': {
'a':100,
'b':80,
'c':80,
'd':0,
},
'b': {
'a':60,
'b':100,
'c':80,
'd':80,
},
'c': {
'a':40,
'b':0,
'c':100,
'd':80,
},
'd': {
'a':60,
'b':40,
'c':60,
'd':100,
},
}

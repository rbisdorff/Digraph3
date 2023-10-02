# The Berge mistery story 
# Golumbic, M. C. Algorithmic Graph Theory and Perfect Graphs
# Annals of Discrete Mathematics 57 p. 20
vertices = {
'A': {'name': 'Abe', 'shortName': 'A'},
'B': {'name': 'Burt', 'shortName': 'B'},
'C': {'name': 'Charlotte', 'shortName': 'C'},
'D': {'name': 'Desmond', 'shortName': 'D'},
'E': {'name': 'Eddie', 'shortName': 'E'},
'I': {'name': 'Ida', 'shortName': 'I'},
}
valuationDomain = {'min':-1,'med':0,'max':1}
edges = {
frozenset(['A','B']) : 1, 
frozenset(['A','C']) : -1, 
frozenset(['A','D']) : -1, 
frozenset(['A','E']) : 1, 
frozenset(['A','I']) : -1, 
frozenset(['B','C']) : -1, 
frozenset(['B','D']) : -1, 
frozenset(['B','E']) : 1, 
frozenset(['B','I']) : 1, 
frozenset(['C','D']) : 1, 
frozenset(['C','E']) : 1, 
frozenset(['C','I']) : 1, 
frozenset(['D','E']) : -1, 
frozenset(['D','I']) : 1, 
frozenset(['E','I']) : 1, 
}

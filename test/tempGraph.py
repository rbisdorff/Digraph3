# Graph instance saved in Python format
from decimal import Decimal
vertices = {
'v1': {'id': 1, 'shortName': 'v1', 'name': 'random vertex'},
'v2': {'id': 2, 'shortName': 'v2', 'name': 'random vertex'},
'v3': {'id': 3, 'shortName': 'v3', 'name': 'random vertex'},
'v4': {'id': 4, 'shortName': 'v4', 'name': 'random vertex'},
'v5': {'id': 5, 'shortName': 'v5', 'name': 'random vertex'},
}
valuationDomain = {'min':-1,'med':0,'max':1}
edges = {
frozenset(['v1','v2']) : 0, 
frozenset(['v1','v3']) : 0, 
frozenset(['v1','v4']) : 0, 
frozenset(['v1','v5']) : 0, 
frozenset(['v2','v3']) : 0, 
frozenset(['v2','v4']) : 0, 
frozenset(['v2','v5']) : 0, 
frozenset(['v3','v4']) : 0, 
frozenset(['v3','v5']) : 0, 
frozenset(['v4','v5']) : 0, 
}

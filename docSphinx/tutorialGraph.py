# Graph instance saved in Python format
vertices = {
'v1': {'shortName': 'v1', 'name': 'random vertex'},
'v2': {'shortName': 'v2', 'name': 'random vertex'},
'v3': {'shortName': 'v3', 'name': 'random vertex'},
'v4': {'shortName': 'v4', 'name': 'random vertex'},
'v5': {'shortName': 'v5', 'name': 'random vertex'},
'v6': {'shortName': 'v6', 'name': 'random vertex'},
'v7': {'shortName': 'v7', 'name': 'random vertex'},
}
valuationDomain = {'min':-1,'med':0,'max':1}
edges = {
frozenset(['v1','v2']) : -1, 
frozenset(['v1','v3']) : -1, 
frozenset(['v1','v4']) : -1, 
frozenset(['v1','v5']) : 1, 
frozenset(['v1','v6']) : -1, 
frozenset(['v1','v7']) : -1, 
frozenset(['v2','v3']) : 1, 
frozenset(['v2','v4']) : 1, 
frozenset(['v2','v5']) : -1, 
frozenset(['v2','v6']) : 1, 
frozenset(['v2','v7']) : -1, 
frozenset(['v3','v4']) : -1, 
frozenset(['v3','v5']) : -1, 
frozenset(['v3','v6']) : -1, 
frozenset(['v3','v7']) : -1, 
frozenset(['v4','v5']) : 1, 
frozenset(['v4','v6']) : -1, 
frozenset(['v4','v7']) : 1, 
frozenset(['v5','v6']) : 1, 
frozenset(['v5','v7']) : -1, 
frozenset(['v6','v7']) : -1, 
}


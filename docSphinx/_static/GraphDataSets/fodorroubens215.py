# relation : roubens215
actionset= ['vwgc',
'r9gt',
'gsax',
'p305',
'tahg',
'audi',
'r18g',
'alfa']
valuationdomain = { 'min':0, 'med':50, 'max': 100}
relation = {

'vwgc': {
'vwgc': 0,
'r9gt': 75,
'gsax': 70,
'p305': 62,
'tahg': 0,
'audi': 0,
'r18g': 0,
'alfa': 0,
},
'r9gt': {
'vwgc': 76,
'r9gt': 0,
'gsax': 90,
'p305': 100,
'tahg': 82,
'audi': 82,
'r18g': 82,
'alfa': 80,
},
'gsax': {
'vwgc': 70,
'r9gt': 86,
'gsax': 0,
'p305': 100,
'tahg': 100,
'audi': 46,
'r18g': 80,
'alfa': 91,
},
'p305': {
'vwgc': 64,
'r9gt': 65,
'gsax': 94,
'p305': 0,
'tahg': 88,
'audi': 22,
'r18g': 94,
'alfa': 74,
},
'tahg': {
'vwgc': 33,
'r9gt': 57,
'gsax': 93,
'p305': 100,
'tahg': 0,
'audi': 0,
'r18g': 80,
'alfa': 86,
},
'audi': {
'vwgc': 0,
'r9gt': 73,
'gsax': 64,
'p305': 92,
'tahg': 76,
'audi': 0,
'r18g': 96,
'alfa': 80,
},
'r18g': {
'vwgc': 0,
'r9gt': 63,
'gsax': 73,
'p305': 85,
'tahg': 82,
'audi': 70,
'r18g': 0,
'alfa': 81,
},
'alfa': {
'vwgc': 0,
'r9gt': 60,
'gsax': 64,
'p305': 60,
'tahg': 77,
'audi': 0,
'r18g': 0,
'alfa': 0,
},}

reflections = {
    'g1':
    frozenset([
    ('gsax','p305')
    ])
    }

rotations = {
    }

# computed hyper graph from berge54.py
actionset = [
'1',
'3',
'2',
'5',
'4',
'7',
'6',
'_1_3_2_',
]
valuationdomain =  {'med': 50, 'max': 100, 'min': 0}
relation = {
'1': {
'1': 0,
'3': 0,
'2': 100,
'5': 0,
'4': 100,
'7': 0,
'6': 0,
'_1_3_2_': 100,
},
'3': {
'1': 100,
'3': 0,
'2': 0,
'5': 100,
'4': 0,
'7': 0,
'6': 0,
'_1_3_2_': 100,
},
'2': {
'1': 0,
'3': 100,
'2': 0,
'5': 0,
'4': 0,
'7': 0,
'6': 100,
'_1_3_2_': 100,
},
'5': {
'1': 0,
'3': 0,
'2': 0,
'5': 0,
'4': 0,
'7': 100,
'6': 0,
'_1_3_2_': 0,
},
'4': {
'1': 0,
'3': 0,
'2': 0,
'5': 0,
'4': 0,
'7': 100,
'6': 0,
'_1_3_2_': 0,
},
'7': {
'1': 0,
'3': 0,
'2': 0,
'5': 0,
'4': 0,
'7': 0,
'6': 0,
'_1_3_2_': 0,
},
'6': {
'1': 0,
'3': 0,
'2': 0,
'5': 0,
'4': 0,
'7': 100,
'6': 0,
'_1_3_2_': 0,
},
'_1_3_2_': {
'1': 100,
'3': 100,
'2': 100,
'5': 100,
'4': 100,
'7': 0,
'6': 100,
'_1_3_2_': 0,
},
}
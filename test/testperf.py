# Saved performance Tableau: 
from decimal import Decimal
from collections import OrderedDict
actions = OrderedDict([
('a1', {
'shortName': 'a1',
'name': 'random decision action',
'comment': 'RandomRankPerformanceTableau() generated.',
}),
('a2', {
'shortName': 'a2',
'name': 'random decision action',
'comment': 'RandomRankPerformanceTableau() generated.',
}),
('a3', {
'shortName': 'a3',
'name': 'random decision action',
'comment': 'RandomRankPerformanceTableau() generated.',
}),
('a4', {
'shortName': 'a4',
'name': 'random decision action',
'comment': 'RandomRankPerformanceTableau() generated.',
}),
('a5', {
'shortName': 'a5',
'name': 'random decision action',
'comment': 'RandomRankPerformanceTableau() generated.',
}),
])
objectives = OrderedDict([
])
criteria = OrderedDict([
('g1', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('14.4'), Decimal('0.0')), 'pref': (Decimal('16.74'), Decimal('0.0')), 'weakVeto': (Decimal('95.84'), Decimal('0.0')), 'veto': (Decimal('96.07'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('3'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g2', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('6.06'), Decimal('0.0')), 'pref': (Decimal('9.99'), Decimal('0.0')), 'weakVeto': (Decimal('77.39'), Decimal('0.0')), 'veto': (Decimal('83.25'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('3'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g3', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('0.43'), Decimal('0.0')), 'pref': (Decimal('24.15'), Decimal('0.0')), 'weakVeto': (Decimal('99.51'), Decimal('0.0')), 'veto': (Decimal('99.62'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('1'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g4', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('12.79'), Decimal('0.0')), 'pref': (Decimal('19.36'), Decimal('0.0')), 'weakVeto': (Decimal('72.16'), Decimal('0.0')), 'veto': (Decimal('97.59'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('1'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g5', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('7.35'), Decimal('0.0')), 'pref': (Decimal('12.13'), Decimal('0.0')), 'weakVeto': (Decimal('88.1'), Decimal('0.0')), 'veto': (Decimal('97.46'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('2'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g6', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('14.59'), Decimal('0.0')), 'pref': (Decimal('31.64'), Decimal('0.0')), 'weakVeto': (Decimal('81.04'), Decimal('0.0')), 'veto': (Decimal('82.56'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('2'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g7', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('6.85'), Decimal('0.0')), 'pref': (Decimal('15.24'), Decimal('0.0')), 'weakVeto': (Decimal('67.83'), Decimal('0.0')), 'veto': (Decimal('99.12'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('3'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
])
evaluation = {
'g1': {
'a1':Decimal("41.03"),
'a2':Decimal("7.30"),
'a3':Decimal("24.61"),
'a4':Decimal("43.41"),
'a5':Decimal("62.73"),
},
'g2': {
'a1':Decimal("35.09"),
'a2':Decimal("89.13"),
'a3':Decimal("32.21"),
'a4':Decimal("79.08"),
'a5':Decimal("52.19"),
},
'g3': {
'a1':Decimal("82.03"),
'a2':Decimal("46.34"),
'a3':Decimal("12.24"),
'a4':Decimal("67.94"),
'a5':Decimal("10.44"),
},
'g4': {
'a1':Decimal("14.03"),
'a2':Decimal("41.51"),
'a3':Decimal("23.83"),
'a4':Decimal("38.67"),
'a5':Decimal("44.23"),
},
'g5': {
'a1':Decimal("66.02"),
'a2':Decimal("44.43"),
'a3':Decimal("24.88"),
'a4':Decimal("85.70"),
'a5':Decimal("11.67"),
},
'g6': {
'a1':Decimal("89.19"),
'a2':Decimal("96.28"),
'a3':Decimal("80.35"),
'a4':Decimal("33.16"),
'a5':Decimal("1.00"),
},
'g7': {
'a1':Decimal("98.36"),
'a2':Decimal("32.40"),
'a3':Decimal("74.62"),
'a4':Decimal("52.34"),
'a5':Decimal("48.59"),
},
}

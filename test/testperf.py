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
'thresholds': {'ind': (Decimal('15.65'), Decimal('0.0')), 'pref': (Decimal('24.74'), Decimal('0.0')), 'weakVeto': (Decimal('96.51'), Decimal('0.0')), 'veto': (Decimal('99.77'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('4'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g2', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('16.33'), Decimal('0.0')), 'pref': (Decimal('31.72'), Decimal('0.0')), 'weakVeto': (Decimal('95.24'), Decimal('0.0')), 'veto': (Decimal('97.29'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('1'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g3', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('3.33'), Decimal('0.0')), 'pref': (Decimal('22.85'), Decimal('0.0')), 'weakVeto': (Decimal('74.17'), Decimal('0.0')), 'veto': (Decimal('78.42'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('5'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g4', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('8.59'), Decimal('0.0')), 'pref': (Decimal('12.2'), Decimal('0.0')), 'weakVeto': (Decimal('92.03'), Decimal('0.0')), 'veto': (Decimal('92.24'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('7'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g5', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('10.53'), Decimal('0.0')), 'pref': (Decimal('12.53'), Decimal('0.0')), 'weakVeto': (Decimal('66.81'), Decimal('0.0')), 'veto': (Decimal('93.84'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('7'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g6', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('0.28'), Decimal('0.0')), 'pref': (Decimal('12.87'), Decimal('0.0')), 'weakVeto': (Decimal('76.85'), Decimal('0.0')), 'veto': (Decimal('94.45'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('3'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g7', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('12.1'), Decimal('0.0')), 'pref': (Decimal('31.72'), Decimal('0.0')), 'weakVeto': (Decimal('92.75'), Decimal('0.0')), 'veto': (Decimal('96.42'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('5'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g8', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('13.52'), Decimal('0.0')), 'pref': (Decimal('27.44'), Decimal('0.0')), 'weakVeto': (Decimal('73.28'), Decimal('0.0')), 'veto': (Decimal('79.73'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('4'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
])
evaluation = {
'g1': {
'a1':Decimal("38.12"),
'a2':Decimal("39.84"),
'a3':Decimal("72.22"),
'a4':Decimal("3.60"),
'a5':Decimal("96.21"),
},
'g2': {
'a1':Decimal("64.83"),
'a2':Decimal("29.11"),
'a3':Decimal("96.90"),
'a4':Decimal("74.50"),
'a5':Decimal("78.39"),
},
'g3': {
'a1':Decimal("0.71"),
'a2':Decimal("74.39"),
'a3':Decimal("7.39"),
'a4':Decimal("9.09"),
'a5':Decimal("77.94"),
},
'g4': {
'a1':Decimal("25.69"),
'a2':Decimal("86.95"),
'a3':Decimal("61.97"),
'a4':Decimal("2.00"),
'a5':Decimal("71.49"),
},
'g5': {
'a1':Decimal("59.35"),
'a2':Decimal("11.28"),
'a3':Decimal("58.05"),
'a4':Decimal("78.03"),
'a5':Decimal("80.26"),
},
'g6': {
'a1':Decimal("73.65"),
'a2':Decimal("98.61"),
'a3':Decimal("48.66"),
'a4':Decimal("66.23"),
'a5':Decimal("96.76"),
},
'g7': {
'a1':Decimal("3.94"),
'a2':Decimal("68.11"),
'a3':Decimal("65.75"),
'a4':Decimal("85.82"),
'a5':Decimal("44.26"),
},
'g8': {
'a1':Decimal("35.10"),
'a2':Decimal("44.95"),
'a3':Decimal("91.28"),
'a4':Decimal("86.55"),
'a5':Decimal("33.41"),
},
}

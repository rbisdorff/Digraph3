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
'thresholds': {'ind': (Decimal('11.19'), Decimal('0.0')), 'pref': (Decimal('11.48'), Decimal('0.0')), 'weakVeto': (Decimal('70.42'), Decimal('0.0')), 'veto': (Decimal('98.87'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('1'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g2', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('15.77'), Decimal('0.0')), 'pref': (Decimal('24.46'), Decimal('0.0')), 'weakVeto': (Decimal('67.76'), Decimal('0.0')), 'veto': (Decimal('75.35'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('2'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g3', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('16.36'), Decimal('0.0')), 'pref': (Decimal('18.25'), Decimal('0.0')), 'weakVeto': (Decimal('69.06'), Decimal('0.0')), 'veto': (Decimal('92.22'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('2'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g4', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('3.13'), Decimal('0.0')), 'pref': (Decimal('28.78'), Decimal('0.0')), 'weakVeto': (Decimal('76.84'), Decimal('0.0')), 'veto': (Decimal('93.88'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('3'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g5', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('13.73'), Decimal('0.0')), 'pref': (Decimal('21.24'), Decimal('0.0')), 'weakVeto': (Decimal('80.45'), Decimal('0.0')), 'veto': (Decimal('90.84'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('1'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g6', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('1.72'), Decimal('0.0')), 'pref': (Decimal('24.58'), Decimal('0.0')), 'weakVeto': (Decimal('95.66'), Decimal('0.0')), 'veto': (Decimal('96.81'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('3'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g7', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('2.75'), Decimal('0.0')), 'pref': (Decimal('28.2'), Decimal('0.0')), 'weakVeto': (Decimal('81.9'), Decimal('0.0')), 'veto': (Decimal('92.8'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('3'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
('g8', {
'name': 'random criterion',
'thresholds': {'ind': (Decimal('13.81'), Decimal('0.0')), 'pref': (Decimal('23.07'), Decimal('0.0')), 'weakVeto': (Decimal('77.51'), Decimal('0.0')), 'veto': (Decimal('84.17'), Decimal('0.0'))},
'scale': [0.0, 100.0],
'weight': Decimal('1'),
'randomMode': ['uniform', 0.0, 100.0],
'comment': 'Evaluation generator: uniform, 0.00, 100.00',
'preferenceDirection': 'max' 
}),
])
evaluation = {
'g1': {
'a1':Decimal("12.19"),
'a2':Decimal("3.21"),
'a3':Decimal("2.74"),
'a4':Decimal("51.41"),
'a5':Decimal("28.62"),
},
'g2': {
'a1':Decimal("37.75"),
'a2':Decimal("61.48"),
'a3':Decimal("99.90"),
'a4':Decimal("72.05"),
'a5':Decimal("10.56"),
},
'g3': {
'a1':Decimal("25.61"),
'a2':Decimal("17.55"),
'a3':Decimal("66.12"),
'a4':Decimal("70.27"),
'a5':Decimal("96.58"),
},
'g4': {
'a1':Decimal("70.07"),
'a2':Decimal("60.75"),
'a3':Decimal("30.85"),
'a4':Decimal("62.92"),
'a5':Decimal("33.46"),
},
'g5': {
'a1':Decimal("0.71"),
'a2':Decimal("27.51"),
'a3':Decimal("93.14"),
'a4':Decimal("33.53"),
'a5':Decimal("63.36"),
},
'g6': {
'a1':Decimal("7.72"),
'a2':Decimal("78.10"),
'a3':Decimal("63.31"),
'a4':Decimal("21.18"),
'a5':Decimal("1.58"),
},
'g7': {
'a1':Decimal("70.42"),
'a2':Decimal("61.61"),
'a3':Decimal("24.71"),
'a4':Decimal("94.93"),
'a5':Decimal("50.20"),
},
'g8': {
'a1':Decimal("88.92"),
'a2':Decimal("55.69"),
'a3':Decimal("84.18"),
'a4':Decimal("96.26"),
'a5':Decimal("90.90"),
},
}

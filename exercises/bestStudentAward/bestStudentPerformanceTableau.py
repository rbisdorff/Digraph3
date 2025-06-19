# Saved performance Tableau: 
from decimal import Decimal
from collections import OrderedDict
name = 'bestStudent'
actions = OrderedDict([
('A', {
'shortName': 'A',
'name': 'Ariana',
'comment': 'Exercise 1.4.4.1.',
}),
('B', {
'shortName': 'B',
'name': 'Bruce',
'comment': 'Exercise 1.4.4.1.',
}),
('C', {
'shortName': 'C',
'name': 'Clare',
'comment': 'Exercise 1.4.4.1.',
}),
('D', {
'shortName': 'D',
'name': 'Daniel',
'comment': 'Exercise 1.4.4.1.',
}),
])
objectives = OrderedDict([
])
criteria = OrderedDict([
('C1', {
'name': 'Grades obtained in Course C1',
'comment': "Ordinal performance scale from 0 pts (weakest) to 20 pts (highest).",
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0')), 'veto': (Decimal('20.0'), Decimal('0.0'))},
'scale': (0.0, 20.0),
'weight': Decimal('2')}),
('C2', {
'name': 'Grades obtained in Course C2',
'comment': "Ordinal performance scale from 0 pts (weakest) to 20 pts (highest).",
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0')), 'veto': (Decimal('20.0'), Decimal('0.0'))},
'scale': (0.0, 20.0),
'weight': Decimal('3')}),
('C3', {
'name': 'Grades obtained in Course C3',
'comment': "Ordinal performance scale from 0 pts (weakest) to 20 pts (highest).",
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0')), 'veto': (Decimal('20.0'), Decimal('0.0'))},
'scale': (0.0, 20.0),
'weight': Decimal('4')}),
('C4', {
'name': 'Grades obtained in Course C4',
'comment': "Ordinal performance scale from 0 pts (weakest) to 20 pts (highest).",
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0')), 'veto': (Decimal('20.0'), Decimal('0.0'))},
'scale': (0.0, 20.0),
'weight': Decimal('2')}),
('C5', {
'name': 'Grades obtained in Course C1',
'comment': "Ordinal performance scale from 0 pts (weakest) to 20 pts (highest).",
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0')), 'veto': (Decimal('20.0'), Decimal('0.0'))},
'scale': (0.0, 20.0),
'weight': Decimal('4')})
])
NA = Decimal('-999')
evaluation = {
'C1': {
'A':Decimal("11"),
'B':Decimal("12"),
'C':Decimal("8"),
'D':Decimal("15"),
},
'C2': {
'A':Decimal("13"),
'B':Decimal("9"),
'C':Decimal("11"),
'D':Decimal("10"),
},
'C3': {
'A':Decimal("9"),
'B':Decimal("13"),
'C':Decimal("14"),
'D':Decimal("12"),
},
'C4': {
'A':Decimal("15"),
'B':Decimal("10"),
'C':Decimal("12"),
'D':Decimal("8"),
},
'C5': {
'A':Decimal("11"),
'B':Decimal("13"),
'C':Decimal("14"),
'D':Decimal("13"),
},

}

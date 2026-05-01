# Saved performance Tableau: 
from decimal import Decimal
from collections import OrderedDict
name = 'studentgrades'
actions = OrderedDict([
('A', {
'shortName': 'A',
'name': 'Ariana',
'comment': 'Grades obtained by Arisana',
}),
('B', {
'shortName': 'B',
'name': 'Bruce',
'comment': 'Grades obtained by Bruce',
}),
('C', {
'shortName': 'C',
'name': 'Clare',
'comment': 'Grades obtained by Clare',
}),
('D', {
'shortName': 'D',
'name': 'Daniel',
'comment': 'Grades obtained by Daniel',
}),
])
objectives = OrderedDict([
])
criteria = OrderedDict([
('C1', {
'name': 'Course C1',
'comment': "Grading scale: 0 - 20, ECTS points 2",
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0'), Decimal('0')), 'pref': (Decimal('1'), Decimal('0')), 'veto': (Decimal('21'), Decimal('0'))},
'scale': (0, 20),
'weight': Decimal('2'),
}),
('C2', {
'name': 'Course C2',
'comment': "Grading scale: 0 - 20, ECTS points 3",
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0'), Decimal('0')), 'pref': (Decimal('1'), Decimal('0')), 'veto': (Decimal('21'), Decimal('0'))},
'scale': (0, 20),
'weight': Decimal('3'),
}),
('C3', {
'name': 'Course C3',
'comment': "Grading scale: 0 - 20, ECTS points 4",
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('1'), Decimal('0')), 'pref': (Decimal('1'), Decimal('0')), 'veto': (Decimal('21'), Decimal('0'))},
'scale': (0, 20),
'weight': Decimal('4'),
}),
('C4', {
'name': 'Course C4',
'comment': "Grading scale: 0 - 20, ECTS points 2",
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0'), Decimal('0')), 'pref': (Decimal('1'), Decimal('0')), 'veto': (Decimal('21'), Decimal('0'))},
'scale': (0, 20),
'weight': Decimal('2'),
}),
('C5', {
'name': 'Course C5',
'comment': "Grading scale: 0 - 20, ECTS points 4",
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0'), Decimal('0')), 'pref': (Decimal('1'), Decimal('0')), 'veto': (Decimal('21'), Decimal('0'))},
'scale': (0, 20),
'weight': Decimal('4'),
}),
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

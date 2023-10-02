#########################################################
# Digraph3 documentation
# Template for creating a new PerformanceTableau instance
# (C) R. Bisdorff Mar 2021
# Digraph3/examples/perfTab_Template.py
##########################################################
from decimal import Decimal
from collections import OrderedDict
#####
# edit the decision actions
# avoid special characters, like '_', '/' or ':',
# in action identifiers and short names
actions = OrderedDict([
('a1', {
'shortName': 'action1',
'name': 'decision alternative a1',
'comment': 'some specific features of this alternative',
}),
('a2', {
'shortName': 'action2',
'name': 'decision alternative a2',
'comment': 'some specific features of this alternative',
}),
('a3', {
'shortName': 'action3',
'name': 'decision alternative a3',
'comment': 'some specific features of this alternative',
}),
('a4', {
'shortName': 'action4',
'name': 'decision alternative a4',
'comment': 'some specific features of this alternative',
}),
('a5', {
'shortName': 'action5',
'name': 'decision alternative a5',
'comment': 'some specific features of this alternative',
}),
])
#####
# edit the decision objectives
# adjust the list of performance criteria
# and the total weight (sum of the criteria weights)
# per objective
objectives = OrderedDict([
('obj1', {
'name': 'decision objective obj1',
'comment': "some specific features of this objective",
'criteria': ['g1', 'g2'],
'weight': Decimal('6'),
}),
('obj2', {
'name': 'decision objective obj2',
'comment': 'some specific features of this objective',
'criteria': ['g3'],
'weight': Decimal('6'),
}),
('obj3', {
'name': 'decision objective obj3',
'comment': 'some specific features of this objective',
'criteria': ['g4','g5','g6'],
'weight': Decimal('6'),
}),
])
#####
# edit the performance criteria
# adjust the objective references
# Decimal1 = constant part of threshold
# Decimal2 = proportional part threshold 

criteria = OrderedDict([
('g1', {
'objective': 'obj1',
'preferenceDirection': 'max',
'name': "performance criteria 1",
'shortName': 'crit1',
'thresholds': {'ind': (Decimal('2.50'), Decimal('0.0')),
               'pref': (Decimal('5.00'), Decimal('0.0')),
               'veto': (Decimal('60.00'), Decimal('0.0')) },
'scale': (0.0, 100.0),
'weight': 3,
'comment': 'performance measurement scale type (cardinal) and unit',
}),
('g2', {
'objective': 'obj1',
'preferenceDirection': 'max',
'name': "performance criteria 2",
'shortName': 'crit2',
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')),
               'pref': (Decimal('1.0'), Decimal('0.0'))},
'scale': (0.0, 10.0),
'weight': 3,
'comment': 'performance measurement scale (ordinal) type and unit (satisfaction points)',
}),
('g3', {
'objective': 'obj2',
'preferenceDirection': 'min',
'name': "performance criteria 3",
'shortName': 'crit3',
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')),
               'pref': (Decimal('10.0'), Decimal('0.0')),
               'veto': (Decimal('60.00'), Decimal('0.0')) },
'scale': (0.0, 100.0),
'weight': 6,
'comment': 'performance measurement scale type and unit',
}),
('g4', {
'objective': 'obj3',
'preferenceDirection': 'max',
'name': "performance criteria 4",
'shortName': 'crit4',
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.025')),
               'pref': (Decimal('0.0'), Decimal('0.05'))},
'scale': (0.0, 100.0),
'weight': 2,
'comment': 'performance measurement scale type and unit',
}),
('g5', {
'objective': 'obj3',
'preferenceDirection': 'max',
'name': "performance criteria 5",
'shortName': 'crit5',
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')),
               'pref': (Decimal('10.0'), Decimal('0.0'))},
'scale': (0.0, 100.0),
'weight': 2,
'comment': 'performance measurement scale type and unit',
}),
('g6', {
'objective': 'obj1',
'preferenceDirection': 'max',
'name': "performance criteria 6",
'shortName': 'crit6',
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')),
               'pref': (Decimal('10.0'), Decimal('0.0'))},
'scale': (0.0, 100.0),
'weight': 2,
'comment': 'performance measurement scale type and unit',
}),
])

#####
# default missing data symbol = -999
NA = Decimal('-999')

#####
# edit the performance evaluations
# criteria to be minimized take negative grades
evaluation = {
'g1': {
'a1':Decimal("41.0"),
'a2':Decimal("100.0"),
'a3':Decimal("63.0"),
'a4':Decimal('23.0'),
'a5': NA,
},
# g2 is of ordinal type and scale 0-10
'g2': {
'a1':Decimal("4"),
'a2':Decimal("10"),
'a3':Decimal("6"),
'a4':Decimal('2'),
'a5':Decimal('9'),
},
# g3 has preferenceDircetion = 'min'
'g3': {
'a1':Decimal("-52.2"),
'a2':NA,
'a3':Decimal("-47.3"),
'a4':Decimal('-35.7'),
'a5':Decimal('-68.00'),
},
'g4': {
'a1':Decimal("71.0"),
'a2':Decimal("89.0"),
'a3':Decimal("55.4"),
'a4':Decimal('83.5'),
'a5':Decimal('10.0'),
},
'g5': {
'a1':Decimal("63.0"),
'a2':Decimal("30.7"),
'a3':Decimal("63.5"),
'a4':Decimal('37.5'),
'a5':Decimal('88.0'),
},
'g6': {
'a1':Decimal("22.5"),
'a2':Decimal("75.0"),
'a3':NA,
'a4':Decimal('54.9'),
'a5':Decimal('75.0'),
},
}
####################

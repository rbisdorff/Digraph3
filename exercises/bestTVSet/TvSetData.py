# Digraph3 exercise 3 best Tv set recommendation
from decimal import Decimal
from collections import OrderedDict
name = 'TvSetData'
actions = OrderedDict([
('T1', {
'shortName': 'T1',
'name': 'model T1',
'comment': 'Potential TV model',
}),
('T2', {
'shortName': 'T2',
'name': 'model T2',
'comment': 'Potential TV model',
}),
('T3', {
'shortName': 'T3',
'name': 'model T3',
'comment': 'Potential TV model',
}),
('T4', {
'shortName': 'T4',
'name': 'model T4',
'comment': 'Potential TV model',
}),
('T5', {
'shortName': 'T5',
'name': 'model T5',
'comment': 'Potential TV model',
}),
('T6', {
'shortName': 'T6',
'name': 'model T6',
'comment': 'Potential TV model',
}),
('T7', {
'shortName': 'T7',
'name': 'model T7',
'comment': 'Potential TV model',
}),
('T8', {
'shortName': 'T8',
'name': 'model T8',
'comment': 'Potential TV model',
}),
])
objectives = OrderedDict([
    ('Costs', {
  'name': 'acquisition price',

  'comment': "in thge shop",

  'criteria': ['Pr'],

  'weight': Decimal('2'),

  }),
    ('Pic', {

  'name': 'Tv set quality',

  'comment': "Screen size, pixels, audio etc",

  'criteria': ['Pq', 'Sq'],

  'weight': Decimal('2'),

  }),
    ('Service', {

  'name': 'after sales service',

  'comment': "Maintenance contract terms",

  'criteria': ['Mq'],

  'weight': Decimal('1'),

  }),
])
criteria = OrderedDict([
('Pr', {
'name': 'Costs of the Tv set',
'comment': "In e",
'preferenceDirection': 'min',
'thresholds': {'ind': (Decimal('25.0'), Decimal('0.0')), 'pref': (Decimal('75.0'), Decimal('0.0')),
               'veto': (Decimal('3000.0'), Decimal('0.0'))},
'scale': (-1300, -900),
'weight': Decimal('2'),
}),
('Pq', {
'name': 'Picture quality',
'comment': "Four levels performance scale: -1 (not good, 0 (average), +1 (good), +2 (very good)",
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0')),
                    'veto': (Decimal('80.0'), Decimal('0.0'))},
'scale': (-1, 2),
'weight': Decimal('1'),
}),
('Sq', {
'name': 'Sound quality',
'comment': "Four levels performance scale: -1 (not good, 0 (average), +1 (good), +2 (very good)",
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0')),
                    'veto': (Decimal('80.0'), Decimal('0.0'))},
'scale': (-1, 2),
'weight': Decimal('1'),
}),
('Mq', {
'name': 'Maintenance quality',
'comment': "Four levels performance scale: -1 (not good, 0 (average), +1 (good), +2 (very good)",
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0')),
                    'veto': (Decimal('80.0'), Decimal('0.0'))},
'scale': (-1, 2),
'weight': Decimal('1'),
}),
])
NA = Decimal('-9999')
evaluation = {
'Pr': {
'T1':Decimal("-1300"),
'T2':Decimal("-1200"),
'T3':Decimal("-1150"),
'T4':Decimal("-1000"),
'T5':Decimal("-950"),
'T6':Decimal("-950"),
'T7':Decimal("-900"),
'T8':Decimal("-900"),
},
'Pq': {
'T1':Decimal("2"),
'T2':Decimal("2"),
'T3':Decimal("2"),
'T4':Decimal("1"),
'T5':Decimal("1"),
'T6':Decimal("0"),
'T7':Decimal("1"),
'T8':Decimal("0"),
},
'Sq': {
'T1':Decimal("2"),
'T2':Decimal("2"),
'T3':Decimal("1"),
'T4':Decimal("1"),
'T5':Decimal("1"),
'T6':Decimal("1"),
'T7':Decimal("0"),
'T8':Decimal("0"),
},
'Mq': {
'T1':Decimal("0"),
'T2':Decimal("1"),
'T3':Decimal("1"),
'T4':Decimal("-1"),
'T5':Decimal("0"),
'T6':Decimal("-1"),
'T7':Decimal("-1"),
'T8':Decimal("0"),
},

}

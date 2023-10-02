# Saved performance Tableau: 
from decimal import Decimal
from collections import OrderedDict
actions = OrderedDict([
('Mp', {
'name': 'Campus Monteprincipe',
'comment': 'South West of Madrid centre.',
}),
('Mo', {
'name': 'Campus Moncloa',
'comment': 'Madrid centre. Same location as San Dominique.',
}),
('Ar', {
'name': 'Campus Arguelles',
'comment': 'Madrid centre.',
}),
('Sd', {
'name': 'San Dominique',
'comment': 'Madrid centre. Same loaction as Campus Moncloa',
}),
('Ma', {
'name': 'Majadahonda',
'comment': 'West of Madrid centre.',
}),
('Po', {
'name': 'Pozuelo',
'comment': 'Sout West of Madrid centre.',
}),
('Lr', {
'name': 'La Rozas',
'comment': 'West of Madrid centre.',
}),
])
objectives = OrderedDict([
])
criteria = OrderedDict([
('ACC', {
'name': 'Accessibility to Madrid city centre',
'comment': 'In minutes. The metropolitan area\n  of Madrid covers a wide area, causing transportation accessibility\n  to be of importantance when choosing a site for a new facility. In a\n  city with heavy traffic congestion, the actual distance might not\n  correlate with accessibility, and therefore we have chosen to\n  measure it in minutes by public transportation from a central\n  transport hub.',
'version': 'performance',
'preferenceDirection': 'min',
'scale': (Decimal('30.00'), Decimal('60.00')),
'weight': Decimal('0.3'),
'thresholds': {'ind': (Decimal('6.5'), Decimal('0.0')), 'pref': (Decimal('12.5'), Decimal('0.0'))},
}),
('SIZ', {
'name': 'Size (in children) of the kindergarten',
'comment': 'size (in children) of the kindergarten to be\n  built as measured with a number of day-care places. The Spanish\n  government regulates \\citep{BOE:2005,BOE:2007} the maximum number of children\n  for $m^2$ and the required common services. The number of day-care\n  places can be derived from the estimated building specifications.',
'version': 'performance',
'preferenceDirection': 'max',
'scale': (Decimal('100.00'), Decimal('300.00')),
'weight': Decimal('0.2'),
'thresholds': {'ind': (Decimal('1.5'), Decimal('0.0')), 'pref': (Decimal('3'), Decimal('0.0'))},
}),
('COP', {
'name': 'land and construction prize',
'comment': 'The sites have differing\n  costs of location and construction depending on the building\n  location (e.g. residential zone, city center or outskirts).',
'version': 'performance',
'preferenceDirection': 'min',
'scale': (Decimal('3000000.00'), Decimal('5500000.00')),
'weight': Decimal('0.3'),
'thresholds': {'ind': (Decimal('10000.00'), Decimal('0.0')), 'pref': (Decimal('100000.00'), Decimal('0.0'))},
}),
('EFF', {
'name': 'Effects to the city landscape',
'comment': 'Government regulations define that\n  effects to urban landscape, green spaces, and cultural heritage must\n  be estimated. We measure them with odinal ranking number from best (1rst) to worst (7th).',
'version': 'performance',
'preferenceDirection': 'min',
'scale': (Decimal('1.00'), Decimal('7.00')),
'weight': Decimal('0.1'),
'thresholds': {},
}),
('MAC', {
'name': 'maintenance costs of the facility',
'comment': 'In euros / month, measured by\n  estimating total fixed and variable costs (supplies, personnel,\n  taxes, etc).',
'version': 'performance',
'preferenceDirection': 'min',
'scale': (Decimal('20000.00'), Decimal('50000.00')),
'weight': Decimal('0.1'),
'thresholds': {'ind': (Decimal('0.00'), Decimal('0.03')), 'pref': (Decimal('0.00'), Decimal('0.08'))},
}),
])
NA = Decimal('-999')
evaluation = {
'ACC': {
'Mp':Decimal("-52.50"),
'Mo':Decimal("-39.17"),
'Ar':Decimal("-36.67"),
'Sd':Decimal("-38.33"),
'Ma':Decimal("-46.33"),
'Po':Decimal("-42.83"),
'Lr':Decimal("-49.00"),
},
'SIZ': {
'Mp':Decimal("234.00"),
'Mo':Decimal("159.00"),
'Ar':Decimal("167.00"),
'Sd':Decimal("134.00"),
'Ma':Decimal("159.00"),
'Po':Decimal("167.00"),
'Lr':Decimal("201.00"),
},
'COP': {
'Mp':Decimal("-3937880.00"),
'Mo':Decimal("-4729000.00"),
'Ar':Decimal("-5238520.00"),
'Sd':Decimal("-4068450.00"),
'Ma':Decimal("-3146000.00"),
'Po':Decimal("-3317270.00"),
'Lr':Decimal("-3904800.00"),
},
'EFF': {
'Mp':Decimal("-3.00"),
'Mo':Decimal("-7.00"),
'Ar':Decimal("-5.00"),
'Sd':Decimal("-6.00"),
'Ma':Decimal("-4.00"),
'Po':Decimal("-1.00"),
'Lr':Decimal("-2.00"),
},
'MAC': {
'Mp':Decimal("-43500.00"),
'Mo':Decimal("-29000.00"),
'Ar':Decimal("-31750.00"),
'Sd':Decimal("-26250.00"),
'Ma':Decimal("-30500.00"),
'Po':Decimal("-31750.00"),
'Lr':Decimal("-38000.00"),
},
}

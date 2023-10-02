# Saved performance Tableau: 
from decimal import Decimal
from collections import OrderedDict
actions = OrderedDict([
('vwgc', {
'name': 'vwgc',
}),
('r9gtl', {
'name': 'r9gtl',
}),
('gsax', {
'name': 'gsax',
}),
('p305', {
'name': 'p305',
}),
('tahg', {
'name': 'tahg',
}),
('audi', {
'name': 'audi',
}),
('r18gtl', {
'name': 'r18gtl',
}),
('alfa', {
'name': 'alfa',
}),
])
objectives = OrderedDict([
])
criteria = OrderedDict([
('speed', { 'name': 'speed', 'scale': (Decimal('140.0'),Decimal('170.0')),
'weight': Decimal('4.0'),
'thresholds': {'ind': (Decimal('5.0'), Decimal('0.0')), 'pref': (Decimal('10.0'), Decimal('0.0')), 
#'veto': (Decimal('10.0'), Decimal('0.0'))
},
'preferenceDirection': 'max' 
}),
('volume', { 'name': 'volume', 'scale': (Decimal('6.13'),Decimal('7.40')),
'weight': Decimal('3.0'),
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('0.1'), Decimal('0.0')), 
#'veto': (Decimal('0.4'), Decimal('0.0'))
},
'preferenceDirection': 'max' 
}),
('price', { 'name': 'price', 'scale': (Decimal('41360.0'),Decimal('52500.0')),
'weight': Decimal('1.0'),
'thresholds': {'ind': (Decimal('500.0'), Decimal('0.0')), 'pref': (Decimal('1000'), Decimal('0.0')), #'veto': (Decimal('2000.0'), Decimal('0.0'))
},
'preferenceDirection': 'min' 
}),
('cons', { 'name': 'consommation', 'scale': (Decimal('7.50'),Decimal('8.50')),
'weight': Decimal('2.0'),
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.1'), Decimal('0.0')), 
#'veto': (Decimal('0.5'), Decimal('0.0'))
},
'preferenceDirection': 'min' 
}),
])
NA = Decimal('-999')
evaluation = {
'speed': {
'vwgc':Decimal("140.00"),
'r9gtl':Decimal("150.00"),
'gsax':Decimal("160.00"),
'p305':Decimal("153.00"),
'tahg':Decimal("164.00"),
'audi':Decimal("148.00"),
'r18gtl':Decimal("155.00"),
'alfa':Decimal("170.00"),
},
'volume': {
'vwgc':Decimal("6.13"),
'r9gtl':Decimal("6.70"),
'gsax':Decimal("6.63"),
'p305':Decimal("6.91"),
'tahg':Decimal("6.65"),
'audi':Decimal("7.36"),
'r18gtl':Decimal("7.40"),
'alfa':Decimal("6.19"),
},
'price': {
'vwgc':Decimal("-41360.00"),
'r9gtl':Decimal("-45700.00"),
'gsax':Decimal("-46450.00"),
'p305':Decimal("-48200.00"),
'tahg':Decimal("-48800.00"),
'audi':Decimal("-50830.00"),
'r18gtl':Decimal("-51700.00"),
'alfa':Decimal("-52500.00"),
},
'cons': {
'vwgc':Decimal("-7.80"),
'r9gtl':Decimal("-7.50"),
'gsax':Decimal("-8.20"),
'p305':Decimal("-8.40"),
'tahg':Decimal("-8.50"),
'audi':Decimal("-7.00"),
'r18gtl':Decimal("-8.10"),
'alfa':Decimal("-7.80"),
},
}

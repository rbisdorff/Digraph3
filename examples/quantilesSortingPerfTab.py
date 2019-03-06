# Saved performance Tableau: 
from decimal import Decimal
actions = {
'a05': {'name': 'a05'},
'a04': {'name': 'a04'},
'a07': {'name': 'a07'},
'a06': {'name': 'a06'},
'a01': {'name': 'a01'},
'a03': {'name': 'a03'},
'a02': {'name': 'a02'},
}
criteria = {
'g03': {
'weight':Decimal("2.00"),'scale': (Decimal("0.00"),Decimal("10.00")),
},
'g02': {
'weight':Decimal("3.00"),'scale': (Decimal("0.00"),Decimal("100.00")),
'thresholds' : {'veto': (Decimal('57.72'), Decimal('0.0')), 'pref': (Decimal('3.15'), Decimal('0.0')), 'ind': (Decimal('2.22'), Decimal('0.0'))} },
'g01': {
'weight':Decimal("3.00"),'scale': (Decimal("0.00"),Decimal("10.00")),
},
'g05': {
'weight':Decimal("2.00"),'scale': (Decimal("0.00"),Decimal("100.00")),
'thresholds' : {'veto': (Decimal('56.96'), Decimal('0.0')), 'pref': (Decimal('2.35'), Decimal('0.0')), 'ind': (Decimal('1.82'), Decimal('0.0'))} },
'g04': {
'weight':Decimal("2.00"),'scale': (Decimal("0.00"),Decimal("100.00")),
'thresholds' : {'veto': (Decimal('51.49'), Decimal('0.0')), 'pref': (Decimal('1.83'), Decimal('0.0')), 'ind': (Decimal('0.94'), Decimal('0.0'))} },
}
evaluation = {
'g03': {
'a05':Decimal("-6.00"),
'a04':Decimal("-8.00"),
'a07':Decimal("-4.00"),
'a06':Decimal("-2.00"),
'a01':Decimal("-8.00"),
'a03':Decimal("-5.00"),
'a02':Decimal("-5.00"),
},
'g02': {
'a05':Decimal("68.92"),
'a04':Decimal("24.82"),
'a07':Decimal("65.77"),
'a06':Decimal("82.67"),
'a01':Decimal("24.95"),
'a03':Decimal("56.20"),
'a02':Decimal("71.14"),
},
'g01': {
'a05':Decimal("7.00"),
'a04':Decimal("7.00"),
'a07':Decimal("8.00"),
'a06':Decimal("7.00"),
'a01':Decimal("4.00"),
'a03':Decimal("1.00"),
'a02':Decimal("9.00"),
},
'g05': {
'a05':Decimal("-75.40"),
'a04':Decimal("-61.61"),
'a07':Decimal("-16.09"),
'a06':Decimal("-59.79"),
'a01':Decimal("-73.05"),
'a03':Decimal("-33.34"),
'a02':Decimal("-71.99"),
},
'g04': {
'a05':Decimal("-62.28"),
'a04':Decimal("-33.66"),
'a07':Decimal("-43.77"),
'a06':Decimal("-86.09"),
'a01':Decimal("-72.79"),
'a03':Decimal("-85.15"),
'a02':Decimal("-84.26"),
},
}

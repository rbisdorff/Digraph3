# Saved digraph instance
from decimal import Decimal
from collections import OrderedDict
actions = OrderedDict([
('A',
{'shortName': 'A', 'name': 'Ariana', 'comment': 'Exercise 1.4.4.1.'}),
('B',
{'shortName': 'B', 'name': 'Bruce', 'comment': 'Exercise 1.4.4.1.'}),
('C',
{'shortName': 'C', 'name': 'Clare', 'comment': 'Exercise 1.4.4.1.'}),
('D',
{'shortName': 'D', 'name': 'Daniel', 'comment': 'Exercise 1.4.4.1.'}),
])
valuationdomain = {'hasIntegerValuation': False, 'min': Decimal("-1.0000"),'med': Decimal("0.0"),'max': Decimal("1.0000")}
relation = {
'A': {
'A': Decimal('0.00'),
'B': Decimal('-0.33'),
'C': Decimal('-0.07'),
'D': Decimal('-0.33'),
},
'B': {
'A': Decimal('0.33'),
'B': Decimal('0.00'),
'C': Decimal('-0.73'),
'D': Decimal('0.33'),
},
'C': {
'A': Decimal('0.07'),
'B': Decimal('0.73'),
'C': Decimal('0.00'),
'D': Decimal('0.73'),
},
'D': {
'A': Decimal('0.33'),
'B': Decimal('0.20'),
'C': Decimal('-0.73'),
'D': Decimal('0.00'),
},
}

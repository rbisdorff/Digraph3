# Saved approval voting profile: 
from collections import OrderedDict
from decimal import Decimal
candidates = OrderedDict([
('A', {'name': 'Alice'}),
('B', {'name': 'Bob'}),
('C', {'name': 'Carol'}),
('D', {'name': 'Dan'}),
('E', {'name': 'Edward'}),
('F', {'name': 'Felix'}),
('G', {'name': 'Gaby'}),
('H', {'name': 'Henry'}),
('I', {'name': 'Isabel'}),
('J', {'name': 'Jane'}),
])
voters = OrderedDict([
('A', {
'weight':1}),
('B', {
'weight':1}),
('C', {
'weight':1}),
('D', {
'weight':1}),
('E', {
'weight':1}),
('F', {
'weight':1}),
('G', {
'weight':1}),
('H', {
'weight':1}),
('I', {
'weight':1}),
('J', {
'weight':1}),
])
IntraGroup = True
ApprovalProbability = 0.25
disapprovalProbability = 0.30
approvalBallot = {
'A': {
'A': Decimal('0'),
'B': Decimal('-1'),
'C': Decimal('1'),
'D': Decimal('0'),
'E': Decimal('0'),
'F': Decimal('1'),
'G': Decimal('-1'),
'H': Decimal('0'),
'I': Decimal('1'),
'J': Decimal('0'),
},
'B': {
'A': Decimal('0'),
'B': Decimal('0'),
'C': Decimal('0'),
'D': Decimal('1'),
'E': Decimal('1'),
'F': Decimal('0'),
'G': Decimal('1'),
'H': Decimal('-1'),
'I': Decimal('-1'),
'J': Decimal('-1'),
},
'C': {
'A': Decimal('1'),
'B': Decimal('-1'),
'C': Decimal('0'),
'D': Decimal('0'),
'E': Decimal('0'),
'F': Decimal('1'),
'G': Decimal('-1'),
'H': Decimal('0'),
'I': Decimal('-1'),
'J': Decimal('-1'),
},
'D': {
'A': Decimal('-1'),
'B': Decimal('-1'),
'C': Decimal('-1'),
'D': Decimal('0'),
'E': Decimal('0'),
'F': Decimal('0'),
'G': Decimal('0'),
'H': Decimal('1'),
'I': Decimal('0'),
'J': Decimal('0'),
},
'E': {
'A': Decimal('-1'),
'B': Decimal('1'),
'C': Decimal('-1'),
'D': Decimal('1'),
'E': Decimal('0'),
'F': Decimal('1'),
'G': Decimal('-1'),
'H': Decimal('1'),
'I': Decimal('-1'),
'J': Decimal('-1'),
},
'F': {
'A': Decimal('0'),
'B': Decimal('-1'),
'C': Decimal('1'),
'D': Decimal('0'),
'E': Decimal('0'),
'F': Decimal('0'),
'G': Decimal('0'),
'H': Decimal('1'),
'I': Decimal('1'),
'J': Decimal('-1'),
},
'G': {
'A': Decimal('-1'),
'B': Decimal('0'),
'C': Decimal('-1'),
'D': Decimal('-1'),
'E': Decimal('1'),
'F': Decimal('0'),
'G': Decimal('0'),
'H': Decimal('1'),
'I': Decimal('0'),
'J': Decimal('0'),
},
'H': {
'A': Decimal('0'),
'B': Decimal('-1'),
'C': Decimal('0'),
'D': Decimal('1'),
'E': Decimal('-1'),
'F': Decimal('1'),
'G': Decimal('0'),
'H': Decimal('0'),
'I': Decimal('0'),
'J': Decimal('0'),
},
'I': {
'A': Decimal('1'),
'B': Decimal('-1'),
'C': Decimal('1'),
'D': Decimal('-1'),
'E': Decimal('-1'),
'F': Decimal('-1'),
'G': Decimal('1'),
'H': Decimal('-1'),
'I': Decimal('0'),
'J': Decimal('1'),
},
'J': {
'A': Decimal('0'),
'B': Decimal('-1'),
'C': Decimal('-1'),
'D': Decimal('1'),
'E': Decimal('-1'),
'F': Decimal('0'),
'G': Decimal('1'),
'H': Decimal('0'),
'I': Decimal('0'),
'J': Decimal('0'),
},

}

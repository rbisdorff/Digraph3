# Saved approval voting profile: 
from collections import OrderedDict
from decimal import Decimal
candidates = OrderedDict([
('b1', {'name': 'Candidate b1'}),
('b2', {'name': 'Candidate b2'}),
('b3', {'name': 'Candidate b3'}),
('b4', {'name': 'Candidate b4'}),
('b5', {'name': 'Candidate b5'}),
])
voters = OrderedDict([
('a1', {
'weight':1}),
('a2', {
'weight':1}),
('a3', {
'weight':1}),
('a4', {
'weight':1}),
('a5', {
'weight':1}),
])
IntraGroup = FalseapprovalProbability = 0.50
disapprovalProbability = 0.50
approvalBallot = {
'a1': {
'b1': Decimal('1'),
'b2': Decimal('-1'),
'b3': Decimal('0'),
'b4': Decimal('0'),
'b5': Decimal('1'),
},
'a2': {
'b1': Decimal('-1'),
'b2': Decimal('1'),
'b3': Decimal('-1'),
'b4': Decimal('-1'),
'b5': Decimal('0'),
},
'a3': {
'b1': Decimal('0'),
'b2': Decimal('0'),
'b3': Decimal('-1'),
'b4': Decimal('0'),
'b5': Decimal('-1'),
},
'a4': {
'b1': Decimal('1'),
'b2': Decimal('-1'),
'b3': Decimal('-1'),
'b4': Decimal('-1'),
'b5': Decimal('1'),
},
'a5': {
'b1': Decimal('-1'),
'b2': Decimal('1'),
'b3': Decimal('1'),
'b4': Decimal('0'),
'b5': Decimal('-1'),
},
}

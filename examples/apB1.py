# Saved approval voting profile: 
from collections import OrderedDict
from decimal import Decimal
candidates = OrderedDict([
('a1', {'name': 'Candidate a1'}),
('a2', {'name': 'Candidate a2'}),
('a3', {'name': 'Candidate a3'}),
('a4', {'name': 'Candidate a4'}),
('a5', {'name': 'Candidate a5'}),
])
voters = OrderedDict([
('b1', {
'weight':1}),
('b2', {
'weight':1}),
('b3', {
'weight':1}),
('b4', {
'weight':1}),
('b5', {
'weight':1}),
])
IntraGroup = FalseapprovalProbability = 0.50
disapprovalProbability = 0.50
approvalBallot = {
'b1': {
'a1': Decimal('-1'),
'a2': Decimal('1'),
'a3': Decimal('1'),
'a4': Decimal('-1'),
'a5': Decimal('-1'),
},
'b2': {
'a1': Decimal('1'),
'a2': Decimal('1'),
'a3': Decimal('0'),
'a4': Decimal('-1'),
'a5': Decimal('0'),
},
'b3': {
'a1': Decimal('0'),
'a2': Decimal('-1'),
'a3': Decimal('-1'),
'a4': Decimal('0'),
'a5': Decimal('1'),
},
'b4': {
'a1': Decimal('0'),
'a2': Decimal('1'),
'a3': Decimal('-1'),
'a4': Decimal('0'),
'a5': Decimal('-1'),
},
'b5': {
'a1': Decimal('-1'),
'a2': Decimal('0'),
'a3': Decimal('0'),
'a4': Decimal('1'),
'a5': Decimal('0'),
},
}


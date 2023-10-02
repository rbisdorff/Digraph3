# BipolarApprovalVotingProfile:
# Condorcet 1785, p. lviij
from collections import OrderedDict
from decimal import Decimal
candidates = OrderedDict([
('A', {'name': 'A'}),
('B', {'name': 'B'}),
])
voters = OrderedDict([
('v1', {
'weight':11}),
('v2', {
'weight':10}),
('v3', {
'weight':3}),
('v4', {
'weight':9}),

])
approvalBallot = {
'v1': {
'A': 1,
'B': 1,
},
'v2': {
'A': 1,
'B': -1,
},
'v3': {
'A': -1,
'B': 1,
},
'v4': {
'A': -1,
'B': -1,
},
}


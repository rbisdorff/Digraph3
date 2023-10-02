# Saved linear voting profile: 
from collections import OrderedDict 
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
linearBallot = {
'a1': [
'b3',
'b4',
'b5',
'b1',
'b2',
],
'a2': [
'b3',
'b5',
'b4',
'b2',
'b1',
],
'a3': [
'b4',
'b2',
'b1',
'b3',
'b5',
],
'a4': [
'b2',
'b4',
'b1',
'b5',
'b3',
],
'a5': [
'b4',
'b2',
'b3',
'b1',
'b5',
],
}

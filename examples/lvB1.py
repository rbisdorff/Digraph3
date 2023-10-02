# Saved linear voting profile: 
from collections import OrderedDict 
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
linearBallot = {
'b1': [
'a3',
'a2',
'a4',
'a5',
'a1',
],
'b2': [
'a5',
'a3',
'a1',
'a4',
'a2',
],
'b3': [
'a3',
'a4',
'a1',
'a5',
'a2',
],
'b4': [
'a3',
'a4',
'a1',
'a2',
'a5',
],
'b5': [
'a3',
'a4',
'a1',
'a2',
'a5',
],
}

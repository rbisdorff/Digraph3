# Saved linear voting profile: 
from collections import OrderedDict 
candidates = OrderedDict([
('b1', {'name': 'Candidate b1'}),
('b2', {'name': 'Candidate b2'}),
('b3', {'name': 'Candidate b3'}),
('b4', {'name': 'Candidate b4'}),
('b5', {'name': 'Candidate b5'}),
('b6', {'name': 'Candidate b6'}),
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
('a6', {
'weight':1}),
])
linearBallot = {
'a1': [
'b5',
'b6',
'b4',
'b3',
'b1',
'b2',
],
'a2': [
'b6',
'b1',
'b4',
'b5',
'b3',
'b2',
],
'a3': [
'b6',
'b3',
'b4',
'b1',
'b5',
'b2',
],
'a4': [
'b3',
'b4',
'b2',
'b6',
'b5',
'b1',
],
'a5': [
'b3',
'b4',
'b5',
'b1',
'b6',
'b2',
],
'a6': [
'b3',
'b5',
'b1',
'b6',
'b4',
'b2',
],
}

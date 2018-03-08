# Saved linear voting profile: 
from collections import OrderedDict 
candidates = OrderedDict([
('a1', {'name': 'a1'}),
('a2', {'name': 'a2'}),
('a3', {'name': 'a3'}),
])
voters = OrderedDict([
('v1', {
'weight':2}),
('v2', {
'weight':3}),
('v3', {
'weight':1}),
('v4', {
'weight':5}),
('v5', {
'weight':4}),
])
linearBallot = {
'v1': [
'a2',
'a1',
'a3',
],
'v5': [
'a3',
'a1',
'a2',
],
'v3': [
'a1',
'a3',
'a2',
],
'v4': [
'a1',
'a2',
'a3',
],
'v2': [
'a3',
'a1',
'a2',
],
}

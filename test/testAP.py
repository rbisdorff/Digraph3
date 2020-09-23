# Saved approval voting profile: 
from collections import OrderedDict 
candidates = OrderedDict([
('a1', {'name': 'a1'}),
('a2', {'name': 'a2'}),
('a3', {'name': 'a3'}),
('a4', {'name': 'a4'}),
('a5', {'name': 'a5'}),
])
voters = OrderedDict([
('v1', {
'weight':1.0}),
('v2', {
'weight':1.0}),
('v3', {
'weight':1.0}),
('v4', {
'weight':1.0}),
('v5', {
'weight':1.0}),
('v6', {
'weight':1.0}),
('v7', {
'weight':1.0}),
('v8', {
'weight':1.0}),
('v9', {
'weight':1.0}),
])
approvalBallot = {
'v1': [
'a3',
'a1',
'a4',
],
'v2': [
'a2',
'a4',
'a3',
],
'v3': [
'a5',
'a3',
'a2',
],
'v4': [
'a5',
'a2',
'a3',
],
'v5': [
'a4',
'a5',
'a1',
],
'v6': [
'a3',
'a1',
'a5',
],
'v7': [
'a1',
'a5',
'a4',
],
'v8': [
'a5',
'a2',
'a1',
],
'v9': [
'a5',
'a3',
'a2',
],
}

# Saved linear voting profile: 
from collections import OrderedDict 
candidates = OrderedDict([
('a1', {'name': 'a1'}),
('a2', {'name': 'a2'}),
('a3', {'name': 'a3'}),
('a4', {'name': 'a4'}),
('a5', {'name': 'a5'}),
])
voters = OrderedDict([
('v01', {
'weight':5}),
('v02', {
'weight':3}),
('v03', {
'weight':2}),
('v04', {
'weight':1}),
('v05', {
'weight':1}),
('v06', {
'weight':1}),
('v07', {
'weight':1}),
('v08', {
'weight':1}),
('v09', {
'weight':1}),
('v10', {
'weight':1}),
])
linearBallot = {
'v01': [
'a4',
'a5',
'a1',
'a2',
'a3',
],
'v02': [
'a5',
'a4',
'a2',
'a3',
'a1',
],
'v03': [
'a5',
'a4',
'a2',
'a1',
'a3',
],
'v04': [
'a2',
'a3',
'a5',
'a1',
'a4',
],
'v05': [
'a2',
'a3',
'a1',
'a5',
'a4',
],
'v06': [
'a3',
'a5',
'a2',
'a4',
'a1',
],
'v07': [
'a3',
'a1',
'a5',
'a4',
'a2',
],
'v08': [
'a5',
'a2',
'a1',
'a4',
'a3',
],
'v09': [
'a2',
'a5',
'a3',
'a4',
'a1',
],
'v10': [
'a3',
'a5',
'a4',
'a2',
'a1',
],
}

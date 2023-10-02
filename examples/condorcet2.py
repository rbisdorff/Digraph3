####################################
# Condorcet, de Caritat N, Essai sur l'application de l'analyse
# à la probabilité des décisions rendues à la pluralité des voix
# Imprimerie Royale 1785, p. lviij (67)
# https://gallica.bnf.fr/ark:/12148/bpt6k417181/f15.item
# LinearVotingProfile format
##################################
from collections import OrderedDict 
candidates = OrderedDict([
('A', {'name': 'Candidate A'}),
('B', {'name': 'Candidate B'}),
('C', {'name': 'Candidate C'}),
])
voters = OrderedDict([
('v1', {
'weight':23}),
('v2', {
'weight':19}),
('v3', {
'weight':16}),
('v4', {
'weight':2}),
])
linearBallot = {
'v1': [
'A',
'C',
'B',
],
'v2': [
'B',
'C',
'A',
],
'v3': [
'C',
'B',
'A',
],
'v4': [
'C',
'A',
'B',
],
}

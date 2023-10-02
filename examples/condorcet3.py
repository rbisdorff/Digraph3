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
'weight':18}),
])
linearBallot = {
'v1': [
'A',
'B',
'C',
],
'v2': [
'C',
'A',
'B',
],
'v3': [
'B',
'C',
'A',
],

}

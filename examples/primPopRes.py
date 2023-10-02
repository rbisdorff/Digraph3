# Saved performance Tableau: 
from decimal import Decimal
from collections import OrderedDict
from outrankingDigraphs import *

actions = OrderedDict([
('aap', {
'shortName': 'aap',
'name': 'Anna Agueb Porterie',
'comment': 'Militante professionnelle de la mobilisation',
}),
('ah', {
'shortName': 'ah',
'name': 'Anne Hidalgo',
'comment': 'Candidate officielle du PS',
}),
('yj', {
'shortName': 'yj',
'name': 'Yannick Jadot',
'comment': 'Députl européen et Candidat EELV',
}),
('pl', {
'shortName': 'pl',
'name': 'Pierre Larroutourou',
'comment': 'Député européen sur la liste de rassemblement PS – Place Publique – Nouvelle Donne',
}),
('cm', {
'shortName': 'acm',
'name': 'Charlotte Marchandise',
'comment': 'Militante associative et consultante sur les questions de santé',
}),
('jlm', {
'shortName': 'jlm',
'name': 'Jean-Luc Mélenchon',
'comment': 'Candidat de la France insoumise',
}),
('ct', {
'shortName': 'ct',
'name': 'Christiane Taubira',
'comment': 'Candidat Radicaux de gauche (2002)',
}),
])
objectives = OrderedDict()
criteria = OrderedDict([
('Approvals', {
'name': 'Approval votes: Very Good, Good and Quite Good',
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.5'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0'))},
'scale': (0.0, 100.0),
'weight': Decimal('1'),
}),
('Abstentions', {
'name': 'Abstentions: Fair',
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.5'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0'))},
'scale': (0.0, 100.0),
'weight': Decimal('0'),
}),
('Disapprovals', {
'name': 'Disapproval votes: Insufficient',
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.5'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0'))},
'scale': (0.0, 100.0),
'weight': Decimal('-1'),
}),

])
NA = Decimal('-999')
totVotes = Decimal('392738')
percents = Decimal('100')
evaluation = {
'Approvals': {
'aap':Decimal("111511")/totVotes*percents,
'ah':Decimal("158611")/totVotes*percents,
'yj':Decimal("256247")/totVotes*percents,
'pl':Decimal("185824")/totVotes*percents,
'cm':Decimal("125377")/totVotes*percents,
'jlm':Decimal("206384")/totVotes*percents,
'ct':Decimal("310654")/totVotes*percents,
},
'Abstentions': {
'aap':Decimal("82673")/totVotes*percents,
'ah':Decimal("93471")/totVotes*percents,
'yj':Decimal("61042")/totVotes*percents,
'pl':Decimal("71124")/totVotes*percents,
'cm':Decimal("85911")/totVotes*percents,
'jlm':Decimal("71822")/totVotes*percents,
'ct':Decimal("31067")/totVotes*percents,
},
'Disapprovals': {
'aap':Decimal("198554")/totVotes*percents,
'ah':Decimal("140656")/totVotes*percents,
'yj':Decimal("75449")/totVotes*percents,
'pl':Decimal("135790")/totVotes*percents,
'cm':Decimal("181450")/totVotes*percents,
'jlm':Decimal("114532")/totVotes*percents,
'ct':Decimal("51017")/totVotes*percents,
},
}

#  for testing purposes
def compute():
    t = PerformanceTableau('primPopRes')
    g = BipolarOutrankingDigraph(t)
    return t,g

    

##########################################################
# Historic Paris Cabernet Sauvignon Wine Tatsting of 1976
# https://www.alcoholproblemsandsolutions.org/historic-paris-wine-tasting-of-1976-judgement-of-paris/
# Source: Balinski M. and Laraki R.,
# *Majority Judgment: Measuring, Ranking and Electing*,
# MIT Press, 2010 pp 156-169
##########################################################
from decimal import Decimal
from collections import OrderedDict
actions = OrderedDict([
('A', {
'name': "Stag's Leap 1973",
'comment': 'Californian',
}),
('B', {
'name': 'Mouton Rothschild 1970',
'comment': 'French',
}),
('C', {
'name': 'Montrose 1970',
'comment': 'French',
}),
('D', {
'name': 'Haut-Brion 1970',
'comment': 'French',
}),
('E', {
'name': 'Ridge Montebello 1971',
'comment': 'Californian',
}),
('F', {
'name': 'Leoville-Las Cases 1971',
'comment': 'French',
}),
('G', {
'name': "Heitz's Martha's Vineyard 1970",
'comment': 'Californiam',
}),
('H', {
'name': 'Clos du Val 1972',
'comment': 'Californian',
}),
('I', {
'name': 'Mayacama 1971',
'comment': 'Californian',
}),
('J', {
'name': 'Freemark Abbey 1969',
'comment': 'Californian',
}),
])
objectives = OrderedDict([
])
criteria = OrderedDict([
('PB', {
'name': 'Pierre Brejoux',
'comment': 'Inspector General of the Institut National des Appellations d’Origine Controllée',
'preferenceDirection': 'max',
'scale': (Decimal('0.00'), Decimal('20.00')),
'weight': Decimal('1.00'),
'thresholds': {'ind': (Decimal('0.00'), Decimal('0.0')), 'pref': (Decimal('2.00'), Decimal('0.0'))},
}),
('AV', {
'name': 'Aubert de Villaine',
'comment': 'Co-director of the Domaine de la Romanée-Conti',
'preferenceDirection': 'max',
'scale': (Decimal('0.00'), Decimal('20.00')),
'weight': Decimal('1.00'),
'thresholds': {'ind': (Decimal('0.00'), Decimal('0.0')), 'pref': (Decimal('2.00'), Decimal('0.0'))},
}),
('MD', {
'name': 'Michel Dovaz',
'comment': 'Institut Oenologique de France',
'preferenceDirection': 'max',
'scale': (Decimal('0.00'), Decimal('20.00')),
'weight': Decimal('1.00'),
'thresholds': {'ind': (Decimal('0.00'), Decimal('0.0')), 'pref': (Decimal('2.00'), Decimal('0.0'))},
}),
('PG', {
'name': 'Patricia Gallagher',
'comment': 'American wine connoisseur',
'preferenceDirection': 'max',
'scale': (Decimal('0.00'), Decimal('20.00')),
'weight': Decimal('1.00'),
'thresholds': {'ind': (Decimal('0.00'), Decimal('0.0')), 'pref': (Decimal('2.00'), Decimal('0.0'))},
}),
('OK', {
'name': 'Odette Kahn',
'comment': 'Director of the Revue du Vin de France',
'preferenceDirection': 'max',
'scale': (Decimal('0.00'), Decimal('20.00')),
'weight': Decimal('1.00'),
'thresholds': {'ind': (Decimal('0.00'), Decimal('0.0')), 'pref': (Decimal('2.00'), Decimal('0.0'))},
}),
('CDM', {
'name': 'Claude Dubois-Millot',
'comment': 'Commercial director of Le Nouveau Guide',
'preferenceDirection': 'max',
'scale': (Decimal('0.00'), Decimal('20.00')),
'weight': Decimal('1.00'),
'thresholds': {'ind': (Decimal('0.00'), Decimal('0.0')), 'pref': (Decimal('2.00'), Decimal('0.0'))},
}),
('RO', {
'name': 'Raymond Oliver',
'comment': 'Owner of the restaurant Le Grand Vefour',
'preferenceDirection': 'max',
'scale': (Decimal('0.00'), Decimal('20.00')),
'weight': Decimal('1.00'),
'thresholds': {'ind': (Decimal('0.00'), Decimal('0.0')), 'pref': (Decimal('2.00'), Decimal('0.0'))},
}),
('SS', {
'name': 'Steven Spurrier',
'comment': 'English Wine merchant in Paris',
'preferenceDirection': 'max',
'scale': (Decimal('0.00'), Decimal('20.00')),
'weight': Decimal('1.00'),
'thresholds': {'ind': (Decimal('0.00'), Decimal('0.0')), 'pref': (Decimal('2.00'), Decimal('0.0'))},
}),
('PT', {
'name': 'Pierre Tari',
'comment': 'proprietor of Chateau Giscours',
'preferenceDirection': 'max',
'scale': (Decimal('0.00'), Decimal('20.00')),
'weight': Decimal('1.00'),
'thresholds': {'ind': (Decimal('0.00'), Decimal('0.0')), 'pref': (Decimal('2.00'), Decimal('0.0'))},
}),
('CV', {
'name': 'Christian Vanneque',
'comment': 'Wine steward at the restaurant La Tour d’Argent',
'preferenceDirection': 'max',
'scale': (Decimal('0.00'), Decimal('20.00')),
'weight': Decimal('1.00'),
'thresholds': {'ind': (Decimal('0.00'), Decimal('0.0')), 'pref': (Decimal('2.00'), Decimal('0.0'))},
}),
('JV', {
'name': 'Jean Claude Vrinat',
'comment': 'Owner of the restaurant Taillevent',
'preferenceDirection': 'max',
'scale': (Decimal('0.00'), Decimal('20.00')),
'weight': Decimal('1.00'),
'thresholds': {'ind': (Decimal('0.00'), Decimal('0.0')), 'pref': (Decimal('2.00'), Decimal('0.0'))},
}),
])
evaluation = {
'PB': {
'A':Decimal("14"),
'B':Decimal("16"),
'C':Decimal("12"),
'D':Decimal("17"),
'E':Decimal("13"),
'F':Decimal("10"),
'G':Decimal("12"),
'H':Decimal("14"),
'I':Decimal("5"),
'J':Decimal("7"),
},
'AV': {
'A':Decimal("15"),
'B':Decimal("14"),
'C':Decimal("16"),
'D':Decimal("15"),
'E':Decimal("9"),
'F':Decimal("10"),
'G':Decimal("7"),
'H':Decimal("5"),
'I':Decimal("12"),
'J':Decimal("7"),
},
'MD': {
'A':Decimal("10"),
'B':Decimal("15"),
'C':Decimal("11"),
'D':Decimal("12"),
'E':Decimal("12"),
'F':Decimal("10"),
'G':Decimal("11"),
'H':Decimal("11"),
'I':Decimal("8"),
'J':Decimal("14"),
},
'PG': {
'A':Decimal("14"),
'B':Decimal("15"),
'C':Decimal("14"),
'D':Decimal("12"),
'E':Decimal("16"),
'F':Decimal("14"),
'G':Decimal("17"),
'H':Decimal("13"),
'I':Decimal("9"),
'J':Decimal("14"),
},
'OK': {
'A':Decimal("15"),
'B':Decimal("12"),
'C':Decimal("12"),
'D':Decimal("12"),
'E':Decimal("7"),
'F':Decimal("12"),
'G':Decimal("2"),
'H':Decimal("2"),
'I':Decimal("13"),
'J':Decimal("5"),
},
'CDM': {
'A':Decimal("16"),
'B':Decimal("16"),
'C':Decimal("17"),
'D':Decimal("13.5"),
'E':Decimal("7"),
'F':Decimal("11"),
'G':Decimal("8"),
'H':Decimal("9"),
'I':Decimal("9.5"),
'J':Decimal("9"),
},
'RO': {
'A':Decimal("14"),
'B':Decimal("12"),
'C':Decimal("14"),
'D':Decimal("10"),
'E':Decimal("12"),
'F':Decimal("12"),
'G':Decimal("10"),
'H':Decimal("10"),
'I':Decimal("14"),
'J':Decimal("8"),
},
'SS': {
'A':Decimal("14"),
'B':Decimal("14"),
'C':Decimal("14"),
'D':Decimal("8"),
'E':Decimal("14"),
'F':Decimal("12"),
'G':Decimal("13"),
'H':Decimal("11"),
'I':Decimal("9"),
'J':Decimal("13"),
},
'PT': {
'A':Decimal("13"),
'B':Decimal("11"),
'C':Decimal("14"),
'D':Decimal("14"),
'E':Decimal("17"),
'F':Decimal("12"),
'G':Decimal("15"),
'H':Decimal("13"),
'I':Decimal("12"),
'J':Decimal("14"),
},
'CV': {
'A':Decimal("16.5"),
'B':Decimal("16"),
'C':Decimal("11"),
'D':Decimal("17"),
'E':Decimal("15.5"),
'F':Decimal("8"),
'G':Decimal("10"),
'H':Decimal("16.5"),
'I':Decimal("3"),
'J':Decimal("6"),
},
'JV': {
'A':Decimal("14"),
'B':Decimal("14"),
'C':Decimal("15"),
'D':Decimal("15"),
'E':Decimal("11"),
'F':Decimal("12"),
'G':Decimal("9"),
'H':Decimal("7"),
'I':Decimal("13"),
'J':Decimal("7"),
},
}
########################################3
# CHE-Hochschul-Ranking 2005
# Die Zeit Nr. 21 19.Mai 2005 Seite 81
# www.zeit.de/studium
# MCS ADT Course
# RB May 2020
# --------------------------------------- 
from decimal import Decimal
from collections import OrderedDict
actions = OrderedDict([
('rwth', {
'name': 'TWTH Aachen',
}),
('uaug', {
'name': 'Uni Augsburg',
}),
('ubam', {
'name': 'Uni Bamberg',
}),
('ubas', {
'name': 'Uni Basel (CH)',
}),
('ubay', {
'name': 'Uni Bayreuth',
}),
('escp', {
'name': 'ESCP-EAP Berlin',
}),
('fber', {
'name': 'FU Berlin',
}),
('hber', {
'name': 'HU Berlin',
}),
('tber', {
'name': 'TU Berlin',
}),
('ubiel', {
'name': 'Uni Bielefeld',
}),
('uboch', {
'name': 'Uni Bochum',
}),
('ubrem', {
'name': 'Uni Bremen',
}),
('ibruc', {
'name': 'Int. Uni Bruchsal',
}),
('tchem', {
'name': 'TU Chemnitz',
}),
('udort', {
'name': 'Uni Dortmund',
}),
('tdres', {
'name': 'TU Dresden',
}),
('eduis', {
'name': 'Uni Duisburg/Essen',
}),
('dduis', {
'name': 'Uni Duisburg/Duisburg',
}),
('udues', {
'name': 'Uni Duesseldorf',
}),
('ueich', {
'name': 'Uni Eichstätt-Ingolstadt',
}),
('uerl', {
'name': 'Uni Erlangen-Nürnberg',
}),
('iflens', {
'name': 'Uni Flensburg',
}),
('hfran', {
'name': 'HfB Frankfurt',
}),
('ufran', {
'name': 'Uni Frankfurt',
}),
('efran', {
'name': 'Europ. Uni Frankfurt',
}),
('tbfrei', {
'name': 'TU Bergakademie Freiberg',
}),
('ufrib', {
'name': 'Uni Fribourg (CH)',
}),
('ugen', {
'name': 'Uni GenÃ¨ve (CH)',
}),
('ugies', {
'name': 'Uni Giessen',
}),
('ugoet', {
'name': 'Uni Goettingen',
}),
('ugraz', {
'name': 'Uni Graz (A)',
}),
('ugreif', {
'name': 'Uni Greifswald',
}),
('uhal', {
'name': 'Uni Halle-Wittenberg',
}),
('hham', {
'name': 'HWP Hamburg',
}),
('uham', {
'name': 'Uni Hamburg',
}),
('uhan', {
'name': 'Uni Hannover',
}),
('uhoh', {
'name': 'Uni Hohenheim',
}),
('uinn', {
'name': 'Uni Innsbruck (A)',
}),
('ujen', {
'name': 'Uni Jena',
}),
('ukas', {
'name': 'Uni Kassel',
}),
('ukiel', {
'name': 'Uni Kiel',
}),
('uklag', {
'name': 'Uni Klagenfurt',
}),
('wkob', {
'name': 'WHU Koblenz',
}),
('ukoel', {
'name': 'Uni Koeln',
}),
('ulaus', {
'name': 'Uni Lausanne (CH)',
}),
('hleip', {
'name': 'HH Leipzip',
}),
('uleip', {
'name': 'Uni Leipzig',
}),
('ulinz', {
'name': 'Uni Linz (A)',
}),
('uluen', {
'name': 'Uni Lüneburg',
}),
('umagd', {
'name': 'Uni Magdeburg',
}),
('umain', {
'name': 'Uni Mainz',
}),
('uman', {
'name': 'Uni Mannheim',
}),
('umar', {
'name': 'Uni Marburg',
}),
('lmuen', {
'name': 'LMU München',
}),
('tmuen', {
'name': 'TU Muenchen',
}),
('umuests', {
'name': 'Uni Münster',
}),
('uneu', {
'name': 'Uni Neuchâtel',
}),
('eoest', {
'name': 'EBS Oestrich-Winkel',
}),
('uold', {
'name': 'Uni Oldenburg',
}),
('uosn', {
'name': 'Uni Osnabrück',
}),
('upad', {
'name': 'Uni Paderborn',
}),
('upas', {
'name': 'Uni Passau',
}),
('upot', {
'name': 'Uni Potsdam',
}),
('ureg', {
'name': 'Uni Rgensburg',
}),
('urost', {
'name': 'Uni Rostock',
}),
('usar', {
'name': 'Uni Saarbrücken',
}),
('usieg', {
'name': 'Uni Siegen',
}),
('ugal', {
'name': 'Uni St. Gallen',
}),
('ustu', {
'name': 'Uni Stuttgart',
}),
('utri', {
'name': 'Uni Trier',
}),
('uteb', {
'name': 'Uni Tuebingen',
}),
('uulm', {
'name': 'Uni Ulm',
}),
('uwien', {
'name': 'Uni Wien (A)',
}),
('wwien', {
'name': 'WU Wien (A)',
}),
('uwit', {
'name': 'Uni Witten-Herdecke',
}),
('uwup', {
'name': 'Uni Wuppertal',
}),
('uwue', {
'name': 'Uni Wuerzburg',
}),
('uzh', {
'name': 'Uni Zürich (CH)',
}),
])
objectives = OrderedDict([
])
criteria = OrderedDict([
('rep', {
'weight': Decimal('6.0'),
'comment': 'Reputation bei Professoren (6/25)',
'name': 'Reputation',
'preferenceDirection': 'max',
'scale': (1.0, 3, 0),
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0')), 'veto': (Decimal('6.0'), Decimal('0.0'))},
}),
('pub', {
'weight': Decimal('6.0'),
'comment': 'Wissenschaftliche Veroeffentlichungen',
'name': 'Publications',
'preferenceDirection': 'max',
'scale': (1.0, 3, 0),
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0')), 'veto': (Decimal('6.0'), Decimal('0.0'))},
}),
('lib', {
'weight': Decimal('6.0'),
'comment': 'Bibliothek Ausstattung',
'name': 'Library',
'preferenceDirection': 'max',
'scale': (1.0, 3, 0),
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0')), 'veto': (Decimal('6.0'), Decimal('0.0'))},
}),
('std', {
'weight': Decimal('6.0'),
'comment': 'Studenten Betreuung',
'name': 'Student care',
'preferenceDirection': 'max',
'scale': (1.0, 3, 0),
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0')), 'veto': (Decimal('6.0'), Decimal('0.0'))},
}),
('tot', {
'weight': Decimal('1.0'),
'comment': 'Gesamturteil',
'name': 'Overall appreciation',
'preferenceDirection': 'max',
'scale': (1.0, 3, 0),
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('1.0'), Decimal('0.0')), 'veto': (Decimal('6.0'), Decimal('0.0'))},
}),
])

evaluation = {
# 1: weak, 2: fair, 3: good
'rep': {
'rwth':Decimal("1.00"),
'uaug':Decimal("2.00"),
'ubam':Decimal("2.00"),
'ubas':Decimal("2.00"),
'ubay':Decimal("3.00"),
'escp':Decimal("3.00"),
'fber':Decimal("1.00"),
'hber':Decimal("1.00"),
'tber':Decimal("1.00"),
'ubiel':Decimal("2.00"),
'uboch':Decimal("1.00"),
'ubrem':Decimal("1.00"),
'ibruc':Decimal("3.00"),
'tchem':Decimal("2.00"),
'udort':Decimal("1.00"),
'tdres':Decimal("2.00"),
'eduis':Decimal("3.00"),
'dduis':Decimal("1.00"),
'udues':Decimal("1.00"),
'ueich':Decimal("3.00"),
'uerl':Decimal("2.00"),
'iflens':Decimal("2.00"),
'hfran':Decimal("3.00"),
'ufran':Decimal("2.00"),
'efran':Decimal("3.00"),
'tbfrei':Decimal("2.00"),
'ufrib':Decimal("2.00"),
'ugen':Decimal("2.00"),
'ugies':Decimal("3.00"),
'ugoet':Decimal("2.00"),
'ugraz':Decimal("1.00"),
'ugreif':Decimal("2.00"),
'uhal':Decimal("3.00"),
'hham':Decimal("2.00"),
'uham':Decimal("1.00"),
'uhan':Decimal("1.00"),
'uhoh':Decimal("2.00"),
'uinn':Decimal("1.00"),
'ujen':Decimal("1.00"),
'ukas':Decimal("1.00"),
'ukiel':Decimal("3.00"),
'uklag':Decimal("3.00"),
'wkob':Decimal("3.00"),
'ukoel':Decimal("1.00"),
'ulaus':Decimal("3.00"),
'hleip':Decimal("3.00"),
'uleip':Decimal("1.00"),
'ulinz':Decimal("2.00"),
'uluen':Decimal("2.00"),
'umagd':Decimal("3.00"),
'umain':Decimal("1.00"),
'uman':Decimal("3.00"),
'umar':Decimal("2.00"),
'lmuen':Decimal("2.00"),
'tmuen':Decimal("3.00"),
'umuests':Decimal("3.00"),
'uneu':Decimal("2.00"),
'eoest':Decimal("3.00"),
'uold':Decimal("2.00"),
'uosn':Decimal("1.00"),
'upad':Decimal("1.00"),
'upas':Decimal("3.00"),
'upot':Decimal("1.00"),
'ureg':Decimal("1.00"),
'urost':Decimal("2.00"),
'usar':Decimal("3.00"),
'usieg':Decimal("1.00"),
'ugal':Decimal("3.00"),
'ustu':Decimal("1.00"),
'utri':Decimal("2.00"),
'uteb':Decimal("2.00"),
'uulm':Decimal("3.00"),
'uwien':Decimal("1.00"),
'wwien':Decimal("1.00"),
'uwit':Decimal("3.00"),
'uwup':Decimal("1.00"),
'uwue':Decimal("1.00"),
'uzh':Decimal("2.00"),
},
'pub': {
'rwth':Decimal("1.00"),
'uaug':Decimal("1.00"),
'ubam':Decimal("2.00"),
'ubas':Decimal("2.00"),
'ubay':Decimal("2.00"),
'escp':Decimal("3.00"),
'fber':Decimal("1.00"),
'hber':Decimal("1.00"),
'tber':Decimal("1.00"),
'ubiel':Decimal("1.00"),
'uboch':Decimal("1.00"),
'ubrem':Decimal("1.00"),
'ibruc':Decimal("3.00"),
'tchem':Decimal("2.00"),
'udort':Decimal("1.00"),
'tdres':Decimal("2.00"),
'eduis':Decimal("3.00"),
'dduis':Decimal("2.00"),
'udues':Decimal("1.00"),
'ueich':Decimal("3.00"),
'uerl':Decimal("2.00"),
'iflens':Decimal("2.00"),
'hfran':Decimal("3.00"),
'ufran':Decimal("2.00"),
'efran':Decimal("2.00"),
'tbfrei':Decimal("3.00"),
'ufrib':Decimal("1.00"),
'ugen':Decimal("1.00"),
'ugies':Decimal("3.00"),
'ugoet':Decimal("2.00"),
'ugraz':Decimal("1.00"),
'ugreif':Decimal("3.00"),
'uhal':Decimal("2.00"),
'hham':Decimal("2.00"),
'uham':Decimal("1.00"),
'uhan':Decimal("1.00"),
'uhoh':Decimal("2.00"),
'uinn':Decimal("1.00"),
'ujen':Decimal("1.00"),
'ukas':Decimal("2.00"),
'ukiel':Decimal("3.00"),
'uklag':Decimal("3.00"),
'wkob':Decimal("3.00"),
'ukoel':Decimal("1.00"),
'ulaus':Decimal("1.00"),
'hleip':Decimal("3.00"),
'uleip':Decimal("1.00"),
'ulinz':Decimal("2.00"),
'uluen':Decimal("2.00"),
'umagd':Decimal("3.00"),
'umain':Decimal("1.00"),
'uman':Decimal("2.00"),
'umar':Decimal("2.00"),
'lmuen':Decimal("2.00"),
'tmuen':Decimal("3.00"),
'umuests':Decimal("2.00"),
'uneu':Decimal("1.00"),
'eoest':Decimal("3.00"),
'uold':Decimal("2.00"),
'uosn':Decimal("2.00"),
'upad':Decimal("1.00"),
'upas':Decimal("3.00"),
'upot':Decimal("1.00"),
'ureg':Decimal("2.00"),
'urost':Decimal("2.00"),
'usar':Decimal("2.00"),
'usieg':Decimal("2.00"),
'ugal':Decimal("1.00"),
'ustu':Decimal("1.00"),
'utri':Decimal("2.00"),
'uteb':Decimal("3.00"),
'uulm':Decimal("3.00"),
'uwien':Decimal("2.00"),
'wwien':Decimal("1.00"),
'uwit':Decimal("3.00"),
'uwup':Decimal("1.00"),
'uwue':Decimal("2.00"),
'uzh':Decimal("1.00"),
},
'lib': {
'rwth':Decimal("1.00"),
'uaug':Decimal("1.00"),
'ubam':Decimal("1.00"),
'ubas':Decimal("3.00"),
'ubay':Decimal("3.00"),
'escp':Decimal("2.00"),
'fber':Decimal("2.00"),
'hber':Decimal("1.00"),
'tber':Decimal("1.00"),
'ubiel':Decimal("3.00"),
'uboch':Decimal("1.00"),
'ubrem':Decimal("1.00"),
'ibruc':Decimal("2.00"),
'tchem':Decimal("2.00"),
'udort':Decimal("2.00"),
'tdres':Decimal("2.00"),
'eduis':Decimal("2.00"),
'dduis':Decimal("1.00"),
'udues':Decimal("1.00"),
'ueich':Decimal("3.00"),
'uerl':Decimal("2.00"),
'iflens':Decimal("1.00"),
'hfran':Decimal("3.00"),
'ufran':Decimal("2.00"),
'efran':Decimal("3.00"),
'tbfrei':Decimal("2.00"),
'ufrib':Decimal("1.00"),
'ugen':Decimal("2.00"),
'ugies':Decimal("2.00"),
'ugoet':Decimal("2.00"),
'ugraz':Decimal("1.00"),
'ugreif':Decimal("3.00"),
'uhal':Decimal("2.00"),
'hham':Decimal("2.00"),
'uham':Decimal("1.00"),
'uhan':Decimal("1.00"),
'uhoh':Decimal("3.00"),
'uinn':Decimal("2.00"),
'ujen':Decimal("1.00"),
'ukas':Decimal("2.00"),
'ukiel':Decimal("3.00"),
'uklag':Decimal("1.00"),
'wkob':Decimal("3.00"),
'ukoel':Decimal("1.00"),
'ulaus':Decimal("3.00"),
'hleip':Decimal("3.00"),
'uleip':Decimal("1.00"),
'ulinz':Decimal("3.00"),
'uluen':Decimal("1.00"),
'umagd':Decimal("3.00"),
'umain':Decimal("1.00"),
'uman':Decimal("3.00"),
'umar':Decimal("1.00"),
'lmuen':Decimal("2.00"),
'tmuen':Decimal("3.00"),
'umuests':Decimal("3.00"),
'uneu':Decimal("1.00"),
'eoest':Decimal("2.00"),
'uold':Decimal("2.00"),
'uosn':Decimal("2.00"),
'upad':Decimal("2.00"),
'upas':Decimal("3.00"),
'upot':Decimal("1.00"),
'ureg':Decimal("2.00"),
'urost':Decimal("2.00"),
'usar':Decimal("2.00"),
'usieg':Decimal("1.00"),
'ugal':Decimal("3.00"),
'ustu':Decimal("1.00"),
'utri':Decimal("1.00"),
'uteb':Decimal("2.00"),
'uulm':Decimal("2.00"),
'uwien':Decimal("2.00"),
'wwien':Decimal("1.00"),
'uwit':Decimal("2.00"),
'uwup':Decimal("2.00"),
'uwue':Decimal("2.00"),
'uzh':Decimal("3.00"),
},
'std': {
'rwth':Decimal("2.00"),
'uaug':Decimal("3.00"),
'ubam':Decimal("2.00"),
'ubas':Decimal("-999.00"),
'ubay':Decimal("2.00"),
'escp':Decimal("3.00"),
'fber':Decimal("3.00"),
'hber':Decimal("1.00"),
'tber':Decimal("3.00"),
'ubiel':Decimal("2.00"),
'uboch':Decimal("3.00"),
'ubrem':Decimal("3.00"),
'ibruc':Decimal("1.00"),
'tchem':Decimal("3.00"),
'udort':Decimal("2.00"),
'tdres':Decimal("3.00"),
'eduis':Decimal("3.00"),
'dduis':Decimal("3.00"),
'udues':Decimal("2.00"),
'ueich':Decimal("2.00"),
'uerl':Decimal("2.00"),
'iflens':Decimal("1.00"),
'hfran':Decimal("-999.00"),
'ufran':Decimal("2.00"),
'efran':Decimal("2.00"),
'tbfrei':Decimal("2.00"),
'ufrib':Decimal("-999.00"),
'ugen':Decimal("-999.00"),
'ugies':Decimal("2.00"),
'ugoet':Decimal("2.00"),
'ugraz':Decimal("-999.00"),
'ugreif':Decimal("2.00"),
'uhal':Decimal("2.00"),
'hham':Decimal("-999.00"),
'uham':Decimal("2.00"),
'uhan':Decimal("1.00"),
'uhoh':Decimal("2.00"),
'uinn':Decimal("-999.00"),
'ujen':Decimal("2.00"),
'ukas':Decimal("2.00"),
'ukiel':Decimal("2.00"),
'uklag':Decimal("-999.00"),
'wkob':Decimal("3.00"),
'ukoel':Decimal("3.00"),
'ulaus':Decimal("-999.00"),
'hleip':Decimal("1.00"),
'uleip':Decimal("1.00"),
'ulinz':Decimal("-999.00"),
'uluen':Decimal("2.00"),
'umagd':Decimal("1.00"),
'umain':Decimal("2.00"),
'uman':Decimal("3.00"),
'umar':Decimal("2.00"),
'lmuen':Decimal("3.00"),
'tmuen':Decimal("1.00"),
'umuests':Decimal("2.00"),
'uneu':Decimal("-999.00"),
'eoest':Decimal("2.00"),
'uold':Decimal("2.00"),
'uosn':Decimal("1.00"),
'upad':Decimal("1.00"),
'upas':Decimal("1.00"),
'upot':Decimal("2.00"),
'ureg':Decimal("3.00"),
'urost':Decimal("2.00"),
'usar':Decimal("3.00"),
'usieg':Decimal("1.00"),
'ugal':Decimal("-999.00"),
'ustu':Decimal("3.00"),
'utri':Decimal("2.00"),
'uteb':Decimal("2.00"),
'uulm':Decimal("2.00"),
'uwien':Decimal("-999.00"),
'wwien':Decimal("-999.00"),
'uwit':Decimal("3.00"),
'uwup':Decimal("2.00"),
'uwue':Decimal("2.00"),
'uzh':Decimal("-999.00"),
},
'tot': {
'rwth':Decimal("2.00"),
'uaug':Decimal("2.00"),
'ubam':Decimal("2.00"),
'ubas':Decimal("-999.00"),
'ubay':Decimal("2.00"),
'escp':Decimal("2.00"),
'fber':Decimal("2.00"),
'hber':Decimal("2.00"),
'tber':Decimal("2.00"),
'ubiel':Decimal("2.00"),
'uboch':Decimal("2.00"),
'ubrem':Decimal("2.00"),
'ibruc':Decimal("2.00"),
'tchem':Decimal("2.00"),
'udort':Decimal("2.00"),
'tdres':Decimal("2.00"),
'eduis':Decimal("2.00"),
'dduis':Decimal("2.00"),
'udues':Decimal("2.00"),
'ueich':Decimal("2.00"),
'uerl':Decimal("2.00"),
'iflens':Decimal("2.00"),
'hfran':Decimal("1.00"),
'ufran':Decimal("3.00"),
'efran':Decimal("2.00"),
'tbfrei':Decimal("2.00"),
'ufrib':Decimal("-999.00"),
'ugen':Decimal("-999.00"),
'ugies':Decimal("2.00"),
'ugoet':Decimal("2.00"),
'ugraz':Decimal("-999.00"),
'ugreif':Decimal("2.00"),
'uhal':Decimal("2.00"),
'hham':Decimal("-999.00"),
'uham':Decimal("2.00"),
'uhan':Decimal("2.00"),
'uhoh':Decimal("2.00"),
'uinn':Decimal("-999.00"),
'ujen':Decimal("2.00"),
'ukas':Decimal("2.00"),
'ukiel':Decimal("2.00"),
'uklag':Decimal("-999.00"),
'wkob':Decimal("2.00"),
'ukoel':Decimal("3.00"),
'ulaus':Decimal("-999.00"),
'hleip':Decimal("1.00"),
'uleip':Decimal("2.00"),
'ulinz':Decimal("-999.00"),
'uluen':Decimal("2.00"),
'umagd':Decimal("2.00"),
'umain':Decimal("2.00"),
'uman':Decimal("3.00"),
'umar':Decimal("2.00"),
'lmuen':Decimal("3.00"),
'tmuen':Decimal("2.00"),
'umuests':Decimal("3.00"),
'uneu':Decimal("-999.00"),
'eoest':Decimal("2.00"),
'uold':Decimal("2.00"),
'uosn':Decimal("2.00"),
'upad':Decimal("2.00"),
'upas':Decimal("2.00"),
'upot':Decimal("2.00"),
'ureg':Decimal("2.00"),
'urost':Decimal("2.00"),
'usar':Decimal("2.00"),
'usieg':Decimal("2.00"),
'ugal':Decimal("-999.00"),
'ustu':Decimal("2.00"),
'utri':Decimal("2.00"),
'uteb':Decimal("2.00"),
'uulm':Decimal("2.00"),
'uwien':Decimal("-999.00"),
'wwien':Decimal("-999.00"),
'uwit':Decimal("2.00"),
'uwup':Decimal("2.00"),
'uwue':Decimal("2.00"),
'uzh':Decimal("-999.00"),
},
}
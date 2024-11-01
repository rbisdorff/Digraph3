# Algorithmic decision making with Python resources
# R. Bisdorff Autumn 2021
# historical quintiles of enrolment quality
# DER SPIEGEL Student survey 2004
# https://www.spiegel.de/lebenundlernen/uni/studentenbefragung-des-spiegel-die-methode-a-%20329082.html
#########################
from decimal import Decimal
from collections import OrderedDict
perfTabType = 'PerformanceTableau'
objectives = OrderedDict([
('HUM', {
'name': 'Humanities',
'criteria': ['germ', 'pol', 'psy', 'soc'],
'weight': Decimal('4.0'),
}),
('LEM', {
'name': 'Law, Economics & Management',
'criteria': ['law', 'eco', 'mgt'],
'weight': Decimal('3.0'),
}),
('LSM', {
'name': 'Life Sciences & Medicine',
'criteria': ['bio', 'med'],
'weight': Decimal('2.0'),
}),
('SCI', {
'name': 'Technology',
'criteria': ['info', 'elec', 'mec'],
'weight': Decimal('3.0'),
}),
])
NA = Decimal('-999.00')
criteria = OrderedDict([
('germ', {
'shortName': 'germ',
'name': 'German Studies',
'comment': 'Humanities',
'weight': Decimal('1.0'),
'scale': (45.0, 65.0),
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'minValue': Decimal('1.00'),
'maxValue': Decimal('61.4'),
}),
('pol', {
'shortName': 'pol',
'name': 'Politology',
'comment': 'Humanities',
'weight': Decimal('1.0'),
'scale': (50.0, 70.0),
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'minValue': Decimal('50.8'),
'maxValue': Decimal('65.9'),
}),
('psy', {
'shortName': 'psy',
'name': 'Psychology',
'comment': 'Humanities',
'weight': Decimal('1.0'),
'scale': (50.0, 70.0),
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'minValue': Decimal('52.5'),
'maxValue': Decimal('64.1'),
}),
('soc', {
'shortName': 'soc',
'name': 'Sociology',
'comment': 'Humanities',
'weight': Decimal('1.0'),
'scale': (45.0, 65.0),
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'minValue': Decimal('1.00'),
'maxValue': Decimal('59.8'),
}),
('law', {
'shortName': 'law',
'name': 'Law Studies',
'comment': 'Law, Economics & Management',
'weight': Decimal('1.0'),
'scale': (35.0, 65.0),
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'minValue': Decimal('39.1'),
'maxValue': Decimal('51.1'),
}),
('eco', {
'shortName': 'eco',
'name': 'Economics',
'comment': 'Law, Economics & Management',
'weight': Decimal('1.0'),
'scale': (45.0, 65.0),
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'minValue': Decimal('49.6'),
'maxValue': Decimal('60.8'),
}),
('mgt', {
'shortName': 'mgt',
'name': 'Management',
'comment': 'Law, Economics & Management',
'weight': Decimal('1.0'),
'scale': (40.0, 80.0),
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'minValue': Decimal('47.5'),
'maxValue': Decimal('68.0'),
}),
('bio', {
'shortName': 'bio',
'name': 'Life Sciences',
'comment': 'Life Sciences & Medicine',
'weight': Decimal('1.0'),
'scale': (45.0, 65.0),
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'minValue': Decimal('1.00'),
'maxValue': Decimal('57.1'),
}),
('med', {
'shortName': 'med',
'name': 'Medicine',
'comment': 'Life Sciences & Medicine',
'weight': Decimal('1.0'),
'scale': (45.0, 65.0),
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'minValue': Decimal('3.00'),
'maxValue': Decimal('60.1'),
}),
('phys', {
'shortName': 'phys',
'name': 'Physics',
'comment': 'Natural Sciences & Mathematics',
'weight': Decimal('1.0'),
'scale': (45.0, 65.0),
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'minValue': Decimal('53.9'),
'maxValue': Decimal('62.8'),
}),
('chem', {
'shortName': 'chem',
'name': 'Chemistry',
'comment': 'Natural Sciences & Mathematics',
'weight': Decimal('1.0'),
'scale': (45.0, 65.0),
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'minValue': Decimal('2.00'),
'maxValue': Decimal('58.8'),
}),
('math', {
'shortName': 'math',
'name': 'Mathematics',
'comment': 'Natural Sciences & Mathematics',
'weight': Decimal('1.0'),
'scale': (45.0, 65.0),
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'minValue': Decimal('51.6'),
'maxValue': Decimal('63.1'),
}),
('info', {
'shortName': 'info',
'name': 'Computer Science',
'comment': 'Technology',
'weight': Decimal('1.0'),
'scale': (45.0, 65.0),
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'minValue': Decimal('3.00'),
'maxValue': Decimal('59.8'),
}),
('elec', {
'shortName': 'elec',
'name': 'Electrical Engineering',
'comment': 'Technology',
'weight': Decimal('1.0'),
'scale': (45.0, 65.0),
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'minValue': Decimal('50.1'),
'maxValue': Decimal('60.2'),
}),
('mec', {
'shortName': 'mec',
'name': 'Mechanical Engineering',
'comment': 'Technology',
'weight': Decimal('1.0'),
'scale': (45.0, 65.0),
'preferenceDirection': 'max',
'thresholds': {'ind': (Decimal('0.1'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'minValue': Decimal('51.9'),
'maxValue': Decimal('57.8'),
}),
])
quantilesFrequencies = [
Decimal("0.00"),
Decimal("0.20"),
Decimal("0.40"),
Decimal("0.60"),
Decimal("0.80"),
Decimal("1.00"),
]
historySizes = {
'germ': 39,'pol': 34,'psy': 34,'soc': 32,'law': 32,'eco': 21,'mgt': 34,'bio': 34,'med': 28,'phys': 37,'chem': 35,'math': 27,'info': 33,'elec': 14,'mec': 13,}
LowerClosed = True
limitingQuantiles = {
'germ': [
Decimal("1.00"),
Decimal("52.14"),
Decimal("54.02"),
Decimal("55.84"),
Decimal("57.48"),
Decimal("61.40"),
],
'pol': [
Decimal("50.80"),
Decimal("54.62"),
Decimal("56.18"),
Decimal("57.78"),
Decimal("59.78"),
Decimal("65.90"),
],
'psy': [
Decimal("52.50"),
Decimal("57.58"),
Decimal("58.46"),
Decimal("59.80"),
Decimal("60.94"),
Decimal("64.10"),
],
'soc': [
Decimal("1.00"),
Decimal("51.70"),
Decimal("53.92"),
Decimal("55.42"),
Decimal("56.26"),
Decimal("59.80"),
],
'law': [
Decimal("39.10"),
Decimal("42.30"),
Decimal("45.08"),
Decimal("46.30"),
Decimal("47.26"),
Decimal("51.10"),
],
'eco': [
Decimal("49.60"),
Decimal("52.14"),
Decimal("53.38"),
Decimal("54.28"),
Decimal("56.94"),
Decimal("60.80"),
],
'mgt': [
Decimal("47.50"),
Decimal("52.16"),
Decimal("52.98"),
Decimal("54.68"),
Decimal("55.96"),
Decimal("68.00"),
],
'bio': [
Decimal("1.00"),
Decimal("50.40"),
Decimal("51.80"),
Decimal("53.14"),
Decimal("55.04"),
Decimal("57.10"),
],
'med': [
Decimal("3.00"),
Decimal("49.20"),
Decimal("49.84"),
Decimal("51.10"),
Decimal("52.42"),
Decimal("60.10"),
],
'phys': [
Decimal("53.90"),
Decimal("58.78"),
Decimal("59.90"),
Decimal("60.96"),
Decimal("61.96"),
Decimal("62.80"),
],
'chem': [
Decimal("2.00"),
Decimal("53.30"),
Decimal("54.20"),
Decimal("55.80"),
Decimal("57.40"),
Decimal("58.80"),
],
'math': [
Decimal("51.60"),
Decimal("56.54"),
Decimal("57.76"),
Decimal("59.44"),
Decimal("61.00"),
Decimal("63.10"),
],
'info': [
Decimal("3.00"),
Decimal("54.40"),
Decimal("55.44"),
Decimal("56.68"),
Decimal("58.10"),
Decimal("59.80"),
],
'elec': [
Decimal("50.10"),
Decimal("54.08"),
Decimal("55.34"),
Decimal("56.54"),
Decimal("57.64"),
Decimal("60.20"),
],
'mec': [
Decimal("51.90"),
Decimal("54.02"),
Decimal("54.48"),
Decimal("55.18"),
Decimal("56.54"),
Decimal("57.80"),
],
}

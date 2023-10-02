#!/usr/bin/env python 3
# -*- coding: utf-8 -*-
# Source: Graffiti magazine, février 2003
# Digraph3 tutorials exercise
# (C) R. BISDORFF 2021 
#####################################
from decimal import Decimal
from collections import OrderedDict

# the movies to be seen in 2003
actions = OrderedDict([
('ah', {
'name': "Ah si j'étais riche",
}),
('aw', {
'name': 'A walk to remember',
}),
('bb', {
'name': 'Bend it like Beckham',
}),
('dl', {
'name': 'Demonlover',
}),
('gny', {
'name': 'Gangs of New York',
}),
('gs', {
'name': 'Ghost Ship',
}),
('hn', {
'name': 'El Hija de la Novia',
}),
('la', {
'name': 'Lantana',
}),
('lor', {
'name': 'Lord of the Rings - The Two Towers',
}),
('ma', {
'name': 'The Magdalene Sisters',
}),
('md', {
'name': 'Mr. Deeds',
}),
('mi', {
'name': 'Mon Idole',
}),
('sa', {
'name': 'the Slaton Sea',
}),
('sc', {
'name': 'the santa Clause 2',
}),
('sha', {
'name': 'Sweet home Alabama',
}),
('ss', {
'name': 'Sweet Sixteen',
}),
('vf', {
'name': "24 heures de la vie d'une femme",
}),
])
# Decision objectives not relevant 
objectives = OrderedDict([])

# The critics rating the movies  
criteria = OrderedDict([
('jt', {
'weight': 1,
'scale': [-2.0, 5.0],
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'preferenceDirection': 'max' 
}),
('td', {
'weight': 1,
'scale': [-2.0, 5.0],
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'preferenceDirection': 'max' 
}),
('cn', {
'weight': 1,
'scale': [-2.0, 5.0],
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'preferenceDirection': 'max' 
}),
('mr', {
'weight': 1,
'scale': [-2.0, 5.0],
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'preferenceDirection': 'max' 
}),
('as', {
'weight': 1,
'scale': [-2.0, 5.0],
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'preferenceDirection': 'max' 
}),
('dr', {
'weight': 1,
'scale': [-2.0, 5.0],
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'preferenceDirection': 'max' 
}),
('vt', {
'weight': 2,
'scale': [-2.0, 5.0],
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'preferenceDirection': 'max' 
}),
('cs', {
'weight': 1,
'scale': [-2.0, 5.0],
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'preferenceDirection': 'max' 
}),
('jh', {
'weight': 2,
'scale': [-2.0, 5.0],
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'preferenceDirection': 'max' 
}),
('rr', {
'weight': 1,
'scale': [-2.0, 5.0],
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'preferenceDirection': 'max' 
}),
('ap', {
'weight': 1,
'scale': [-2.0, 5.0],
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'preferenceDirection': 'max' 
}),
('mk', {
'weight': 1,
'scale': [-2.0, 5.0],
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'preferenceDirection': 'max' 
}),
('cf', {
'weight': 1,
'scale': [-2.0, 5.0],
'thresholds': {'ind': (Decimal('0.0'), Decimal('0.0')), 'pref': (Decimal('0.5'), Decimal('0.0'))},
'preferenceDirection': 'max' 
}),
])

# The critics' opinions
# -2 (I hate), -1 (don't like), 1 (maybe),
# 2 (good), 3 (excellent), 4 (not to be missed)
# 5 (a master piece), 999 (NA: Not seen) 
NA = Decimal('999')
evaluation = {
'jt': {
'ah':Decimal("1.00"),
'aw':Decimal("-1.00"),
'bb':Decimal("2.00"),
'dl':Decimal("1.00"),
'gny':Decimal("4.00"),
'gs':Decimal("1.00"),
'hn':Decimal("2.00"),
'la':Decimal("3.00"),
'lor':Decimal("4.00"),
'ma':Decimal("3.00"),
'md':Decimal("1.00"),
'mi':Decimal("2.00"),
'sa':Decimal("1.00"),
'sc':Decimal("1.00"),
'sha':Decimal("2.00"),
'ss':Decimal("3.00"),
'vf':Decimal("1.00"),
},
'td': {
'ah':Decimal("3.00"),
'aw':Decimal("999.00"),
'bb':Decimal("1.00"),
'dl':Decimal("1.00"),
'gny':Decimal("2.00"),
'gs':Decimal("-1.00"),
'hn':Decimal("999.00"),
'la':Decimal("999.00"),
'lor':Decimal("2.00"),
'ma':Decimal("3.00"),
'md':Decimal("1.00"),
'mi':Decimal("2.00"),
'sa':Decimal("999.00"),
'sc':Decimal("999.00"),
'sha':Decimal("999.00"),
'ss':Decimal("3.00"),
'vf':Decimal("1.00"),
},
'cn': {
'ah':Decimal("-1.00"),
'aw':Decimal("999.00"),
'bb':Decimal("2.00"),
'dl':Decimal("999.00"),
'gny':Decimal("4.00"),
'gs':Decimal("999.00"),
'hn':Decimal("2.00"),
'la':Decimal("3.00"),
'lor':Decimal("999.00"),
'ma':Decimal("3.00"),
'md':Decimal("999.00"),
'mi':Decimal("1.00"),
'sa':Decimal("999.00"),
'sc':Decimal("999.00"),
'sha':Decimal("1.00"),
'ss':Decimal("4.00"),
'vf':Decimal("1.00"),
},
'mr': {
'ah':Decimal("999.00"),
'aw':Decimal("999.00"),
'bb':Decimal("2.00"),
'dl':Decimal("1.00"),
'gny':Decimal("4.00"),
'gs':Decimal("-1.00"),
'hn':Decimal("2.00"),
'la':Decimal("4.00"),
'lor':Decimal("2.00"),
'ma':Decimal("2.00"),
'md':Decimal("999.00"),
'mi':Decimal("999.00"),
'sa':Decimal("1.00"),
'sc':Decimal("999.00"),
'sha':Decimal("1.00"),
'ss':Decimal("3.00"),
'vf':Decimal("999.00"),
},
'as': {
'ah':Decimal("999.00"),
'aw':Decimal("999.00"),
'bb':Decimal("1.00"),
'dl':Decimal("-1.00"),
'gny':Decimal("4.00"),
'gs':Decimal("999.00"),
'hn':Decimal("999.00"),
'la':Decimal("2.00"),
'lor':Decimal("3.00"),
'ma':Decimal("999.00"),
'md':Decimal("1.00"),
'mi':Decimal("-1.00"),
'sa':Decimal("999.00"),
'sc':Decimal("999.00"),
'sha':Decimal("-1.00"),
'ss':Decimal("3.00"),
'vf':Decimal("999.00"),
},
'dr': {
'ah':Decimal("999.00"),
'aw':Decimal("999.00"),
'bb':Decimal("2.00"),
'dl':Decimal("1.00"),
'gny':Decimal("3.00"),
'gs':Decimal("1.00"),
'hn':Decimal("999.00"),
'la':Decimal("2.00"),
'lor':Decimal("4.00"),
'ma':Decimal("3.00"),
'md':Decimal("-1.00"),
'mi':Decimal("999.00"),
'sa':Decimal("999.00"),
'sc':Decimal("999.00"),
'sha':Decimal("2.00"),
'ss':Decimal("3.00"),
'vf':Decimal("999.00"),
},
'vt': {
'ah':Decimal("999.00"),
'aw':Decimal("999.00"),
'bb':Decimal("1.00"),
'dl':Decimal("-1.00"),
'gny':Decimal("3.00"),
'gs':Decimal("999.00"),
'hn':Decimal("1.00"),
'la':Decimal("3.00"),
'lor':Decimal("2.00"),
'ma':Decimal("3.00"),
'md':Decimal("999.00"),
'mi':Decimal("1.00"),
'sa':Decimal("999.00"),
'sc':Decimal("999.00"),
'sha':Decimal("999.00"),
'ss':Decimal("3.00"),
'vf':Decimal("999.00"),
},
'cs': {
'ah':Decimal("1.00"),
'aw':Decimal("2.00"),
'bb':Decimal("3.00"),
'dl':Decimal("-1.00"),
'gny':Decimal("2.00"),
'gs':Decimal("1.00"),
'hn':Decimal("2.00"),
'la':Decimal("2.00"),
'lor':Decimal("3.00"),
'ma':Decimal("2.00"),
'md':Decimal("999.00"),
'mi':Decimal("-1.00"),
'sa':Decimal("2.00"),
'sc':Decimal("-1.00"),
'sha':Decimal("2.00"),
'ss':Decimal("2.00"),
'vf':Decimal("999.00"),
},
'jh': {
'ah':Decimal("1.00"),
'aw':Decimal("999.00"),
'bb':Decimal("2.00"),
'dl':Decimal("1.00"),
'gny':Decimal("3.00"),
'gs':Decimal("999.00"),
'hn':Decimal("2.00"),
'la':Decimal("3.00"),
'lor':Decimal("3.00"),
'ma':Decimal("3.00"),
'md':Decimal("999.00"),
'mi':Decimal("1.00"),
'sa':Decimal("2.00"),
'sc':Decimal("999.00"),
'sha':Decimal("-1.00"),
'ss':Decimal("3.00"),
'vf':Decimal("1.00"),
},
'rr': {
'ah':Decimal("1.00"),
'aw':Decimal("1.00"),
'bb':Decimal("3.00"),
'dl':Decimal("1.00"),
'gny':Decimal("3.00"),
'gs':Decimal("-1.00"),
'hn':Decimal("2.00"),
'la':Decimal("3.00"),
'lor':Decimal("2.00"),
'ma':Decimal("2.00"),
'md':Decimal("-1.00"),
'mi':Decimal("-1.00"),
'sa':Decimal("999.00"),
'sc':Decimal("1.00"),
'sha':Decimal("1.00"),
'ss':Decimal("1.00"),
'vf':Decimal("1.00"),
},
'ap': {
'ah':Decimal("999.00"),
'aw':Decimal("-1.00"),
'bb':Decimal("2.00"),
'dl':Decimal("-1.00"),
'gny':Decimal("2.00"),
'gs':Decimal("1.00"),
'hn':Decimal("3.00"),
'la':Decimal("3.00"),
'lor':Decimal("2.00"),
'ma':Decimal("999.00"),
'md':Decimal("1.00"),
'mi':Decimal("999.00"),
'sa':Decimal("999.00"),
'sc':Decimal("1.00"),
'sha':Decimal("2.00"),
'ss':Decimal("3.00"),
'vf':Decimal("999.00"),
},
'mk': {
'ah':Decimal("2.00"),
'aw':Decimal("1.00"),
'bb':Decimal("3.00"),
'dl':Decimal("999.00"),
'gny':Decimal("2.00"),
'gs':Decimal("999.00"),
'hn':Decimal("3.00"),
'la':Decimal("3.00"),
'lor':Decimal("1.00"),
'ma':Decimal("3.00"),
'md':Decimal("-1.00"),
'mi':Decimal("999.00"),
'sa':Decimal("3.00"),
'sc':Decimal("1.00"),
'sha':Decimal("1.00"),
'ss':Decimal("3.00"),
'vf':Decimal("999.00"),
},
'cf': {
'ah':Decimal("999.00"),
'aw':Decimal("1.00"),
'bb':Decimal("2.00"),
'dl':Decimal("-1.00"),
'gny':Decimal("2.00"),
'gs':Decimal("-1.00"),
'hn':Decimal("3.00"),
'la':Decimal("3.00"),
'lor':Decimal("3.00"),
'ma':Decimal("999.00"),
'md':Decimal("-1.00"),
'mi':Decimal("999.00"),
'sa':Decimal("999.00"),
'sc':Decimal("1.00"),
'sha':Decimal("1.00"),
'ss':Decimal("3.00"),
'vf':Decimal("999.00"),
},
}

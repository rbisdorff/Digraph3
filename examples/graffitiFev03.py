#!/usr/bin/python
# -*- coding: utf-8 -*-
# Source: Graffiti magazine février 2003
# Digraph3 exercise
# (C) R. BISDORFF 2021 
#####################################
# ---------------------------------------
# Movie Critics
#
# jt, Jhemp Thilges, Revue, Télé-Revue, Graffiti, Nico, Le Quotidien
# td, Thibaut Demeyer, Woxx, La Voix du Luxembourg
# cn, Claude Neu, RTL Radio Lëtzebuerg
# mr, Martine Reuter, Tageblatt, RSC 100.7
# as, Alaisn stevenart, La Meuse
# dr, Duncan Roberts, Luxembourg News
# vt, Vivian Thill, Le Jeudi
# cs, Christian Spielmann, Journal
# jh, Joy Hoffmann, Zinemag
# rr, Raoúl Reis, Correio, Radio Ara, Radio Amizade
# ap, Albert Petesch, Luxemburger Wort, Télécran
# mk, Mark Kripple, Luxemburger Wort, Télécran
# cf, Claude François, Luxembburger Wort, Télécran
##############################
from decimal import Decimal
from collections import OrderedDict

#####################
# No decision objectives in this case
objectives = OrderedDict()

############################
# The movie critics 
criteria = OrderedDict([
('jt', {
'comment': 
'weight':1.0,'scale':[-2.0, 5.0],
'thresholds' :{'ind': (0.0, 0.0), 'pref': (0.5, 0.0)}}),
('td', {
'weight':1.0,'scale':[-2.0, 5.0],
'thresholds' :{'ind': (0.0, 0.0), 'pref': (0.5, 0.0)}}),
('cn', {
'weight':1.0,'scale':[-2.0, 5.0],
'thresholds' :{'ind': (0.0, 0.0), 'pref': (0.5, 0.0)}}),
('mr', {
'weight':1.0,'scale':[-2.0, 5.0],
'thresholds' :{'ind': (0.0, 0.0), 'pref': (0.5, 0.0)}}),
('as', {
'weight':1.0,'scale':[-2.0, 5.0],
'thresholds' :{'ind': (0.0, 0.0), 'pref': (0.5, 0.0)}}),
('dr', {
'weight':1.0,'scale':[-2.0, 5.0],
'thresholds' :{'ind': (0.0, 0.0), 'pref': (0.5, 0.0)}}),
('vt', {
'weight':2.0,'scale':[-2.0, 5.0],
'thresholds' :{'ind': (0.0, 0.0), 'pref': (0.5, 0.0)}}),
('cs', {
'weight':1.0,'scale':[-2.0, 5.0],
'thresholds' :{'ind': (0.0, 0.0), 'pref': (0.5, 0.0)}}),
('jh', {
'weight':2.0,'scale':[-2.0, 5.0],
'thresholds' :{'ind': (0.0, 0.0), 'pref': (0.5, 0.0)}}),
('rr', {
'weight':1.0,'scale':[-2.0, 5.0],
'thresholds' :{'ind': (0.0, 0.0), 'pref': (0.5, 0.0)}}),
('ap', {
'weight':1.0,'scale':[-2.0, 5.0],
'thresholds' :{'ind': (0.0, 0.0), 'pref': (0.5, 0.0)}}),
('mk', {
'weight':1.0,'scale':[-2.0, 5.0],
'thresholds' :{'ind': (0.0, 0.0), 'pref': (0.5, 0.0)}}),
('cf', {
'weight':1.0,'scale':[-2.0, 5.0],
'thresholds' :{'ind': (0.0, 0.0), 'pref': (0.5, 0.0)}}),
])

####################################
# Movies
actions = OrderedDict([
('ah', {'name': "Ah si j'étais riche"}),
('aw', {'name': "A walk to remember"}),
('bb', {'name': "Bend it like Beckham"}),
('dl', {'name': "Demonlover"}),
('gny', {'name': "Gangs of New York"}),
('gs', {'name': "Ghost Ship"}),
('hn', {'name': "El Hija de la Novia"}),
('la', {'name': "Lantana"}),
('lor', {'name': "Lord of the Rings - The Two Towers"}),
('ma', {'name': "The Magdalene Sisters"}),
('md', {'name': "Mr. Deeds"}),
('mi', {'name': "Mon Idole"}),
('sa', {'name': "the Slaton Sea"}),
('sc', {'name': "the santa Clause 2"}),
('sha', {'name': "Sweet home Alabama"}),
('ss', {'name': "Sweet Sixteen"}),
('vf', {'name': "24 heures de la vie d'une femme"}),
])

#################
# the critic's opinions
# -2 (00, I hate), -1 (0, don't like), 1 (*, maybe),
# 2 (**, good), 3 (***, excellent), 4 (****, not to be missed)
# 5 (*****, a master piece), 999 (NA: Not seen) 
NA = 999
evaluation = {
'jt': 
{'ah': 1, 'aw': -1, 'bb': 2, 'dl': 1, 'gny': 4, 'gs': 1, 'hn': 2, 'la': 3, 'lor': 4,
 'ma': 3, 'md': 1, 'mi': 2, 'sa': 1, 'sc': 1, 'sha': 2, 'ss': 3, 'vf': 1},

'td': 
{'ah': 3, 'aw': 999, 'bb': 1, 'dl': 1, 'gny': 2, 'gs': -1, 'hn': 999, 'la': 999,
 'lor': 2, 'ma': 3, 'md': 1, 'mi': 2, 'sa': 999, 'sc': 999, 'sha': 999, 'ss': 3, 'vf': 1},

'cn': 
{'ah': -1, 'aw': 999, 'bb': 2, 'dl': 999, 'gny': 4, 'gs': 999, 'hn': 2, 'la': 3,
 'lor': 999, 'ma': 3, 'md': 999, 'mi': 1, 'sa': 999, 'sc': 999, 'sha': 1, 'ss': 4, 'vf': 1},

'mr': 
{'ah': 999, 'aw': 999, 'bb': 2, 'dl': 1, 'gny': 4, 'gs': -1, 'hn': 2, 'la': 4,
 'lor': 2, 'ma': 2, 'md': 999, 'mi': 999, 'sa': 1, 'sc': 999, 'sha': 1, 'ss': 3, 'vf': 999},

'as': 
{'ah': 999, 'aw': 999, 'bb': 1, 'dl': -1, 'gny': 4, 'gs': 999, 'hn': 999, 'la': 2,
 'lor': 3, 'ma': 999, 'md': 1, 'mi': -1, 'sa': 999, 'sc': 999, 'sha': -1, 'ss': 3, 'vf': 999},

'dr': 
{'ah': 999, 'aw': 999, 'bb': 2, 'dl': 1, 'gny': 3, 'gs': 1, 'hn': 999, 'la': 2,
 'lor': 4, 'ma': 3, 'md': -1, 'mi': 999, 'sa': 999, 'sc': 999, 'sha': 2, 'ss': 3, 'vf': 999},

'vt': 
{'ah': 999, 'aw': 999, 'bb': 1, 'dl': -1, 'gny': 3, 'gs': 999, 'hn': 1, 'la': 3,
 'lor': 2, 'ma': 3, 'md': 999, 'mi': 1, 'sa': 999, 'sc': 999, 'sha': 999, 'ss': 3, 'vf': 999},

'jh': 
{'ah': 1, 'aw': 999, 'bb': 2, 'dl': 1, 'gny': 3, 'gs': 999, 'hn': 2, 'la': 3,
 'lor': 3, 'ma': 3, 'md': 999, 'mi': 1, 'sa': 2, 'sc': 999, 'sha': -1, 'ss': 3, 'vf': 1},

'cs': 
{'ah' : 1, 'aw': 2, 'bb': 3,   'dl': -1, 'gny': 2, 'gs': 1, 'hn': 2, 'la': 2,
 'lor': 3, 'ma': 2, 'md': 999, 'mi': -1, 'sa': 2, 'sc': -1, 'sha': 2, 'ss': 2, 'vf': 999},

'rr': 
{'ah': 1, 'aw': 1, 'bb': 3, 'dl': 1, 'gny': 3, 'gs': -1, 'hn': 2, 'la': 3,
 'lor': 2, 'ma': 2, 'md': -1, 'mi': -1, 'sa': 999, 'sc': 1, 'sha': 1, 'ss': 1, 'vf': 1},

'ap': 
{'ah': 999, 'aw': -1, 'bb': 2, 'dl': -1, 'gny': 2, 'gs': 1, 'hn': 3, 'la': 3,
 'lor': 2, 'ma': 999, 'md': 1, 'mi': 999, 'sa': 999, 'sc': 1, 'sha': 2, 'ss': 3, 'vf': 999},

'mk': 
{'ah': 2, 'aw': 1, 'bb': 3, 'dl': 999, 'gny': 2, 'gs': 999, 'hn': 3, 'la': 3,
 'lor': 1, 'ma': 3, 'md': -1, 'mi': 999, 'sa': 3, 'sc': 1, 'sha': 1, 'ss': 3, 'vf': 999},

'cf': 
{'ah': 999, 'aw': 1, 'bb': 2, 'dl': -1, 'gny': 2, 'gs': -1, 'hn': 3, 'la': 3,
 'lor': 3, 'ma': 999, 'md': -1, 'mi': 999, 'sa': 999, 'sc': 1, 'sha': 1, 'ss': 3, 'vf': 999},

}
	




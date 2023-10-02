#!/usr/bin/python
# socialChoice33.py
# Taylor Alan D., Social Choice and the Mathematics of Manipulation, CUP, 2005 
# RB July 2005
# ---------------------------------------
# 
#
# each voter represents a criteria
criteria = ['v_1', 'v_2', 'v_3','v_4','v_5','v_6','v_7']

# no thresholds 
threshold = {
    'v_1' : { 'ind':(0.0, 0.0),'pref':(1.0,0.0), 'veto':(5.0, 0.0)},
    'v_2' : { 'ind':(0.0, 0.0),'pref':(1.0,0.0), 'veto':(5.0, 0.0)},
    'v_3' : { 'ind':(0.0, 0.0),'pref':(1.0,0.0), 'veto':(5.0, 0.0)},
    'v_4' : { 'ind':(0.0, 0.0),'pref':(1.0,0.0), 'veto':(5.0, 0.0)},
    'v_5' : { 'ind':(0.0, 0.0),'pref':(1.0,0.0), 'veto':(5.0, 0.0)},
    'v_6' : { 'ind':(0.0, 0.0),'pref':(1.0,0.0), 'veto':(5.0, 0.0)},
    'v_7' : { 'ind':(0.0, 0.0),'pref':(1.0,0.0), 'veto':(5.0, 0.0)},
}

# all voters are equi-significant
weightorder = [['v_1', 'v_2', 'v_3','v_4','v_5','v_6','v_7']]
weightset = {'v_1':1.0, 'v_2':1.0, 'v_3':1.0,'v_4':1.0,'v_5':1.0,'v_6':1.0,'v_7':1.0}

# five candidates
actionset = ['a', 'b', 'c', 'd', 'e']

# individual voting profiles expressed as numerical rank orders
evaluation = {
'v_1': 
{ 'a':5.0, 'b':4.0, 'c':3.0, 'd':2.0, 'e':1.0 },
'v_2': 
{ 'a':5.0, 'b':3.0, 'c':1.0, 'd':4.0, 'e':2.0 },
'v_3': 
{ 'a':5.0, 'b':3.0, 'c':1.0, 'd':4.0, 'e':2.0 },
'v_4': 
{ 'a':1.0, 'b':4.0, 'c':5.0, 'd':3.0, 'e':2.0 },
'v_5': 
{ 'a':2.0, 'b':3.0, 'c':5.0, 'd':4.0, 'e':1.0 },
'v_6': 
{ 'a':2.0, 'b':5.0, 'c':4.0, 'd':3.0, 'e':1.0 },
'v_7': 
{ 'a':1.0, 'b':2.0, 'c':4.0, 'd':3.0, 'e':5.0 },
}

# Roubens 215
criteria = ['speed','volume','price','cons']
actionset= ['vwgc','r9gtl','gsax','p305','tahg','audi','r18gtl','alfa']
#weightorder=[ ['speed','volume'],['price','cons']]
weightorder=[['price'], ['cons'],['volume'],['speed']]
#weightset = {'speed': 2.0, 'volume': 2.0, 'price': 3.0, 'cons': 3.0}
weightset = {'speed': 4.0, 'volume': 3.0, 'price': 1.0, 'cons': 2.0}
threshold = {
'speed': { 'ind':(5.0, 0.0),    'pref':(0.0, 0.10),  'veto':(10.0, 0.1)},
'volume': {'ind':(0.0, 0.05),   'pref':(0.0, 0.10),  'veto':(0.4, 0.1)},
'price': { 'ind':(500.0, -0.02), 'pref':(1000, -0.10), 'veto':(2000.0,-0.15)},
'cons':  { 'ind':(0.1, -0.05),   'pref':(0.10, -0.10), 'veto':(0.2,-0.15)}
}
evaluation = {
'speed': {'vwgc':140.0,'r9gtl':150.0,'gsax':160.0,'p305': 153.0, 'tahg':164.0,'audi':148.0,'r18gtl':155.0,'alfa':170.0},
'volume' : {'vwgc':6.13,'r9gtl':6.70,'gsax':6.63,'p305': 6.91, 'tahg':6.65,'audi':7.36,'r18gtl':7.40,'alfa':6.19},
'price' : {'vwgc':-41360.0,'r9gtl':-45700.0,'gsax':-46450.0,'p305': -48200.0, 'tahg': -48800.0,'audi':-50830.0,'r18gtl':-51700.0,'alfa':-52500.0},
'cons' : {'vwgc':-7.8,'r9gtl':-7.5,'gsax':-8.2,'p305': -8.4, 'tahg': -8.5,'audi':-7.0,'r18gtl':-8.1,'alfa':-7.8},
}

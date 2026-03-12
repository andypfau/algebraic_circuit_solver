"""
S-parameters of a RLC low-pass filter
"""



import sys
sys.path.insert(0, '.'); sys.path.insert(0, '..')

from lib import Circuit, V, R, L, C, Constants
import math
import numpy as np
from sympy import Symbol, Eq, lambdify
import plotly.graph_objects as go



# RLC low-pass filter
s, z0 = Constants.laplace_s(), Symbol('Z_0')
filter = Circuit()
filter.add(V(1, 0, v=Symbol('V_01'), rs=z0, refdes='V01'))
filter.add(R(1, 3, r=Symbol('R')))
filter.add(L(3, 2, l=Symbol('L'), s=s))
filter.add(C(2, 0, c=Symbol('C'), s=s))
filter.add(V(2, 0, v=Symbol('V_02'), rs=z0, refdes='V02'))


# solve
solution = filter.solution()
print('Solution:', solution)



# substitute concrete values, calculate S-parameters
assert len(solution) == 1
SUBS = {'R':10, 'L':1e-9, 'C':3e-12, 'Z_0':50}
SUBS_P1 = {'V_01':1, 'V_02':0}  # enable source at port 1, to calculate S_i,1
SUBS_P2 = {'V_01':0, 'V_02':1}  # enable source at port 2, to calculate S_i,2
v1 = solution[0][Symbol('V_1')]
i1 = -solution[0][Symbol('I_V01')]
v2 = solution[0][Symbol('V_2')]
i2 = -solution[0][Symbol('I_V02')]
s11 = ((v1 - z0*i1) / (v1 + z0*i1)).subs(SUBS|SUBS_P1)
s21 = ((v2 - z0*i2) / (v1 + z0*i1)).subs(SUBS|SUBS_P1)
s12 = ((v1 - z0*i1) / (v2 + z0*i2)).subs(SUBS|SUBS_P2)
s22 = ((v2 - z0*i2) / (v2 + z0*i2)).subs(SUBS|SUBS_P2)
print('S11:', s11)
print('S21:', s21)
print('S12:', s12)
print('S22:', s22)


# get S-parameters
s11_fn = lambdify(s, s11)
s21_fn = lambdify(s, s21)
s12_fn = lambdify(s, s12)
s22_fn = lambdify(s, s22)
f_range = np.geomspace(1e6, 100e9, 301)
s_range = 1j*math.tau*f_range
v2db = lambda v: 20*np.log10(np.maximum(1e-15, abs(v)))

fig = go.Figure()
fig.add_trace(go.Scatter(x=f_range/1e9, y=v2db(s11_fn(s_range)), name='S11'))
fig.add_trace(go.Scatter(x=f_range/1e9, y=v2db(s21_fn(s_range)), name='S21'))
fig.add_trace(go.Scatter(x=f_range/1e9, y=v2db(s12_fn(s_range)), name='S12'))
fig.add_trace(go.Scatter(x=f_range/1e9, y=v2db(s22_fn(s_range)), name='S22'))
fig.update_layout(title='S-Parameters', xaxis_type='log', width=800, height=500, xaxis_title='f / GHz', yaxis_title='B')
fig.show()

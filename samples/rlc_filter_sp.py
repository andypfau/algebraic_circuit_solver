"""
S-parameters of a RLC low-pass filter
"""

# TODO



import sys
sys.path.insert(0, '.'); sys.path.insert(0, '..')

from lib import Circuit, V, R, L, C, Constants
import math
import numpy as np
from sympy import Symbol, Eq, lambdify, fraction, solve
import plotly.graph_objects as go



# RLC low-pass filter
s = Constants.laplace_s()
z0 = 50
filter = Circuit()
filter.add(V(1, 0, v=1, rs=z0))
filter.add(R(1, 2, r=Symbol('R')))
filter.add(L(2, 3, l=Symbol('L'), s=s))
filter.add(C(3, 0, c=Symbol('C'), s=s))
filter.add(R(3, 0, r=z0))


# solve
solution = filter.solution()
print('Solution:')
print(solution)


# substitute concrete values, calculate S-parameters
# note that we can only calcualte S_i1, because there is only a source at port 1
assert len(solution) == 1
SUBS = {'R':1, 'L':1e-9, 'C':3e-12}
v1 = solution[0][Symbol('V_1')].subs(SUBS)
i1 = solution[0][Symbol('I_R1')].subs(SUBS)
v2 = solution[0][Symbol('V_3')].subs(SUBS)
i2 = -solution[0][Symbol('I_R2')].subs(SUBS)
s11 = (v1 - z0*i1) / (v1 + z0*i1)
s21 = (v2 - z0*i2) / (v1 + z0*i1)
print('S11:', s11)
print('S21:', s21)


# get S-parameters
s11_fn = lambdify(s, s11)
s21_fn = lambdify(s, s21)
f_range = np.geomspace(1e6, 100e9, 301)
v2db = lambda v: 20*np.log10(np.maximum(1e-15, abs(v)))

fig = go.Figure()
fig.add_trace(go.Scatter(x=f_range/1e9, y=v2db(s11_fn(1j*math.tau*f_range)), name='S11'))
fig.add_trace(go.Scatter(x=f_range/1e9, y=v2db(s21_fn(1j*math.tau*f_range)), name='S21'))
fig.update_layout(title='S-Parameters', xaxis_type='log', width=800, height=500, xaxis_title='f / GHz', yaxis_title='B')
fig.show()

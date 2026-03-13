"""
DC transfer function of a diode

The circuit consists of a voltage source, a resistor, and a diode.
The script calculates the diode current vs. source voltage, and plots it.
"""



import sys
sys.path.insert(0, '.'); sys.path.insert(0, '..')

from lib import Circuit, V, R, D, Constants
import math
import numpy as np
from sympy import Symbol, Eq, lambdify
import plotly.graph_objects as go



# diode with resistor
filter = Circuit()
filter.add(V(1, 0, v=Symbol('V_0')))
filter.add(R(1, 2, r=Symbol('R')))
filter.add(D(2, 0, i_sat=Symbol('I_Sat'), n=Symbol('n'), temp_k=Symbol('Temp')))


# solve
print('Solving', filter.equations(), '...')
solution = filter.solution()
print('Solution:')
print(solution)


# substitute concrete values, and create a numeric function
assert len(solution) == 1
substitutions = {'I_Sat':1e-14, 'n':1, 'Temp':273.15+27, 'R':1 } | Constants.substitutions()
tf = solution[0][Symbol('I_D1')].subs(substitutions)
print('Transfer Function:', tf)


# plot transfer function
# this requires the scipy package, otherwise lambdify fails to resolve the LambertW function
tf_fn = lambdify(Symbol('V_0'), tf)
vf_range = np.linspace(-0.1, +0.8, 101)
if_range = np.real(tf_fn(vf_range))

fig = go.Figure()
fig.add_trace(go.Scatter(x=vf_range, y=if_range/1e-3))
fig.update_layout(title='Transfer Function', width=800, height=500, xaxis_title='VF / V', yaxis_title='IF / mA')
fig.show()

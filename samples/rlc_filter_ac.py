"""
AC transfer function and poles/zeros of a RLC low-pass filter

The circuit consists of a voltage source, a resistor, an inductor, and a capacitor.
  Those form a low-pass filter.
The script calculates the filter's transfer function, plots it, then calculates
  the filter's poles and zeros, and plots those as well.
"""



import sys
sys.path.insert(0, '.'); sys.path.insert(0, '..')

from lib import Circuit, V, R, L, C, Constants
import math
import numpy as np
from sympy import Symbol, Eq, lambdify, fraction, solve
import plotly.graph_objects as go



# RLC low-pass filter
s = Constants.laplace_s()
filter = Circuit()
filter.add(V(1, 0, v=1))
filter.add(R(1, 2, r=Symbol('R')))
filter.add(L(2, 3, l=Symbol('L'), s=s))
filter.add(C(3, 0, c=Symbol('C'), s=s))


# solve
solution = filter.solution()
print('Solution:')
print(solution)


# substitute concrete values, calculate transfer function
assert len(solution) == 1
SUBS = {'R':10, 'L':1e-9, 'C':10e-12}
tf = solution[0][Symbol('V_3')].subs(SUBS)
print('Transfer Function:', tf)


# plot transfer function
tf_fn = lambdify(s, tf)
f_range = np.geomspace(1e6, 10e9, 301)
v2db = lambda v: 20*np.log10(np.maximum(1e-15, abs(v)))

fig = go.Figure()
fig.add_trace(go.Scatter(x=f_range/1e9, y=v2db(tf_fn(1j*math.tau*f_range))))
fig.update_layout(title='Transfer Function', xaxis_type='log', width=800, height=500, xaxis_title='f / GHz', yaxis_title='TF / dB')
fig.show()


# determine poles and zeros, and plot them
num,den = fraction(tf)
print(num, den)
zeros = solve(Eq(num,0), s, dict=True, set=False)
poles = solve(Eq(den,0), s, dict=True, set=False)
poles_f = np.array([complex(e[s]) for e in poles])
zeros_f = np.array([complex(e[s]) for e in zeros])
print(poles_f, zeros_f)
extent = max([abs(e) for e in [*poles_f,*zeros_f]]) * 1.1

fig = go.Figure()
fig.add_trace(go.Scatter(x=np.real(poles_f), y=np.imag(poles_f), mode='markers', line=dict(color='red'), marker=dict(symbol='cross')))
fig.add_trace(go.Scatter(x=np.real(zeros_f), y=np.imag(zeros_f), mode='markers', line=dict(color='green'), marker=dict(symbol='circle-open')))
fig.update_layout(title='Poles and Zeros', xaxis_range=(-extent,+extent), yaxis_range=(-extent,+extent), width=500, height=500)
fig.show()

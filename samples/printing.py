"""
AC transfer function of a RLC low-pass filter, printed in various formats.
"""


import sys
sys.path.insert(0, '.'); sys.path.insert(0, '..')

from lib import Circuit, V, R, L, C, Constants
import math
from sympy import Symbol, Eq, lambdify, fraction, solve, printing
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
tf = solution[0][Symbol('V_3')]


# print in various formats
print('Plain:')
print(tf)
print()
print('Pretty-Print:')
print(printing.pretty(tf))
print()
print('MathML:')
print(printing.mathml(tf))
print()
print('LaTeX:')
print(printing.latex(tf))
print()
print('Python:')
print(printing.pycode(tf))
print()
print('C:')
print(printing.ccode(tf))
print()
print('C++:')
print(printing.cxxcode(tf))
print()
print('Java Script:')
print(printing.jscode(tf))
print()
print('Maple:')
print(printing.maple_code(tf))
print()
print('Mathematica:')
print(printing.mathematica_code(tf))
print()
print('Octave:')
print(printing.octave_code(tf))

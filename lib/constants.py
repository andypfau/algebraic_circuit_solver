from .types import ComplexType, ScalarType
from sympy import Expr, Symbol



class Constants:


    @staticmethod
    def substitutions() -> dict[Expr,Expr]:
        CONSTANTS = {
            'k_B': 1.380649e-23,
            'q_0': 1.602176634e-19,
        }
        return {Symbol(name):value for name,value in CONSTANTS.items()}


    @staticmethod
    def elementary_charge() -> ScalarType:
        return Symbol('q_0')


    @staticmethod
    def boltzmann() -> ScalarType:
        return Symbol('k_B')


    @staticmethod
    def laplace_s() -> ComplexType:
        return Symbol('s', complex=True)

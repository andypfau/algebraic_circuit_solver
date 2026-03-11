from __future__ import annotations

from .types import ComplexType, ScalarType, NodeType, RefdesType
from .refdes import RefdesDatabase
from .constants import Constants
from .component_base import Component, Component2Terminal

import re
import math
from sympy import Symbol, Expr, Eq, oo, exp, ln
from abc import ABC
from typing import Iterable



class V(Component2Terminal):


    def __init__(self, node1: NodeType, node2: NodeType, v: ComplexType, rs: ComplexType = 0, refdes: RefdesType|None = None):
        super().__init__(node1=node1, node2=node2, refdes_prefix='V', refdes=refdes)
        self.v, self.rs = v, rs


    def _get_voltage(self, i: ComplexType) -> ComplexType:
        return self.v - self.rs * i
    

    def __repr__(self):
        return f'V(refdes={self.refdes},v={self.v},rs={self.rs})'
        


class I(Component2Terminal):


    def __init__(self, node1: NodeType, node2: NodeType, i: ComplexType, rp: ComplexType = oo, refdes: RefdesType|None = None):
        super().__init__(node1=node1, node2=node2, refdes_prefix='I', refdes=refdes)
        self.i, self.rp = i, rp


    def _get_current(self, v: ComplexType) -> ComplexType:
        return self.i + v / self.rp
    

    def __repr__(self):
        return f'I(refdes={self.refdes},i={self.v},rp={self.rp})'
        


class R(Component2Terminal):


    def __init__(self, node1: NodeType, node2: NodeType, r: ScalarType, refdes: RefdesType|None = None):
        super().__init__(node1=node1, node2=node2, refdes_prefix='R', refdes=refdes)
        self.r = r

        
    def _get_voltage(self, i: ComplexType) -> ComplexType:
        return self.r * i
    

    def __repr__(self):
        return f'R(refdes={self.refdes},r={self.r})'



class L(Component2Terminal):


    def __init__(self, node1: NodeType, node2: NodeType, l: ScalarType, s: ComplexType = None, refdes: RefdesType|None = None):
        super().__init__(node1=node1, node2=node2, refdes_prefix='L', refdes=refdes)
        self.l, self.s = l, s or Constants.laplace_s()

        
    def _get_voltage(self, i: ComplexType) -> ComplexType:
        z = self.s * self.l
        return z * i
    

    def __repr__(self):
        return f'C(refdes={self.refdes},c={self.r},s={self.s})'



class C(Component2Terminal):


    def __init__(self, node1: NodeType, node2: NodeType, c: ScalarType, s: ComplexType = None, refdes: RefdesType|None = None):
        super().__init__(node1=node1, node2=node2, refdes_prefix='C', refdes=refdes)
        self.c, self.s = c, s or Constants.laplace_s()

        
    def _get_voltage(self, i: ComplexType) -> ComplexType:
        z = 1 / (self.s * self.c)
        return z * i
    

    def __repr__(self):
        return f'C(refdes={self.refdes},c={self.r},s={self.s})'
        


class D(Component2Terminal):


    def __init__(self, node1: NodeType, node2: NodeType, i_sat: ScalarType, n: ScalarType = 1, temp_k: ScalarType = None, refdes: RefdesType|None = None):
        super().__init__(node1=node1, node2=node2, refdes_prefix='D', refdes=refdes)
        self.i_sat, self.n, self.temp_k = i_sat, n, temp_k


    def _get_voltage(self, i: ComplexType) -> ComplexType:
        v_th = Constants.boltzmann() * self.temp_k / Constants.elementary_charge()
        return self.n * v_th * ln(i / self.i_sat + 1)


    # def _get_current(self, v: ComplexType) -> ComplexType:
    #     v_th = Constants.boltzmann() * self.temp_k / Constants.elementary_charge()
    #     return self.i_sat * (exp(v / (self.n * v_th)) - 1)
    

    def __repr__(self):
        return f'D(refdes={self.refdes})'  # TODO



class MOSFET(Component):


    def __init__(self, source_node: NodeType, gate_node: NodeType, drain_node: NodeType, k: ScalarType, w: ScalarType, h: ScalarType, v_th: ScalarType, refdes: RefdesType|None = None):
        super().__init__((source_node,gate_node,drain_node), refdes_prefix='M', refdes=refdes)
        self.k, self.w, self.h, self.v_th = k, w, h, v_th

        
    def _get_equation(self, node_voltages: dict[NodeType,ComplexType], component_currents: dict[tuple[RefdesType,int],ComplexType]) -> list[Eq]:
        (vs, vg, vd) = self._get_my_terminals(node_voltages)
        i_s = component_currents[(self.refdes,0)]
        ig = component_currents[(self.refdes,1)]
        id = component_currents[(self.refdes,2)]

        raise NotImplementedError()
        
        return [Eq()]
    

    def __repr__(self):
        return f'M(refdes={self.refdes})'  # TODO

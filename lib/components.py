from __future__ import annotations

from .trivial import ComplexType, ScalarType, NodeType, RefdesType

import re
import math
from sympy import Symbol, Expr, Eq
from abc import ABC
from typing import Iterable



class Component:


    _all_refdes: set[RefdesType] = set()


    def __init__(self, n_terminals: int, refdes_prefix: str, refdes: RefdesType|None = None):
        self._n_terminals = n_terminals
        self._refdes = self._make_refdes(refdes_prefix=refdes_prefix, refdes=refdes)


    def _make_refdes(self, refdes_prefix: str, refdes: str|None = None) -> str:
        
        if refdes is None:
            i = 1
            while True:
                refdes = f'{refdes_prefix}{i}'
                if refdes not in Component._all_refdes:
                    break
                i += 1
        
        if not re.match(r'[a-zA-Z]+[0-9]*', refdes):
            raise ValueError(f'Invalid refdes "{refdes}"')
        if refdes in Component._all_refdes:
            raise ValueError(f'Duplicate refdes "{refdes}"')
        
        Component._all_refdes.add(refdes)
        
        return refdes


    @property
    def refdes(self) -> str:
        return self._refdes


    def _get_equation(self, nodes: list[NodeType], node_voltages: dict[NodeType,ComplexType], component_currents: dict[tuple[RefdesType,int]|ComplexType]) -> list[Eq]:
        raise NotImplementedError()


    def _get_my_terminals(self, nodes: list[NodeType], node_voltages: dict[NodeType,ComplexType]) -> Iterable[ComplexType]:
        assert len(nodes) == self._n_terminals
        return [node_voltages[node] for node in nodes]
    


class Component2Terminal(Component):


    def __init__(self, refdes_prefix: str, refdes: RefdesType|None):
        super().__init__(n_terminals=2, refdes_prefix=refdes_prefix)


    def _get_equation(self, nodes: list[NodeType], node_voltages: dict[NodeType,ComplexType], component_currents: dict[tuple[RefdesType,int],ComplexType]) -> list[Eq]:
        (v0, v1) = self._get_my_terminals(nodes, node_voltages)
        i = component_currents[(self.refdes,0)]
        return [Eq(v1-v0, self._get_voltage(i))]


    def _get_my_terminals(self, nodes: list[NodeType], node_voltages: dict[NodeType,ComplexType]) -> Iterable[ComplexType]:
        assert len(nodes) == self._n_terminals
        return [node_voltages[node] for node in nodes]


    def _get_voltage(self, current: ComplexType) -> ComplexType:
        raise NotImplementedError()



class V(Component2Terminal):


    def __init__(self, v: ComplexType, rs: ComplexType, refdes: RefdesType|None = None):
        super().__init__(refdes_prefix='V', refdes=refdes)
        self.v, self.rs = v, rs


    def _get_voltage(self, i: ComplexType) -> ComplexType:
        return self.v - self.rs * i
        


class R(Component2Terminal):


    def __init__(self, r: ScalarType, refdes: RefdesType|None = None):
        super().__init__(refdes_prefix='R', refdes=refdes)
        self.r = r

        
    def _get_voltage(self, i: ComplexType) -> ComplexType:
        return self.r * i

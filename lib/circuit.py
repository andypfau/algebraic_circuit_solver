from __future__ import annotations

from .types import ComplexType, ScalarType, NodeType, RefdesType
from .components import Component
from .refdes import RefdesDatabase

import re
import math
from sympy import Symbol, Expr, Eq, solve
from abc import ABC
from typing import Iterable, overload



class Circuit:


    def __init__(self, ref_node: NodeType = 0):
        self.ref_node = ref_node
        self._components: list[Component] = []
        self._refdes_db = RefdesDatabase()
    

    def add(self, component: Component):
        component._connect_to_refdes_db(self._refdes_db)
        self._components.append(component)


    def equations(self) -> tuple[list[Eq],list[Expr]]:
        node_voltages = self._create_node_voltages_dict()
        all_voltage_symbols = set([v for v in node_voltages.values() if v!=0])
        component_currents = self._create_component_currents_dict()
        all_component_currents = set([i for i in component_currents.values() if isinstance(i,Symbol)])
        node_current_equations = self._generate_node_current_equations(node_voltages, component_currents)
        component_equations = self._generate_component_equations(node_voltages, component_currents)
        all_equations = list([*node_current_equations, *component_equations])
        all_unknowns = list([*all_voltage_symbols, *all_component_currents])
        return all_equations, all_unknowns


    def solution(self) -> list[dict[Symbol,Expr]]:
        equations, unknowns = self.equations()
        return solve(equations, unknowns, dict=True, set=False)


    def _create_node_voltages_dict(self) -> dict[NodeType,ComplexType]:
        
        # set of all nodes in the circuit
        nodes_set = set()
        for component in self._components:
            for node in component.terminals:
                nodes_set.add(node)
        nodes = sorted(list(nodes_set))

        # find the reference node
        ref_node: NodeType = None
        for node in nodes:
            if node == self.ref_node:
                ref_node = node
                break
        if ref_node is None:
            raise RuntimeError(f'Reference node "{self.ref_node}" not found')

        # define a voltage symbol for each node
        result = dict()
        i = 1
        for node in nodes:
            if node == self.ref_node:
                result[node] = 0
            else:
                result[node] = Symbol(f'V_{node}')
                i += 1
        return result
    

    def _create_component_currents_dict(self) -> dict[tuple[RefdesType,int],ComplexType]:
        result = dict()

        for comp in self._components:
            if len(comp.terminals) == 2:
                i = Symbol(f'I_{comp.refdes}')
                result[(comp.refdes,0)] = i
                result[(comp.refdes,1)] = -i
            else:
                for i in range(len(comp.terminals)):
                    result[(comp.refdes,i)] = Symbol(f'I_{comp.refdes}_{i+1}')
        return result
    

    def _generate_node_current_equations(self, node_voltages: dict[NodeType,ComplexType], component_currents: dict[tuple[RefdesType,int],ComplexType]) -> list[Eq]:
        result = []
        for equation_node in node_voltages.keys():
            lhs = 0
            if equation_node == 0:
                continue  # no equation for the reference node
            for component in self._components:
                for i_terminal,component_node in enumerate(component.terminals):
                    if component_node != equation_node:
                        continue
                    terminal_current = component_currents[(component.refdes,i_terminal)]
                    lhs += terminal_current
            result.append(Eq(lhs, 0))
        return result


    def _generate_component_equations(self, node_voltages: dict[NodeType,ComplexType], component_currents: dict[tuple[RefdesType,int],ComplexType]) -> list[Eq]:
        result = []
        for component in self._components:
            eqs = component._get_equation(node_voltages=node_voltages, component_currents=component_currents)
            result.extend(eqs)
        return result

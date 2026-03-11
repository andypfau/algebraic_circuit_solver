from __future__ import annotations

from .types import ComplexType, ScalarType, NodeType, RefdesType
from .refdes import RefdesDatabase

from sympy import Eq, Symbol
from typing import Iterable



class Component:


    def __init__(self, terminals: Iterable[NodeType], refdes_prefix: str, refdes: RefdesType|None = None):
        self._nodes = tuple(terminals)
        self._refdes_prefix = refdes_prefix
        self._refdes = refdes
        self._refdes_db: RefdesDatabase|None = None
    

    def __repr__(self):
        return f'Componente(refdes={self.refdes})'


    def _connect_to_refdes_db(self, db: RefdesDatabase):
        self._refdes_db = db
    
    def _ensure_refdes(self):
        if self._refdes is not None:
            return
        if self._refdes_db is None:
            raise RuntimeError('No refdes database connected')
        if self._refdes is None:
            self._refdes = self._refdes_db.get_new_refdes(self._refdes_prefix)
        else:
            self._refdes_db.register_redes(self._refdes)


    @property
    def refdes(self) -> str:
        self._ensure_refdes()
        assert self._refdes is not None
        return self._refdes


    @property
    def nodes(self) -> list[NodeType]:
        return tuple(self._nodes)


    def _get_equation(self, node_voltages: dict[NodeType,ComplexType], component_currents: dict[tuple[RefdesType,int]|ComplexType]) -> list[Eq]:
        raise NotImplementedError()


    def _get_my_terminals(self, node_voltages: dict[NodeType,ComplexType]) -> Iterable[ComplexType]:
        return [node_voltages[node] for node in self._nodes]
    


class Component2Terminal(Component):


    def __init__(self, node1: NodeType, node2: NodeType, refdes_prefix: str, refdes: RefdesType|None):
        super().__init__((node1, node2), refdes_prefix=refdes_prefix, refdes=refdes)


    def _get_equation(self, node_voltages: dict[NodeType,ComplexType], component_currents: dict[tuple[RefdesType,int],ComplexType]) -> list[Eq]:
        (v1, v0) = self._get_my_terminals(node_voltages)
        i = component_currents[(self.refdes,0)]
        
        v_comp = self._get_voltage(i)
        if v_comp is not NotImplemented:
            return [Eq(v1-v0, v_comp)]

        i_comp = self._get_current(v1-v0)
        if i_comp is not NotImplemented:
            i_node = component_currents[(self.refdes,0)]
            return [Eq(i_node, i_comp)]

        raise NotImplementedError()


    def _get_my_terminals(self, node_voltages: dict[NodeType,ComplexType]) -> Iterable[ComplexType]:
        assert len(self._nodes) == 2
        return (node_voltages[self._nodes[0]], node_voltages[self._nodes[1]])


    def _get_voltage(self, current: ComplexType) -> ComplexType:
        return NotImplemented


    def _get_current(self, voltage: ComplexType) -> ComplexType:
        return NotImplemented

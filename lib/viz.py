from __future__ import annotations
from .circuit import Circuit, NodeType, RefdesType
from graphviz import Digraph


NODE_ATTRS=dict(
    shape='circle',
    style='filled,solid',
    fillcolor='Gainsboro',
    pencolor='Black',
    fontsize='11.0',
    fontcolor='DeepPink',
)
REF_NODE_ATTRS=dict(
    shape='rectangle',
    style='filled,solid,rounded',
    fillcolor='Gainsboro',
    pencolor='Black',
    fontsize='11.0',
    fontcolor='DeepPink',
)
COMPONENT_ATTRS=dict(
    shape='rectangle',
    style='filled',
    fillcolor='Snow',
    pencolor='Black',
    fontsize='14.0',
    fontcolor='DarkBlue',
)
BRANCH_ATTRS=dict(
    color='Black',
    fontsize='9.0',
    fontcolor='DodgerBlue',
)


class CircuitViz:

    def __init__(self, circuit: Circuit):
        self._circuit = circuit

    
    def draw(self, graph: Digraph):

        def graph_node_name(node: NodeType) -> str:
            return f'N{node}'
        def graph_component_name(refdes: RefdesType) -> str:
            return f'C{refdes}'
        
        # draw all circuit nodes
        node_dict = self._circuit._create_node_voltages_dict()
        for node_name in node_dict.keys():
            is_ref_node = node_name == self._circuit.ref_node
            graph.attr('node', **(REF_NODE_ATTRS if is_ref_node else NODE_ATTRS))
            graph.node(graph_node_name(node_name), label=str(node_name))

        # draw all circuit components and wires
        for comp in self._circuit._components:
            graph.attr('node', **COMPONENT_ATTRS)
            graph.node(graph_component_name(comp.refdes), label=str(comp.refdes))
            for i,terminal in enumerate(comp.terminals):
                is_last_terminal = i == (len(comp.terminals) - 1)
                graph.attr('edge', **BRANCH_ATTRS)
                graph.attr('edge', dict(arrowsize = '0.0' if is_last_terminal else ''))
                graph.edge(graph_node_name(terminal), graph_component_name(comp.refdes), headlabel=str(i))

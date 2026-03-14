from __future__ import annotations
from .circuit import Circuit, NodeType, RefdesType
from graphviz import Digraph



class CircuitVizStyle:

    def __init__(self):

        self.node_attrs = dict(
            shape='circle',
            style='filled,solid',
            fillcolor='Gainsboro',
            pencolor='Black',
            fontsize='11.0',
            fontcolor='DeepPink',
        )

        self.ref_node_attrs = dict(
            shape='rectangle',
            style='filled',
            fillcolor='Snow',
            pencolor='Black',
            fontsize='14.0',
            fontcolor='DarkBlue',
        )

        self.branch_attrs = dict(
            color='Black',
            fontsize='9.0',
            fontcolor='DodgerBlue',
        )

        self.component_attrs = dict(
            shape='rectangle',
            style='filled,solid,rounded',
            fillcolor='Gainsboro',
            pencolor='Black',
            fontsize='11.0',
            fontcolor='DeepPink',
        )



class CircuitViz:

    def __init__(self, circuit: Circuit, style: CircuitVizStyle = None):
        self._circuit = circuit
        self._style = style or CircuitVizStyle()

    
    def render(self, graph: Digraph = None) -> Digraph:

        if graph is None:
            graph = Digraph()

        def graph_node_name(node: NodeType) -> str:
            return f'N{node}'
        def graph_component_name(refdes: RefdesType) -> str:
            return f'C{refdes}'
        
        # draw all circuit nodes
        node_dict = self._circuit._create_node_voltages_dict()
        for node_name in node_dict.keys():
            is_ref_node = node_name == self._circuit.ref_node
            graph.attr('node', **(self._style.ref_node_attrs if is_ref_node else self._style.node_attrs))
            graph.node(graph_node_name(node_name), label=str(node_name))

        # draw all circuit components and wires
        for comp in self._circuit._components:
            graph.attr('node', **self._style.component_attrs)
            graph.node(graph_component_name(comp.refdes), label=str(comp.refdes))
            for i,terminal in enumerate(comp.terminals):
                is_last_terminal = i == (len(comp.terminals) - 1)
                graph.attr('edge', **self._style.branch_attrs)
                graph.attr('edge', dict(arrowsize = '0.0' if is_last_terminal else ''))
                graph.edge(graph_node_name(terminal), graph_component_name(comp.refdes), headlabel=str(i))
        
        return graph

My Spice
========

A circuit simulator in Python, simply for the joy of programming it, as an educational project.

## Basic Concept

- Represent a circuit as a graph. Each node is a wire, and each edge is a circuit element, e.g. a source or a passive.
- Create equations based on Kirchhoff's current law.
- Solve the equation system using `sympy`.


## Conventions

- Each node's current flows from the node into the component.
- Each node of the component, except the last one, gets its own current.
    - For a 2-terminal device, on the 1st node, the current is I_REFDES, and on the 2nd node, it is -I_REFDES.
    - For a 3-terminal device, the currents are names I_REFDES_1, I_REFDES_2, etc., and the current into the last node is -(I_REFDES_1+I_REFDES_2+...).
- The voltage is always referenced to the last node.
    - For a 2-terminal device, the voltage is from the 1st node to the 2nd node.

Examples:
- V(1,0,5): 5 V source, positive terminal on node 1, negative terminal on node 0.
- R(1,0,10): 10 Ω resistor, voltage and current arrows both go from node 1 to node 0.


## Missing

- Parse Spice netlist
- Create Spice netlist
- Create graph

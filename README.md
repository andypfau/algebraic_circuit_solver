Algebraic Circuit Solver
========================

A circuit solver which returns sympy expressions.


## Idea and Scope

There are many circuit simulators out there. But they are all numeric, and I sometimes am interested in the transfer function as an algebraic expression.

Another motivation for this project was the curiosity of writing my own circuit solver. In the past I failed to do this with Kirchhoff's voltage law, so this time I used Kirchhoff's current law, which easily works for nonplanar networks.

This project is not intended to be a competition to a full circuit simulator. It is not intended to provide a full set of simulators (so far it can do DC/OP, AC and S-parameters). It is not intended to have its own schematic editor. It is not intended to provide field simulations.


## Basic Concept

- Represent a circuit as a graph. Each node is a wire, and each edge is a circuit element, e.g. a source or a passive.
- Create equations based on Kirchhoff's current law.
- Solve the equation system using `sympy`.


## Library Overview

- `lib/`: the Python package itself.
    - `Component`: circuit components, e.g. `V`, `I`, `R`, `L`, `C`.
    - `Circuit`: captures the schematic.
    - `Constants`: convenience functions for typially used constants.
- `samples/`: sample code.
- `pipenv/`: environment for [Pipenv](https://pipenv.pypa.io/).
- `test/`: testcases for [unittest](https://docs.python.org/3/library/unittest.html).


## Requirements

Use the environment in `pipenv/` with [Pipenv](https://pipenv.pypa.io/):
```bash
cd pipenv
python -m pipenv source
```


## Details

### Flow

- You enter the schematic, by calling `Circuit.add()`.
- You ask the circuit for the equations, by calling `Circuit.equations()`.
    - Reference designators, if missing, are automatically generated.
    - For each node voltage, a Sympy symbol is created, named `"V_NODENAME"`, except for the reference node (which by default is `0`).
    - Each n-terminal component gets n-1 currents assigned, name `"I_REFDES"`. E.g. a resistor `"R1"` gets the current `"I_R1"`.
    - For each node, an equation based on Kirchhoff's current law is generated.
    - Each component is asked to generate its own specific equations.
    - All equations, and all unknwons (node voltages, component currents) are returned.
- You may now solve the equation system, e.g. with `sympy.solve()`.

### Conventions

- Node names: may be any integer or string, but must be a valid name prefix in Sympy.
    - E.g. `1` or `"N1"`.
- Reference designators:
    - Must be unique.
    - Must consist of one or more letters, plus some optional digits.
        - E.g. `"V1"`.
- Each node's current flows from the node into the component.
- Currents:
    - Each terminal of the component, except the last one, gets its own current.
        - E.g. a 2-terminal device, the 1st node gets a current, the 2nd node gets the negative of that same current.
        - E.g. a 3-terminal device, the 1st and 2nd terminal get their own currents, the 3rd terminal gets the negative sum of those currents.
    - Currents flow *from* the conencting node *into* the component's terminal.
        - This means that e.g. if you want to inject a current of 1 mA into a node, you must reverse the current source, because the current flows away from the node.
- Voltage arrows go from the node to the reference node.

Examples of component definitions:
- `V(1,0,5)`: a 5 V source, positive terminal on node 1 (`"V_1"`), negative terminal on node 0 (reference node).
- `R(2,1,10)`: a 10 Ω resistor, voltage and current arrows both go from node 2 (`"V_2"`) to node 1 (`"V_1"`). If $V_2-V_1>0$, then $I_{R1}>0$.


## Missing Features

- Spice netlist import/export
- Create graph

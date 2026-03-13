import sys
sys.path.insert(0, '.'); sys.path.insert(0, '..')

from lib import Circuit, R, L, C, V, I
from sympy import Symbol
import unittest



class TestCircuits(unittest.TestCase):


    def test_trivial(self):
        circ = Circuit()
        circ.add(V(1, 0, v=5))
        circ.add(R(1, 0, r=1e3))
        sol = circ.solution()
        self.assertEqual(len(sol), 1)
        self.assertAlmostEqual(sol[0][Symbol('V_1')], 5)
        self.assertAlmostEqual(sol[0][Symbol('I_V1')], -5/1e3)
        self.assertAlmostEqual(sol[0][Symbol('I_R1')], 5/1e3)


    def test_trivial_vsrcres(self):
        circ = Circuit()
        circ.add(V(1, 0, v=5, rs=1e3))
        circ.add(R(1, 0, r=1e3))
        sol = circ.solution()
        self.assertEqual(len(sol), 1)
        self.assertAlmostEqual(sol[0][Symbol('V_1')], 5/2)
        self.assertAlmostEqual(sol[0][Symbol('I_V1')], -5/2e3)
        self.assertAlmostEqual(sol[0][Symbol('I_R1')], 5/2e3)


    def test_trivial_isrcres(self):
        circ = Circuit()
        circ.add(I(1, 0, i=-10e-3, rp=1e3))
        circ.add(R(1, 0, r=1e3))
        sol = circ.solution()
        self.assertEqual(len(sol), 1)
        self.assertAlmostEqual(sol[0][Symbol('V_1')], 10e-3*(1e3/2))
        self.assertAlmostEqual(sol[0][Symbol('I_I1')], -10e-3/2)
        self.assertAlmostEqual(sol[0][Symbol('I_R1')], 10e-3/2)


    def test_voltage_divider(self):
        circ = Circuit()
        circ.add(V(1, 0, 5))
        circ.add(R(1, 2, 1e3))
        circ.add(R(2, 0, 3e3))
        sol = circ.solution()
        self.assertEqual(len(sol), 1)
        self.assertAlmostEqual(sol[0][Symbol('V_1')], 5)
        self.assertAlmostEqual(sol[0][Symbol('V_2')], 5*(3/4))
        self.assertAlmostEqual(sol[0][Symbol('I_V1')], -5/4e3)
        self.assertAlmostEqual(sol[0][Symbol('I_R1')], 5/4e3)
        self.assertAlmostEqual(sol[0][Symbol('I_R2')], 5/4e3)


    def test_nonplanar(self):
        circ = Circuit()
        # a nonplanar circuit, i.e. one which cannot be drawn in 2D without wires
        #   crossing, and which would be hard to solve with Kirhhoff's voltage law
        circ.add(V(1, 0,  10.0, refdes='V0' ))
        circ.add(R(1, 0, 100.0, refdes='R10'))
        circ.add(R(2, 0, 200.0, refdes='R20'))
        circ.add(R(2, 1, 210.0, refdes='R21'))
        circ.add(R(3, 0, 300.0, refdes='R30'))
        circ.add(R(3, 1, 310.0, refdes='R31'))
        circ.add(R(3, 2, 320.0, refdes='R32'))
        sol = circ.solution()
        self.assertEqual(len(sol), 1)
        # solution from LTspice simulation
        self.assertAlmostEqual(sol[0][Symbol('V_1'  )], + 10.000000e+0, delta=1e-6)
        self.assertAlmostEqual(sol[0][Symbol('V_2'  )], +  4.885173e+0, delta=1e-6)
        self.assertAlmostEqual(sol[0][Symbol('V_3'  )], +  4.907429e+0, delta=1e-6)
        self.assertAlmostEqual(sol[0][Symbol('I_V0' )], -140.783970e-3, delta=1e-6)
        self.assertAlmostEqual(sol[0][Symbol('I_R10')], +100.000000e-3, delta=1e-6)
        self.assertAlmostEqual(sol[0][Symbol('I_R20')], + 24.425866e-3, delta=1e-6)
        self.assertAlmostEqual(sol[0][Symbol('I_R21')], - 24.356317e-3, delta=1e-6)
        self.assertAlmostEqual(sol[0][Symbol('I_R30')], + 16.358098e-3, delta=1e-6)
        self.assertAlmostEqual(sol[0][Symbol('I_R31')], - 16.427647e-3, delta=1e-6)
        self.assertAlmostEqual(sol[0][Symbol('I_R32')], + 69.549737e-6, delta=1e-6)



class TestTypes(unittest.TestCase):


    def test_symbolic_values(self):
        circ = Circuit()
        circ.add(V(1, 0, Symbol('V_Src')))
        circ.add(R(1, 0, Symbol('R_1')))
        sol = circ.solution()
        self.assertEqual(len(sol), 1)
        sol0num = {k:v.subs({Symbol('V_Src'):5, Symbol('R_1'):1e3}) for k,v in sol[0].items()}
        self.assertAlmostEqual(sol0num[Symbol('V_1')], 5)
        self.assertAlmostEqual(sol0num[Symbol('I_R1')], 5/1e3)


    def test_float_values(self):
        circ = Circuit()
        circ.add(V(1, 0, 5))
        circ.add(R(1, 0, 1e3))
        sol = circ.solution()
        self.assertEqual(len(sol), 1)
        self.assertAlmostEqual(sol[0][Symbol('V_1')], 5)
        self.assertAlmostEqual(sol[0][Symbol('I_R1')], 5/1e3)
        


if __name__ == '__main__':
    unittest.main()

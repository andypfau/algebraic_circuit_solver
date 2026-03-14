import sys
sys.path.insert(0, '.'); sys.path.insert(0, '..')

from lib import Circuit, Constants, R, L, C, V, I
from sympy import Symbol, symbols, Expr, simplify
import unittest
from typing import override



class TestCaseSympy(unittest.TestCase):

    
    def assertExprEquals(self, ex1: Expr, ex2: Expr):
        """ Check if two Sympy expressions are equivalent """
        diff = simplify(ex1 - ex2)
        if diff != 0:
            self.fail(f'Expressions not equal: ({ex1}) - ({ex2}) = {diff} != 0')

    
    @override
    def assertAlmostEqual(self, first, second, places = None, msg = None, delta = 1e-6):
        """ same as base method, but with reasonable delta, to avoid false negatives due to rounding errors """
        return super().assertAlmostEqual(first, second, places, msg, delta)
    


class TestCircuits(TestCaseSympy):


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
        circ.add(R(2, 0, 2e3))
        sol = circ.solution()
        self.assertEqual(len(sol), 1)
        self.assertAlmostEqual(sol[0][Symbol('V_1')], 5)
        self.assertAlmostEqual(sol[0][Symbol('V_2')], 5*(2/3)),
        self.assertAlmostEqual(sol[0][Symbol('I_V1')], -5/3e3)
        self.assertAlmostEqual(sol[0][Symbol('I_R1')], 5/3e3)
        self.assertAlmostEqual(sol[0][Symbol('I_R2')], 5/3e3)


    def test_filter_symbolic(self):
        v0, l, c = symbols('V0 L1 C1')
        s = Constants.laplace_s()
        circ = Circuit()
        circ.add(V(1, 0, v0))
        circ.add(L(1, 2, l))
        circ.add(C(2, 0, c))
        sol = circ.solution()
        self.assertEqual(len(sol), 1)
        z_c, z_l = 1/(s*c), s*l
        self.assertExprEquals(sol[0][Symbol('V_1')], v0)
        self.assertExprEquals(sol[0][Symbol('V_2')], v0*z_c/(z_c+z_l))
        self.assertExprEquals(sol[0][Symbol('I_V1')], -v0/(z_l+z_c))
        self.assertExprEquals(sol[0][Symbol('I_L1')], v0/(z_l+z_c))
        self.assertExprEquals(sol[0][Symbol('I_C1')], v0/(z_l+z_c))


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
        self.assertAlmostEqual(sol[0][Symbol('V_1'  )], + 10.000000e+0)
        self.assertAlmostEqual(sol[0][Symbol('V_2'  )], +  4.885173e+0)
        self.assertAlmostEqual(sol[0][Symbol('V_3'  )], +  4.907429e+0)
        self.assertAlmostEqual(sol[0][Symbol('I_V0' )], -140.783970e-3)
        self.assertAlmostEqual(sol[0][Symbol('I_R10')], +100.000000e-3)
        self.assertAlmostEqual(sol[0][Symbol('I_R20')], + 24.425866e-3)
        self.assertAlmostEqual(sol[0][Symbol('I_R21')], - 24.356317e-3)
        self.assertAlmostEqual(sol[0][Symbol('I_R30')], + 16.358098e-3)
        self.assertAlmostEqual(sol[0][Symbol('I_R31')], - 16.427647e-3)
        self.assertAlmostEqual(sol[0][Symbol('I_R32')], + 69.549737e-6)



class TestValueTypes(unittest.TestCase):


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



class TestRefes(unittest.TestCase):


    def test_invalid_refdes(self):
        circ = Circuit()
        with self.assertRaises(ValueError):
            circ.add(V(1, 0, v=10, refdes='123'))


    def test_duplicate_refdes(self):
        circ = Circuit()
        circ.add(R(1, 0, r=10, refdes='R1'))
        with self.assertRaises(ValueError):
            circ.add(R(1, 0, r=10, refdes='R1'))



class TestMiscBehavior(unittest.TestCase):


    def test_invlid_refnode(self):
        circ = Circuit()
        circ.add(R(1, 0, r=10, refdes='R1'))
        with self.assertRaises(RuntimeError):
            circ.equations(ref_node='Ref')
        


if __name__ == '__main__':
    unittest.main()

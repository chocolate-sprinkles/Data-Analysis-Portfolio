import unittest
import payroll_formulas as pf

class TestFormulas(unittest.TestCase):
    def test_cpp_contributions_tc1(self):
        self.assertEqual(round(pf.cpp_contributions(0,0.0595,3500,3754,52,1000),2),55.5)

if __name__ == "__main__":
    unittest.main()
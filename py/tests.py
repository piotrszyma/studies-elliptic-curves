import unittest
from algorithms import pollard_rho


class TestRhoPollard(unittest.TestCase):

    def test(self):
        params = pollard_rho.generate_params()
        g_prim, p, y = params.g_prim, params.p, params.y
        print(f"Running test for {params}")
        x_found = pollard_rho.PollardRhoDL(params).run()
        assert pow(g_prim, x_found, p) == y


if __name__ == '__main__':
    unittest.main()

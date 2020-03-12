import unittest
from algorithms import pollard_rho
from utils.primegen import random_safe_prime_library


class TestRhoPollard(unittest.TestCase):
    def test_primes_from_openssl(self):
        params = pollard_rho.generate_params()
        g_prim, p, y = params.g_prim, params.p, params.y
        print(f"Running test for {params}")
        x_found = pollard_rho.PollardRhoDL(params).run()
        assert pow(g_prim, x_found, p) == y

    def test_primes_from_library(self):
        params = pollard_rho.generate_params(
            primes_generating_function=random_safe_prime_library
        )
        g_prim, p, y = params.g_prim, params.p, params.y
        print(f"Running test for {params}")
        x_found = pollard_rho.PollardRhoDL(params).run()
        assert pow(g_prim, x_found, p) == y


if __name__ == "__main__":
    unittest.main()

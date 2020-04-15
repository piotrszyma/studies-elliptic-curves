import unittest

from algorithms import pollard_rho
from utils import primegen


class TestRhoPollard(unittest.TestCase):
    def test_prime_from_openssl(self):
        prime = primegen.random_safe_prime_from_openssl(40)
        params = pollard_rho.generate_params(prime)
        g_prim, p, y = params.g_prim, params.p, params.y

        x_found = pollard_rho.PollardRhoDL(params).run()

        assert pow(g_prim, x_found, p) == y, f"Failed for {params}"

    def test_prime_from_gensafeprime(self):
        prime = primegen.random_safe_prime_from_gensafeprime(40)
        params = pollard_rho.generate_params(prime)
        g_prim, p, y = params.g_prim, params.p, params.y

        x_found = pollard_rho.PollardRhoDL(params).run()

        assert pow(g_prim, x_found, p) == y, f"Failed for {params}"


if __name__ == "__main__":
    unittest.main()

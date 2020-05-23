import unittest

import utils

IntWithBinIndex = utils.IntWithBinIndex


class UtilsTests(unittest.TestCase):
    def test_int_with_bin_index(self):
        num = int('0b1010110111', base=2)

        wrapped = IntWithBinIndex(num)

        assert wrapped[0] == 1
        assert wrapped[1] == 1
        assert wrapped[2] == 1
        assert wrapped[3] == 0
        assert wrapped[4] == 1
        assert wrapped[5] == 1
        assert wrapped[6] == 0
        assert wrapped[7] == 1
        assert wrapped[8] == 0
        assert wrapped[9] == 1
        assert wrapped[10] == 0
        assert wrapped[100] == 0




if __name__ == "__main__":
    unittest.main()

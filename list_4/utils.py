
class IntWithBinIndex(int):
    def __getitem__(self, value):
        # try:
        #     val = int(bin(self)[2:][value])
        # except IndexError:
        #     val = 0

        return (self >> value) & 1

        # try:
        #     assert val == val2
        # except:
        #     import pdb; pdb.set_trace()
        #     raise
        # return val

    def __repr__(self):
        return f'{bin(self)} ({str(self)})'

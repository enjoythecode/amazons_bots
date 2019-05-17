from bitarray import bitarray
import bitboard_constants


class AmazonsState:
    def __init__(self, board_config):

        config = bitboard_constants.starting_configurations[board_config]

        self.occupancy_bitboard = config[0]
        self.white_bitboard = config[1]
        self.black_bitboard = config[2]
        self.fire_bitboard = config[3]

    def print_board(self):
        s = ""
        for i in range(100):
            if self.occupancy_bitboard[i]:
                if self.white_bitboard[i]:
                    s += 'W'
                elif self.black_bitboard[i]:
                    s += 'B'
                else:
                    s += 'X'
            else:
                s += "_"

        # reversing because our implementation holds the bits in reverse order
        print("\n".join([" ".join(s[i*10:(i+1)*10]) for i in range(10)][::-1]))


# test = AmazonsState('10_0')
# test.print_board()

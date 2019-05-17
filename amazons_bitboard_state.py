from bitarray import bitarray
import bitboard_constants


class AmazonsState:
    def __init__(self, board_size):

        self.occupancy_bitboard = bitboard_constants[board_size][0]
        self.white_bitboard = bitboard_constants[board_size][1]
        self.black_bitboard = bitboard_constants[board_size][2]
        self.fire_bitboard = bitboard_constants[board_size][3]

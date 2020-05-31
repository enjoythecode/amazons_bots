from itertools import combinations
import math
from random import randint
import copy

# to be used to generate block boards from actual game positions
# 0..99 horizontal
# 100..199 vertical
# 200..299 diagonal
# 300..399 anti-diagonal
block_masks = [None] * 400

# integers that are multiplied with block boards to find the correct index of the move boards. one for each square
# 0..99 horizontal
# 100..199 vertical
# 200..299 diagonal
# 300..399 anti-diagonal
magic_numbers = [None] * 400

# the amount of shifts required for the hashing for any particular square/direction combination. also determines size
magic_shifts = [None] * 400

# the resulting move boards. to be accessed using the magic number calculation only [direction + square][magic hash]
# 0..99 horizontal
# 100..199 vertical
# 200..299 diagonal
# 300..399 anti-diagonal
move_boards = [None] * 400

# arbitrary number of shifts, OK as long as it is consistent
HASH_SHIFTS = 30


def r(b):
    return "\n".join([" ".join(bin(b)[2:][::-1][i * 10:(i + 1) * 10]) for i in range(10)][::-1])


def magic_hash(bb, magic, shift):
    x = ((bb * magic) & ((2**shift - 1) << HASH_SHIFTS)) >> HASH_SHIFTS
    #if shift < 4:
    #    print(bb, bin(bb*magic),bin(x), magic, bb, shift)
    return x
# 0111001110000010100101101111001110111000000001111011000000000000

def moveboard_from_blockboard(bb, square, d):
    # not fully implemented yet!
    s_x = square % 10
    s_y = int((square - s_x) / 10)
    mb = 0
    if d == 0:  # horizontal
        mb = 0
        # check left
        for d_x in range(1, s_x+1):
            if bb & (1 << ((s_x - d_x) + s_y * 10)):  # obstacle!
                break
            mb += 2**((s_x - d_x) + s_y * 10)

        # check right
        for d_x in range(1, 10-s_x):
            if bb & (1 << ((s_x + d_x) + s_y * 10)):  # obstacle!
                break
            mb += 2**((s_x + d_x) + s_y * 10)

    if d == 1:  # vertical

        # check down
        for d_y in range(1, s_y+1):
            if bb & (1 << (s_x + (s_y - d_y) * 10)):  # obstacle!
                break
            mb += 2**(s_x + (s_y - d_y) * 10)

        # check up
        for d_y in range(1, 10-s_y):
            if bb & (1 << (s_x + (s_y + d_y) * 10)):  # obstacle!
                break
            mb += 2**(s_x + (s_y + d_y) * 10)

    if d == 2:  # diagonal

        # check SW
        for d in range(1, min(s_x, s_y)+1):
            if bb & (1 << (s_x - d + (s_y - d) * 10)):  # obstacle!
                break
            mb += 2**(s_x - d + (s_y - d) * 10)

        # check NE
        for d in range(1, 10-max(s_x, s_y)):
            if bb & (1 << (s_x + d + (s_y + d) * 10)):  # obstacle!
                break
            mb += 2**(s_x + d + (s_y + d) * 10)

    if d == 3:  # anti-diagonal

        # check SE
        for d in range(1, min(s_x, s_y) + 1):
            if bb & (1 << (s_x + d + (s_y - d) * 10)):  # obstacle!
                break
            mb += 2 ** (s_x + d + (s_y - d) * 10)

        # check NE
        for d in range(1, 10 - max(s_x, s_y)):
            if bb & (1 << (s_x - d + (s_y + d) * 10)):  # obstacle!
                break
            mb += 2 ** (s_x - d + (s_y + d) * 10)

    if mb != 0:
        return mb


def generate_block_masks():

    for square in range(100):  # for each square
        s_x = square % 10
        s_y = math.floor(square / 10)

        b = 0
        for x in range(10):
            if not x == s_x:
                b += 2 ** (s_y * 10 + x)
        block_masks[square] = b

        b = 0
        for y in range(10):
            if not y == s_y:
                b += 2 ** (y*10 + s_x)
        block_masks[100 + square] = b

        b = 0
        for x in range(10):
            for y in range(10):
                if not y == s_y and not x == s_x:
                    if x+y == s_x + s_y:
                        b += 2 ** (y*10 + x)
        block_masks[200 + square] = b

        b = 0
        for x in range(10):
            for y in range(10):
                if not y == s_y and not x == s_x:
                    if x - y == s_x - s_y:
                        b += 2 ** (y * 10 + x)
        block_masks[300 + square] = b


def generate_magic_numbers_and_move_boards():

    # generate their move_boards
    # brute-force a magic number
    # if satisfied, store the magic number and the move boards, discard the block boards

    for direction in range(4):

        for square in range(100):
            print(direction, square)
            # generate all possible block boards from a block mask

            temp_block_boards = []
            #  find indexes of 1s, get the combinations of those indexes and record them to temp_block_boards
            bit_indexes = []
            block_mask = block_masks[100*direction + square]
            i = 0
            while block_mask:
                if block_mask & 1:
                    bit_indexes.append(i)
                i += 1
                block_mask >>= 1

            bit_index_combinations = []
            for length in range(10):
                bit_index_combinations.extend(combinations(bit_indexes, length))

            for bit_index_combination in bit_index_combinations:
                new_block_board = 0
                for turn_on in bit_index_combination:
                    new_block_board += 2 ** (turn_on)
                temp_block_boards.append(new_block_board)

            # generate move_boards from these temp_block_boards

            temp_shift_bits = int(math.log(len(temp_block_boards), 2))
            repeat = True
            temp_magic = 0
            temp_move_boards = [None] * len(temp_block_boards)

            while repeat:  # keep searching until we find a good number that satisfies all constraints
                temp_magic = randint(2**randint(60,65), 2**randint(65, 70))
                temp_move_boards = [None] * len(temp_block_boards)
                repeat = False

                for temp_block_board in temp_block_boards:
                    temp_hash = magic_hash(temp_block_board, temp_magic, temp_shift_bits)

                    temp_move_board = moveboard_from_blockboard(temp_block_board, square, direction)

                    # if index is free, put the moveboard there
                    if temp_move_boards[temp_hash] is None:
                        temp_move_boards[temp_hash] = temp_move_board
                    else:
                        if temp_move_boards[temp_hash] == temp_move_board:
                            # temp_magic is NOT magic!
                            repeat = True
                            # print(temp_hash)
                            break

            # we are done! save the computed values
            magic_numbers[direction * 100 + square] = temp_magic
            magic_shifts[direction * 100 + square] = temp_shift_bits
            move_boards[direction * 100 + square] = copy.deepcopy(temp_move_boards)


if __name__ == "__main__":
    # Generating move boards and magic numbers
    print("a")
    generate_block_masks()
    print("b")
    generate_magic_numbers_and_move_boards()
    print("c")
    b = 2**6 + 2**30 + 2**39 + 2**60 + 2**69 + 2**93 + 2**96
    print(move_boards[3][magic_hash(b, magic_numbers[3], magic_shifts[3])] |
          move_boards[103][magic_hash(b, magic_numbers[103], magic_shifts[103])] |
          move_boards[203][magic_hash(b, magic_numbers[203], magic_shifts[203])] |
          move_boards[303][magic_hash(b, magic_numbers[303], magic_shifts[303])]
          )

    # Done generating move boards and magic numbers

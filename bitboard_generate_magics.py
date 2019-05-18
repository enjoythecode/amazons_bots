from bitarray import bitarray as ba
from itertools import combinations
import math
from random import randint

# to be used to generate block boards from actual game positions
# 0..99 horizontal
# 100..199 vertical
# 200..299 diagonal
# 300..399 anti-diagonal
block_masks = [0] * 400

# integers that are multiplied with block boards to find the correct index of the move boards. one for each square
# 0..99 horizontal
# 100..199 vertical
# 200..299 diagonal
# 300..399 anti-diagonal
magic_numbers = []

# the amount of shifts required for the hashing for any particular square/direction combination. also determines size
magic_shifts = []

# the resulting move boards. to be accessed using the magic number calculation only [direction + square][magic hash]
# 0..99 horizontal
# 100..199 vertical
# 200..299 diagonal
# 300..399 anti-diagonal
move_boards = []


def r(b):
    return "\n".join([" ".join(b[i * 10:(i + 1) * 10]) for i in range(10)][::-1])


def magic_hash(bb, magic, shift):
    return ba((int(bb.to01(), 2) * magic) >> shift)


def moveboard_from_blockboard(bb, d):
    raise NotImplemented("not the way this is supposed to be used")


def generate_block_masks():

    for square in range(100):  # for each square
        s_x = square % 10
        s_y = math.floor(square / 10)

        b = ba('0'*100)
        for x in range(10):
            if not x == s_x:
                b[s_y*10 + x] = True
        block_masks[square] = b

        b = ba('0'*100)
        for y in range(10):
            if not y == s_y:
                b[y*10 + s_x] = True
        block_masks[100 + square] = b

        b = ba('0'*100)
        for x in range(10):
            for y in range(10):
                if not y == s_y and not x == s_x:
                    if x+y == s_x + s_y:
                        b[y*10 + x] = True
        block_masks[200 + square] = b

        b = ba('0' * 100)
        for x in range(10):
            for y in range(10):
                if not y == s_y and not x == s_x:
                    if x - y == s_x - s_y:
                        b[y * 10 + x] = True
        block_masks[300 +square] = b


def generate_magic_numbers_and_move_boards():

    # generate their move_boards
    # brute-force a magic number
    # if satisfied, store the magic number and the move boards, discard the block boards

    for direction in range(4):

        for square in range(100):
            # generate all possible block boards from a block mask

            temp_block_boards = []
            #  find indexes of 1s, get the combinations of those indexes and record them to temp_block_boards
            bit_indexes = []
            block_mask_string = block_masks[100*direction + square].to01()
            for i in range(100):
                if block_mask_string[i] == '1':
                    bit_indexes.append(i)

            bit_index_combinations = []
            for length in range(10):
                bit_index_combinations.extend(combinations(bit_indexes, length))

            for bit_index_combination in bit_index_combinations:
                new_block_board = ba('0'*100)
                for turn_on in bit_index_combination:
                    new_block_board[turn_on] = True
                temp_block_boards.append(new_block_board)

            # generate move_boards from these temp_block_boards

            shift_bits = 100 - math.log(len(temp_block_boards), 2)
            repeat = True
            temp_magic = 0  # initialized in the loop

            while repeat:  # keep searching until we find a good number that satisfies all constraints
                temp_magic = randint(1000,1000000)
                temp_move_boards = [None] * len(temp_block_boards)
                repeat = False

                for temp_block_board in temp_block_boards:
                    h = magic_hash(temp_block_board, temp_magic, shift_bits)

                    # hash to find index
                    # if index is free, put the moveboard there
                    # if the index is not free AND (the moveboard at the index != current moveboard):
                    #  repeat = True; continue;


if __name__ == "__main__":
    generate_block_masks()
    generate_magic_numbers_and_move_boards()
    # generate block boards
    # get the indexes of all 1's in a block mask, iterate through all permutations using itertools
    # re-check how this stuff is supposed to be done
    # calculate magic numbers
    # store the magic numbers

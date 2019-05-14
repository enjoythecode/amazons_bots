starting_board_6x0=[
    [0,0,1,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,2],
    [2,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,1,0,0]
]

starting_board_4x0 = [
    [0,1,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,2,0]
]

import copy

def prettify_board_character(n):
    return ".WBX"[n]

class AmazonsState:
    """ A state of the game, i.e. the game board. These are the only functions which are
        absolutely necessary to implement UCT in any 2-player complete information deterministic 
        zero-sum game, although they can be enhanced and made quicker, for example by using a 
        GetRandomMove() function to generate a random move during rollout.
        By convention the players are numbered 1 and 2.
        Assumes square game board
    """
    def __init__(self, board, pjm = 2):
        self.playerJustMoved = pjm # At the root pretend the player just moved is player 2 - player 1 has the first move
        self.board = copy.deepcopy(board)
        self.game_size = len(board)

    def clone(self):
        """ Create a deep clone of this game state.
        """
        st = AmazonsState(copy.deepcopy(self.board), self.playerJustMoved)
        return st

    def make_move(self, move):
        """ Update a state by carrying out the given move.
            Must update playerJustMoved.
        """
        self.playerJustMoved = 3 - self.playerJustMoved
        self.board[int(move[0][0])][int(move[0][1])] = 0
        self.board[int(move[1][0])][int(move[1][1])] = self.playerJustMoved
        self.board[int(move[2][0])][int(move[2][1])] = 3
        
    
    def count_possible_moves(self, player = None):
        """ Get # of possible moves from this state.
        """
        out = 0
        if player is None:
            player = 3 - self.playerJustMoved

        queen_moves = self.get_possible_queen_moves(player)

        for q in queen_moves:
            out += self.count_possible_shots_from_queen(q[1],q[0])

        return out


    def get_possible_moves(self, player = None):
        """ Get all possible moves from this state.
        """
        out = []
        if player is None:
            player = 3 - self.playerJustMoved

        queen_moves = self.get_possible_queen_moves(player)
        for q in queen_moves:
            out.extend([ [q[0],q[1],s] for s in self.get_possible_shots_from_queen(q[1],q[0]) ])
        return out

    def get_possible_queen_moves(self, player = None):
        out = []
        if player is None:
            player = 3 - self.playerJustMoved
        for q_x in range(self.game_size):
            for q_y in range(self.game_size):
                if self.board[q_x][q_y] == player:
                    q = str(q_x)+str(q_y)
                    out.extend( [[q, x] for x in self.get_valid_moves(q)])

        return out

    def count_possible_queen_moves(self, player = None):
        if player is None:
            player = 3 - self.playerJustMoved
        out = 0

        for q_x in range(self.game_size):
            for q_y in range(self.game_size):
                if self.board[q_x][q_y] == player:
                    q = str(q_x)+str(q_y)
                    out += self.count_valid_moves(q)

        return out

    def get_possible_shots_from_queen(self, source, ignore):
        return self.get_valid_moves(source, ignore, True)

    def count_possible_shots_from_queen(self, source, ignore):
        return self.count_valid_moves(source, ignore, True)

    def get_valid_moves(self, cell_from, ignore = None, include_ignore = False):
        out = []
        from_x = int(cell_from[0])
        from_y = int(cell_from[1])
        ignore_x = int(ignore[0]) if not ignore is None else -1
        ignore_y = int(ignore[1]) if not ignore is None else -1

        x, y = from_x, from_y
        while x+1 < self.game_size:
            x += 1
            if self.board[x][y] != 0:
                if (ignore_x == x and ignore_y == y):
                    if include_ignore:
                        out.append(str(x) + str(y))
                    continue
                else:
                    break
            else:
                out.append(str(x) + str(y))

        x, y = from_x, from_y
        while x > 0:
            x -= 1
            if self.board[x][y] != 0:
                if (ignore_x == x and ignore_y == y):
                    if include_ignore:
                        out.append(str(x) + str(y))
                    continue
                else:
                    break
            else:
                out.append(str(x) + str(y))

        x, y = from_x, from_y
        while y+1 < self.game_size:
            y += 1
            if self.board[x][y] != 0:
                if (ignore_x == x and ignore_y == y):
                    if include_ignore:
                        out.append(str(x) + str(y))
                    continue
                else:
                    break
            else:
                out.append(str(x) + str(y))

        x, y = from_x, from_y
        while y > 0:
            y -= 1
            if self.board[x][y] != 0:
                if ignore_x == x and ignore_y == y:
                    if include_ignore:
                        out.append(str(x) + str(y))
                    continue
                else:
                    break
            else:
                out.append(str(x) + str(y))

        x, y = from_x, from_y
        while x+1 < self.game_size and y+1 < self.game_size:
            x += 1
            y += 1
            if self.board[x][y] != 0:
                if (ignore_x == x and ignore_y == y):
                    if include_ignore:
                        out.append(str(x) + str(y))
                    continue
                else:
                    break
            else:
                out.append(str(x) + str(y))

        x, y = from_x, from_y
        while x+1 < self.game_size and y > 0:
            x += 1
            y -= 1
            if self.board[x][y] != 0:
                if (ignore_x == x and ignore_y == y):
                    if include_ignore:
                        out.append(str(x) + str(y))
                    continue
                else:
                    break
            else:
                out.append(str(x) + str(y))

        x, y = from_x, from_y
        while x > 0 and y+1 < self.game_size:
            x -= 1
            y += 1
            if self.board[x][y] != 0:
                if (ignore_x == x and ignore_y == y):
                    if include_ignore:
                        out.append(str(x) + str(y))
                    continue
                else:
                    break
            else:
                out.append(str(x) + str(y))

        x, y = from_x, from_y
        while x > 0 and y > 0:
            x -= 1
            y -= 1
            if self.board[x][y] != 0:
                if (ignore_x == x and ignore_y == y):
                    if include_ignore:
                        out.append(str(x) + str(y))
                    continue
                else:
                    break
            else:
                out.append(str(x) + str(y))

        return out

    def count_valid_moves(self, cell_from, ignore = None, include_ignore = False):
        out = 0
        from_x = int(cell_from[0])
        from_y = int(cell_from[1])
        ignore_x = int(ignore[0]) if not ignore is None else -1
        ignore_y = int(ignore[1]) if not ignore is None else -1

        x, y = from_x, from_y
        while x+1 < self.game_size:
            x += 1
            if self.board[x][y] != 0:
                if (ignore_x == x and ignore_y == y):
                    if include_ignore:
                        out += 1
                    continue
                else:
                    break
            else:
                out += 1

        x, y = from_x, from_y
        while x > 0:
            x -= 1
            if self.board[x][y] != 0:
                if (ignore_x == x and ignore_y == y):
                    if include_ignore:
                        out += 1
                    continue
                else:
                    break
            else:
                out += 1

        x, y = from_x, from_y
        while y+1 < self.game_size:
            y += 1
            if self.board[x][y] != 0:
                if (ignore_x == x and ignore_y == y):
                    if include_ignore:
                        out += 1
                    continue
                else:
                    break
            else:
                out += 1

        x, y = from_x, from_y
        while y > 0:
            y -= 1
            if self.board[x][y] != 0:
                if (ignore_x == x and ignore_y == y):
                    if include_ignore:
                        out += 1
                    continue
                else:
                    break
            else:
                out += 1

        x, y = from_x, from_y
        while x+1 < self.game_size and y+1 < self.game_size:
            x += 1
            y += 1
            if self.board[x][y] != 0:
                if (ignore_x == x and ignore_y == y):
                    if include_ignore:
                        out += 1
                    continue
                else:
                    break
            else:
                out += 1

        x, y = from_x, from_y
        while x+1 < self.game_size and y > 0:
            x += 1
            y -= 1
            if self.board[x][y] != 0:
                if (ignore_x == x and ignore_y == y):
                    if include_ignore:
                        out += 1
                    continue
                else:
                    break
            else:
                out += 1

        x, y = from_x, from_y
        while x > 0 and y+1 < self.game_size:
            x -= 1
            y += 1
            if self.board[x][y] != 0:
                if (ignore_x == x and ignore_y == y):
                    if include_ignore:
                        out += 1
                    continue
                else:
                    break
            else:
                out += 1

        x, y = from_x, from_y
        while x > 0 and y > 0:
            x -= 1
            y -= 1
            if self.board[x][y] != 0:
                if (ignore_x == x and ignore_y == y):
                    if include_ignore:
                        out += 1
                    continue
                else:
                    break
            else:
                out += 1

        return out



    def is_game_going_on(self):
        return bool(self.count_possible_queen_moves())

    def check_game_end(self):
        p1 = self.count_possible_queen_moves(1)
        p2 = self.count_possible_queen_moves(2)
        if p1 == 0 and p2 == 0:
            return self.playerJustMoved # player who just moved wins
        elif p1 == 0:
            return 2 # player 2 won
        elif p2 == 0:
            return 1 # player 1 won
        else:
            return 0 # game going on


    def __repr__(self):
        """ Don't need this - but good style.
        """
        return "\n".join(
            [" ".join([prettify_board_character(c) for c in x]) for x in self.board]
            )
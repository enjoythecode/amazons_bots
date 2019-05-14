import base_amazons_state
import blocker_v1, human, blocker_v2, blocker_v3, blocker_v4, blocker_v5, blocker_v6, random_bot, mcts_v1
import time
import itertools


bots = [
        blocker_v1,
        mcts_v1,
        # human,
        blocker_v2,
        blocker_v3,
        blocker_v4,
        blocker_v5,
        blocker_v6,
        random_bot,
    ]
# [12, 21, 15, 15, 27, 12, 24] 6_0
# [9, 30 (n=2500), 21, 15, 36, 24, 24, 9] 6_0
points = [0] * len(bots)


class Game:
    game_size = -1
    game_config = -1
    player_count = 2
    current_move_count = 0

    def __init__(self, bot_1, bot_2, game_size=6, game_config=0):
        self.players = [bot_1, bot_2]
        
        self.out_file = open("matches/match" + str(time.time()).split(".")[0] + ".amazons", "w+")
        
        self.game_size = game_size
        self.game_config = game_config

        self.out_file.write(self.players[0].meta_name+"\n")
        self.out_file.write(self.players[1].meta_name+"\n")
        self.out_file.write(self.players[0].meta_description+"\n")
        self.out_file.write(self.players[1].meta_description+"\n")
        self.out_file.write(self.players[0].meta_developer+"\n")
        self.out_file.write(self.players[1].meta_developer+"\n")

        starting_board = None

        if game_size == 6 and game_config == 0:
            starting_board = base_amazons_state.starting_board_6x0
        elif game_size == 4 and game_config == 0:
            starting_board = base_amazons_state.starting_board_4x0

        self.base_state = base_amazons_state.AmazonsState(starting_board)
        
        self.players[0].greet()
        self.players[1].greet()

    def next_move(self):
        time_start = time.time()
        move = self.players[self.current_move_count % self.player_count].next_move(self.base_state)
        time_end = time.time()

        self.base_state.make_move(move)
        self.out_file.write(" ".join(move)+"\n")
        print(self.base_state)
        print("Move#" + str(self.current_move_count + 1) + ": P" + str(self.current_move_count % self.player_count + 1)
              + " played '" + " ".join(move) + "'in " + str(round(time_end-time_start, 3)))
        self.current_move_count += 1

    def play(self):
        while True:
            self.next_move()
            result = self.base_state.check_game_end()
            if result != 0:
                return result


for match_up in itertools.permutations(range(len(bots)), 2):
    g = Game(bots[match_up[0]].amazons_player(1, 2), bots[match_up[1]].amazons_player(2, 1), 6, 0)
    res = g.play()
    if res == 1:
        points[match_up[0]] += 3
    if res == 2:
        points[match_up[1]] += 3
    if res == 3:
        points[match_up[0]] += 1
        points[match_up[1]] += 1

print(points)

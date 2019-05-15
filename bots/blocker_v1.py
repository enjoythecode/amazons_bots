import base_amazons_player

class AmazonsPlayer(base_amazons_player.AmazonsPlayer):
    def __init__(self, friend, enemy):
        self.meta_developer = "enjoythecode"
        self.meta_name = "Blocking2Victory (B2V) v1"
        self.meta_description = "Maximises possible moves of itself. Looks 1 move ahead."
        self.meta_id = "BTV_0001"
        self.friend = friend
        self.enemy = enemy

    def next_move(self, state):
        max_val = -1000000
        max_move = None

        possible_moves = state.get_possible_moves()
        for move in possible_moves:
            possible_game = state.clone()
            possible_game.make_move(move)
            
            x = possible_game.count_possible_moves(self.friend)

            if x > max_val:
                max_val = x
                max_move = move

        return max_move 
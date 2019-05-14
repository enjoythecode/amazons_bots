import base_amazons_player

class amazons_player(base_amazons_player.amazons_player):
    def __init__(self, friend, enemy):
        self.meta_developer = "enjoythecode"
        self.meta_name = "Blocking2Victory (B2V) v2"
        self.meta_description = "Minimises possible moves of its enemy. Looks 1 move ahead."
        self.meta_id = "BTV_0002"
        self.friend = friend
        self.enemy = enemy

    def next_move(self, state):
        max_val = -1000000
        max_move = None

        possible_moves = state.get_possible_moves()
        for move in possible_moves:
            possible_game = state.clone()
            possible_game.make_move(move)
            
            x = -1 * possible_game.count_possible_moves(self.enemy)

            if x > max_val:
                max_val = x
                max_move = move

        return max_move 
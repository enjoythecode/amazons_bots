import base_amazons_player, random

class amazons_player(base_amazons_player.amazons_player):
    def __init__(self, friend, enemy):
        self.meta_developer = "enjoythecode"
        self.meta_name = "random bot"
        self.meta_description = "Plays randomly"
        self.friend = friend
        self.enemy = enemy

    def next_move(self, state):

        return random.choice(state.get_possible_moves())
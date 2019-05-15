class AmazonsPlayer:

    def __init__(self):
        self.meta_name = "Base minmax implementation to be extended by other bots"
        self.meta_developer = "Anonymous"
        self.meta_description = "Description goes here"

    def greet(self):
        print(self.meta_name + " by " + self.meta_developer + ". [" + self.meta_description + "]")

    def next_move(self, board_state):
        """
        Takes in a amazons_state and returns a move object ["AB","CD","EF"]
        """
        print("minmax not implemented yet!")
        return "!!"

    def utility(self):
        raise NotImplementedError("Utility functions not implemented by the child class!")
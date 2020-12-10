class Profile():

    def __init__(self, strategies, gains):

        self.strategies = strategies

        self.gains = gains

    def __repr__(self):

        return str(self.strategies) + " = " + str(self.gains) + "\n"

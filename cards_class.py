class Card:
    def __init__(self, rank, suit, visible=True, value=None):
        self.rank = rank
        self.suit = suit
        self.visible = visible
        self.value = value
        self.open = False

    def __str__(self):
        return f"{self.rank} of {self.suit} value: {self.value}"


if __name__ == "__main__":
    pass
    # value_by_game = {
    #     "blackjack": {"A": 11, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    #                   "J": 10, "Q": 10, "K": 10},
    #     "poker": {"A": 14, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11,
    #               "Q": 12, "K": 13},
    #     "valueless": {"A": None, "1": None, "2": None, "3": None, "4": 4, "5": None, "6": None, "7": None, "8": None,
    #                   "9": None, "10": None, "J": None, "Q": None, "K": None}
    # }

    # with open("card_values_by_game.json", "w") as file:
    #     json.dump(value_by_game, file, indent=1)

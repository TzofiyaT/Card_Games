import random
import json
from cards_class import *


class Deck:

    # constant class variable
    ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
    suits = ("♠", "♥", "♣", "♦")
    values = {}

    def __init__(self, game_name, shuffle=True):
        # self.init_deck()
        self.game_name = game_name
        self.values = dict(self.get_card_value_from_json())
        if not self.values:
            raise NameError(f"{self.game_name} is not a valid name")
        # list comprehension
        self.cards = [Card(rank, suit, value=self.values.get(rank)) for rank in self.ranks for suit in self.suits]
        if shuffle:
            self.shuffle_deck()
        self.pile = []

    def get_card_value_from_json(self):
        with open("card_values_by_game.json", "r") as files:
            values = json.load(files)
            # if self.game_name in values:
            game_value = values.get(self.game_name)
            return game_value

    def restart(self):
        self.cards = [Card(rank, suit, value=self.values.get(rank)) for rank in self.ranks for suit in self.suits]
        self.shuffle_deck()
        self.pile = []

    # def init_deck(self):
    #     for suit in self.suits:
    #         for rank in self.ranks:
    #             card = Card(rank, suit)
    #             self.cards.append(card)

    def shuffle_using_random(self):  # I will implement shuffle myself for practice
        random.shuffle(self.cards)

    def shuffle_deck(self):
        shuffle_list_of_cards = []
        while len(self.cards) > 0:
            card_index = random.randrange(0, len(self.cards))
            random_card = self.cards.pop(card_index)
            shuffle_list_of_cards.append(random_card)
        self.cards = shuffle_list_of_cards

    def deal(self):
        if self.cards:
            return self.cards.pop()
        return None

    def take_card_from_player_to_deal(self, card_to_add: Card):
        self.cards.insert(0, card_to_add)

    def open_card(self):
        return self.pile[len(self.pile)-1]


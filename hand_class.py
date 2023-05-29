from deck_class import *


class Hand:
    def __init__(self, name):
        self.name = name
        self.cards_hand = []
        self.score = 0

    def take_card(self, card: Card):
        self.cards_hand.append(card)

    def drop_card(self, index: int):
        index = int(index)
        if len(self.cards_hand) > index:
            return self.cards_hand.pop(index)
        else:
            raise ValueError(f"{index} not in range of 0 - {len(self.cards_hand)-1}")

    # def card_to_tell(self, number):
    #     self.card_said = number
        # self.card_said.append(number)
        # self.card_said.append(amount)

    def choosing_false(self, card, card_from_pile):
        if card_from_pile == card:
            return True
        return False

    def sum_score(self):
        total = 0
        try:
            for card in self.cards_hand:
                total += card.value
        except (TypeError, AttributeError):
            return None
        else:
            self.score = total



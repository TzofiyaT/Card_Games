from hand_class import *


class Game:
    def __init__(self):
        self.deck = Deck("true_or_false", True)
        self.players = []
        self.last_card = self.deck.cards[0]
        self.winner = None
        self.the_player = ""
        self.card_said = []

    def add_player(self, name):
        hand = Hand(name)
        self.players.append(hand)

    def names_of_cards(self, cards):
        cards_name = {"♠": "spades", "♥": "hearts", "♣": "clubs", "♦": "diamonds"}
        new_names = []
        for card in cards:
            new_names.append(f"static/images/{card.rank}_of_{cards_name[card.suit]}")
        return new_names

    def return_to_name(self, card):
        rank = card[14]
        cards_name = {"s": "♠", "h": "♥", "c": "♣", "d": "♦"}
        suit = cards_name[card[19]]
        value = self.deck.values.get(card[14])
        new_card = Card(rank, suit, value)
        return new_card

    def next_player(self):
        for p in range(len(self.players)):
            if p == len(self.players)-1:
                self.the_player = self.players[0]
                return self.the_player
            if self.players[p] == self.the_player:
                self.the_player = self.players[p+1]
                return self.the_player

    def start(self, num):
        self.dealing_cards(num)
        self.first_pile()
        self.the_player = self.players[0]

    def dealing_cards(self, num_cards):
        for player in self.players:
            for _ in range(num_cards):
                player.cards_hand.append(self.deck.deal())
        return True

    def first_pile(self):
        self.last_card = self.deck.cards.pop()
        self.card_said = self.last_card.rank
        self.last_card.open = True
        self.deck.pile.append(self.last_card)

    def check_deal(self):
        if self.deck.cards:
            return True
        return False

    def put_card_to_pile(self, player: Hand, index, index_tell):
        self.card_said = self.list_to_choose_the_card_to_say()[index_tell]
        self.last_card = player.drop_card(index)
        self.last_card.open = False
        self.deck.pile.append(self.last_card)

    def take_card_from_deal(self, player: Hand):
        card_to_take = self.deck.deal()
        if card_to_take:
            player.take_card(card_to_take)

    def pile_to_player(self, player: Hand):
        for c in self.deck.pile:
            player.cards_hand.append(c)
        self.deck.pile = []

    def say_false(self, last_player: Hand, said_player: Hand):
        if said_player.choosing_false(self.card_said, self.deck.open_card().rank):
            self.card_said = "2"
            self.pile_to_player(said_player)
            return True
        self.card_said = "2"
        self.pile_to_player(last_player)
        return False

    def list_to_choose_the_card_to_say(self):
        list_to_choose = []
        for key, value in self.deck.values.items():
            if int(self.deck.values[self.card_said]) <= int(value):
                list_to_choose.append(key)
        return list_to_choose

    def winn(self):
        for player in self.players:
            if not player.cards_hand:
                self.winner = player
        if self.winner:
            return True
        return False


if __name__ == "__main__":
    g = Game()
    g.dealing_cards(10)
    g.first_pile()
    g.return_to_name(['s', 't', 'a', 't', 'i', 'c', '/', 'i', 'm', 'a', 'g', 'e', 's', '/', 'A', '_', 'o', 'f', '_', 'd', 'i', 'a', 'm', 'o', 'n', 'd', 's'])
    # print(g.deck.cards)
    # print(g.last_card)
    # print(g.list_to_choose_the_card_to_say())
    # for i in g.players[0].cards_hand:
    #     print(i)
    # g.put_card_to_pile(g.players[0], 1, 4)
    # print(g.deck.pile)
    # g.take_card_from_deal(g.players[0])
    # for i in g.players[0].cards_hand:
    #     print(i)
    # print(len((g.say_false(g.players[0], g.players[1])).cards_hand))
    # for i in g.players[0].cards_hand:
    #     print(i)
    # print(g.deck.values)
    #
    # print(g.players[0].cards_hand[0])
    #
    # print(g.players[2].name)
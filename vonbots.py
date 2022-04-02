from random import randint
from Player import Player
from math import log


DECK_SIZE = 24

# 20% chance of taking the card
class PlayerV(Player):
    def wants_card(self, card, schmibbets, game_state):
        return True if randint(0, 5) == 0 else False


# Will take card if it's adjacent to a currently owned card and has more than 4 schmibbets
# Will take card if it's within 2 numbers of a currently owned card, and has more schmibbets than the player does
# Won't take card if it's 2 away, and the directly adjacent card has already been taken
# Will take card if it is more likely to draw another card with a higher number than the current value
#   Will only take a card in this way if the card has more schmibbets than the player does
class PlayerW(Player):
    def wants_card(self, card, schmibbets, game_state):
        if schmibbets > self.schmibbets:
            under = 0
            over = 0
            card_val = card - schmibbets
            for i in game_state.get_cards_taken():
                if i < card - card_val:
                    under += 1
                if i > card - card_val:
                    over += 1
            if under < over:
                return True
        for i in self.cards:
            if card in [i - 1, i + 1] and schmibbets > 4:
                return True
            if schmibbets > self.schmibbets:
                if card == i - 2 and i - 1 in game_state.get_cards_taken():
                    return True
                if card == i + 2 and i + 1 in game_state.get_cards_taken():
                    return True
        return False


# Will take card if it has none and one of the following are true:
#    a) Card is less than 11
#    b) Card is less than 21 and has 5 Schmibbets
#    c) Card is less than 31 and has 10 Schmibbets
#    d) Card has 15 Schmibbets
# Will take card if value is less than 9
# Will take card if it's directly preceding an existing card
# Will take card if it's directly succeeding an existing card and has 5 Schmibbets
class PlayerX(Player):
    def wants_card(self, card, schmibbets, game_state):
        if not self.cards:
            if card <= 10:
                return True
            if card <= 20 and schmibbets >= 5:
                return True
            if card <= 30 and schmibbets >= 10:
                return True
            if schmibbets >= 15:
                return True
        if card - schmibbets <= 8:
            return True
        for i in self.cards:
            if card == i - 1:
                return True
            if schmibbets >= 5 and card == i + 1:
                return True
        return False


# Will take card if it has none and one of the following are true:
#    a) Card is in lower third and has 5 schmibbets
#    b) Card is in middle third and has 10 schmibbets
#    c) Card has 15 schmibbets
# Will take card if value is less than 5
# Will take card if it's directly preceding an existing card
# Will take card if it's directly succeeding an existing card and has 5 schmibbets
class PlayerY(Player):
    def wants_card(self, card, schmibbets, game_state):
        if not self.cards:
            if card <= 14 and schmibbets >= 5:
                return True
            if card <= 25 and schmibbets >= 10:
                return True
            if schmibbets >= 15:
                return True
        if card - schmibbets <= 4:
            return True
        for i in self.cards:
            if card == i - 1:
                return True
            if card == i + 1 and schmibbets >= 5:
                return True
        return False


class PlayerZ(Player):
    def wants_card(self, card, schmibbets, game_state):
        if not self.cards and card / 3 - schmibbets <= 0:
            return True
        if card - schmibbets < 6 or (self.schmibbets < self.starting_schmibbets and card - schmibbets < 9):
            return True
        for i in self.cards:
            if card == i - 1 and (schmibbets > 0 or i - 2 not in game_state.get_cards_taken()):
                return True
            if card == i + 1 and (schmibbets > 4 or i + 2 not in game_state.get_cards_taken()):
                return True
            if schmibbets > 4 and card == i - 2 and i - 1 in game_state.get_cards_taken():
                return True
            if schmibbets > 9 and card == i + 2 and i + 1 in game_state.get_cards_taken():
                return True
        return False


class GoodPlayer(Player):
    def wants_card(self, card, schmibbets, game_state):
        INITIAL_SCHMIB_VALUE = 4

        if self.is_card_adjacent(card):
            return True

        # schmib_factor = INITIAL_SCHMIB_VALUE + (-(INITIAL_SCHMIB_VALUE - 1) * (DECK_SIZE - len(game_state.deck)) / DECK_SIZE)
        schmib_factor = -1.4 * log(self.schmibbets+1) + (7 * (DECK_SIZE - len(game_state.deck)) / DECK_SIZE)
        print(f"{self.schmibbets}, {schmib_factor}")

        decision = (card + -schmibbets * schmib_factor) < 0

        if decision:
            print(f"taking card {card} with schmibbets {schmibbets}")
        return decision

    def is_card_adjacent(self, card):
        for c in self.cards:
            if abs(c - card) == 1:
                return True
        return False


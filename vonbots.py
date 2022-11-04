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
    ADJACENT_CARD_PARAM = 3.5
    SEMI_ADJACENT_MULTIPLE_PARAM = .25
    MYSTERY_VALUE_PARAM = 1.2
    SCHMIBBET_VALUE_PARAM = 4

    def wants_card(self, card, schmibbets, game_state):
        if self.is_card_adjacent(card):
            return True

        card_value = 0

        cards_available = game_state.get_cards_available()

        if (card + 1) in cards_available:
            card_value += self.ADJACENT_CARD_PARAM
            if (card + 2) in cards_available:
                card_value += self.ADJACENT_CARD_PARAM * self.SEMI_ADJACENT_MULTIPLE_PARAM
        if (card - 1) in cards_available:
            card_value += self.ADJACENT_CARD_PARAM
            if (card - 2) in cards_available:
                card_value += self.ADJACENT_CARD_PARAM * self.SEMI_ADJACENT_MULTIPLE_PARAM


        turn_factor = (1 - 1 / (1 + len(game_state.deck) / 25)) * self.MYSTERY_VALUE_PARAM
        decision = (card_value + schmibbets * self.SCHMIBBET_VALUE_PARAM) * turn_factor - card>= 0

        return decision

    def is_card_adjacent(self, card):
        for c in self.cards:
            if abs(c - card) == 1:
                return True
        return False

class FuturePlayer(Player):
    # SCHMIBBETS_PER_VALUE_EST = .138
    # TURNS_PER_GAME = 22.5

    def wants_card(self, card, schmibbets, game_state):
        return false
    #     if self.is_card_adjacent(card):
    #         # print(f"taking card {card} with schmibbets {schmibbets}. {self.cards}")
    #         return True

    #     # est_turns_remaining = self.est_turns_remaining(card, schmibbets, game_state)
    #     # if est_turns_remaining > self.schmibbets: # take it we need schmibbets period
    #     #     print(f"taking card {card} with schmibbets {schmibbets}. {self.cards} because turns")
    #     #     return True

    #     card_value = 0

    #     cards_available = game_state.get_cards_available()

    #     init_card_value = 3.5
    #     second_card_ratio = .25
    #     if (card + 1) in cards_available:
    #         card_value += init_card_value
    #         if (card + 2) in cards_available:
    #             card_value += init_card_value * second_card_ratio
    #     if (card - 1) in cards_available:
    #         card_value += init_card_value
    #         if (card - 2) in cards_available:
    #             card_value += init_card_value * second_card_ratio

    #     # turn_factor = (est_turns_remaining / self.TURNS_PER_GAME)
    #     turn_factor = (1 - 1 / (1 + len(game_state.deck) / 25)) * 1.2
    #     decision = (card_value + schmibbets * 4) * turn_factor - card>= 0

    #     # print(f"card: {card}, value: {card_value}, schmibbets: {schmibbets}, turn_factor: {turn_factor}")
    #     # decision = schmibbets / card > .138 # take it if it's more than average


    #     # if decision:
    #     #     print(f"taking card {card} with schmibbets {schmibbets}. {self.cards} because value")

    #     return decision

    # def is_card_adjacent(self, card):
    #     for c in self.cards:
    #         if abs(c - card) == 1:
    #             return True
    #     return False

    # # def est_turns_remaining(self, current_card, current_schmibbets, game_state):
    # #     turns = max(current_card * self.SCHMIBBETS_PER_VALUE_EST - current_schmibbets, 0)
    # #     for card in game_state.deck: # cheating
    # #         turns += card * self.SCHMIBBETS_PER_VALUE_EST

    # #     return turns / len(game_state.players)



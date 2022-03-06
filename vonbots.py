from random import randint
from Player import Player


# 20% chance of taking the card
class PlayerV(Player):
    def __init__(self, schmibbets, knownCards):
        super().__init__(schmibbets, knownCards)

    def take_card(self, card, schmibbets):
        return True if randint(0, 5) == 0 or self.schmib == 0 else False


# Will take card if it's adjacent to a currently owned card and has more than 4 schmibbets
# Will take card if it's within 2 numbers of a currently owned card, and has more schmibbets than the player does
# Won't take card if it's 2 away, and the directly adjacent card has already been taken
# Will take card if it is more likely to draw another card with a higher number than the current value
#   Will only take a card in this way if the card has more schmibbets than the player does
class PlayerW(Player):
    def __init__(self, schmibbets, knownCards):
        super().__init__(schmibbets, knownCards)

    def take_card(self, card, schmibbets):
        if self.schmib == 0:
            return True
        if schmibbets > self.schmib:
            currentDeck = [i for i in range(3, 36) if i not in self.knownCards]
            under = 0
            over = 0
            card_val = card - schmibbets
            for i in currentDeck:
                if i < card - card_val:
                    under += 1
                if i > card - card_val:
                    over += 1
            if under < over:
                return True
        for i in self.cards:
            if card in [i - 1, i + 1] and schmibbets > 4:
                return True
            if schmibbets > self.schmib:
                if card == i - 2 and i - 1 not in self.knownCards:
                    return True
                if card == i + 2 and i + 1 not in self.knownCards:
                    return True
        return False

# Will take card if it's adjacent to a currently owned card and has more than 3 schmibbets
# Will take card if player has none, the card is <= 16, and has 5 or more schmibbets
# Will take card if it's in lowest third, and the schmibbets cancel out it's value.
class PlayerX(Player):
    def __init__(self, schmibbets, knownCards):
        super().__init__(schmibbets, knownCards)

    def take_card(self, card, schmibbets):
        if self.schmib == 0:
            return True
        if card <= 14 and card - schmibbets <= 0:
            return True
        if not self.cards and 5 <= schmibbets:
            return True if card <= 16 else False
        if schmibbets > 3:
            for i in self.cards:
                if card in [i - 1, i + 1]:
                    return True
        return False

# Will take card if it's adjacent to a currently owned card and has more than 2 schmibbets
# Will take card if player has none and the card - schmibbets + 13 is <= the average value of the deck
class PlayerY(Player):
    def __init__(self, schmibbets, knownCards):
        super().__init__(schmibbets, knownCards)

    def take_card(self, card, schmibbets):
        if self.schmib == 0:
            return True
        currentDeck = [i for i in range(3, 36) if i not in self.knownCards]
        average = sum(currentDeck) / len(currentDeck)
        if card - schmibbets + 14 <= average - (11 - self.schmib):
            return True
        for i in self.cards:
            if card == i - 1:
                if schmibbets >= 3 or i - 2 in self.knownCards:
                    return True
            if card == i + 1:
                if schmibbets >= 3 or i + 2 in self.knownCards:
                    return True
        return False

# Will take card if it's adjacent to a currently owned card and has more than 3 schmibbets
# Will take card if it has more schmibbets than the player does, and the card is <= 19
# Will take card if player has none, and the value of the card is <= 1
class PlayerZ(Player):
    def __init__(self, schmibbets, knownCards):
        super().__init__(schmibbets, knownCards)

    def take_card(self, card, schmibbets):
        if self.schmib == 0:
            return True
        if not self.cards and card - schmibbets <= 1:
            return True
        if schmibbets > 3:
            for i in self.cards:
                if card in [i - 1, i + 1]:
                    return True
        return True if schmibbets > self.schmib and card <= 19 else False

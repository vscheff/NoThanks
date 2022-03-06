class Player:
    def __init__(self, schmibbets, knownCards):
        self.cards = []
        self.schmib = schmibbets
        self.knownCards = knownCards

    def clear(self, schmibbets):
        self.cards = []
        self.schmib = schmibbets

    def get_score(self):
        if not self.cards:
            return 0
        if len(self.cards) == 1:
            return self.cards[0] - self.schmib
        self.cards.sort()
        score = 0
        for i in range(len(self.cards) - 1, 0, -1):
            if self.cards[i - 1] != self.cards[i] - 1:
                score += self.cards[i]
        return score + self.cards[0] - self.schmib

    def add_card(self, card):
        self.cards.append(card)

    def add_schmib(self, schmibbets):
        self.schmib += schmibbets

    def take_card(self, card, schmibbets):
        return True if not self.schmib else False

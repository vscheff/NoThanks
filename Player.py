from dataclasses import dataclass

class Player:
    def __str__(self):
        return type(self).__name__

    def stats(self):
        return {str(self) : self.player_stats.print()}

    def __init__(self, schmibbets):
        self.cards = []
        self.starting_schmibbets = schmibbets
        self.schmibbets = schmibbets
        self.score = None

        self.player_stats = PlayerStats()

    def clear(self):
        self.cards = []
        self.schmibbets = self.starting_schmibbets
        self.score = None

    def calculate_score(self):
        self.cards.sort()
        score = 0

        prev_card = None
        for card in self.cards:
            if card - 1 != prev_card:
                score += card

            prev_card = card

        score -= self.schmibbets

        self.score = score
        return score

    def add_card(self, card):
        self.cards.append(card)

    def add_schmib(self, schmibbets):
        self.schmibbets += schmibbets

    def wants_card(self, card, schmibbets, game_state):
        return True if not self.schmibbets else False


@dataclass(unsafe_hash=True)
class PlayerStats:
    wins: int = 0
    average_score = None
    games_played: int = 0


    def print(self):
        return {
        "wins": self.wins,
        "average_score": int(self.average_score)
        }

    def update(self, won, score):
        if self.average_score is None:
            self.average_score = score
        else:
            self.average_score = (self.average_score * self.games_played / (self.games_played + 1)) + (score / (self.games_played + 1))

        self.games_played += 1

        if won:
            self.wins += 1


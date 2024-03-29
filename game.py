from random import randint, shuffle
from math import floor
import vonbots as v
from Human import Human
from dataclasses import dataclass
from typing import List
from Player import Player
from copy import deepcopy,copy
from collections import defaultdict
from statistics import mean
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt



NUM_GAMES = 1000
DEBUG = False
ANALYTICS = False
analytics = defaultdict(list)


SCHMIBBETS = None
PLAYERS = [v.PlayerV,
           v.PlayerW,
           v.PlayerX,
           v.PlayerY,
           v.PlayerZ,
           v.GoodPlayer]
# PLAYERS.append(Human(SCHMIBBETS, knownCards))
NUM_PLAYERS = len(PLAYERS)

if SCHMIBBETS is None:
    SCHMIBBETS = 11 if NUM_PLAYERS < 6 else 55 // NUM_PLAYERS

PLAYERS = [player(SCHMIBBETS) for player in PLAYERS]

def main():
    game = Game(PLAYERS)
    sim = Sim(game)

    sim.run(NUM_GAMES)


@dataclass(unsafe_hash=True)
class GameState:
    ORIGINAL_DECK = set(i for i in range(3, 36))

    players: List[Player]
    deck: List[int]
    turn: int = 0

    def get_cards_taken(self):
        return set(card for player in self.players for card in player.cards)

    def get_cards_available(self):
        return self.ORIGINAL_DECK - self.get_cards_taken()


class Game():
    players = []
    def __init__(self, players):
        self.players = players

    def start(self):
        # Set up
        deck = [i for i in range(3, 36)]

        for i in range(9):
            deck.pop(randint(0, len(deck) - 1))

        shuffle(deck)
        players = copy(self.players)
        shuffle(players)

        game_state = GameState(players=players, deck=deck)

        if DEBUG:
            print(f'Turn Order: {players}\n')

        # Play game
        while deck:
            card = deck.pop()
            schmibbets = 0
            while True:
                cur_player = players[game_state.turn]

                if ANALYTICS:
                    analytics[card] = analytics[card] + [schmibbets]

                if cur_player.schmibbets == 0 or cur_player.wants_card(card, schmibbets, game_state):
                    cur_player.add_card(card)
                    cur_player.add_schmib(schmibbets)
                    break
                else:
                    cur_player.schmibbets -= 1
                    schmibbets += 1
                    game_state.turn = (game_state.turn + 1) % NUM_PLAYERS

            if DEBUG:
                print(f"{cur_player} got Card {card} for {schmibbets} Schmibbets. "
                      f"Has cards {cur_player.cards}\n"
                      f"Schmibbets: {', '.join([str(i.schmibbets) for i in PLAYERS])}\n")
        if DEBUG:
            print()
            for i in range(NUM_PLAYERS):
                p = PLAYERS[i]
                print(f"Player {i}: {p.get_score()} with {p.schmibbets} schmibbets. Cards: {p.cards}")


        for player in players:
            player.calculate_score()

        return game_state


class Sim():
    def __init__(self, game):
        self.game = game
        self.players = game.players
        self.NUM_PLAYERS = len(self.players)

    def run(self, games = 1000):
        gamesWon = [0 for _ in range(self.NUM_PLAYERS)]
        totalScore = [0 for _ in range(self.NUM_PLAYERS)]

        for _ in range(games):
            if DEBUG:
                print(f"GAME {_}")
            # play game
            game_state = self.game.start()

            # update player stats
            winner = None
            for player in game_state.players:
                if not winner or winner.score > player.score:
                    winner = player

            for player in game_state.players:
                player.player_stats.update(won=(player==winner), score=player.score)
                player.clear()
            

        for player in game_state.players:
            print(player.stats())

        if ANALYTICS:
            def f(a,n,x1):
                return (a*np.power(x1,-n));

            xdata = np.array(sorted(analytics))
            ydata = np.array([mean(analytics[card]) for card in sorted(analytics)])
            pars, cov = curve_fit(f=f, xdata=xdata, ydata=ydata)

            fit_y = f(xdata, pars[0], pars[1])

            plt.plot(xdata, ydata, 'o', label='data')
            plt.plot(xdata, fit_y, '-', label='fit')
            plt.legend()
            plt.show()


            # for card in sorted(analytics):
                # print(f"card {card}: avg schmib {}")


if __name__ == '__main__':
    main()

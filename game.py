from random import randint
from math import floor
import vonbots as v
from Human import Human

knownCards = []

NUM_GAMES = 1000
SCHMIBBETS = None
PLAYERS = [v.PlayerV(SCHMIBBETS, knownCards),
           v.PlayerW(SCHMIBBETS, knownCards),
           v.PlayerX(SCHMIBBETS, knownCards),
           v.PlayerY(SCHMIBBETS, knownCards),
           v.PlayerZ(SCHMIBBETS, knownCards)]
# PLAYERS.append(Human(SCHMIBBETS, knownCards))
NUM_PLAYERS = len(PLAYERS)

turns = [i for i in range(NUM_PLAYERS)]

if SCHMIBBETS is None:
    SCHMIBBETS = 11 if NUM_PLAYERS < 6 else 55 // NUM_PLAYERS

def main():
    print('\nPlaying one game:\n')
    playGame(True)

    print('\n\nPlaying many games:')
    playMany(NUM_GAMES)

def playMany(games):
    gamesWon = [0 for _ in range(NUM_PLAYERS)]
    totalScore = [0 for _ in range(NUM_PLAYERS)]
    for i in range(games):
        scores = playGame()
        min_score = min(scores)
        for j in range(NUM_PLAYERS):
            if min_score == scores[j]:
                gamesWon[j] += 1
            totalScore[j] += scores[j]
    averageScore = [round(i / games) for i in totalScore]

    print(f'\nGames won: {gamesWon}\nAverage score: {averageScore}\n')

def playGame(single=False):
    for player in PLAYERS:
        player.clear(SCHMIBBETS)
    knownCards.clear()
    knownCards.extend([i for i in range(3, 36)])
    deck = knownCards.copy()
    for i in range(9):
        deck.pop(randint(0, len(deck) - 1))

    shuffle_turns()
    turn = 0
    player_turn = turns[turn]
    while deck:
        card = deck.pop(randint(0, len(deck) - 1))
        knownCards.remove(card)
        schmibbets = 0
        while True:
            if PLAYERS[player_turn].schmib == 0 or PLAYERS[player_turn].take_card(card, schmibbets):
                PLAYERS[player_turn].add_card(card)
                PLAYERS[player_turn].add_schmib(schmibbets)
                break
            else:
                PLAYERS[player_turn].add_schmib(-1)
                schmibbets += 1
                turn = 0 if turn == NUM_PLAYERS - 1 else turn + 1
                player_turn = turns[turn]

        if single:
            print(f"Player {player_turn} got Card {card} for {schmibbets} Schmibbets. "
                  f"Has cards {PLAYERS[player_turn].cards}\n"
                  f"Schmibbets: {', '.join([str(i.schmib) for i in PLAYERS])}\n")

    if single:
        print()
        for i in range(NUM_PLAYERS):
            p = PLAYERS[i]
            print(f"Player {i}: {p.get_score()} with {p.schmib} schmibbets. Cards: {p.cards}")

    return [i.get_score() for i in PLAYERS]

def shuffle_turns():
    for i in range(NUM_PLAYERS - 1, 0, -1):
        j = randint(0, i)
        turns[i], turns[j] = turns[j], turns[i]


if __name__ == '__main__':
    main()

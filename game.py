from random import randint
import vonbots as v
from Human import Human

SCHMIBBETS = 9
knownCards = []
PLAYERS = [v.PlayerV(SCHMIBBETS, knownCards),
           v.PlayerW(SCHMIBBETS, knownCards),
           v.PlayerX(SCHMIBBETS, knownCards),
           v.PlayerY(SCHMIBBETS, knownCards),
           v.PlayerZ(SCHMIBBETS, knownCards)]
# PLAYERS.append(Human(SCHMIBBETS, knownCards))
NUM_PLAYERS = len(PLAYERS)

def main():
    print('\nPlaying one game:\n')
    playGame(True)

    print('\n\nPlaying many games:')
    playMany(1000)

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
    for player in PLAYERS:s
        player.clear(SCHMIBBETS)
    knownCards.clear()
    knownCards.extend([i for i in range(3, 36)])
    deck = knownCards.copy()
    for i in range(9):
        deck.pop(randint(0, len(deck) - 1))
    player_turn = randint(0, NUM_PLAYERS - 1)
    while deck:
        rand_index = randint(0, len(deck) - 1)
        card = deck.pop(rand_index)
        knownCards.pop(rand_index)
        schmibbets = 0
        while True:
            if PLAYERS[player_turn].take_card(card, schmibbets):
                PLAYERS[player_turn].add_card(card)
                PLAYERS[player_turn].add_schmib(schmibbets)
                break
            else:
                PLAYERS[player_turn].add_schmib(-1)
                schmibbets += 1
                player_turn = 0 if player_turn == NUM_PLAYERS - 1 else player_turn + 1

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


if __name__ == '__main__':
    main()

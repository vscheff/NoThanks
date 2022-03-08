from Player import Player

class Human(Player):
    def __init__(self, schmibbets, knownCards):
        super().__init__(schmibbets, knownCards)

    def take_card(self, card, schmibbets):
        while True:
            usr_inp = input(f"Take card #{card} for {schmibbets} Schmibbets? (y/n): ").strip().lower()
            if usr_inp in ['y', 'yes', '1']:
                return True
            if usr_inp in ['n', 'no', '0']:
                return False

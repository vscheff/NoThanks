# NoThanks
To run simulations execute game.py

game.py parameters:

    - SCHMIBBETS := Starting amount of schmibbets for all players
    - PLAYERS := List of all bots playing the game. Add or remove custom bots from this list

To create a custom bot, create a class that inherits from Player.Player()
Overwrite the .take_card() method with your own function that returns a boolean value indicating whether the bot will take the card.

# NoThanks
To run simulations execute game.py

game.py parameters:

    - NUM_GAMES := Number of games to simulate when game.playMany() is called.
    - SCHMIBBETS := Starting amount of Schmibbets for all players. Leave this None to auto-assign starting Schmibbets per the game rules.
    - PLAYERS := List of all bots playing the game. Add or remove custom bots from this list

To create a custom bot, create a class that inherits from Player.Player()

Overwrite the .take_card() method with your own function that returns a boolean value indicating whether the bot will take the card.


To play the game yourself, add a Human.Human() object to PLAYERS. Not recommended to "playMany" with a Human player.

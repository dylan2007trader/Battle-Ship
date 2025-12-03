# Battle-Ship
I thought it would be fun to implement battle ship in python.

I only used 2 inputs to make this code easy to check.
Player 1 would input a file of 5 ships with 2 coordinates of the ship start and end position.
Player 2 would have a second input with a file with guesses on every line till the game ends.

The battleship grid is made using object oriented programming. I have 3 classes, a GridPos which represents a single grid position on the grid.
I have a Ship class that shows the type of ship, its size, and what positions it ois located on the grid.
I lastly have a Grid object that represents the board of the game with it being made of GridPos objects.

There is a lot of error checking to make sure the game is being played appropriately. I used the project to work on this part of my resume.

There should be 5 ships, one of each type; if not print the following error message and quit:
Error message: "ERROR: fleet composition incorrect"

If the ship is out of the grid area, print the following error message and quit:
Error message: "ERROR: ship out-of-bounds: " + line

If the ship is not horizontal or vertical, print the following error message and quit:
Error message: "ERROR: ship not horizontal or vertical: " + line

If the ship overlaps with another ship, print the following error message and quit:
Error message: "ERROR: overlapping ship: " + line

If the ship is an incorrect size for its type, print the following error message and quit:
Error message: "ERROR: incorrect ship size: " + line

If a guess is at a position not within the board, print the following error message, discard the guess, and continue processing:
Error message: "illegal guess"

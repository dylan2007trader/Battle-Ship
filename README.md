# Battle-Ship
I thought it would be fun to implement battle ship in python.

Battleship Game – README
Overview

This program implements a simplified, text-based version of the classic Battleship game.
Player 1 provides ship placements, and Player 2 provides guesses. The program:

Loads ship placements and guesses from two input files

Validates fleet composition, sizes, orientations, and bounds

Builds an internal 10×10 board

Places ships using a custom coordinate-conversion system

Processes guesses sequentially

Prints hits, misses, repeat guesses, and sunk ship events

Ends when all ships are sunk

This project is designed to match the structure and style expected for CSC 120.

How to Run

The program requires two input files:

Ship placement file

Guesses file

Example run:

python3 battleship.py


You will be prompted twice:

ships.txt
guesses.txt

Input Format
Ship File

Each ship must appear exactly once. The valid ships are:

Type	Size	Name
A	5	Aircraft Carrier
B	4	Battleship
S	3	Submarine
D	3	Destroyer
P	2	Patrol Boat

Each line must follow this format:

<ShipType> x1 y1 x2 y2


Example:

A 0 0 0 4
B 2 2 5 2
S 9 0 9 2
D 4 7 6 7
P 8 8 9 8


Coordinates must be integers 0–9.

Ships must be strictly horizontal (same row) or vertical (same column).

The program will reject:

Out-of-bounds placements

Incorrect ship lengths

Diagonal placements

Overlapping ships

Duplicate ship types

Wrong number of total ships

Guess File

Each line must contain:

x y


Example:

0 0
1 1
5 2


Guesses outside the board or with incorrect formatting result in:

illegal guess

Output Behavior
Misses
miss
miss (again)

Hits
hit
hit (again)

Sinking a ship

When the final part of a ship is hit:

A sunk

Game end

After all ships are sunk:

all ships sunk: game over


The program then exits.

Internal Details
Board Structure

10×10 grid of GridPos objects

Each cell stores:

A reference to a Ship (or None)

A _guessed boolean

Ship Handling

A Ship tracks:

Its kind (A/B/S/D/P)

Its size

Its health (_active)

Two endpoint coordinates

hit_ship() decreases _active and prints hit/sunk messages.

Coordinate Conversion

All input coordinates are converted using:

convert_coordinates()


This swaps and transforms coordinates to match the assignment’s unique grid system.

Game Loop

read_inputs() iterates through guesses until:

All ships are sunk

Or guesses run out

Error Handling

The program exits immediately on:

Overlapping ships

Out-of-bounds placements

Incorrect fleet composition

Incorrect ship size

Non-horizontal/vertical ships

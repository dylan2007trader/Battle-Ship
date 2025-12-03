"""
    Purpose: Implements a simple Battleship game. Handles the board, ships, 
        coordinate conversion, ship placement, and processing guesses. 
        Prints hits, misses, and sinking events. Validates ship positions and
        guess inputs. Player 1 would add 5 ships to a battleship grid and
        Player 2 would guess till the ships are destroyed.
"""

import sys

class GridPos:
    """Represents a single position on the board.

    Primary methods:
        - __str__: returns the character representing the position 
        (ship or '*')
    
    Constructed with x and y coordinates. Can hold ship and track if guessed.
    """

    def __init__(self, x_pos, y_pos):
        """Initialize a grid position.

        Parameters:
            x_pos: integer row index
            y_pos: integer column index
        
        Attributes:
            _ship: the Ship object occupying this position (None if empty)
            _guessed: boolean indicating if this position was guessed
        """
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._ship = None  # No ship initially
        self._guessed = False  # Track if this position has been guessed

    def __str__(self):
        if self._ship is None:  # (*) means no ship at that postition
            return '*'
        return str(self._ship)

class Board:
    """Represents the 10x10 Battleship board.

    Primary methods:
        - get_grid_pos: returns a specific GridPos object
        - add_ship: adds a Ship object to the collection
        - __str__: prints the current board as a string
    
    Constructed with a 10x10 grid of GridPos objects.
    """

    def __init__(self):
        """Initialize a 10x10 board with empty GridPos objects.
        Also initializes a collection which is an empty list for 
        ships later on.

        Parameters: None

        Attributes: self._grid is 10 by 10 grid of empty GridPos objects
        self._collection is an empty list for ships later on
        """
        grid = []
        # Outer loop: create rows of the board
        for num1 in range(10):
            line = []
            # Inner loop: create each column (cell) in the row
            for num2 in range(10):
                line.append(GridPos(num1, num2))  # Initialize each cell
            grid.append(line)  # Add completed row to grid
        self._grid = grid
        self._collection = []

    def get_grid_pos(self, x_pos, y_pos):
        """Return the GridPos object at the specified coordinates.

        Parameters:
            x_pos: row index (0-9)
            y_pos: column index (0-9)
        Returns:
            GridPos object at that position
        """
        return self._grid[x_pos][y_pos]

    def add_ship(self, ship):
        """Add a Ship object to the board's ship collection.

        Parameters:
            ship: Ship object to add
        Returns: None
        """
        self._collection.append(ship)

    def __str__(self):
        string = ''
        # Loop over each row in the grid
        for line in self._grid:
            new = ''
            # Loop over each cell in the row
            for grid_pos in line:
                new += str(grid_pos) + ' '  # Append cell display to string
            new = new.strip()  # Remove trailing space from row
            new += '\n'  # Add newline for next row
            string += new  # Add completed row to full board string
        return string

class Ship:
    """Represents a ship on the board. The ship could be one 
    of 5 different ships.

    Primary methods:
        - hit_ship: reduce active count and print status
        - __str__: returns ship's kind
    """

    def __init__(self, kind, size, positions):
        """Initialize a ship.

        Parameters:
            kind: single-character string identifier of the ship
            size: number of grid positions the ship occupies
            positions: list of two coordinates defining ship placement
        
        The ship starts fully active (all positions un-hit) which is the size.
        """
        self._kind = kind
        self._size = size
        self._positions = positions
        self._active = size

    def hit_ship(self):
        """Mark the ship as hit and print status.

        Behavior:
            - Decreases the number of active positions.
            - Prints "hit" if still active.
            - Prints "<ship> sunk" if ship is destroyed.
        
        Paramters: None

        Returns: None
        """
        self._active -= 1  # Reduce ship's active parts by 1
        if self._active == 0:
            print("{} sunk".format(str(self)))  # All parts hit; ship sunk
        else:
            print("hit")  # Ship partially hit but still afloat

    def __str__(self):
        return self._kind



def convert_coordinates(x_pos, y_pos):
    """Convert user input coordinates to internal board coordinates.
    This converts game units to a regular computer-science grid positions.

    Parameters:
        x_pos: input x coordinate
        y_pos: input y coordinate

    Returns:
        List of [converted_x, converted_y] for internal use.
    """
    store_y = y_pos  # Temporarily store original y
    y_pos = x_pos  # Swap x and y for internal representation
    # Adjust x_pos for board layout: special mapping for game rules
    if store_y > 4:  # if store_y >4, need to subtract from it
        x_pos = store_y + 1 - 2 * (store_y - 4)
    else:  # this adds to store_y if it is (0-4)
        x_pos = store_y + 1 + 2 * (4 - store_y)
    return [x_pos, y_pos]


def set_grid_positions_helper(
    board, first, second, ship, ship_object, is_vert, dif, negative):
    """Helper to place a ship on the board in vertical or horizontal 
    orientation.

    Parameters:
        board: Board object
        first: converted start coordinate
        second: converted end coordinate
        ship: original ship input line
        ship_object: Ship object to place
        is_vert: True if ship is vertical, False if horizontal
        dif: length of the ship including both endpoints
        negative: True if ship is placed "backwards" along the grid

    Returns: None
    """
    if is_vert:  # Place vertical ship
        for row in range(dif):  # Loop over rows of the ship
            if negative:  # starts at first if negative
                grid_pos = board.get_grid_pos(first[0] + row, first[1])
            else:  # starts at second if positive
                grid_pos = board.get_grid_pos(second[0] + row, first[1])
            if grid_pos._ship is not None:  # Check for overlapping ships
                print("ERROR: overlapping ship: " + ship)  # Print error
                sys.exit(0)  # Exit if invalid
            grid_pos._ship = ship_object  # Place ship in grid
        return  # Done placing vertical ship
    for col in range(dif):  # Place horizontal ship
        if negative:  # starts at first if negative
            grid_pos = board.get_grid_pos(first[0], first[1] + col)
        else:  # starts at second if positive
            grid_pos = board.get_grid_pos(first[0], second[1] + col)
        if grid_pos._ship is not None:  # Check for overlapping ships
            print("ERROR: overlapping ship: " + ship)  # Print error
            sys.exit(0)  # Exit if invalid
        grid_pos._ship = ship_object  # Place ship in grid


def set_grid_positions(board, first, second, ship, ship_object):
    """Place a ship object on the board between two coordinates.

    Parameters:
        board: Board object
        first: converted start coordinate
        second: converted end coordinate
        ship: original ship input line
        ship_object: Ship object to place

    Returns: None
    """
    if first[0] != second[0]:  # Vertical ship if x coordinates differ
        dif = first[0] - second[0]  # Difference in rows
        is_vert = True
    elif first[1] != second[1]:  # Horizontal ship if y coordinates differ
        dif = first[1] - second[1]  # Difference in columns
        is_vert = False
    negative = False  # Track if placement goes in negative direction
    if dif < 0:
        dif = -dif  # Make difference positive for looping
        negative = True  # Placement goes "backwards" from first coordinate
    dif += 1  # Include both endpoints

    set_grid_positions_helper(
        board, first, second, ship, ship_object, is_vert, dif, negative)

def add_ships(board, ships, dic):
    """
    Add all ships to the board using the provided dictionary of sizes. 
    Converts ship coordinates, creates Ship objects, and places them on 
    the board.

    Parameters:
        board: Board object where ships are placed.
        ships: List of ship input strings with coordinates and type.
        dic: Dictionary mapping ship type to its size.

    Returns:
        None
    """
    for ship in ships:  # Loop through each ship in input

        first = convert_coordinates(int(ship[2]), int(ship[4]))
        second = convert_coordinates(int(ship[6]), int(ship[8]))
        # Convert the coordinates to board grid coordinates
        positions = [first, second]  # Store both positions in a list

        ship_object = Ship(ship[0], dic[ship[0]], positions)  # create ship
        board.add_ship(ship_object)
        # Add the ship object to the board's collection
        set_grid_positions(board, first, second, ship, ship_object)
        # Place the ship on board grid between first and second coordinates

def bad_size(ships, dic):
    """
    Check for incorrect ship sizes and exit the program if any are invalid.

    Parameters:
        ships: List of ship input strings with coordinates and type.
        dic: Dictionary mapping ship type to its expected size.

    Returns:
        None
    """
    for ship in ships:  # Loop through each ship in input
        correct = dic[ship[0]]  # Expected size of current ship
        
        # Calculate difference in coordinates to determine actual size
        if ship[2] != ship[6]:  
            dif = int(ship[2]) - int(ship[6])  # Row difference
        elif ship[4] != ship[8]:  
            dif = int(ship[4]) - int(ship[8])  # Column difference

        if correct != (dif + 1) and correct != (-(dif) + 1):
            # Check if the actual size matches the expected size
            print("ERROR: incorrect ship size: " + ship)
            sys.exit(0)  # Exit the program

def bad_ships_comp(ships):
    """
    Ensure the fleet composition contains exactly one of each required
    ship type.
    
    Parameters:
        ships: List of ship input strings with type and coordinates.
        
    Returns:
        None
    """
    if len(ships) != 5:  # Must have exactly 5 ships in the fleet
        print("ERROR: fleet composition incorrect")  # Print error message
        sys.exit(0)  # Exit program

    checks = [False] * 5  # Track found ship types
    for ship in ships:  
        if (not checks[0]) and ship[0] == 'A':  # Aircraft carrier check
            checks[0] = True  # Mark as found
            continue
        elif (not checks[1]) and ship[0] == 'B':  # Battleship check
            checks[1] = True
            continue
        elif (not checks[2]) and ship[0] == 'S':  # Submarine check
            checks[2] = True
            continue
        elif (not checks[3]) and ship[0] == 'D':  # Destroyer check
            checks[3] = True
            continue
        elif (not checks[4]) and ship[0] == 'P':  # Patrol boat check
            checks[4] = True
            continue
        print("ERROR: fleet composition incorrect")  # Duplicate/invalid ship
        sys.exit(0)  # Exit program

def ship_out_bounds(ships):
    """Check that all ship coordinates are within the 10x10 board bounds.
    
    Parameters:
        ships: list of strings representing ship placements in the format
               "ShipName x1 y1 x2 y2" (each coordinate is 0-9).
    
    Returns:
        None. Exits the program if any coordinate is out of bounds.
    """
    for ship in ships:  # Iterate over all ships in the list
        for num in ship[2:].split():
            # Skip the ship identifier and get coordinates
            if int(num) < 0 or int(num) > 9:
                # Check if coordinate is outside 0-9
                print("ERROR: ship out-of-bounds: " + ship)
                sys.exit(0)  # Exit program

def ship_not_horiz_or_vert(ships):
    """Ensure each ship is placed either strictly horizontally or vertically.

    Parameters:
        ships: list of strings representing ship placements in the format
               "ShipName x1 y1 x2 y2".

    Returns:
        None. Exits the program if a ship is not horizontal or vertical.
    """
    for ship in ships:  # Loop through all ships
        if ship[2] != ship[6]:  # Check if x-coordinates differ
            if ship[4] == ship[8]:  # Vertical: y-coordinates equal
                continue
        elif ship[4] != ship[8]:  # Check if y-coordinates differ
            if ship[2] == ship[6]:  # Horizontal: x-coordinates equal
                continue
        print("ERROR: ship not horizontal or vertical: " + ship)
        sys.exit(0)  # Exit program

def continue_game(board):
    """Check if the game should continue based on ships' remaining health.

    Parameters:
        board: Board object containing the collection of ships.

    Returns:
        True if at least one ship still has active (unsunk) positions,
        False if all ships have been sunk.
    """
    for ship in board._collection:  # Loop through all ships on the board
        if ship._active > 0:  # If ship still has positions remaining
            return True  # Game should continue
    return False  # All ships are sunk

def read_inputs(board, guesses):
    """Process a list of guesses, updating the board and printing results.
    Parameters:
        board: Board object containing ships and their positions.
        guesses: List of string guesses in "x y" format.
    Returns: None
    """
    count = 0  # Index for the current guess
    while continue_game(board) and count < len(guesses):
        # Loop until game over or guesses exhausted
        guess = guesses[count].strip()  # Remove extra whitespace
        count += 1
        if not guess:  # Empty line check
            print("illegal guess")
            continue
        both = guess.split()  # Split into x and y coordinates
        if len(both) != 2:  # Check for proper guess format
            print("illegal guess")
            continue
        both = convert_coordinates(int(both[0]), int(both[1]))
        x_pos = int(both[0])
        y_pos = int(both[1])
        if (x_pos > 9 or x_pos < 0) or (y_pos > 9 or y_pos < 0):  # In bounds?
            print("illegal guess")
            continue
        cur_grid_pos = board.get_grid_pos(x_pos, y_pos)  # get position object
        ship = cur_grid_pos._ship  # Get ship at this position, if any
        if ship is None:  # No ship at guessed position
            if cur_grid_pos._guessed:  # Already guessed this position
                print("miss (again)")
            else:
                cur_grid_pos._guessed = True  # Mark position as guessed
                print("miss")
        else:  # Ship present at guessed position
            if cur_grid_pos._guessed:  # Already guessed this position
                print("hit (again)")
            else:
                cur_grid_pos._guessed = True  # Mark position as guessed
                ship.hit_ship()  # Register a hit or sunk
    print("all ships sunk: game over")  # all ships sunk
    sys.exit(0)  # Exit the program

def read_file():
    """Prompt for a file name, read all lines, and strip trailing whitespace.

    Returns:
        List of strings: each line from the file without trailing whitespace.
    """
    file_name = input()  # Get the input file name
    file = open(file_name, 'r')
    lines = file.readlines()  # Read all lines
    for index in range(len(lines)):
        lines[index] = lines[index].rstrip()  # Remove trailing whitespace
    file.close()
    return lines  # Return cleaned lines

def main():
    """Main function that initializes the board, validates ships, adds ships,
       and processes guesses from input files.
    """
    ships = read_file()  # Read ship placement info from input file
    guesses = read_file()  # Read guess coordinates from input file
    dic = {'A': 5, 'B': 4, 'S': 3, 'D': 3, 'P': 2}  # Ship sizes

    ship_out_bounds(ships)  # Validate ships are within board bounds
    ship_not_horiz_or_vert(ships)  # Ensure ships are horizontal/vertical
    bad_ships_comp(ships)  # Check fleet composition correctness
    bad_size(ships, dic)  # Validate ship lengths

    board = Board()  # Create the game board
    add_ships(board, ships, dic)  # Place ships on the board

    read_inputs(board, guesses)  # Process guesses until game ends

main()
import sys
from random import randint

# Stat variables
shots_count = 0
hits_count = 0
miss_count = 0

win = False
shots = []

# Board variables
attacker_board = [['-'] * 10 for n in range(10)]
defender_board = [['-'] * 10 for n in range(10)]

# Boat dict
boats = {
    'p': { 'location': [], 'hits': [], 'sunk': False }, 
    's': { 'location': [], 'hits': [], 'sunk': False },
    'a': { 'location': [], 'hits': [], 'sunk': False }
}

def print_stats():
    print "Stats:"
    print "  Shots: " + str(shots_count)
    print "   Hits: " + str(hits_count)
    print " Misses: " + str(miss_count)
    print "  Hit %: " + str(hits_count / float(shots_count))
    print " Miss %: " + str(miss_count / float(shots_count))
    
def print_board(board):
    sys.stdout.write('  ')
    print " ".join(str(x) for x in range(10))
    i = 0
    for row in board:
        sys.stdout.write(str(i) + " ")
        print " ".join(row)
        i += 1

def check_position(row, col, boat_type, boat_length):
    compare = [(row, col)]
    for boat in boats:
        for item in compare:
            if item in boats[boat]['location']:
                print(boats[boat]['location'])
                print(item)
                print('here')

def place_boat(row,col,boat_type,orientation):
    # How long is our boat
    if boat_type == 'p':
        boat_length = 2
    elif boat_type == 's':
        boat_length = 3
    elif boat_type == 'a':
        boat_length = 4
    else:
        raise 'UnknownBoatType'

    if check_position(row, col, boat_type, boat_length):
        raise 'InvalidPosition'

    # Which way is our boat going to be placed
    if orientation == 'vertical':
        # col is constant
        
        # Add boat to boats dict
        boats[boat_type]['location'] = [(row+i,col) for i in range(boat_length)]

        # Add boat to defender board
        for i in range(boat_length):
            defender_board[row+i][col] = boat_type

    elif orientation == 'horizontal':
        # row is constant
        # Add boat to boats dict
        boats[boat_type]['location'] = [(row,col+i) for i in range(boat_length)]

        # Add boat to defender board
        for i in range(boat_length):
            defender_board[row][col+i] = boat_type
    else:
        raise 'UnknownBoatOrientation'


def check_win():
    if {boat for boat, info in boats.items() if not info['sunk']}:
        print "There are still some boats floating!"
        print {boat for boat, info in boats.items() if info['sunk']}
    else:
        print "You sank all the boats!"
        global win
        win = True
        print_stats()

def check_sunk(boat):
    if [x for x in boats[boat]['location'] if x not in boats[boat]['hits']] + [x for x in boats[boat]['hits'] if x not in boats[boat]['location']]:
        print boat + " is still floating!"
    else:
        print "You sunk boat: " + boat + "!"
        boats[boat]['sunk'] = True
        check_win()
        
def fire(row,col):
    # Check index range
    if row in range(10) and col in range(10):
        
        print "Firing at: (" + str(row) + ',' + str(col) + ")!"
        if (row,col) in shots:
            print 'You already shot this location. Skipping'
        else:
            # Track every shot
            shots.append((row,col))
            
            # Lets see if its a hit
            boat_hit = {boat for (boat, info) in boats.items() if (row,col) in info['location']}
            # We got a hit!
            if boat_hit:
                # Sets are a lttle crazy to work with
                boat = boat_hit.pop()
                print 'You hit: ' + boat + '!'
                
                # Lets mark our attacker board
                mark_attacker_board(row,col,boat)
                
                # Increment some stats
                global hits_count
                hits_count += 1
                
                # Put successful hit into boats dict to check for sunk
                boats[boat]['hits'].append((row,col))
                check_sunk(boat)
                
            else:
                print 'You missed!'
                mark_attacker_board(row,col,'X')
                
                global miss_count
                miss_count += 1
            
            global shots_count
            shots_count += 1
            print_board(attacker_board)
    else:
        print "Row: " + str(row) + " Col: " + str(col) + " is not in range. Skipping" 

def mark_attacker_board(row,col,boat_type):
    attacker_board[row][col] = boat_type

def check_boat_position(row, col, boat_type, orientation):
    
    if boat_type == 'p':
        boat_size = 2
    elif boat_type == 's':
        boat_size = 3
    elif boat_size == 'a':
        boat_size = 4
    else:
        raise 'InvalidBoatType'

    check_positions = []
    for p in range(boat_size):
        if orientation == 'horizontal':
            check_positions.append((row, col+p))
        elif orientation == 'veritical':
            check_positions.append((row+p, col))
        else:
            raise 'InvalidOrientation'
            
    for b,i in boats.items():
        for pos in check_positions:
            if pos in boats[b]['positions']:
                print pos
                print boats[b]['positions']


def attack():
    new_boats = ['p','s','a']
    for b in new_boats:
        new_row = randint(0,7)
        new_col = randint(0,7)
        new_orientation = randint(0,1)
    
        if new_orientation == 0:
            
            place_boat(new_row, new_col, b, 'horizontal')
        else:
            place_boat(new_row, new_col, b, 'vertical')

        print_board(defender_board)
def defend():
    pass

def main():
    # TODO: Randomize placement
    # Place patrol boat
    place_boat(2,2,'p','horizontal')
    # Place submarine
    place_boat(3,6,'s','horizontal')
    # Place aircraft carrier
    place_boat(4,8,'a','vertical')

    # Whats our board look like
    print_board(defender_board)

    # Fire some shots until we win!
    global win
    while (win != True):
       new_row = randint(0,9)
       new_col = randint(0,9)
       fire(new_row,new_col)
    
if __name__ == "__main__":
    #main()
    
    selection = False
    
    while not selection:
        print "Chose mode:"
        print "1. Attack"
        print "2. Defend"
        mode = raw_input('Selection?: ')
        if mode == "1":
            print "Ok lets attack!"
            selection = True
            attack()
        elif mode == "2":
            print "Ok lets defend!"
            selection = True
            defend()
        else:
            print "Please select a mode! 1 or 2!"


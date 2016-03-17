# Define functions so you don't have to constantly deal with row major order!
def get(gas, x, y):
    # check to see that the coordinates are in the grid
    if x<0 or x>=(gas["width"]) or y<0 or y>=(gas["height"]):
        return []
    else:
        return gas["state"][x+y*gas["width"]]

def set(gas, x, y, new_cell):
    # do nothing if coordinates are not in grid
    if not(x<0 or x>=(gas["width"]) or y<0 or y>=(gas["height"])):
        gas["state"][x+y*gas["width"]] = new_cell

# Collision function: both walls and particles IN PLACE
def collide(gas):
    for x in range(gas["width"]):
        for y in range(gas["height"]):
            cell = get(gas, x, y)
            # check for wall collision
            # Reverse direction of all particles
            if 'w' in cell:
                new_cell = ['w']
                if 'u' in cell: new_cell.append('d')
                if 'd' in cell: new_cell.append('u')
                if 'l' in cell: new_cell.append('r')
                if 'r' in cell: new_cell.append('l')
                set(gas, x, y, new_cell)
                cell = new_cell
            # check for particle collisions: sort simplifies comparison
            if sorted(cell) == ['l', 'r']:
                # Check for [LR] - horizontal collision
                cell = ['d', 'u']
            elif sorted(cell) == ['d', 'u']:
                # Check for [UD] - vertical collision
                cell = ['l', 'r']

            set(gas, x, y, cell)
    return gas

# Propagate function moves particles for one timestep IN PLACE
# Exploit the observation that you can propagate up and to the left in place
# and propagate down and to the right in place given our rules of propagation
def propagate(gas):
    for x in range(gas["width"]):
        for y in range(gas["height"]):
            # propagate up and to the left
            cell = get(gas, x, y)
            if 'u' in cell:
                cell.remove('u')
                next_cell = get(gas, x, y-1)
                next_cell.append('u')
                set(gas, x, y-1, next_cell)
            if 'l' in cell:
                cell.remove('l')
                next_cell = get(gas, x-1, y)
                next_cell.append('l')
                set(gas, x-1, y, next_cell)

            # propagate down and to the right
            _x = gas["width"]-x-1
            _y = gas["height"]-y-1
            cell = get(gas, _x, _y)
            if 'd' in cell:
                cell.remove('d')
                next_cell = get(gas, _x, _y+1)
                next_cell.append('d')
                set(gas, _x, _y+1, next_cell)
            if 'r' in cell:
                cell.remove('r')
                next_cell = get(gas, _x+1, _y)
                next_cell.append('r')
                set(gas, _x+1, _y, next_cell)
    return gas

def step(gas):

    # Simply call the collision function followed by propagate
    out = propagate(collide(gas))
    return out

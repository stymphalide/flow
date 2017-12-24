import numpy as np

"""
	@moduledoc
	Holder for the game class.
	It can be initialised with an arbitrary number of colors and
	grid size.

	The game starts with one controllable cornerstone at the top left corner.
	By Changing the color of this block to the color of one of the surrounding colors,
	one can concatenate the two blocks and thus control larger and larger areas of the field.

	One gains a reward of plus 10 for every block that is concatenated and -1 for every move that is required.
"""

def initialise_game(colorSize, width, height):
	grid =  initialise_grid(colorSize, width, height)
	control_grid = initialise_control_grid(width, height)
	score = 0
	ended = has_game_ended(control_grid)
	return {'grid' : grid , 'control_grid' : control_grid, 'score' : score, 'ended' : ended}

def update_game(color, state):
	new_state_tuple = play_color(color, state['grid'], state['control_grid'])
	ended = has_game_ended(new_state_tuple[1])
	score = state['score'] + new_state_tuple[2]
	if ended:
		score += 100
	return { 'grid' : new_state_tuple[0],
	'control_grid' : new_state_tuple[1],
	'score' : score,
	'ended' : ended
	}

def initialise_grid(colorSize, width, height):
	grid = np.random.randint(colorSize, size=(width, height), dtype=int)
	# Check that there are no neighbouring fields with the same color as the input colour-
	input_color = grid[0,0]
	if width > 1:
		if grid[1,0]  == input_color:
			grid[1,0] = (grid[1,0] + 1) % colorSize
	if height > 1:
		if grid[0,1] == input_color:
			grid[0,1] = (grid[0,1] + 1) % colorSize
	return grid

def initialise_control_grid(width, height):
	grid = np.zeros(shape=(width, height), dtype=bool)
	grid[0, 0] = True
	return grid

def play_color(color, grid, control_grid):
	if grid.shape != control_grid.shape:
		raise
	width = grid.shape[0]
	height = grid.shape[1]
	for i in range(width):
		for j in range(height):
			if control_grid[i, j]:
				grid[i, j] = color
	checked_grid = check_neighbors(grid, control_grid)
	r = reward(checked_grid)
	control_grid = control_grid + checked_grid
	end = has_game_ended(control_grid)
	return (grid, control_grid, r)

def check_neighbors(grid, control_grid):
	checked_grid = check_neighbor(grid, control_grid)
	while check_neighbor(grid, control_grid + checked_grid).any():
		checked_grid = checked_grid + check_neighbor(grid, control_grid + checked_grid)
	return checked_grid

def check_neighbor(grid, control_grid):
	if grid.shape != control_grid.shape:
		raise
	shape = grid.shape
	checked_grid = np.zeros(shape=shape, dtype=bool)
	for i in range(shape[0]):
		for j in range(shape[1]):
			if control_grid[i,j]:
				# Check the neighbours
				if i == shape[0] - 1:
					pass
				else:
					if control_grid[i+1, j]:
						pass
					else:
						if grid[i, j] == grid[i+1, j]:
							checked_grid[i+1, j] = True
				if j == shape[1] - 1:
					pass
				else:
					if control_grid[i, j+1]:
						pass
					else:
						if grid[i, j] == grid[i, j+1]:
							checked_grid[i, j+1] = True
	return checked_grid

def has_game_ended(control_grid):
	return control_grid.all()

def reward(checked_neighbors):
	# Give +10 for every true field and the whole thing minus 1
	reward = 0
	for k in np.asarray(checked_neighbors).flatten():
		if k:
			reward += 10
	reward -= 1
	return reward



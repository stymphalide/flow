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



class  Game(object):
	def __init__(self, colorSize, width, height):
		self.colorSize = colorSize
		self.width = width
		self.height = height
		self.grid = self.initialise_grid(colorSize, width, height)
		self.control_grid = self.initialise_control_grid(width, height)

	def initialise_grid(self, colorSize, width, height):
		return np.random.randint(colorSize, size=(width, height), dtype=int)

	def initialise_control_grid(self, width, height):
		grid = np.zeros(shape=(width, height), dtype=bool)
		grid[0, 0] = True
		return grid
	
	def play_color(self, color):
		grid = self.grid
		control_grid = self.control_grid
		for i in range(self.width):
			for j in range(self.height):
				if control_grid[i, j]:
					grid[i, j] = color
		checked_grid = self.check_neighbors(grid, control_grid)
		control_grid = control_grid or checked_grid


	def check_neighbors(self, grid, control_grid):
		checked_grid = self.check_neighbor(grid, control_grid)
		while self.check_neighbor(grid, control_grid + checked_grid).any():
			checked_grid = checked_grid + self.check_neighbor(grid, control_grid + checked_grid)
		return checked_grid


	def check_neighbor(self, grid, control_grid):
		# Initialise grid
		checked_grid = np.zeros(shape=(self.width, self.height), dtype=bool)
		for i in range(self.width):
			for j in range(self.height):
				if control_grid[i,j]:
					# Check the neighbours
					if control_grid[i+1, j]:
						pass
					else:
						if grid[i, j] == grid[i+1, j]:
							checked_grid[i+1, j] = True
					if control_grid[i, j+1]:
						pass
					else:
						if grid[i, j] == grid[i, j+1]:
							checked_grid[i, j+1] = True
		return checked_grid

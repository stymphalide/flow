import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense

import pickle

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import src.game as g

# Set Globals
color_size = 2
height = 3
width = 3

# Set Model requirements
input_size = height*width
output_size = color_size
# Hyperparameters
epsilon = 0.7
gamma = 0.99
number_of_games = 1000
mb_size = 300
view_interval = 100

# Make model
model = Sequential()
model.add(Dense(5, kernel_initializer='uniform', input_shape=(input_size,), activation='relu' ))
model.add(Dense(5, kernel_initializer='uniform', activation='relu'))
model.add(Dense(5, kernel_initializer='uniform', activation='relu'))
model.add(Dense(output_size, kernel_initializer='uniform', activation='linear')) 
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

def observe():
	states = []
	for t in range(number_of_games):
		if t % view_interval == 0:
			print("Game no " + str(t))
		state = g.initialise_game(color_size, width, height)
		while not state['ended']:
			if t % view_interval == 0:
				print(state)
			if np.random.random() < epsilon:
				action = np.random.randint(color_size)
			else:
				Q = model.predict(state['grid'].reshape([1,input_size]))
				action = np.argmax(Q)
			if t % view_interval == 0:
				print(action)
			new_state = g.update_game(action, state)
			reward = new_state['score'] - state['score']
			# Save and update the whole thing.
			states.append((state['grid'].reshape([1,input_size]), action, reward, new_state['grid'].reshape([1,input_size]), new_state['ended'], state))
			state = new_state
	return states

def train(data):
	np.random.shuffle(data)
	minibatch = data[0:mb_size]

	inputs = np.zeros((mb_size, input_size))
	targets = np.zeros((mb_size, output_size))


	for i in range(mb_size):
		state = minibatch[i][0]
		action = minibatch[i][1]
		reward = minibatch[i][2]
		state_new = minibatch[i][3]
		finished = minibatch[i][4]
		game_state = minibatch[i][5]
		new_game_state = g.update_game(action, game_state)

		inputs[i] = state
		targets[i] = model.predict(state)

		if finished:
			targets[i, action] = reward
		else:
			rewards = []
			for i in range(color_size):
				next_game = g.update_game(i, new_game_state)
				rewards.append(next_game['score'] - new_game_state['score'])
			targets[i, action] = reward + gamma*np.max(rewards)
		model.train_on_batch(inputs, targets)


for t in range(10):
	epsilon *= 0.99
	print("Gather new Data")
	data = observe()
	print("Fit to it")
	train(data)

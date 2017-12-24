import json
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import src.game as g
import numpy as np

def parser(data):
	data = json.loads(data)
	if type(data) == dict:
		if data['color'] != None and data['state'] != None:
			color = data['color']
			state = data['state']
			state['grid'] = np.array(state['grid'])
			state['control_grid'] = np.array(state['control_grid'])
			game_data = g.update_game(color, state)
			if game_data['ended']:
				game_data['ended'] = True
			else:
				game_data['ended'] = False
			game_data['grid'] = np.ndarray.tolist(game_data['grid'])
			game_data['control_grid'] = np.ndarray.tolist(game_data['control_grid'])
	elif type(data) == str:
		if data == "start":
			game_data = g.initialise_game(6, 10, 10)
			if game_data['ended']:
				game_data['ended'] = True
			else:
				game_data['ended'] = False
			game_data['grid'] = np.ndarray.tolist(game_data['grid'])
			game_data['control_grid'] = np.ndarray.tolist(game_data['control_grid'])
	else:
		return False
	json_data = json.dumps(game_data)
	return json_data
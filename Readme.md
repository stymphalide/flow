# Flow
Is a fun grid game. A Grid of size 10x10 is initialised with different colors. One controls the upper left corner, by swapping the color of that piece one can enlarge the controlled area until it is the whole board.
## Prerequisites
### Python
- The program assumes python3.5 (Which is necessary for the webSocketServer)
It requires python websockets to be installed
	`pip install websockets`

### Elm
To compile an index.html file one requires the functional programming language https://guide.elm-lang.org/install.html.
After installing run
	`elm-package install -y`
	`elm-make src/Main.elm`

## Play the Game
Run
	`git clone https://github.com/stymphalide/flow.git
	elm-make src/Main.elm
	python3.5 src/api.py`
Then open the indx.html file in a browser.

## AI
The goal is to train a simple bot to play that game.
Not very amazing results yet.

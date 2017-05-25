# ![Hexplode](hexplode/static/img/hexplode-logo.png)

Chain reaction strategy game as featured in the [Man AHL Coder Prize 2016](http://www.ahl.com/coderprize2016)

You can [play the demo online.](http://hexplode.pythonanywhere.com/)

Hexplode is played by 2 players on a board of hexagonal tiles. The players take turns to place a counter on the board,
they can only play a counter in an empty tile or a tile they already own. When the number of counters on a given tile
equals the number of adjacent tiles the tile hexplodes and the contents of the tile are equally distributed to its
neighbours changing the ownership of neighbouring counters over to the current player in the process. This process can
often generate a chain reaction. The winner is the player that removes all of their opponents counters from the board.

This repo contains an implementation of the game that was used in the Man AHL Coder Prize 2016 competition. It allows
you to write algo players in python and play against them or have them play against each other.

This repo contains everything you need to run the game including all the 3rd party libraries it depends on.

Once you have cloned the repo run ```python game.py``` to launch the game in your browser. The only requirements on
your system are python* and a relatively up-to-date web browser. 

The challenge in the original competition was to write an algo player for the game and two example algo players were
provided in the algos package to help entrants get started. You can measure the relative performance of all your algos
by running ```python simulate.py```.

The game of Hexplode originally appeared in 1982 in PCW (Personal Computer World) magazine as a BASIC program for the BBC Micro written by J. Ansell.

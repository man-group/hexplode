Hexplode is played by 2 players on a board of hexagonal tiles. The players take turns to place a counter on the board,
they can only play a counter in an empty tile or a tile they already own. When the number of counters on a given tile
equals the number of adjacent tiles the tile hexplodes and the contents of the tile are equally distributed to its
neighbours changing the ownership of neighbouring counters over to the current player in the process. This process can
often generate a chain reaction. The winner is the player that removes all of their opponents counters from the board.

This bundle contains an implementation of the game that allows you to write algo players in python and play against them
or have them play against each other. It should contain everything you need to run the game, once you have cloned it 
run ```python game.py``` to launch the game in your browser. The only requirements on your system are python* and a
relatively up-to-date web browser. 

Your challenge is to write an algo player for the game, there are two example algo players in the algos package to help
you get started. You can measure the relative performance of all your algos by running ```python simulate.py```. Your
competition entry should just be the python module for your algo.

* will work with python 2.7 and 3.3 onwards but all submissions must be python 3.4
from hexplode import algo_player
import random


@algo_player(name="Random Player",
             description="Picks tiles at random.")
def random_player(board, game_id, player_id):
    '''
    Example implementation of an algo player for the game Hexplode

    The function takes the current board state and the id of the game and player
    it is playing in and for and returns the id of the tile it wishes to place a
    counter in.

    If an algo returns an invalid move or takes too long to make a move it will
    forfeit the game.

    This particular algo implementation simply places its counter in a tile
    selected at random from all the tiles it would be legal to pay in.

    :param board:
        The current state of the board. This is a dict of the form::
            {
                <tile id>: {
                    'counters': <number of counters on tile or None>,
                    'player': <player id of the player who holds the tile or None>,
                    'neighbours': <list of ids of neighbouring tile>
                },
                ...
            }
    :param game_id:
        The id of the game that the algo is playing in.
    :param player_id:
        The id of the player that the algo is playing on behalf of.
    :returns:
        The id of a tile the algo wishes to place a counter in.
    '''
    # Find tiles that are not owned by my opponent(s), they are legal to play in
    legal_moves = []
    for tile_id, tile in board.items():
        if tile["player"] is None or tile["player"] == player_id:
            legal_moves.append(tile_id)

    # Pick a tile at random
    return random.choice(legal_moves)

from hexplode import algo_player


@algo_player(name="Corner Hugger",
             description="Hangs out in the corners")
def corner_hugger(board, game_id, player_id):
    '''
    Example implementation of an algo player for the game Hexplode

    The function takes the current board state and the id of the game and player
    it is playing in and for and returns the id of the tile it wishes to place a
    counter in.

    If an algo returns an invalid move or takes too long to make a move it will
    forfeit the game.

    This particular algo implementation finds a tile that is closest to
    exploding and places its counter in it. This rule generally causes it to
    build out from a corner and prefer explosions.

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
    # Put the legal moves into buckets based on the number of counters they are
    # away from exploding
    possible_moves = {}
    for tile_id, tile in board.items():
        if tile["player"] is None:
            possible_moves.setdefault(len(tile["neighbours"]), []).append(tile_id)
        elif tile["player"] == player_id:
            possible_moves.setdefault(len(tile["neighbours"]) - tile["counters"], []).append(tile_id)

    # Pick the moves closest to an explosion
    best_moves = possible_moves[min(possible_moves)]

    # Return the first one
    return best_moves[0]


@corner_hugger.on_start_game
def start_game(game_id, player_id, boardsize, opponent_id):
    '''
    Example implementation of a start game handler for an algo player in the
    game Hexplode. Your algo does not need to implement this event handler but
    may choose to do so if any form of pre-game preparation or processing is
    required.

    The function takes the the id of the game the algo will be playing in, the
    id of the player the algo will play for, the board size and the id of the
    opposing algorithm. No return value is expected. 

    This example algo implementation does not actually need to perform any steps
    at the start of the game but uses the event as a opportunity to update its own
    score of how many game it has played.

    :param game_id:
        The id of the game that the algo was playing in.
    :param player_id:
        The id of the player that the algo was playing on behalf of.
    :param boardsize:
        The board will be a hexagon with side <boardsize> tiles.
    :param opponent_id:
        The id of the opposing algorithm, will be 'Human' if the opponent is
        not an algo player.
    '''
    global games_played
    games_played += 1


games_played = 0


@corner_hugger.on_game_over
def game_over(board, game_id, player_id, winner_id):
    '''
    Example implementation of a game over handler for an algo player in the game
    Hexplode. Your algo does not need to implement this event handler but may
    choose to do so if any form of post game clean-up or processing is required.

    The function takes the final board state, the id of the game the algo was
    playing in, the id of the player the algo was playing for and the id of the
    winning player. No return value is expected. 

    This example algo implementation does not actually need to perform any steps
    at the end of the game but uses the event as a opportunity to update its own
    score of how well it is doing.

    :param board:
        The final state of the board. This is a dict of the form::
            {
                <tile id>: {
                    'counters': <number of counters on tile or None>,
                    'player': <player id of the player who holds the tile or None>,
                    'neighbours': <list of ids of neighbouring tile>
                },
                ...
            }
    :param game_id:
        The id of the game that the algo was playing in.
    :param player_id:
        The id of the player that the algo was playing on behalf of.
    :param winner_id:
        The id of the winning player.
    '''
    global games_won
    if winner_id == player_id:
        games_won += 1


games_won = 0

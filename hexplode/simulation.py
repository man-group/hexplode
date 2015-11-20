from __future__ import print_function
from uuid import uuid4
from .algos import _algos
from .app import algo_name_to_uuid
from itertools import combinations
from datetime import datetime, timedelta
from traceback import format_exc
from copy import deepcopy
from sys import stderr
import os
try:
    from texttable import Texttable
except ImportError:
    # If texttable isn't installed fall back to the copy in ./dependencies
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "dependencies"))
    from texttable import Texttable


MOVE_TIMEOUT = timedelta(seconds=5)


def _log_err(msg):
    stderr.write(msg)
    stderr.write(os.linesep)
    stderr.flush()


def _make_id(i, j):
    return "tile_{}_{}".format(i, j)


def _make_neighbours(i, j, boardsize):
    maxi = 2 * boardsize - 1
    maxj = min(boardsize + i, 3 * boardsize - 2 - i)
    neighbours = []

    if j - 1 >= 0:
        neighbours.append(_make_id(i, j - 1))  # North neighbour
    if j + 1 < maxj:
        neighbours.append(_make_id(i, j + 1))  # South neighbour
    if i < (maxi - 1) / 2:
        # West of the central column
        neighbours.append(_make_id(i + 1, j))  # Northeast neighbour
        neighbours.append(_make_id(i + 1, j + 1))  # Southeast neighbour
        if i - 1 >= 0:
            # East of the first column
            if j - 1 >= 0:
                neighbours.append(_make_id(i - 1, j - 1))  # Northwest neighbour
            if j < maxj - 1:
                neighbours.append(_make_id(i - 1, j))  # Southwest neighbour
    elif i > ((maxi - 1) / 2):
        # East of the central column
        neighbours.append(_make_id(i - 1, j))  # Northwest neighbour
        neighbours.append(_make_id(i - 1, j + 1))  # Soutwest neighbour
        if i + 1 < maxi:
            # West of the last column
            if j - 1 >= 0:
                neighbours.append(_make_id(i + 1, j - 1))  # Northeast neighbour
            if j < maxj - 1:
                neighbours.append(_make_id(i + 1, j))  # Southeast neighbour
    else:
        # On the central column
        if j - 1 >= 0:
            neighbours.append(_make_id(i - 1, j - 1))  # Northwest neighbour
            neighbours.append(_make_id(i + 1, j - 1))  # Northeast neighbour
        if j < maxj - 1:
            neighbours.append(_make_id(i - 1, j))  # Southwest neighbour
            neighbours.append(_make_id(i + 1, j))  # Southeast neighbour
    return neighbours


def _make_board(boardsize):
    return {_make_id(i, j): dict(counters=None,
                                 player=None,
                                 neighbours=_make_neighbours(i, j, boardsize))
            for i in range(2 * boardsize - 1)
            for j in range(min(boardsize + i, 3 * boardsize - 2 - i))}


def _place_counter(board, tile_id, scores, player_id):
    if not _player_has_all_the_counters(scores, player_id):
        tile = board[tile_id]

        if tile["player"] is not None and tile["counters"] is not None:
            scores[tile["player"]] -= tile["counters"]

        counters = (tile["counters"] if tile["counters"] else 0) + 1
        if counters == len(tile["neighbours"]):
            tile["player"] = None
            tile["counters"] = None
            for neighbour in tile["neighbours"]:
                _place_counter(board, neighbour, scores, player_id)
        else:
            tile["player"] = player_id
            tile["counters"] = counters
            scores[player_id] += counters


def _player_has_all_the_counters(scores, player_id):
    return sum(scores) > len(scores) and all([score <= 0 for pid, score in enumerate(scores) if pid != player_id])


def _is_game_over(scores):
    return any([_player_has_all_the_counters(scores, playerId) for playerId, _ in enumerate(scores)]) 


def _is_valid_move(board, move, player_id):
    return board[move]["player"] in (None, player_id)

   
def send_game_over(board, game_id, winner_id, algo_game_over_handlers, deepcopy):
    for player_id, handler in enumerate(algo_game_over_handlers):
        if handler is not None:
            try:
                handler(deepcopy(board), game_id[player_id], player_id, winner_id)
            except:
                _log_err("Error from Player {} when handling game over:".format(player_id + 1))
                _log_err(format_exc())

   
def send_start_game(game_id, boardsize, algo_ids, algo_start_game_handlers):
    for player_id, handler in enumerate(algo_start_game_handlers):
        if handler is not None:
            try:
                handler(game_id[player_id], player_id, boardsize, algo_ids[(player_id + 1) % 2])
            except:
                _log_err("Error from Player {} when handling start game.".format(player_id + 1))
                _log_err(format_exc())


def run_test(algos,
             algo_ids,
             algo_start_game_handlers,
             algo_game_over_handlers,
             boardsize,
             deepcopy):
    game_id = [uuid4() for _ in algos]
    send_start_game(game_id, boardsize, algo_ids, algo_start_game_handlers)
    board = _make_board(boardsize)
    scores = [0] * len(algos)
    player_id = 0
    moves = 0
    while not _is_game_over(scores):
        try:
            then = datetime.now()
            move = algos[player_id](deepcopy(board), game_id[player_id], player_id)
            time_taken = datetime.now() - then

            if time_taken > MOVE_TIMEOUT:
                raise RuntimeError("Took too long to make move {}".format(time_taken))
            if  not _is_valid_move(board, move, player_id):
                raise RuntimeError("Made illegal move {}".format(move))
        except:
            _log_err("Error from Player {}".format(player_id + 1))
            _log_err(format_exc())
            winner_id = (player_id + 1) % 2  # The other guy won
            send_game_over(board, game_id, winner_id, algo_game_over_handlers, deepcopy)
            return winner_id, moves, True

        _place_counter(board, move, scores, player_id)
        moves += 1

        player_id = (player_id + 1) % len(algos)

    winner_id = scores.index(max(scores))
    send_game_over(board, game_id, winner_id, algo_game_over_handlers, deepcopy)
    return winner_id, moves, False


def run_simulation(algo_1, algo_2, boardsize, iterations, do_deepcopy):
    algo_names = [algo_1, algo_2]
    algo_ids = list(map(algo_name_to_uuid, algo_names))
    algo_fns = [_algos[algo_id].fn for algo_id in algo_names]
    algo_game_over_handlers = [_algos[algo_id].on_game_over for algo_id in algo_names]
    algo_start_game_handlers = [_algos[algo_id].on_start_game for algo_id in algo_names]
    
    results = []
    stats = {}
    for _ in range(iterations):
        winner_id, moves, default = run_test(algo_fns,
                                             algo_ids,
                                             algo_start_game_handlers,
                                             algo_game_over_handlers,
                                             boardsize,
                                             deepcopy if do_deepcopy else lambda x: x)
        
        winner_name = algo_names[winner_id]
        results.append(winner_name)
        stats.setdefault(winner_name, dict(moves=0, default=0, wins=0))
        stats[winner_name]['moves'] += moves
        stats[winner_name]['default'] += int(default)
        stats[winner_name]['wins'] += 1.0
        algo_names.reverse()
        algo_ids.reverse()
        algo_fns.reverse()
        algo_game_over_handlers.reverse()
        algo_start_game_handlers.reverse()

    return results, stats


def simulate_all_with_stats(boardsize, iterations, do_deepcopy=True):
    algos = _algos.keys()
    if len(algos) < 2:
        print("Only {} algo defined - can't simulate.".format(len(algos)))
        return []
    results = {algo: 0 for algo in algos}
    total_stats = {}
    print("Running simulation...")
    for algo_1, algo_2 in combinations(algos, 2):
        winners, stats = run_simulation(algo_1,
                                        algo_2,
                                        boardsize=boardsize,
                                        iterations=iterations,
                                        do_deepcopy=do_deepcopy)
                                      
        algo_1_wins = len(list(filter(lambda x: x == algo_1, winners)))
        algo_2_wins = len(winners) - algo_1_wins

        print("{}({}) vs {}({})".format(algo_1, algo_1_wins,
                                        algo_2, algo_2_wins))

        results[algo_1] += algo_1_wins
        results[algo_2] += algo_2_wins
        
        for algo in set(stats.keys()).intersection(total_stats.keys()):
            for col in total_stats[algo].keys():
                total_stats[algo][col] += stats[algo][col]
        for algo in set(stats.keys()) - set(total_stats.keys()):
                total_stats[algo] = stats[algo]
            
        
    return list(reversed(sorted(results.items(), key=lambda item: item[1]))), total_stats


def simulate_all(boardsize, iterations, do_deepcopy=True):
    return simulate_all_with_stats(boardsize, iterations, do_deepcopy)[0]


def display_table(results):
    table = Texttable()
    table.set_cols_align(["l", "r"])
    table.set_deco(Texttable.BORDER | Texttable.HEADER | Texttable.VLINES)
    table.add_rows([["Algo", "Wins"]] + results)
    print(table.draw()) 


def display_stats(stats):
    stats = [[a, s['moves'] / s['wins'], s['default'] / s['wins']] for a, s in stats.items()]
    table = Texttable()
    table.set_cols_align(["l", "r", "r"])
    table.set_deco(Texttable.BORDER | Texttable.HEADER | Texttable.VLINES)
    table.add_rows([["Algo", "Moves", "Defaults"]] + stats)
    print(table.draw()) 

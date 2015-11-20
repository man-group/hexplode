from collections import namedtuple
import platform
import re
ALLOWED_ALGO_NAME = re.compile("^[a-zA-Z0-9 _-]+$")


AlgoMetaData = namedtuple("AlgoMetaData", "description,fn,on_game_over,on_start_game")
_algos = {}


def _filename(fn):
    if platform.python_version_tuple()[0] == '2':
        return fn.func_code.co_filename
    else:
        return fn.__code__.co_filename


def algo_player(name, description):
    def _on_game_over(fn):
        _algos[name] = AlgoMetaData(description=_algos[name].description,
                                    fn=_algos[name].fn,
                                    on_game_over=fn,
                                    on_start_game=_algos[name].on_start_game)
        return fn

    def _on_start_game(fn):
        _algos[name] = AlgoMetaData(description=_algos[name].description,
                                    fn=_algos[name].fn,
                                    on_game_over=_algos[name].on_game_over,
                                    on_start_game=fn)
        return fn

    def _algo(fn):
        if name in _algos:
            raise ValueError("Algo '{}' is already defined.".format(name))
        elif not ALLOWED_ALGO_NAME.match(name):
            raise ValueError("Algos can only have names containing letters,"
                             " numbers, space, underscore and hyphen.")
        elif _filename(fn) in {_filename(i.fn) for i in _algos.values()}:
            raise ValueError("You must put each algo in its own file.")
        else:
            _algos[name] = AlgoMetaData(description=description,
                                        fn=fn,
                                        on_game_over=None,
                                        on_start_game=None)
            fn.on_game_over = _on_game_over
            fn.on_start_game = _on_start_game
            return fn

    return _algo

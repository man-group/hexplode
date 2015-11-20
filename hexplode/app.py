import os
from ._flask import Flask, send_file, json, request
import webbrowser
from .algos import _algos, _filename
from uuid import uuid4
from traceback import format_exc
import subprocess
import platform


_PORT = 5000
app = Flask(__name__)


@app.route('/')
def game_page():
    return send_file('static/hexplode.html')


@app.route('/algos')
def list_algos():
    try:
        return json.dumps({"ok" : {algo_name: algo.description for algo_name, algo in _algos.items()}})
    except:
        return json.dumps({"error" : format_exc()})


@app.route('/algos/<algo_name>', methods=['POST'])
def move(algo_name):
    try:
        data = request.json
        return json.dumps({"ok" : _algos[algo_name].fn(data["board"], data["gameId"], data["playerId"])})
    except:
        return json.dumps({"error" : format_exc()})


algo_uuids = {'Human': 'Human'}


def algo_name_to_uuid(algo_name):
    return algo_uuids.setdefault(algo_name, uuid4())


@app.route('/newgame', methods=['POST'])
def new_game():
    try:
        data = request.json
        algo_names = data['player1'], data['player2']
        game_id = [str(uuid4()) for _ in range(2)]

        for player_id, algo_name in enumerate(algo_names):
            if algo_name != "Human":
                event_handler = _algos[algo_name].on_start_game
                if event_handler is not None:
                    event_handler(game_id[player_id],
                                  player_id,
                                  data['boardsize'],
                                  algo_name_to_uuid(algo_names[(player_id + 1) % 2]))
        
        return json.dumps({"ok" : game_id})
    except:
        return json.dumps({"error" : format_exc()})


@app.route('/gameover/<algo_name>', methods=['POST'])
def game_over(algo_name):
    try:
        data = request.json
        event_handler = _algos[algo_name].on_game_over
        if event_handler is not None:
            event_handler(data["board"], data["gameId"], data["playerId"], data["winnerId"])
        return json.dumps({"ok" : "ok"})
    except:
        return json.dumps({"error" : format_exc()})


@app.route('/startgame/<algo_name>', methods=['POST'])
def start_game(algo_name):
    try:
        data = request.json
        event_handler = _algos[algo_name].on_start_game
        if event_handler is not None:
            event_handler(data["gameId"], data["playerId"], data["boardsize"], data["opponentId"])
        return json.dumps({"ok" : "ok"})
    except:
        return json.dumps({"error" : format_exc()})


def _verify_impl(filepath):
    from hexplode.simulation import simulate_all
    from hexplode.algos import _algos
    import imp
    from os.path import basename, splitext
    map(_algos.pop, list(_algos))
    imp.load_source(splitext(basename(filepath))[0], filepath)
    assert len(_algos) == 1
    algo_name = list(_algos.keys())[0]
    _algos[algo_name + "_copy"] = _algos[algo_name] 
    return simulate_all(boardsize=4, iterations=1)


@app.route('/verify/<algo_name>')
def verify_algo(algo_name):
    try:
        # TODO: I'd like to run this in a more sandboxed way, ATM this doesn't
        # give much over just calling the inmemory copy we already have 
        algo_file = _filename(_algos[algo_name].fn)
        from multiprocessing import Process 
        p = Process(target=_verify_impl, args=(algo_file,))
        p.start()
        p.join()
        return json.dumps({"ok" : "ok"})
    except:
        return json.dumps({"error" : format_exc()})

    
def browser(hostname, port, debug):
    if 'SUPPRESS_BROWSER_START' not in os.environ:
        if debug:
            # If we have reloading turned on, suppress future browser starts
            os.environ['SUPPRESS_BROWSER_START'] = ""
        webbrowser.open_new_tab("http://{}:{}".format(hostname, port))


def start_other(hostname, port, debug, open_browser):
    if open_browser:
        browser(hostname, port, debug)
    from werkzeug.serving import WSGIRequestHandler
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(host=hostname,
            port=port,
            debug=debug)


def is_nginx_up():
    if platform.python_version_tuple()[0] == '2':
        from urllib2 import urlopen, URLError
    else:
        from urllib.request import urlopen
        from urllib.error import URLError
    try:
        urlopen("http://localhost:{}/".format(_PORT)).close()
    except URLError:
        return False
    return True


def start_windows(debug, open_browser):
    nginx_dir = os.path.join(os.path.dirname(__file__), "dependencies", "nginx")
    nginx_exe = os.path.join(nginx_dir, "nginx.exe")

    if not is_nginx_up():
        subprocess.Popen(nginx_exe, cwd=nginx_dir)

    try:
        from flup.server.fcgi import WSGIServer
    except ImportError:
        # If flup isn't installed fall back to the copy in ./dependencies
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), "dependencies"))
        from flup.server.fcgi import WSGIServer

    if open_browser:
        browser('localhost', _PORT, debug)
    WSGIServer(app, debug=debug, bindAddress=('localhost', _PORT + 1)).run()
    

def start(hostname='localhost', port=_PORT, debug=True, open_browser=True):
    if (platform.system() == "Windows"
        and hostname == 'localhost'
        and port == _PORT):
        start_windows(debug, open_browser)
    else:
        start_other(hostname, port, debug, open_browser)

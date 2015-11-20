import os

try:
    from requests import *
except ImportError:
    # If requests isn't installed fall back to the copy in ./dependencies
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "dependencies"))
    from requests import *

del os

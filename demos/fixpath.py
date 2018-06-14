# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.

# Add demo dir's parent to sys path, so that 'import colorama' always finds
# the local source in preference to any installed version of colorama.
import sys
from os.path import normpath, dirname, join
local_colorama_module = normpath(join(dirname(__file__), '..'))
sys.path.insert(0, local_colorama_module)

Unicorp Turtles 42
##################

Untitled game for pyweek 42

Config
******

On running, if it doesn't exist a config file will be created.
- on linux, at ~/.config/unicorp_turtles_42/config.json
- on windows, at $HOME\Application Settings\unicorp_turtles_42\config.json
- on Mac OS X, at ~Library/Application Support/unicorp_turtles_42/config.json

That file contains actions like LEFT or FIRE mapped to list of key that will
trigger such actions. The full list is available at
https://pyglet.readthedocs.io/en/latest/modules/window_key.html#key-constants

Build
*****

Require pex to be available in path, maybe a venv activated with the project
and build installed.

.. code:: bash

	python -m build
	pex pyglet dist/unicorp_turtles_42-*.whl -c turtle -o dist/unicorp-turtles-42



# DPongPy

Didactical implementation of PONG as an online multiplayer game, aimed at exemplifying distributed systems.

## Relevant features

- Supports offline game (1-4 players, no AI)
- No points, no winner, just 1-4 paddles and a ball
- Supports online game (1-4 players, no AI) via UDP

## How to install

```bash
pip install dpongpy
```

## How to play

Run `python -m dpongpy --help` to see the available options.

Two modes are available: 
- `local` for playing offline (all players sharing the same keyboard) 
- `centralised` for online (all players connecting to a central server)

When in `centralised` mode, the server must be started first, and the clients must _connect_ to it.
In this case, the server is called `coordinator`, and the clients are called `terminal`s.
You should start the coordinator first, and then the terminals.
The `coordinator` instance of `dpongpy` shall keep track of the game state and update it according to the inputs coming from the `terminal` instances.
When a `coordinator` is started, no window is shown, yet logs may be printed on the console.
When a `terminal` is started, a window is shown, and the game can be played (provided that the `coordinator` is running).
Terminals may observe that the ball is reset to the central position whenever a player joins or leaves the game.

When in `local` mode, the game will include, by default, 2 paddles and the ball.
Users may specify which and how many paddles to include in their game via the `--size` option (`-s`).
After the `--side` option, you shall specify the side of the paddle (i.e. `left`, `right`, `up`, or `down`).
You should also specify which key mappings to use for each paddle, via the `--keys` option (`-k`).
Available key mappings are `wasd`, `ijkl`, `arrows`, and `numpad`.
You should specify the key mapping for each paddle, in the order they were specified via the `--side` option.
Therefore, default options are: `-s left -k wasd -s right -k arrows`.

When in `centralised` mode, it is up to `terminal`s to choose their paddle and the corresponding key mapping.
This is done, once again, via the `--side` and `--keys` options.
In this case, however, there is no default choice, and the user __must__ specify the side and key mapping of the paddle they want to control.


## Project structure

Overview:
```bash
<root directory>
├── CHANGELOG.md            # Changelog for the last stable release
├── dpongpy                 # Main package
│   ├── __init__.py         # Main module: here we implement the game loop business logic for the local game
│   ├── __main__.py         # Main module's entry point: this is where argument parsing occurs
│   ├── log.py              # Logging utilities
│   ├── model.py            # Model module: here we define classes for Pong-related domain entities (paddle, ball, game)
│   ├── controller          # Controller package
│   │   ├── __init__.py     # Controller module: here we define interfaces for input and event handlers
│   │   └── local.py        # Local controller module: here we implement the afore mentioned interfaces in a non-distributed way
│   ├── view.py             # View module: here we define the game rendering logic
│   └── remote              # Remote package
│       ├── __init__.py     # Remote module: here we define interfaces for remote communication (client, server, address) in a protocol-agnostic way
│       ├── udp.py          # UDP module: here we implement the afore mentioned interfaces in a UDP-specific way
│       ├── presentation.py # Presentation module: facilities for (de)serializing Pong-related domain entities
│       └── centralised     # Centralised package
│           └── __init__.py # Centralised module: here we re-define the game loop business logic to work as either centralised server or a terminal client
├── LICENSE                 # License file
├── package.json            # NPM package file (for semantic-release)
├── package-lock.json       # NPM package lock file (for semantic-release)
├── poetry.lock             # Poetry lock file for fixing Python dependencies
├── poetry.toml             # Poetry configuration file
├── pyproject.toml          # Project metadata definition, compliant to the Poetry standard
├── README.md               
├── release.config.js       # semantic-release configuration file (for release on PyPI)
├── renovate.json           # Renovate configuration file (for automatic dependency updates)
├── requirements.txt        # Use this to automatically install Poetry dependencies, then run `poetry install` to actually install the project dependencies
└── tests                   # Unit tests of the project: the file names are self-explanatory
    ├── test_model.py
    ├── test_presentation.py
    └── test_udp.py
```

# AngryBirds Game

"Angry Birds game created using python and pygame"

Author: Sayan Mandal

The main objective of making this game is to extend the single-player version of the original Angry Birds game to a turn-by-turn based two-player game where each player aims to destroy the opponents fortress by launching projectile from his slingshot.

## Directory Structure


The structure of the project directory is as follows:

```bash

AngryBirds/
├── README.md
├── scripts/
│   ├── Game.py
│   └── MainMenu.py
│   └── birds.py
│   └── blocks.py
│   └── utils.py
├── Media
│   ├── Fonts
│   ├── Sprites
├── Data/
│   ├── GameHistory.csv
├── Report
│   ├── Screenshots
│   ├── Report.tex
│   ├── Report.pdf
└── main.py

```

• Scripts – Various scripts that manages various parts of the game
• Media - Contains sprites and fonts used in the game
• Data – Contains player scores of the last 10 games played
• main.py – Main game loop
• Report - Contains report of the project

## Instructions to run

1. Clone the repository:
```bash 
git clone <https://github.com/SayanMandal1001/AngryBirds.git>
```

2. Python must be installed on the device prior to this. Then the pygame module must be installed using the following command:
```bash
pip install pygame
```

3. To run the program, open the terminal in the directory containing ”main.py” and then use one of the following commands whichever is suitable.
```bash
python main.py
```
```bash
python3 main.py
```

Note: For further information refer to the 'Report.pdf' file present in the Report folder.
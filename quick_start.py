import importlib
import importlib.util as util
import os, sys

# check if directory is correct
assert os.getcwd().split("/")[-1] == 'pygame_towerdefense'

# check if venv exist
if (not os.path.isdir("./venv")):
    os.system("bash ./setup_virtualenv.sh")

# check if pygame exist
if (util.find_spec("pygame") is None):
    os.system(f"{os.getcwd()}/venv/bin/pip install -r requirements.txt")

# # run the game
run_game = importlib.import_module('game.main')



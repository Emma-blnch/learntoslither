check mémoire : valgrind --tool=memcheck python3 main.py -sessions 1 -visual off

# Activer le venv
source .venv/bin/activate

# Test headless (rapide, pas besoin d'écran)
python3 main.py -sessions 20 -visual off

# Test avec fenêtre pygame
python3 main.py -sessions 3 -visual on -speed 6

# Test board-size bonus
python3 main.py -sessions 5 -visual on -board-size 15 -speed 8

# Vérifier la norme localement
python3 -m flake8 --max-line-length=79 --exclude=__pycache__,.git,.venv .

check mémoire : valgrind --tool=memcheck python3 main.py -sessions 1 -visual off

# Activer le venv
source .venv/bin/activate

# Test headless (rapide, pas besoin d'écran)
python3 src/main.py -sessions 20 -visual off

# Test avec fenêtre pygame
python3 src/main.py -sessions 3 -visual on -speed 6

# Test board-size bonus
python3 src/main.py -sessions 5 -visual on -board-size 15 -speed 8

# Vérifier la norme localement
./scripts/norm.sh

# Évaluer sans apprendre
python3 src/main.py -sessions 20 -visual off -load models/5000sess.json -dontlearn
python3 src/main.py -sessions 20 -visual off -load models/100sess.json -dontlearn

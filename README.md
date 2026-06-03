# Learn2Slither — Reinforcement Learning Snake

Un serpent qui apprend à survivre et à grandir par essais et erreurs,
en utilisant le Q-learning (reinforcement learning).

---

## Notions clés

### Reinforcement Learning (RL)
Paradigme d'apprentissage où un agent interagit avec un environnement,
reçoit des récompenses ou punitions, et ajuste son comportement pour
maximiser les récompenses cumulées au fil du temps.

### Q-learning
Algorithme de RL qui maintient une table de valeurs Q(état, action)
représentant la qualité estimée d'une action dans un état donné.

Formule de mise à jour :
```
Q(s, a) = Q(s, a) + α * (r + γ * max(Q(s', a')) - Q(s, a))
```
- `α` (alpha) : taux d'apprentissage — vitesse de mise à jour des Q-valeurs
- `γ` (gamma) : facteur d'actualisation — importance des récompenses futures
- `r` : récompense immédiate reçue
- `s'` : état suivant après l'action

### Exploration vs Exploitation (epsilon-greedy)
- **Exploration** : action aléatoire (probabilité epsilon) — découvrir de nouveaux états
- **Exploitation** : meilleure action connue (probabilité 1-epsilon) — utiliser ce qui a été appris
- Epsilon décroît au fil des sessions : le serpent explore moins et exploite plus

### State (vision du serpent)
Le serpent ne voit que dans les 4 directions cardinales depuis sa tête.
Chaque direction est encodée comme une string de caractères :
- `W` = Wall (mur)
- `H` = Snake Head (tête)
- `S` = Snake body Segment (corps)
- `G` = Green apple (pomme verte)
- `R` = Red apple (pomme rouge)
- `0` = Empty (case vide)

La clé d'état donnée à l'agent encode pour chaque direction :
- danger immédiat dans la case suivante (0/1)
- présence d'une pomme verte dans cette direction (0/1)
- présence d'une pomme rouge dans cette direction (0/1)

→ Max 4096 états possibles, Q-table convergée en ~1000 sessions.

### Architecture modulaire
```
Environment → Interpreter → Agent → Environment
```
- **Environment** : grille, serpent, pommes, règles du jeu
- **Interpreter** : lit l'environnement, produit la vision et le reward
- **Agent** : reçoit état + reward, met à jour la Q-table, choisit l'action

---

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Utilisation

```bash
# Syntaxe générale
./scripts/snake [options]

# Options disponibles
-sessions N          nombre de sessions d'entraînement (défaut: 1)
-visual on|off       affichage pygame (défaut: on)
-save PATH           sauvegarder le modèle après entraînement
-load PATH           charger un modèle existant
-dontlearn           désactiver l'apprentissage (évaluation pure)
-step-by-step        avancer manuellement (touche pour chaque step)
-speed FPS           vitesse d'affichage en frames/sec (défaut: 10)
-board-size N        taille du board NxN (défaut: 10)
-max-steps N         limite de steps par session (défaut: board_size^2 * 10)
```

---

## Commandes de test

### Fonctionnement de base
```bash
# Training court headless
./scripts/snake -sessions 100 -visual off

# Training avec affichage
./scripts/snake -sessions 5 -visual on -speed 8

# Training et sauvegarde du modèle
./scripts/snake -sessions 1000 -visual off -save models/1000sess.json

# Charger un modèle et continuer à apprendre
./scripts/snake -sessions 500 -visual off \
    -load models/1000sess.json -save models/1500sess.json
```

### Évaluation des modèles (sans apprentissage)
```bash
# Évaluer un modèle sur 20 sessions
./scripts/snake -sessions 20 -visual off \
    -load models/1000sess.json -dontlearn

# Évaluer avec affichage et step-by-step
./scripts/snake -sessions 3 -visual on \
    -load models/1000sess.json -dontlearn -step-by-step -speed 5

# Comparer 3 niveaux d'entraînement
./scripts/snake -sessions 20 -visual off -load models/1sess.json   -dontlearn
./scripts/snake -sessions 20 -visual off -load models/10sess.json  -dontlearn
./scripts/snake -sessions 20 -visual off -load models/100sess.json -dontlearn
```

### Bonus — taille de board variable
```bash
# Board 5x5 avec le modèle entraîné sur 10x10
./scripts/snake -sessions 5 -visual on \
    -load models/1000sess.json -dontlearn -board-size 5

# Board 20x20 avec le même modèle
./scripts/snake -sessions 5 -visual on \
    -load models/1000sess.json -dontlearn -board-size 20
```

### Générer les modèles obligatoires (soutenance)
```bash
./scripts/snake -sessions 1    -visual off -save models/1sess.json
./scripts/snake -sessions 10   -visual off -save models/10sess.json
./scripts/snake -sessions 100  -visual off -save models/100sess.json
./scripts/snake -sessions 1000 -visual off -save models/1000sess.json
```

### Vérification mémoire et qualité
```bash
# Norme flake8 (via Docker)
./scripts/norm.sh

# Mémoire avec faulthandler (segfaults extensions C)
PYTHONFAULTHANDLER=1 ./scripts/snake -sessions 1000 -visual off

# Surveillance RAM pendant un long training
./scripts/snake -sessions 10000 -visual off -save models/10000sess.json &
watch -n 2 "ps -o pid,rss,comm -p \$(pgrep -f main.py) \
    | awk '{print \$1, \$2/1024\"MB\", \$3}'"
```

### Cas d'erreur attendus
```bash
# Argument de mauvais type -> usage argparse + exit 1
./scripts/snake -sessions abc -visual off

# Sessions négatif -> boucle vide, termine proprement
./scripts/snake -sessions -5 -visual off
# Game over, max length = 0, max duration = 0

# Sessions 0 -> termine immédiatement
./scripts/snake -sessions 0 -visual off
# Game over, max length = 0, max duration = 0

# Board trop petit (< 3) -> message clair + exit 1
./scripts/snake -sessions 1 -visual off -board-size 2
# Error: board-size must be at least 3

./scripts/snake -sessions 1 -visual off -board-size 0
# Error: board-size must be at least 3

# Modèle inexistant -> message clair + exit 1
./scripts/snake -sessions 1 -visual off -load models/inexistant.json
# Error: model file not found: models/inexistant.json

# Modèle corrompu ou fichier invalide -> message clair + exit 1
./scripts/snake -sessions 1 -visual off -load /tmp/corrupt.json
# Error: invalid model file: /tmp/corrupt.json

# Save vers un chemin inexistant -> session tourne, erreur à la sauvegarde
./scripts/snake -sessions 1 -visual off -save /nonexistent/path/model.json
# Game over, max length = X, max duration = Y
# Error: cannot save model: [Errno 2] No such file or directory: ...

# Aucun argument -> session unique avec valeurs par défaut (visual on)
./scripts/snake
```

---

## Structure du projet

```
learn2slither/
├── src/
│   ├── main.py         # CLI, boucle principale
│   ├── environment.py  # Board, règles du jeu
│   ├── snake.py        # Structure de données du serpent
│   ├── interpreter.py  # Vision, état, rewards
│   ├── agent.py        # Q-table, apprentissage
│   ├── display.py      # Affichage pygame + terminal
│   └── constants.py    # Hyperparamètres, couleurs, constantes
├── models/             # Modèles sauvegardés (.json)
├── scripts/
│   ├── snake           # Exécutable principal
│   └── norm.sh         # Vérification norme flake8
├── Dockerfile
└── requirements.txt
```

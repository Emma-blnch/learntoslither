# 🐍 Learn2Slither — Snake AI with Reinforcement Learning

A snake that learns to survive and grow by trial and error, using **Q-learning**,
built from scratch in Python. 42 Paris project.

The snake only sees what is in the 4 directions from its head. It has to learn
to eat green apples (+1 length), avoid red apples (−1 length), and not crash
into walls or itself.

## 📊 Results

Evaluation over 100 games on a 10×10 board, learning disabled:

| model | average length | max length | red apples among apples eaten |
|---|---|---|---|
| after 100 training sessions | 3.8 | 6 | 31 % |
| **after 1,000 training sessions** | **16.4** | **32** | **2 %** |

After 1,000 sessions the snake has learned to avoid red apples almost entirely
and to reach a length of 32 on a 100-cell board.

![statistics of the 1,000-session model](docs/eval_1000sess.png)

## 🧠 How it works

**Q-learning.** The agent keeps a table of values Q(state, action), the expected
quality of each action in each state, updated after every move:

```
Q(s, a) = Q(s, a) + α · (r + γ · max Q(s', a') − Q(s, a))
```

- `α`: learning rate · `γ`: discount factor (weight of future rewards)
- `r`: reward (green apple +15, red apple −10, each step −0.5, death −100)

**Exploration vs exploitation (epsilon-greedy).** With probability ε the snake
tries a random move, otherwise it plays the best known one. ε decreases after
each session: the snake explores less and exploits more over time.

**State.** For each of the 4 directions, the agent gets 3 bits: immediate
danger, green apple in sight, red apple in sight. That's at most 4,096 states,
and the Q-table converges in about 1,000 sessions.

**Architecture.**

```
Environment → Interpreter → Agent → Environment
```

- **Environment**: board, snake, apples, game rules
- **Interpreter**: reads the board, builds the snake's vision, the state and the reward
- **Agent**: receives state + reward, updates the Q-table, chooses the next action

Bonus: models trained on 10×10 also play on boards of other sizes, and every
session can be exported as JSON statistics and plotted.

## ⚙️ Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 🚀 Usage

```bash
# Watch the trained model play
./scripts/snake -sessions 3 -visual on -load models/1000sess.json -dontlearn -speed 8

# Train from scratch and save the model
./scripts/snake -sessions 1000 -visual off -save models/my_model.json

# Evaluate a model and export its statistics, then plot them
./scripts/snake -sessions 100 -visual off -load models/1000sess.json -dontlearn -stats-out stats/eval.json
./scripts/plot-stats stats/eval.json
```

Options:

```
-sessions N          number of training sessions (default: 1)
-visual on|off       pygame display (default: on)
-save PATH           save the model after training
-load PATH           load an existing model
-dontlearn           disable learning (pure evaluation)
-step-by-step        advance one step per key press
-speed FPS           display speed in frames/sec (default: 10)
-board-size N        NxN board size (default: 10)
-max-steps N         step limit per session (default: board_size² × 10)
-stats-out PATH      save per-session statistics as JSON
```

Pre-trained models are in `models/` (1, 10, 100, 1,000 and 1,500 sessions).

## 📁 Project structure

```
src/
├── main.py         # CLI, main loop
├── environment.py  # board and game rules
├── snake.py        # snake data structure
├── interpreter.py  # vision, state, rewards
├── agent.py        # Q-table, learning
├── display.py      # pygame + terminal display
├── constants.py    # hyperparameters, colors, constants
└── plot_stats.py   # bonus: charts from the JSON statistics
models/             # saved models (.json)
scripts/            # snake (main executable), plot-stats
```

<details>
<summary>🧪 Test commands (defense checklist)</summary>

```bash
# Mandatory models
./scripts/snake -sessions 1    -visual off -save models/1sess.json
./scripts/snake -sessions 10   -visual off -save models/10sess.json
./scripts/snake -sessions 100  -visual off -save models/100sess.json
./scripts/snake -sessions 1000 -visual off -save models/1000sess.json

# Variable board size (bonus)
./scripts/snake -sessions 5 -visual on -load models/1000sess.json -dontlearn -board-size 20

# Code style and memory
flake8 ./src
PYTHONFAULTHANDLER=1 ./scripts/snake -sessions 1000 -visual off

# Expected errors (clear message + exit 1)
./scripts/snake -sessions abc -visual off              # argparse usage
./scripts/snake -sessions 1 -visual off -board-size 2  # board-size must be at least 3
./scripts/snake -sessions 1 -visual off -load models/missing.json  # model file not found
```

</details>

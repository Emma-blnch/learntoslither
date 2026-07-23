import argparse
import json
import os
import sys


def parse_args():
    p = argparse.ArgumentParser(prog='plot_stats')
    p.add_argument('path', type=str, metavar='PATH',
                   help='fichier JSON généré par -stats-out')
    p.add_argument('-out', type=str, default=None, metavar='PATH',
                   help='sauvegarder le graphique en image '
                        '(défaut: <PATH>_plot.png)')
    p.add_argument('-show', action='store_true',
                   help='afficher le graphique dans une fenêtre')
    return p.parse_args()


def load_stats(path):
    with open(path) as f:
        data = json.load(f)
    return data['sessions'], data['summary']


def plot(sessions, summary, out, show):
    import matplotlib
    if not show:
        matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    session_ids = [s['session'] for s in sessions]
    lengths = [s['length'] for s in sessions]
    steps = [s['steps'] for s in sessions]
    green = [s['green_eaten'] for s in sessions]
    red = [s['red_eaten'] for s in sessions]

    outcomes = {}
    for s in sessions:
        outcomes[s['outcome']] = outcomes.get(s['outcome'], 0) + 1

    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    fig.suptitle(f"Statistiques — {summary['sessions_run']} sessions")

    ax = axes[0][0]
    ax.plot(session_ids, lengths, marker='o', markersize=2,
            color='tab:blue')
    ax.axhline(summary['length_avg'], color='tab:blue', linestyle='--',
               alpha=0.5, label=f"moyenne: {summary['length_avg']:.2f}")
    ax.set_title('Longueur par session')
    ax.set_xlabel('Session')
    ax.set_ylabel('Longueur')
    ax.legend()

    ax = axes[0][1]
    ax.plot(session_ids, steps, marker='o', markersize=2,
            color='tab:orange')
    ax.axhline(summary['steps_avg'], color='tab:orange', linestyle='--',
               alpha=0.5, label=f"moyenne: {summary['steps_avg']:.2f}")
    ax.set_title('Steps par session')
    ax.set_xlabel('Session')
    ax.set_ylabel('Steps')
    ax.legend()

    ax = axes[1][0]
    labels = sorted(outcomes)
    ax.bar(labels, [outcomes[k] for k in labels], color='tab:red')
    ax.set_title('Répartition des issues')
    ax.set_ylabel('Nombre de sessions')

    ax = axes[1][1]
    ax.plot(session_ids, green, label='vertes', color='tab:green')
    ax.plot(session_ids, red, label='rouges', color='tab:red')
    ax.set_title('Pommes mangées par session')
    ax.set_xlabel('Session')
    ax.set_ylabel('Pommes')
    ax.legend()

    fig.tight_layout()

    if out:
        dirname = os.path.dirname(out)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        fig.savefig(out)
        print(f'Graphique sauvegardé dans {out}')
    if show:
        plt.show()


def main():
    args = parse_args()

    try:
        sessions, summary = load_stats(args.path)
    except FileNotFoundError:
        print(f'Error: stats file not found: {args.path}', file=sys.stderr)
        sys.exit(1)
    except (ValueError, KeyError):
        print(f'Error: invalid stats file: {args.path}', file=sys.stderr)
        sys.exit(1)

    if not sessions:
        print('Error: no session data to plot', file=sys.stderr)
        sys.exit(1)

    out = args.out
    if out is None and not args.show:
        out = os.path.splitext(args.path)[0] + '_plot.png'

    plot(sessions, summary, out=out, show=args.show)


if __name__ == '__main__':
    main()

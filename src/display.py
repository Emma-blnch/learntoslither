from constants import (
    Cell,
    CELL_SIZE, FPS_DEFAULT,
    COLOR_BG, COLOR_GRID,
    COLOR_SNAKE_HEAD, COLOR_SNAKE_BODY,
    COLOR_GREEN_APPLE, COLOR_RED_APPLE,
)

_CELL_COLORS = {
    Cell.HEAD: COLOR_SNAKE_HEAD,
    Cell.BODY: COLOR_SNAKE_BODY,
    Cell.GREEN: COLOR_GREEN_APPLE,
    Cell.RED: COLOR_RED_APPLE,
}

# contsntes pour barre info sous plateau
_INFO_BAR_H = 36
_INFO_FONT_SIZE = 22
_INFO_COLOR = (30, 30, 30)
_INFO_BG = (220, 220, 220)


class Display:
    def __init__(self, board_size, cell_size=CELL_SIZE, headless=False):
        self.headless = headless
        self.board_size = board_size
        self.cell_size = cell_size
        self._screen = None
        self._clock = None
        self._font = None
        self._fps = FPS_DEFAULT
        self._step_by_step = False
        if headless:
            return
        # si pas "-visual off" alors import pygame
        # pour avoir fenetre du plateau de jeu
        import pygame
        self._pygame = pygame
        pygame.init()
        w = board_size * cell_size
        h = board_size * cell_size + _INFO_BAR_H
        self._screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption('Learn2Slither')
        self._clock = pygame.time.Clock()  # pour limiter FPS
        self._font = pygame.font.SysFont('monospace', _INFO_FONT_SIZE)

    def set_speed(self, fps):
        self._fps = fps

    def set_step_by_step(self, enabled):
        self._step_by_step = enabled

    # si pas headless, dessine le plateau + barre info
    def render(self, board, session=0, length=0, step=0):
        if self.headless:
            return True
        pg = self._pygame
        self._draw_board(board)
        self._draw_info(session, length, step)
        pg.display.flip()  # affiche frame
        self._clock.tick(self._fps)
        # si step by step attend input utilisateur
        # pour afficher prochaine frame
        if self._step_by_step:
            return self._wait_step()
        # sinon traite les events normalement
        return self._handle_events()

    # remplit le fond et les cases de couleur
    def _draw_board(self, board):
        pg = self._pygame
        cs = self.cell_size
        self._screen.fill(COLOR_BG)
        for r in range(board.size):
            for c in range(board.size):
                cell = board.grid[r][c]
                x, y = c * cs, r * cs
                color = _CELL_COLORS.get(cell, COLOR_BG)
                if cell != Cell.EMPTY:
                    pg.draw.rect(self._screen, color, (x, y, cs, cs))
                pg.draw.rect(
                    self._screen, COLOR_GRID, (x, y, cs, cs), 1
                )

    # dessine barre d'info
    def _draw_info(self, session, length, step):
        pg = self._pygame
        board_h = self.board_size * self.cell_size
        bar_rect = (0, board_h, self.board_size * self.cell_size, _INFO_BAR_H)
        pg.draw.rect(self._screen, _INFO_BG, bar_rect)
        text = (
            f'Session: {session}   '
            f'Length: {length}   '
            f'Step: {step}'
        )
        surf = self._font.render(text, True, _INFO_COLOR)
        self._screen.blit(surf, (8, board_h + 7))

    # parcours events pygame(clavier/souris/fenetre,
    # ex: touche echap ou croix de la fenetre)
    def _handle_events(self):
        pg = self._pygame
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False
        return True

    # attend touche autre que echap
    def _wait_step(self):
        pg = self._pygame
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return False
                    return True
            self._clock.tick(30)

    # ferme proprement pygame
    def close(self):
        if self.headless:
            return
        self._pygame.quit()

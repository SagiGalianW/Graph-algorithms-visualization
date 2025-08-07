import pygame

class Instruction:
    def __init__(self, text, x, y, w, bg_color=(240, 240, 240), text_color=(0, 0, 0), border_color=(0, 0, 0)):
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.font = pygame.font.SysFont(None, 20)
        self.lines = []
        self.line_height = 0
        self.h = 0
        self._initiate(self.text)
        self.x = x
        self.y = y
        self.w = w
        self.rect = pygame.Rect(x, y, w, self.h)

    def draw(self, win):
        pygame.draw.rect(win, self.bg_color, self.rect)
        pygame.draw.rect(win, self.border_color, self.rect, width=1)
        self._draw_text(win)
    
    def _initiate(self, text):
        self.lines = self.text.split('\n')
        self.line_height = self.font.get_height() + 2
        self.h = len(self.lines) * self.line_height + 5

    def _draw_text(self, win):
        y_offset = self.rect.y + 5
        for line in self.lines:
            line_surface = self.font.render(line, True, self.text_color)
            win.blit(line_surface, (self.rect.x + 5, y_offset))
            y_offset += self.line_height

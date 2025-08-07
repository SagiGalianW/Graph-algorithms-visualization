import pygame

class Button:
    def __init__(self, id, x, y, w, h, text, base_color, text_color, instruction, font_size=20):
        self.id = id
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.text = text
        self.base_color = base_color
        self.color = base_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, font_size)
        self.hovered = False
        self.animation_speed = 10  # how fast color animates
        self.hover_color = (100, 100, 100)
        self.base_color = self.color
        self.instruction = instruction

    def draw(self, win):
        if self.is_mouse_on():
            self.color = self.hover_color
            self.instruction.draw(win)
        else:
            self.color = self.base_color
        pygame.draw.rect(win, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        win.blit(text_surface, text_rect)

    def is_mouse_on(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return mouse_x >= self.x and mouse_x <= self.x + self.w and mouse_y >= self.y and mouse_y <= self.y + self.h

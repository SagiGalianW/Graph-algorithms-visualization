import pygame 
import math

class Vertex:
    def __init__(self, name, x, y, r, color):
        self.name = name
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.choosen = False

    def draw(self, win, font):
        if self.choosen:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.x = mouse_x
            self.y = mouse_y
        pygame.draw.circle(win, self.color, (self.x, self.y), self.r)
        text_surface = font.render(self.name, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        win.blit(text_surface, text_rect)
       
    
    def is_mouse_over(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        distance = math.hypot(mouse_x - self.x, mouse_y - self.y)
        return distance <= self.r

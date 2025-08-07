import math
import pygame

class Edge:
    def __init__(self, v, u, w, color=(0, 0, 0)):  # v --w--> u
        self.v = v
        self.u = u
        self.w = w
        self.color = color
        self.text_rect = pygame.Rect(0, 0, 0, 0)
    
    def draw(self, win, font):
        dx = self.u.x - self.v.x
        dy = self.u.y - self.v.y
        length = math.hypot(dx, dy)
        if length == 0:
            return  # overlapping vertices, skip drawing edge
        # Unit direction vector
        ux = dx / length
        uy = dy / length

        # Calculate start and end points offset by vertex radius
        start_x = self.v.x + ux * self.v.r
        start_y = self.v.y + uy * self.v.r
        end_x = self.u.x - ux * self.u.r
        end_y = self.u.y - uy * self.u.r

        # Draw the line from adjusted start to adjusted end
        pygame.draw.line(win, self.color, (start_x, start_y), (end_x, end_y), 3)

        # Draw the weight text at midpoint slightly above line
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        text_surface = font.render(str(self.w), True, (250, 0, 0))
        self.text_rect = text_surface.get_rect(center=(mid_x, mid_y - 10))
        win.blit(text_surface, self.text_rect)
    
    def is_mouse_on(self):
        return self.text_rect.collidepoint(pygame.mouse.get_pos())
    
    def decrease_weight(self):
        if self.w >= 2:
            self.w -= 1
            
    def increase_weight(self):
        self.w += 1
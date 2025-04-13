import pygame

pygame.init()

x_axis = 500
y_axis = 500

window = pygame.display.set_mode((x_axis, y_axis))
pygame.display.set_caption('Maze Game')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (204, 204, 0)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)

name_font = pygame.font.SysFont(None, 60)
header_font = pygame.font.SysFont(None, 45)

class Button:
    def __init__(self, x_pos, y_pos, width_1, height_1, text, color, hover, txt_color):
        self.color = color
        self.hover = hover
        self.text = text
        self.txt_color = txt_color
        self.rect = pygame.Rect(x_pos, y_pos, width_1, height_1)
        self.font = pygame.font.SysFont(None, 40)

    def create(self, display):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            color_1 = self.hover
        else:
            color_1 = self.color
        pygame.draw.rect(display, color_1, self.rect)

        text_display = self.font.render(self.text, True, self.txt_color)
        text_render = text_display.get_rect(center=self.rect.center)
        display.blit(text_display, text_render)

    def check(self, event1):
        if event1.type == pygame.MOUSEBUTTONDOWN:
            if event1.button == 1 and self.rect.collidepoint(event1.pos):
                return True
        return False

button_width = 200
button_height = 50
x1 = (x_axis - button_width) // 2
y1 = 170
space = 70

Buttons = [
        Button(x1, y1, button_width, button_height, 'Easy', GREEN, DARK_GREEN, WHITE),
        Button(x1, y1 + space, button_width, button_height, 'Medium', YELLOW, DARK_YELLOW, WHITE),
            Button(x1, y1 + 2 * space, button_width, button_height, 'Hard', RED, DARK_RED, WHITE)
        ]

x = 20
y = 20
width = 10
height = 30
speed = 5

START = False
running = True

while running:
    window.fill(WHITE)
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not START:
                for button in Buttons:
                    if button.check(event):
                       level = button.text
                       if level == "Easy":
                           speed = 1
                       elif level == "Medium":
                           speed = 2
                       elif level == "Hard":
                           speed = 3
                       START = True

    if not START:
        name_text = name_font.render('Maze Game', True, BLACK)
        header_text = header_font.render('Select Difficulty:', True, BLACK)

        name_rect = name_text.get_rect(center=(x_axis // 2, 50))
        header_rect = header_text.get_rect(center=(x_axis // 2, 100))

        window.blit(name_text, name_rect)
        window.blit(header_text, header_rect)

        for button in Buttons:
            button.create(window)
    else:
        arrows = pygame.key.get_pressed()

        if arrows[pygame.K_LEFT]:
            x -= speed
        if arrows[pygame.K_RIGHT]:
            x += speed
        if arrows[pygame.K_UP]:
            y -= speed
        if arrows[pygame.K_DOWN]:
            y += speed

        pygame.draw.rect(window, (0, 0, 255), (x, y, width, height))

    pygame.display.update()

pygame.quit()



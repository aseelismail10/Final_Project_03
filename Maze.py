import pygame
pygame.init()

window = pygame.display.set_mode((500, 500))

pygame.display.set_caption('Maze Game')

x = 20
y = 20
width = 10
height = 30
speed = 5

running = True
while running:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

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

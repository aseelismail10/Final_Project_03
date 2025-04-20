import pygame
import random
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
PLAYER_COLOR = (173,216,230)
GOAL = (255,0,0)

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
#Player movements within the maze. Removes "the wall" in between the two cells
Direction = {
    "N": (0,-1),
    "S": (0,1),
    "E": (1,0),
    "W": (-1,0)
}
Opp = {
    "N":"S",
    "S":"N",
    "E":"W",
    "W":"E"
}

def maze_generation(row,col):
    maze = [[{"N":True, "S":True, "E":True, "W":True} for _ in range(col)] for _ in range(row)]

    visited = [[False for _ in range (col)] for _ in range(row)] #track visited cells

    cell_path = [(0,0)] #Begin from the top left
    visited[0][0] = True #dont go back to the same cell when creating the maze!

    while cell_path: #this adds randomness... get a shuffled list of directions
        current_col, current_row = cell_path[-1] #get current cell's position from top of path stack
        directions = list(Direction.items())
        random.shuffle(directions)

        moved = False
        for direction, (delta_col, delta_row) in directions: #get cell position of nearby cells
            next_col = current_col + delta_col
            next_row = current_row + delta_row

            if 0 <= next_col < col and 0 <= next_row < row and not visited[next_row][next_col]: #see if nearby cells have been visited and if inside the maze
                maze[current_row][current_col][direction] = False
                maze[next_row][next_col][Opp[direction]] = False

                visited[next_row][next_col] = True #mark visited
                cell_path.append((next_col, next_row)) #add nearby cell to the path
                moved = True
                break #exit for loop and move to new cell
        if not moved:
            cell_path.pop() #if stuck and cant move to a new cell, go back to the last cell you came from
    return maze #return maze with walls

def visual_maze(window,maze,cell_size):#draws out maze
    window.fill(BLACK)
    row = len(maze)
    col = len(maze[0])
    for y in range(row):
        for x in range(col):
            cell = maze[y][x] #x and y position of the cell based on pixels of the screen
            cell_x = x * cell_size
            cell_y = y * cell_size
            if cell["N"]:
                pygame.draw.line(window, WHITE, (cell_x, cell_y), (cell_x + cell_size, cell_y), 2)
            if cell["S"]:
                pygame.draw.line(window, WHITE, (cell_x, cell_y + cell_size), (cell_x + cell_size, cell_y + cell_size), 2)
            if cell["E"]:
                pygame.draw.line(window, WHITE, (cell_x + cell_size, cell_y), (cell_x + cell_size, cell_y + cell_size), 2)
            if cell["W"]:
                pygame.draw.line(window, WHITE, (cell_x, cell_y), (cell_x, cell_y + cell_size), 2)

def draw_out_player(window, player_position, cell_size):
    x,y = player_position
    center = (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2) #center circle within the cell
    pygame.draw.circle(window, PLAYER_COLOR, center, cell_size//3)

def draw_goal(win, col, row, cell_size):
    x, y = col - 1, row - 1
    center = (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2)
    pygame.draw.circle(win, GOAL, center, cell_size // 3)


def move_player(maze, player_position, delta_row, delta_col):
    x, y = player_position
    new_x, new_y = x + delta_col, y + delta_row
    if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze):
        cell = maze[y][x]
    if delta_row == -1 and not cell["N"]:  # Check if moving up (North)
        player_position[1] -= 1
    elif delta_row == 1 and not cell["S"]:  # Check if moving down (South)
        player_position[1] += 1
    elif delta_col == -1 and not cell["W"]:  # Check if moving left (West)
        player_position[0] -= 1
    elif delta_col == 1 and not cell["E"]:  # Check if moving right (East)
        player_position[0] += 1

#Start Menu
START = False
level = None
running = True

while running:
    window.fill(WHITE)
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not START:
                for button in Buttons:
                    if button.check(event):
                       level = button.text
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
            pygame.display.update()
    else: #select difficulty

        if level == "Easy":
            row,col = 6,8
        elif level == "Medium":
            row,col = 8,10
        elif level == "Hard":
            row,col = 10,12

        width,height = 800, 800
        cell_size = width//col
        win = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Maze Game")

        frame_timer = pygame.time.Clock() #makes game run smoother
        maze = maze_generation(row,col)
        player_position = [0,0]
        running = True

        while running:
            frame_timer.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        move_player(maze, player_position, 0, -1)
                    elif event.key == pygame.K_RIGHT:
                        move_player(maze, player_position, 0, 1)
                    elif event.key == pygame.K_UP:
                        move_player(maze, player_position, -1, 0)
                    elif event.key == pygame.K_DOWN:
                        move_player(maze, player_position, 1, 0)

            visual_maze(win, maze, cell_size)
            draw_goal(win, col, row, cell_size )
            draw_out_player(win, player_position, cell_size)
            pygame.display.update()

            if player_position == [col - 1, row - 1]:
                print("You Win")
                pygame.time.wait(1000)
                running = False

pygame.quit()
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
BLUE = (0,0,255)
DARK_BLUE = (0, 0, 139)
PLAYER_COLOR = (173,216,230)
GOAL = (255,0,0)
LIGHT_GREEN = (144,238,144) #green background
DARK_GREEN = (0, 100, 0) #our wall color

time_list_easy = []
time_list_medium = []
time_list_hard = []

bee_image = pygame.image.load('bee.png')
bee_image = pygame.transform.smoothscale(bee_image, (50, 50)) # Adjust size if needed

flower_image = pygame.image.load('flower.png')
flower_image = pygame.transform.scale(flower_image, (40, 40))  # Adjust size if needed

maze_count = 0
losses_count = 0
wins_count = 0

name_font = pygame.font.SysFont(None, 60)
stat_font = pygame.font.SysFont(None, 45)

header_font = pygame.font.SysFont(None, 45)

class Button:
"""creation of button class seen in the game display (ie: restart, game statistics, easy, medium, hard, return, end)"""
    def __init__(self, x_pos, y_pos, width_1, height_1, text, color, hover, txt_color):
        self.color = color
        self.hover = hover
        self.text = text
        self.txt_color = txt_color
        self.rect = pygame.Rect(x_pos, y_pos, width_1, height_1)
        self.font = pygame.font.SysFont('comicsansms', 30, bold=True)

    def create(self, display):
    """ created the buttons for the player to move"""
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
    """checks the event type (when the arrows are clicked to move the character)"""
        if event1.type == pygame.MOUSEBUTTONDOWN:
            if event1.button == 1 and self.rect.collidepoint(event1.pos):
                return True
        return False

button_width = 250
button_height = 50
x1 = (x_axis - button_width) // 2
y1 = 170
space = 70
"""Array to display buttons and add the colors"""
Home_Buttons = [
        Button(x1, y1, button_width, button_height, 'Easy', GREEN, DARK_GREEN, WHITE),
        Button(x1, y1 + space, button_width, button_height, 'Medium', YELLOW, DARK_YELLOW, WHITE),
        Button(x1, y1 + 2 * space, button_width, button_height, 'Hard', RED, DARK_RED, WHITE),

        ]

game_statistic = Button(x1, y1 + 3 * space, button_width, button_height, 'Game Statistics', BLUE, DARK_BLUE, WHITE)

button_return = Button(15, 425,150, 50, 'Return', GREEN, DARK_GREEN, WHITE)
button_restart = Button(175,425,150,50,'Restart', YELLOW, DARK_YELLOW, WHITE)
button_exit = Button(335,425, 150, 50, 'Exit', RED, DARK_RED, WHITE)

returning_button = Button(170, y_axis // 1.25, 150, 50, 'Return', BLUE, DARK_BLUE, WHITE)

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
"""Generation of the maze using branching and randomization"""
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
"""the maze display for the user to play the game"""
    window.fill(LIGHT_GREEN)
    row = len(maze)
    col = len(maze[0])
    for y in range(row):
        for x in range(col):
            cell = maze[y][x] #x and y position of the cell based on pixels of the screen
            cell_x = x * cell_size
            cell_y = y * cell_size
            if cell["N"]:
                pygame.draw.line(window, DARK_GREEN, (cell_x, cell_y), (cell_x + cell_size, cell_y), 2)
            if cell["S"]:
                pygame.draw.line(window, DARK_GREEN, (cell_x, cell_y + cell_size), (cell_x + cell_size, cell_y + cell_size), 2)
            if cell["E"]:
                pygame.draw.line(window, DARK_GREEN, (cell_x + cell_size, cell_y), (cell_x + cell_size, cell_y + cell_size), 2)
            if cell["W"]:
                pygame.draw.line(window, DARK_GREEN, (cell_x, cell_y), (cell_x, cell_y + cell_size), 2)

def draw_out_player(window, player_position, cell_size):
"""Draws the player at their current position on the game window."""
    x,y = player_position
    center = (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2) #center within the cell
    window.blit(bee_image, (center[0] - 15, center[1] - 15))

def draw_goal(win, col, row, cell_size):
"""Includes the goal as a flower on the maze grid."""
    x, y = col - 1, row - 1
    center = (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2)
    window.blit(flower_image, (center[0] - 20, center[1] - 20))


def move_player(maze, player_position, delta_row, delta_col):
"""Attempts to move the player in the maze based on input direction (arrows pressed), checks for walls and maze boundaries."""
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

def end_message(window, message, color, width, height):
    font = pygame.font.SysFont(None, 60)
    text = font.render(message, True, color)
    rect = text.get_rect(center=(width // 2, (340 // 2)))
    window.blit(text, rect)
    pygame.display.update()
    pygame.time.wait(2000)

def game_statistics(window):
"""Displays the player's game statistics (ie: as wins, losses, percentages, best times, and total games played)"""
    window.fill(LIGHT_GREEN)
    text = stat_font.render("Game Statistics", True, WHITE)
    text_rect = text.get_rect(center=(x_axis // 2, y_axis // 8))
    window.blit(text, text_rect)

    list_stats = [
        f'Total wins: {wins_count}',
        f'Win Percentage: {((wins_count/maze_count) * 100)}%' if maze_count > 0 else 'Win Percentage: N/A',
        f'Total losses: {losses_count}',
        f'Lost Percentage: {((losses_count/maze_count) * 100)}%' if maze_count > 0 else 'Lost Percentage: N/A',
        f'Best time: Easy - {min(time_list_easy)} secs' if time_list_easy else "Best time: Easy - N/A",
        f'Best time: Medium - {min(time_list_medium)} secs' if time_list_medium else 'Best time: Medium - N/A',
        f'Best time: Hard - {min(time_list_hard)} secs' if time_list_hard else 'Best time: Hard - N/A',
        f'Total games: {maze_count}' if maze_count else "Total games: N/A"
    ]
    font = pygame.font.SysFont(None, 25)
    y = y_axis // 3
    for i in list_stats:
        text = font.render(i, True, WHITE)
        rect = text.get_rect(center=(x_axis // 2, y - 50))
        window.blit(text, rect)
        y += 35

    returning_button.create(window)
    pygame.display.update()
    return returning_button
#Start Menu
START = False
stats = False
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
            for button in Home_Buttons:
                if button.check(event):
                   level = button.text

                   if level == "Easy":
                       row, col = 6, 8
                   elif level == "Medium":
                       row, col = 8, 10
                   elif level == "Hard":
                       row, col = 10, 12
                   START = True

                if game_statistic.check(event):
                    stats = True
                    START = False
        if stats:
            while stats:
                returning_button = game_statistics(window)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif returning_button.check(event):
                        stats = False
                pygame.time.delay(100)

        #     window.fill(WHITE)
            #     pygame.display.update()
            #     pygame.time.delay(500)
            #
            # pygame.display.update()
            #


    if not START and not stats:
        name_font = pygame.font.SysFont('comicsansms', 60, bold=True)
        header_font = pygame.font.SysFont('comicsansms', 45, bold=True)
        name_text = name_font.render('Maze Game', True, BLACK)
        header_text = header_font.render('Select Difficulty:', True, BLACK)

        name_rect = name_text.get_rect(center=(x_axis // 2, 50))
        header_rect = header_text.get_rect(center=(x_axis // 2, 100))

        window.blit(name_text, name_rect)
        window.blit(header_text, header_rect)

        for button in Home_Buttons:
            button.create(window)
        game_statistic.create(window)
        pygame.display.update()
    else: #select difficulty

        width,height = 500, 500
        cell_size = width//col
        win = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Maze Game")

        frame_timer = pygame.time.Clock()
        maze = maze_generation(row,col)
        player_position = [0,0]
        level_running = True

        countdown_times = {"Easy": 30, "Medium": 25, "Hard": 20}
        countdown_time = countdown_times[level]
        start_ticks = pygame.time.get_ticks()
        font_timer = pygame.font.SysFont('comicsansms', 20, bold=True)


        while level_running:
            frame_timer.tick(60)
            seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
            time_left = max(0, countdown_time - int(seconds_passed))

            win.fill(BLACK)


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

                if button_return.check(event):
                    START = False
                    level_running = False

                if button_restart.check(event):
                    maze_count += 1
                    player_position = [0,0]
                    start_ticks = pygame.time.get_ticks()
                    maze = maze

                if button_exit.check(event):
                    pygame.quit()
                    exit()


            visual_maze(win, maze, cell_size)
            draw_goal(win, col, row, cell_size)
            draw_out_player(win, player_position, cell_size)

            button_return.create(win)
            button_restart.create(win)
            button_exit.create(win)


            timer_text = font_timer.render(f"Time: {time_left}", True, (255, 255, 255))
            win.blit(timer_text, (10, 10))

            pygame.display.update()

            if time_left <= 0:
                end_message(win,"Time's up! You lost!!", RED, width, height)
                losses_count += 1
                maze_count += 1
                level_running = False

            if player_position == [col - 1, row - 1]:
                if level == 'Easy':
                    time_list_easy.append(30-time_left)
                elif level == 'Medium':
                    time_list_medium.append(25-time_left)
                else:
                    time_list_hard.append(20-time_left)
                wins_count += 1
                maze_count += 1
                end_message(win, "You Win!", GREEN, width, height)
                level_running = False

pygame.quit()

import pygame
import sys
import random

# Global constants for screen dimensions and grid size
screen_width = 480
screen_height = 480
gridsize = 20
grid_width = screen_width // gridsize  
grid_height = screen_height // gridsize  

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width / 2), (screen_height / 2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (17, 24, 47)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * gridsize)) % screen_width), (cur[1] + (y * gridsize)) % screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((screen_width / 2), (screen_height / 2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self):
        self.position = (0, 0)
        self.color = (200, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_width - 1) * gridsize, random.randint(0, grid_height - 1) * gridsize)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                rr = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (84, 194, 205), rr)

def get_player_name():
    # Create a new window for entering player name
    input_box = pygame.Rect(screen_width / 2 - 100, screen_height / 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Fill the background
        screen.fill((0, 0, 0))
        # Render the prompt text
        prompt_font = pygame.font.Font(None, 32)
        prompt_surface = prompt_font.render("What is your name?", True, (255, 255, 255))  # White text
        screen.blit(prompt_surface, (screen_width / 2 - prompt_surface.get_width() / 2, screen_height / 2 - 60))

        # Render the current text
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width

        # Draw the text input box
        pygame.draw.rect(screen, color, input_box, 2)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()

def main():
    pygame.init()

    global screen
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()
    
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    # Get player's name
    player_name = get_player_name()

    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("monospace", 16)

    while True:
        clock.tick(10)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        
        # The header background
        header_rect = pygame.Rect(0, 0, screen_width, 40)
        pygame.draw.rect(screen, (0, 0, 0), header_rect)  # Black background for the header

        # Render and display player name
        name_text = myfont.render(f"Player: {player_name}", True, (255, 255, 255))  # White text
        score_text = myfont.render(f"Score: {snake.score}", True, (255, 255, 255))  # White text
        screen.blit(name_text, (10, 10))
        screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))

        pygame.display.update()

main()

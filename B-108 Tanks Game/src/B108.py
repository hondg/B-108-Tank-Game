import pygame

# Initialize pygame
pygame.init()

# Set up the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("B/108")

# Set up the tanks
TANK_WIDTH = 50
TANK_HEIGHT = 50
tank1_x = 50
tank1_y = 360
tank1_direction = "right"
tank2_x = 700
tank2_y = 360
tank2_direction = "left"

# Load the tank images 
tank1_images = {
    "up" : pygame.image.load("Assets/redup.png"),
    "down" : pygame.image.load("Assets/reddown.png"),
    "left" : pygame.image.load("Assets/redleft.png"),
    "right" : pygame.image.load("Assets/redright.png")
}
tank2_images = {
    "up" : pygame.image.load("Assets/blueup.png"),
    "down" : pygame.image.load("Assets/bluedown.png"),
    "left" : pygame.image.load("Assets/blueleft.png"),
    "right" : pygame.image.load("Assets/blueright.png")
}
tank3_images = {
    "up" : pygame.image.load("Assets/greenup.png"),
    "down" : pygame.image.load("Assets/greendown.png"),
    "left" : pygame.image.load("Assets/greenleft.png"),
    "right" : pygame.image.load("Assets/greenright.png")
}
tank4_images = {
    "up" : pygame.image.load("Assets/purpleup.png"),
    "down" : pygame.image.load("Assets/purpledown.png"),
    "left" : pygame.image.load("Assets/purpleleft.png"),
    "right" : pygame.image.load("Assets/purpleright.png")
}
# Load the bullet image
bullet_image = pygame.image.load('Assets/bullet.png')

# Set up the bullets
BULLET_DELAY = 500
BULLET_SPEED = 10
bullet1_list = []
bullet2_list = []
MAX_BULLET = 3

# Set the time since the last bullet was fired for each tank to 0
last_bullet1_time = 0
last_bullet2_time = 0


# Initialize scores for each tank
tank1_score = 0
tank2_score = 0

# Load win screens
player1_winscreen = pygame.image.load("Assets/player1_winscreen.jpg")
player2_winscreen = pygame.image.load("Assets/player2_winscreen.jpg")

# Load start screen
entry_screen = pygame.image.load("Assets/entry_screen.jpg")

# Load arena image
arena_image = pygame.image.load("Assets/arena.jpg")

# Load the explosion animation image
explosion_image = pygame.image.load("Assets/explosion.png").convert_alpha()

# Load the obstacle image
obstacle1_image = pygame.image.load("Assets/Obstacle1.png")
obstacle1_positions = [(350, 350)]
obstacle2_image = pygame.image.load("Assets/Obstacle2.png")
obstacle2_positions = [(100, 100), (100, 600), (600, 600), (600,100)]

obstacle_rects = [pygame.Rect(350, 350, 110, 90), pygame.Rect(100, 100, 110, 70), pygame.Rect(100, 600, 110, 70), pygame.Rect(600, 600, 110, 70), pygame.Rect(600, 100, 110, 70)]



# Function to display explosion animation
def explosion_animation(x, y):
    window.blit(explosion_image, (x, y))
    pygame.display.update()
    pygame.time.delay(50)


# Set up the clock
clock = pygame.time.Clock()


# Create the tank selection screen function
tank_images = [
        pygame.image.load("Assets/redup.png"),
        pygame.image.load("Assets/blueup.png"),
        pygame.image.load("Assets/greenup.png"),
        pygame.image.load("Assets/purpleup.png")
    ]
def tank_selection_screen():
    # Load tank selection screen image
    tank_selection_screen_image = pygame.image.load("Assets/tank_selection_screen.jpg")
    # Load tank images for selection
    tank_images = [
        pygame.image.load("Assets/redup.png"),
        pygame.image.load("Assets/blueup.png"),
        pygame.image.load("Assets/greenup.png"),
        pygame.image.load("Assets/purpleup.png")
    ]
    # Set initial tank selection
    tank1_selected = 0
    tank2_selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Handle tank selection for player 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                tank1_selected = (tank1_selected - 1) % len(tank_images)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                tank1_selected = (tank1_selected + 1) % len(tank_images)

            # Handle tank selection for player 2
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                tank2_selected = (tank2_selected - 1) % len(tank_images)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                tank2_selected = (tank2_selected + 1) % len(tank_images)

            # Handle starting the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return tank1_selected, tank2_selected

        window.blit(tank_selection_screen_image, (0, 0))

        # Display tank images for selection
        tank1_rect = tank_images[tank1_selected].get_rect(center=(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2))
        tank2_rect = tank_images[tank2_selected].get_rect(center=(WINDOW_WIDTH // 4 * 3, WINDOW_HEIGHT // 2))
        window.blit(tank_images[tank1_selected], tank1_rect)
        window.blit(tank_images[tank2_selected], tank2_rect)
        pygame.display.flip()


# Call the tank selection screen function before the main game loop
tank1_selected, tank2_selected = tank_selection_screen()

# Set up the tanks
tank1_image = tank_images[tank1_selected]
tank2_image = tank_images[tank2_selected]






# Create the start screen function
def start_screen():
    
    window.blit(entry_screen,(0,0))
    pygame.display.flip()

    # Wait for the player to press SPACE
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


# Call the start screen function before the main game loop
start_screen()

game_over = False

# Main game loop
while not game_over:
    current_time=pygame.time.get_ticks()
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        
        # Handle tank 1 firing
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and len(bullet1_list) < MAX_BULLET and current_time - last_bullet1_time > BULLET_DELAY:
            bullet1_list.append({
                "x": tank1_x + TANK_WIDTH/2,
                "y": tank1_y + TANK_HEIGHT/2,
                "direction": tank1_direction
            })
            last_bullet1_time = current_time

        # Handle tank 2 firing
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and len(bullet2_list) < MAX_BULLET and current_time - last_bullet2_time > BULLET_DELAY:
            bullet2_list.append({
                "x": tank2_x + TANK_WIDTH/2,
                "y": tank2_y + TANK_HEIGHT/2,
                "direction": tank2_direction
            })
            last_bullet2_time = current_time   
   
    # Handle tank 1 movement
    keys = pygame.key.get_pressed()
    tank1_rect = pygame.Rect(tank1_x, tank1_y, TANK_WIDTH, TANK_HEIGHT)
    if keys[pygame.K_a] and tank1_x > 0 :
        new_tank1_rect = tank1_rect.move(-5, 0)
        if not new_tank1_rect.colliderect(pygame.Rect(tank2_x, tank2_y, TANK_WIDTH, TANK_HEIGHT)):
            tank1_x -= 5
            tank1_direction = "left"
    elif keys[pygame.K_d] and tank1_x < WINDOW_WIDTH - TANK_WIDTH:
        new_tank1_rect = tank1_rect.move(5, 0)
        if not new_tank1_rect.colliderect(pygame.Rect(tank2_x, tank2_y, TANK_WIDTH, TANK_HEIGHT)):
            tank1_x += 5
            tank1_direction = "right"
    elif keys[pygame.K_w] and tank1_y > 0:
        new_tank1_rect = tank1_rect.move(0, -5)
        if not new_tank1_rect.colliderect(pygame.Rect(tank2_x, tank2_y, TANK_WIDTH, TANK_HEIGHT)):
            tank1_y -= 5
            tank1_direction = "up"
    elif keys[pygame.K_s] and tank1_y < WINDOW_HEIGHT - TANK_HEIGHT:
        new_tank1_rect = tank1_rect.move(0, 5)
        if not new_tank1_rect.colliderect(pygame.Rect(tank2_x, tank2_y, TANK_WIDTH, TANK_HEIGHT)):
            tank1_y += 5
            tank1_direction = "down"
    
    
    # Handle tank 2 movement
    tank2_rect = pygame.Rect(tank2_x, tank2_y, TANK_WIDTH, TANK_HEIGHT)
    if keys[pygame.K_LEFT] and tank2_x > 0 :
        new_tank2_rect = tank2_rect.move(-5, 0)
        if not new_tank2_rect.colliderect(pygame.Rect(tank1_x, tank1_y, TANK_WIDTH, TANK_HEIGHT)):
            tank2_x -= 5
            tank2_direction = "left"
    elif keys[pygame.K_RIGHT] and tank2_x < WINDOW_WIDTH - TANK_WIDTH:
        new_tank2_rect = tank2_rect.move(5, 0)
        if not new_tank2_rect.colliderect(pygame.Rect(tank1_x, tank1_y, TANK_WIDTH, TANK_HEIGHT)):
            tank2_x += 5
            tank2_direction = "right"
    elif keys[pygame.K_UP] and tank2_y > 0:
        new_tank2_rect = tank2_rect.move(0, -5)
        if not new_tank2_rect.colliderect(pygame.Rect(tank1_x, tank1_y, TANK_WIDTH, TANK_HEIGHT)):
            tank2_y -= 5
            tank2_direction = "up"
    elif keys[pygame.K_DOWN] and tank2_y < WINDOW_HEIGHT - TANK_HEIGHT:
        new_tank2_rect = tank2_rect.move(0, 5)
        if not new_tank2_rect.colliderect(pygame.Rect(tank1_x, tank1_y, TANK_WIDTH, TANK_HEIGHT)):
            tank2_y += 5
            tank2_direction = "down"


    # Draw the arena
    window.blit(arena_image, (0, 0))

    for position in obstacle1_positions:
        window.blit(obstacle1_image, position)
    for position in obstacle2_positions:
        window.blit(obstacle2_image, position)

    # Draw the tanks
    if tank1_direction == "up":
        tank1_image = tank1_images["up"]
    elif tank1_direction == "down":
        tank1_image = tank1_images["down"]
    elif tank1_direction == "left":
        tank1_image = tank1_images["left"]
    else:
        tank1_image = tank1_images["right"]
    window.blit(tank1_image, (tank1_x, tank1_y))
    
    if tank2_direction == "up":
        tank2_image = tank2_images["up"]
    elif tank2_direction == "down":
        tank2_image = tank2_images["down"]
    elif tank2_direction == "left":
        tank2_image = tank2_images["left"]
    else:
        tank2_image = tank2_images["right"]
    window.blit(tank2_image, (tank2_x, tank2_y))


    # Check for collisions between bullets and tanks
    for bullet in bullet1_list:
        bullet_rect = pygame.Rect(bullet["x"], bullet["y"], 10, 10)
        tank2_rect = pygame.Rect(tank2_x, tank2_y, TANK_WIDTH, TANK_HEIGHT)
        if bullet_rect.colliderect(tank2_rect):
            explosion_animation(tank2_x, tank2_y)
            tank1_score += 1
            bullet1_list.remove(bullet)
        elif bullet["x"] < 0 or bullet["x"] > WINDOW_WIDTH or bullet["y"] < 0 or bullet["y"] > WINDOW_HEIGHT:
            bullet1_list.remove(bullet)

    for bullet in bullet2_list:
        bullet_rect = pygame.Rect(bullet["x"], bullet["y"], 10, 10)
        tank1_rect = pygame.Rect(tank1_x, tank1_y, TANK_WIDTH, TANK_HEIGHT)
        if bullet_rect.colliderect(tank1_rect):
            explosion_animation(tank1_x, tank1_y)
            tank2_score += 1
            bullet2_list.remove(bullet)
        elif bullet["x"] < 0 or bullet["x"] > WINDOW_WIDTH or bullet["y"] < 0 or bullet["y"] > WINDOW_HEIGHT:
            bullet2_list.remove(bullet)
    
    # Check for collision between bullets and obstacles
    for obstacle_rect in obstacle_rects:
        for bullet in bullet1_list + bullet2_list:
            bullet_rect = pygame.Rect(bullet["x"], bullet["y"], 10, 10)
            if bullet_rect.colliderect(obstacle_rect):
                # Remove the bullet from the list
                if bullet in bullet1_list:
                    bullet1_list.remove(bullet)
                if bullet in bullet2_list:
                    bullet2_list.remove(bullet)


    # Handle bullet firing for tank 1
    if keys[pygame.K_SPACE] and len(bullet1_list) < MAX_BULLET:
        if current_time - last_bullet1_time > BULLET_DELAY:
            if tank1_direction == "left":
                bullet_x = tank1_x
                bullet_y = tank1_y + TANK_HEIGHT/2 - 5
                bullet_direction = "left"
            elif tank1_direction == "right":
                bullet_x = tank1_x + TANK_WIDTH - 10
                bullet_y = tank1_y + TANK_HEIGHT/2 - 5
                bullet_direction = "right"
            elif tank1_direction == "up":
                bullet_x = tank1_x + TANK_WIDTH/2 - 5
                bullet_y = tank1_y
                bullet_direction = "up"
            elif tank1_direction == "down":
                bullet_x = tank1_x + TANK_WIDTH/2 - 5
                bullet_y = tank1_y + TANK_HEIGHT - 10
                bullet_direction = "down"
            bullet = {"x": bullet_x, "y": bullet_y, "direction": bullet_direction}
            bullet1_list.append(bullet)
            last_bullet1_time = current_time
    # Handle bullet firing for tank 2
    if keys[pygame.K_RETURN] and len(bullet2_list) < 50 and current_time - last_bullet2_time >= 100000:
        if tank2_direction == "left":
            bullet_x = tank2_x
            bullet_y = tank2_y + TANK_HEIGHT/2 - 5
            bullet_direction = "left"
        elif tank2_direction == "right":
            bullet_x = tank2_x + TANK_WIDTH - 10
            bullet_y = tank2_y + TANK_HEIGHT/2 - 5
            bullet_direction = "right"
        elif tank2_direction == "up":
            bullet_x = tank2_x + TANK_WIDTH/2 - 5
            bullet_y = tank2_y
            bullet_direction = "up"
        elif tank2_direction == "down":
            bullet_x = tank2_x + TANK_WIDTH/2 - 5
            bullet_y = tank2_y + TANK_HEIGHT - 10
            bullet_direction = "down"
        bullet = {"x": bullet_x, "y": bullet_y, "direction": bullet_direction}
        bullet2_list.append(bullet)
        last_bullet2_time = current_time

    # Update the position of the bullets
    for bullet in bullet1_list:
        if bullet["direction"] == "up":
            bullet["y"] -= BULLET_SPEED
        elif bullet["direction"] == "down":
            bullet["y"] += BULLET_SPEED
        elif bullet["direction"] == "left":
            bullet["x"] -= BULLET_SPEED
        elif bullet["direction"] == "right":
            bullet["x"] += BULLET_SPEED
        window.blit(bullet_image, (bullet["x"], bullet["y"]))

    for bullet in bullet2_list:
        if bullet["direction"] == "up":
            bullet["y"] -= BULLET_SPEED
        elif bullet["direction"] == "down":
            bullet["y"] += BULLET_SPEED
        elif bullet["direction"] == "left":
            bullet["x"] -= BULLET_SPEED
        elif bullet["direction"] == "right":
            bullet["x"] += BULLET_SPEED
        window.blit(bullet_image, (bullet["x"], bullet["y"]))

    for obstacle_rect in obstacle_rects:
        if tank1_rect.colliderect(obstacle_rect):
            if tank1_direction == "left":
                tank1_x = obstacle_rect.right
            elif tank1_direction == "right":
                tank1_x = obstacle_rect.left - TANK_WIDTH
            elif tank1_direction == "up":
                tank1_y = obstacle_rect.bottom
            elif tank1_direction == "down":
                tank1_y = obstacle_rect.top - TANK_HEIGHT
        if tank2_rect.colliderect(obstacle_rect):
            if tank2_direction == "left":
                tank2_x = obstacle_rect.right
            elif tank2_direction == "right":
                tank2_x = obstacle_rect.left - TANK_WIDTH
            elif tank2_direction == "up":
                tank2_y = obstacle_rect.bottom
            elif tank2_direction == "down":
                tank2_y = obstacle_rect.top - TANK_HEIGHT



    # Draw the scores
    font = pygame.font.SysFont(None, 25)
    tank1_score_text = font.render("Player1: " + str(tank1_score), True, (255,0,0), (0,0,0))
    tank2_score_text = font.render("Player2: " + str(tank2_score), True, (0,0,255), (0,0,0))
    window.blit(tank1_score_text, (10, 10))
    window.blit(tank2_score_text, (WINDOW_WIDTH - tank2_score_text.get_width() - 10, 10))
    
    # Check if either tank has won
    if tank1_score >= 5:
        # Display win screen for tank 1
        window.blit(player1_winscreen, (0, 0))
        pygame.display.update()
        pygame.time.delay(3000)
        game_over = True
    elif tank2_score >= 5:
        # Display win screen for tank 2
        window.blit(player2_winscreen, (0, 0))
        pygame.display.update()
        pygame.time.delay(3000)
        game_over = True

    
    #Update the display
    pygame.display.update()

    # Limit the game to 60 frames per second
    clock.tick(60)

    
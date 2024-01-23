import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions 6.1 inches (assuming resolution of 720x1440)
width, height = 600, 1000
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("BallBounceAuto")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Board and ball dimensions
board_width, board_height = 120, 20  # Modified board design and increased speed
ball_radius = 11

# Initial board position
board_x, board_y = width // 2 - board_width // 2, height - board_height - 10
board_speed = 10  # Increased board movement speed

# Initial ball position and speed
ball_x, ball_y = width // 2, height - board_height - ball_radius - 15
ball_speed_x, ball_speed_y = 8, -8  # Increased ball speed

# Block parameters
num_blocks = 25
block_width, block_height = width // (num_blocks // 2), 20  # Fill 50% of the screen
blocks = [(i * block_width, random.randint(50, 150)) for i in range(num_blocks // 2)]

# Level counter
level = 1

# Scores
score = 0

# Game over flag
game_over = False

# Function to simulate pressing the ENTER key automatically
def press_enter():
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN}))

# Load music
pygame.mixer.music.load('audio.mp3')
pygame.mixer.music.play(-1)  # -1 means play on repeat

# Bounce animation function
def bounce_animation():
    frames = 5
    for frame in range(frames):
        window.fill(white)
        pygame.draw.rect(window, (0, 0, 255), (board_x, board_y, board_width, board_height))
        pygame.draw.circle(window, (255, 0, 0), (int(ball_x), int(ball_y)), ball_radius)
        
        # Display blocks
        for block in blocks:
            pygame.draw.rect(window, (0, 255, 0), (block[0], block[1], block_width, block_height))
        
        # Update score and level display
        font = pygame.font.Font(None, 36)
        score_text = font.render("SCORES: {}".format(score), True, black)
        window.blit(score_text, (width - score_text.get_width() - 10, 10))
        level_text = font.render("LEVEL: {}".format(level), True, black)
        window.blit(level_text, (10, 10))
        
        pygame.display.flip()
        pygame.time.delay(10)

# Main game loop
while level <= 15:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Automatic ball bounce
    if not game_over:
        if ball_x + ball_radius > width or ball_x - ball_radius < 0:
            ball_speed_x = -ball_speed_x

    if not game_over:
        # Ball movement
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Ball bounce off walls
        if ball_x <= 0 or ball_x >= width:
            ball_speed_x = -ball_speed_x
        if ball_y <= 0:
            ball_speed_y = -ball_speed_y

        # Automatic ball bounce off the board
        if (
            board_x < ball_x < board_x + board_width
            and board_y < ball_y + ball_radius < board_y + board_height
        ):
            ball_speed_y = -ball_speed_y

        # Prevent the ball from passing under the board
        if ball_y + ball_radius > board_y + board_height:
            ball_y = board_y + board_height - ball_radius
            ball_speed_y = -ball_speed_y  # Change the direction of the ball

        # Check for block removal
        for block in blocks:
            block_x, block_y = block[0], block[1]
            if (
                block_x < ball_x < block_x + block_width
                and block_y < ball_y < block_y + block_height
            ) or (
                block_x < ball_x + ball_radius < block_x + block_width
                and block_y < ball_y + ball_radius < block_y + block_height
            ) or (
                block_x < ball_x - ball_radius < block_x + block_width
                and block_y < ball_y - ball_radius < block_y + block_height
            ) or (
                block_x < ball_x - ball_radius < block_x + block_width
                and block_y + block_height > ball_y + ball_radius > block_y
            ) or (
                block_x < ball_x + ball_radius < block_x + block_width
                and block_y - ball_radius < ball_y < block_y + block_height
            ):
                blocks.remove(block)
                ball_speed_x = -ball_speed_x  # Change speed direction along X
                ball_speed_y = -ball_speed_y  # Change speed direction along Y
                score += 1

        # Check for end of level
        if not blocks:
            level += 1
            ball_speed_y -= 1  # Increase ball speed on each new level
            blocks = [(i * block_width, random.randint(50, 150)) for i in range(num_blocks // 2)]

            # Check for completion of all levels
            if level > 15:  # Change 3 to the desired number of levels
                game_over = True
                level = 1
                score = 0
                ball_speed_y = -8
                blocks = [(i * block_width, random.randint(50, 150)) for i in range(num_blocks // 2)]

                # Call the function to simulate pressing the ENTER key automatically
                press_enter()

        # Check for game over
        if ball_y > height:
            game_over = True

        # Reset the ball if it goes beyond the screen boundaries
        if ball_x - ball_radius < 0:
            ball_x = ball_radius
            ball_speed_x = -ball_speed_x
        elif ball_x + ball_radius > width:
            ball_x = width - ball_radius
            ball_speed_x = -ball_speed_x

        # Automatic bounce off walls
        if not game_over:
            if ball_x + ball_radius > width or ball_x - ball_radius < 0:
                ball_speed_x = -ball_speed_x

        # Automatic movement of the board towards the ball
        if ball_x > board_x + board_width // 2 and board_x + board_width < width:
            board_x += board_speed
        elif ball_x < board_x + board_width // 2 and board_x > 0:
            board_x -= board_speed

    # Display all objects
    window.fill(white)
    pygame.draw.rect(window, (0, 0, 255), (board_x, board_y, board_width, board_height))
    pygame.draw.circle(window, (255, 0, 0), (int(ball_x), int(ball_y)), ball_radius)

    # Display blocks
    for block in blocks:
        pygame.draw.rect(window, (0, 255, 0), (block[0], block[1], block_width, block_height))

    # Update score and level display
    font = pygame.font.Font(None, 36)
    score_text = font.render("SCORES: {}".format(score), True, black)
    window.blit(score_text, (width - score_text.get_width() - 10, 10))
    level_text = font.render("LEVEL: {}".format(level), True, black)
    window.blit(level_text, (10, 10))

    # Display "Game successfully completed! :))" and move to the next level if the game is over
    if game_over:
        font = pygame.font.Font(None, 120)
        text = font.render("FINISH", True, (255, 0, 0))
        window.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
        pygame.display.flip()

        # Wait until the player presses ENTER
        wait_for_enter = True
        while wait_for_enter:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = False
                        wait_for_enter = False
                        score = 0
                        ball_speed_y = -8
                        blocks = [(i * block_width, random.randint(50, 150)) for i in range(num_blocks // 2)]

    # Update the window
    pygame.display.flip()

    # Set the screen update frequency
    pygame.time.Clock().tick(60)

import pygame
from Brick import Bricks
from Paddles import *
from UI import ScoreBoard
from physics_objects import Ball
#from Screen import *


pygame.init()
Width = 525
Height = 600
BackCOLOR = "black"
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Not Breakout")
clock = pygame.time.Clock()
fps = 60
dt = 1/fps
clock = pygame.time.Clock()

#objects
pad = Paddle(x=250, y=550, width=100, height=20, screen_width=600)

bricks = Bricks(screen, brick_width =40 , brick_height=20)
ball = Ball(x=300, y=300, radius=5, screen=screen)
score = ScoreBoard(text_x = 300, x=200, color="white", screen = screen) # screen)
score.set_high_score()

# Game Loop
running = True
ball_active = True
while running:
    screen.fill(BackCOLOR)  # Clear screen with background color

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update Paddle Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        pad.move_right()
    if keys[pygame.K_LEFT]:
        pad.move_left()
   

     # Draw and update ball only if ball is active
    if ball_active:
        ball.move()
        ball.check_for_contact_on_x()
        ball.check_for_contact_on_y()

    # Ball-Paddle Collision
    if (
        pad.rect.y < ball.y + ball.radius < pad.rect.y + pad.height and
        pad.rect.x < ball.x < pad.rect.x + pad.width
    ):
        ball.bounce_y()
        ball.y = pad.y - ball.radius
    speed_multiplier = 1.035
    # Ball-Brick Collision
    for brick in bricks.bricks[:]:  # Copy the list to avoid iteration issues
        if brick.collidepoint(ball.x, ball.y - ball.radius) or brick.collidepoint(ball.x, ball.y + ball.radius):
            bricks.bricks.remove(brick)
            ball.bounce_y()
            score.update_score(10)
               # Increase ball speed
            ball.x_speed *= speed_multiplier
            ball.y_speed *= speed_multiplier
            break  # Prevent multiple collisions in one frame

    # Ball falls off the bottom
    if ball.y + ball.radius >= Height:
        ball.y = pad.y - ball.radius
        pygame.time.delay(2000)
        ball.bounce_y()
        score.lives -= 1
    # Check for win condition
    if len(bricks.bricks) <= 0:
        score.success()
        ball_active = False
        if keys[pygame.K_w]:
            if score.success():
                bricks.bricks.clear()
                bricks.set_values()
                ball_active=True
                score.level+=1
            
    #check for lose condition
    # Check if there are more trials
    if score.is_game_over():
        score.game_over()
    
    if score.lives == 0:
      ball_active = False
    
    if keys[pygame.K_0]:
        if score.is_game_over():
            score.score = 0
            score.lives = 5
            bricks.bricks.clear()
            bricks.set_values()
            ball_active=True
            ball.x_speed =2
            ball.y_speed=2
            score.level=0
        

    # Draw objects
    pad.draw(screen)
    bricks.show_bricks()
    score.show_scores()
    #ball.draw(screen)

    # Refresh screen
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
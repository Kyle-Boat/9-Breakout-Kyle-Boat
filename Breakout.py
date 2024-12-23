import pygame
from Brick import Bricks
from UI import ScoreBoard
from physics_objects import Ball, Paddle



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
bricks = Bricks(screen, width =40 , height=20)
ball = Ball(x=300, y=300, radius=5, screen=screen)
score = ScoreBoard(text_x = 300, x=200, color="white", screen = screen) # screen)
score.set_high_score()

# Game Loop
running = True
ball_active = True
while running:
    screen.fill(BackCOLOR)  

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        pad.right()
    if keys[pygame.K_LEFT]:
        pad.left()
   

     
    if ball_active:
        ball.move()
        ball.collisonX()
        ball.collisiony()

    
    if (
        pad.rect.y < ball.y + ball.radius < pad.rect.y + pad.height and
        pad.rect.x < ball.x < pad.rect.x + pad.width
    ):
        ball.bouncey()
        ball.y = pad.y - ball.radius
    speed_multiplier = 1.035
    
    for brick in bricks.bricks[:]:  
        if brick.collidepoint(ball.x, ball.y - ball.radius) or brick.collidepoint(ball.x, ball.y + ball.radius):
            bricks.bricks.remove(brick)
            ball.bouncey()
            score.update_score(10)
               # Increase ball speed
            ball.velX *= speed_multiplier
            ball.velY *= speed_multiplier
            break  

    # Ball falls off the bottom
    if ball.y + ball.radius >= Height:
        ball.y = pad.y - ball.radius
        pygame.time.delay(2000)
        ball.bouncey()
        score.lives -= 1
    # Check for win condition
    if len(bricks.bricks) <= 0:
        score.win()
        ball_active = False
        if keys[pygame.K_w]:
            if score.win():
                bricks.bricks.clear()
                bricks.set_values()
                ball_active=True
                score.level+=1
            
   
    if score.if_game_over():
        score.game_over()
    
    if score.lives == 0:
      ball_active = False
    
    if keys[pygame.K_0]:
        if score.if_game_over():
            score.score = 0
            score.lives = 5
            bricks.bricks.clear()
            bricks.set_values()
            ball_active=True
            ball.velX =2
            ball.velY=2
            score.level=0
        

    # Draw objects
    pad.draw(screen)
    bricks.draw_bricks()
    score.draw_scores()
    #ball.draw(screen)

    # Refresh screen
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
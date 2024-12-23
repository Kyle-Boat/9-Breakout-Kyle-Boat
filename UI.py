import pygame 
import datetime


class ScoreBoard:
    def __init__(self,text_x, x, color, screen):
        self.screen = screen
        self.color = color
        self.x = x
        self.score = 0
        self.lives = 5
        self.highScore = 0
        self.highScoreDate = ""
        self.level = 0
        self.text_x = text_x
        self.color = pygame.Color("white")
        self.font = pygame.font.SysFont("calibri", 20)
        self.now = datetime.datetime.now()
        self.formatted_date_time = self.now.strftime("%Y-%m-%d %H:%M:%S")


    def update_score(self, points=1):
        self.score += points

    def draw_scores(self):
        score_text = self.font.render(f"Score: {self.score}", True, self.color)
        lives_text = self.font.render(f"Lives: {self.lives}", True, self.color)
        high_score_text = self.font.render(f"High Score: {self.highScore}", True, self.color)
        level_text = self.font.render(f"Level: {self.level}", True, self.color)

        score_text_rect = score_text.get_rect(topleft=(self.x, 10))
        lives_text_text_rect = lives_text.get_rect(topleft=(self.x, 26))
        high_score_text_rect = high_score_text.get_rect(topleft=(self.x, 42))
        level_text_text_rect = level_text.get_rect(topleft=(self.x, 58))

        self.screen.blit(score_text, (self.x, 10))
        self.screen.blit(lives_text, (self.x, 26))
        self.screen.blit(high_score_text, (self.x, 42))
        self.screen.blit(level_text, (self.x, 58))


    def if_game_over(self):
        if self.lives == 0:
            return True
        return False

    def game_over(self):
        game_over_color = 'red'
        game_over_font = pygame.font.SysFont("calibri", 30)
        game_over_text = game_over_font.render(f"Game Over! Click '0' to restart.", True, game_over_color)
        game_over_rect = game_over_text.get_rect(topright=(50, 300))
        self.screen.blit(game_over_text, (50, 300))
        self.record_high_score()

    def win(self):
        game_success_color = 'green'
        game_success_font = pygame.font.SysFont("calibri", 30)
        game_success_text = game_success_font.render(f"You won! Click 'W' to restart.", True, game_success_color)
        game_success_rect = game_success_text.get_rect(topleft=(50, 300))
        self.screen.blit(game_success_text, (50, 300))
        self.record_high_score()
        
    
    def set_high_score(self):
        now = datetime.datetime.now()
        formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open("HighestScores.txt", mode="r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            with open("HighestScores.txt", mode="w") as data:
                data.write("0")
                score = 0
        else:
            score = lines[0]

        self.highScore = score
        
        

    def record_high_score(self):
        if self.score >= self.highScore:
            with open("HighestScores.txt", mode="w") as file:
                file.write(f"{self.score} {self.formatted_date_time}"  )
                
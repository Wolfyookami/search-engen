import pygame
import random

pygame.init()

screen_width = 600
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
border_color = (0, 0, 0)
pipe_border_color = (0, 0, 0)

font = pygame.font.Font(None, 36)

bird_x = 50
bird_y = 400
bird_width = 30
bird_height = 30
gravity = 0.9
bird_velocity = 0

pipe_width = 70
pipe_gap = 200
pipe_x = screen_width
pipe_height = random.randint(150, 600)

run = True
game_active = False
clock = pygame.time.Clock()
score = 0

button_font = pygame.font.Font(None, 48)
button_text = button_font.render("Play", True, white)
button_rect = button_text.get_rect(center=(screen_width // 2, screen_height // 2))

upgrade_font = pygame.font.Font(None, 36)
upgrade_text = upgrade_font.render("Upgrade Speed", True, white)
upgrade_rect = upgrade_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

coin_upgrade_font = pygame.font.Font(None, 36)
coin_upgrade_text = coin_upgrade_font.render("Upgrade 2x Coin", True, white)
coin_upgrade_rect = coin_upgrade_text.get_rect(center=(screen_width // 2, screen_height // 2 + 200))

speed_level = 1
max_speed_level = 10
total_coins = 0
coins_in_game = 0
upgrade_cost = 100
cost_increase_factor = 1.5
pipe_speed = 5

coin_multiplier_level = 1
max_coin_multiplier_level = 3
coin_multiplier_costs = [500, 1000, 2000]
coin_multiplier_effects = [2, 3, 4]

def upgrade_speed():
    global speed_level, pipe_speed, upgrade_cost, total_coins
    if speed_level < max_speed_level and total_coins >= upgrade_cost:
        total_coins -= upgrade_cost
        speed_level += 1
        upgrade_cost = int(upgrade_cost * cost_increase_factor)
        pipe_speed += 1

def upgrade_coin_multiplier():
    global coin_multiplier_level, total_coins
    if coin_multiplier_level < max_coin_multiplier_level and total_coins >= coin_multiplier_costs[coin_multiplier_level - 1]:
        total_coins -= coin_multiplier_costs[coin_multiplier_level - 1]
        coin_multiplier_level += 1

def reset_game():
    global bird_y, bird_velocity, pipe_x, pipe_height, score, coins_in_game
    bird_y = 400
    bird_velocity = 0
    pipe_x = screen_width
    pipe_height = random.randint(150, 600)
    score = 0
    coins_in_game = 0

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and game_active:
            if event.key == pygame.K_SPACE:
                bird_velocity = -10
        if event.type == pygame.MOUSEBUTTONDOWN and not game_active:
            mouse_pos = event.pos
            if button_rect.collidepoint(mouse_pos):
                game_active = True
                reset_game()
            if upgrade_rect.collidepoint(mouse_pos):
                upgrade_speed()
            if coin_upgrade_rect.collidepoint(mouse_pos):
                upgrade_coin_multiplier()

    if game_active:
        bird_velocity += gravity
        bird_y += bird_velocity

        pipe_x -= pipe_speed
        if pipe_x < -pipe_width:
            pipe_x = screen_width
            pipe_height = random.randint(150, 600)
            score += 1

            if score % 10 == 0:
                coins_in_game += coin_multiplier_effects[coin_multiplier_level - 1]
                total_coins += coin_multiplier_effects[coin_multiplier_level - 1]

        if bird_y > screen_height or bird_y < 0 or (
            pipe_x < bird_x + bird_width < pipe_x + pipe_width and 
            (bird_y < pipe_height or bird_y + bird_height > pipe_height + pipe_gap)):
            game_active = False

    screen.fill(white)

    pygame.draw.rect(screen, border_color, (0, 0, screen_width, screen_height), 5)

    if game_active:
        pygame.draw.rect(screen, black, (bird_x, bird_y, bird_width, bird_height))
        pygame.draw.rect(screen, green, (pipe_x, 0, pipe_width, pipe_height))
        pygame.draw.rect(screen, green, (pipe_x, pipe_height + pipe_gap, pipe_width, screen_height - pipe_height - pipe_gap))
        pygame.draw.rect(screen, pipe_border_color, (pipe_x, 0, pipe_width, pipe_height), 3)
        pygame.draw.rect(screen, pipe_border_color, (pipe_x, pipe_height + pipe_gap, pipe_width, screen_height - pipe_height - pipe_gap), 3)

        score_text = font.render(f'Score: {score}', True, black)
        screen.blit(score_text, (10, 10))

        coins_text = font.render(f'Coins: {coins_in_game}', True, black)
        screen.blit(coins_text, (screen_width - 150, 10))

        speed_level_text = font.render(f'Speed Level: {speed_level}', True, black)
        screen.blit(speed_level_text, (screen_width - 200, screen_height - 50))

        coin_multiplier_text = font.render(f'Coin Multiplier: {coin_multiplier_effects[coin_multiplier_level - 1]}x', True, black)
        screen.blit(coin_multiplier_text, (10, screen_height - 50))

    else:
        pygame.draw.rect(screen, blue, button_rect)
        screen.blit(button_text, button_rect)

        if speed_level < max_speed_level:
            pygame.draw.rect(screen, red, upgrade_rect)
            screen.blit(upgrade_text, upgrade_rect)

            upgrade_cost_text = font.render(f'Cost: {upgrade_cost} coins', True, black)
            screen.blit(upgrade_cost_text, (screen_width // 2 - 100, screen_height // 2 + 150))

        if coin_multiplier_level < max_coin_multiplier_level:
            pygame.draw.rect(screen, red, coin_upgrade_rect)
            screen.blit(coin_upgrade_text, coin_upgrade_rect)

            coin_multiplier_cost_text = font.render(f'Cost: {coin_multiplier_costs[coin_multiplier_level - 1]} coins', True, black)
            screen.blit(coin_multiplier_cost_text, (screen_width // 2 - 150, screen_height // 2 + 250))

        total_coins_text = font.render(f'Total Coins: {total_coins}', True, black)
        screen.blit(total_coins_text, (screen_width - 200, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

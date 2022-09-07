import pygame
from pygame.locals import *
from pygame import mixer
import sys
import random
from app.buttons import Button
import webbrowser

pygame.init()

BG = pygame.image.load("../Autober/app/Items/BG2.png")
BG2 = pygame.image.load("../Autober/app/Items/Background.png")
Grass = pygame.image.load("../Autober/app/Items/grass.png")


def get_font(size):
    return pygame.font.Font("../Autober/app/Items/font.ttf", size)


game_size = width, height = (600, 900)

road_width = int(width / 1.5)
center_road = road_width / 2
road_mark = int(width / 80)
y_coord = -200
right_lane = width / 2 + road_width / 4
left_lane = width / 2 - road_width / 4
speed = 1
blocks = ("roadblock", "car2")

# screen size
screen = pygame.display.set_mode(game_size)
pygame.display.set_caption("Autober")
pygame.display.update()

# Background Sound & Other
mixer.music.load('../Autober/app/Items/sound.mid')
mixer.music.play(-1)

btn_pressed = mixer.Sound('../Autober/app/Items/press.wav')
move = mixer.Sound('../Autober/app/Items/move.wav')
hit = mixer.Sound('../Autober/app/Items/hit.wav')

# cars image and location
car = pygame.image.load('../Autober/app/Items/car.png')
car_loc = car.get_rect()
car_loc.center = right_lane, height * 0.8

car2 = pygame.image.load('../Autober/app/Items/truck.png')
car2_loc = car2.get_rect()
car2_loc.center = left_lane, height * 0.2

# barrier = pygame.image.load('../Autober/app/Items/barrier.png')
# barrier_loc = barrier.get_rect()
# barrier_loc.center = right_lane, height * 0.2

score = 0
counter = 0


def play():
    global car_loc, car2_loc, right_lane, y_coord, left_lane, score, counter, speed
    while True:

        screen.blit(Grass, (0, 0))

        counter += 1
        if counter == 1000:
            speed += 0.2
            counter = 0
            # print(counter)
        car2_loc[1] += speed

        if car2_loc[1] > height:  # or barrier_loc[1] > height:
            score += 1
            if random.randint(0, 1) == 0:
                car2_loc.center = right_lane, y_coord
            else:
                car2_loc.center = left_lane, y_coord
        # Car hit
        if car_loc[0] == car2_loc[0] and car2_loc[1] > car_loc[1] - 250:
            print("Lost", "Score :", score)
            final_score = score
            score = 0
            counter = 0
            speed = 1
            car2_loc.center = left_lane, y_coord
            hit.play()
            mixer.music.stop()
            try_again(final_score)
            break

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                move.play()
                if event.key in [K_a, K_LEFT] and car_loc[0] > (width - road_width) / 2:
                    car_loc = car_loc.move([-int(center_road), 0])
                if event.key in [K_d, K_RIGHT] and car_loc[0] < (width - road_width) / 2:
                    car_loc = car_loc.move([int(center_road), 0])

        # road
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (width / 2 - center_road, 0, road_width, height))
        # road marks
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (width / 2 - road_mark / 2, 0, road_mark, height))

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (width / 2 + road_width / 2 - road_mark * 2.5, 0, road_mark, height))

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (width / 2 - road_width / 2 + road_mark * 2, 0, road_mark, height))

        screen.blit(car, car_loc)
        screen.blit(car2, car2_loc)
        # screen.blit(barrier, barrier_loc)

        pygame.display.update()


def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        main_mouse_pos = pygame.mouse.get_pos()

        title_text = get_font(30).render("Autober", True, "#FFFF00")
        title_rect = title_text.get_rect(center=(width / 2, height * 0.1))

        main_text = get_font(20).render("Developed by Nostaame", True, "#000000")
        main_rect = main_text.get_rect(center=(width / 2, height * 0.2))

        play_btn = Button(image=pygame.image.load("../Autober/app/Items/Play Rect.png"),
                          pos=(width / 2, int(height * 0.4)),
                          text_input="PLAY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        leaderboard_btn = Button(image=pygame.image.load("../Autober/app/Items/Play Rect.png"),
                                 pos=(width / 2, int(height * 0.6)),
                                 text_input="LEADERBOARD", font=get_font(30), base_color="#d7fcd4",
                                 hovering_color="White")
        quit_btn = Button(image=pygame.image.load("../Autober/app/Items/Quit Rect.png"),
                          pos=(width / 2, height * 0.8),
                          text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        screen.blit(title_text, title_rect)
        screen.blit(main_text, main_rect)

        for button in [play_btn, leaderboard_btn, quit_btn]:
            button.changeColor(main_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.checkForInput(main_mouse_pos):
                    btn_pressed.play()
                    play()
                if leaderboard_btn.checkForInput(main_mouse_pos):
                    btn_pressed.play()
                    webbrowser.open("http://127.0.0.1:5000/leaderboard")

                if quit_btn.checkForInput(main_mouse_pos):
                    btn_pressed.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def try_again(high_score):
    while True:
        screen.blit(BG2, (0, 0))

        lost_text = get_font(30).render("YOU LOST!!", True, "#b68f40")
        lost_rect = lost_text.get_rect(center=(width / 2, height * 0.1))

        scoreword_text = get_font(30).render("SCORE", True, "#b68f40")
        scoreword_rect = scoreword_text.get_rect(center=(width / 2, height * 0.2))

        score_text = get_font(30).render(str(high_score), True, "#b68f40")
        score_rect = score_text.get_rect(center=(width / 2, height * 0.3))

        try_mouse_pos = pygame.mouse.get_pos()

        retry_btn = Button(image=pygame.image.load("../Autober/app/Items/Retry Rect.png"),
                           pos=(width / 2, height / 2),
                           text_input="RETRY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        back_btn = Button(image=pygame.image.load("../Autober/app/Items/Retry Rect.png"),
                          pos=(width / 2, height * 0.7),
                          text_input="MENU", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        screen.blit(lost_text, lost_rect)
        screen.blit(scoreword_text, scoreword_rect)
        screen.blit(score_text, score_rect)

        for button in [retry_btn, back_btn]:
            button.changeColor(try_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if retry_btn.checkForInput(try_mouse_pos):
                    mixer.music.play(-1)
                    play()
                if back_btn.checkForInput(try_mouse_pos):
                    btn_pressed.play()
                    mixer.music.play(-1)
                    main_menu()
        pygame.display.update()

# main_menu()

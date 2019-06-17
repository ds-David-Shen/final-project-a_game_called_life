'''
-------------------------------------------------------------------------------
Name:	master.py
Purpose:
create a game using python arcade
the game we created is snake (because python = snake)
Author:	Shen D, Chen X
Created:	13/06/2019
Finished:   17/06/2019
-----------------------------------------------------------------------------
'''

import arcade
import random
import time
import os

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

# Set how many rows and columns we will have
ROW_COUNT = 20
COLUMN_COUNT = 20

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell
# and on the edges of the screen.
# set to one to see the grid easier when testing
MARGIN = 0

# set scores and high score to start at 0
score = 0
high_score = 0

direction = 0

# set if screen is chosen
title = True
play_screen = False
game_over = False
how_to_play = False

# set frame rate per second
fps = 5

# create key press delay so player cannot break the game by switching direction too quickly
key_press_delay = time.time()

# set if song is chosen
song_chosen = False

# default theme of music
theme = "sounds/maintheme.mp3"

# for gif in game over screen (arcade does not support gifs)
game_over_image_frame = 0

# create two lists to store x and y coordinates of the snake
rsnake = []
csnake = []

# set position of bug
bug_xPos = random.randint(0, COLUMN_COUNT - 2)
bug_yPos = random.randint(0, ROW_COUNT - 2)

# Do the math to figure out screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN

grid = []


# create sound function
def sound(sound):
    play_sound = arcade.load_sound(sound)
    arcade.play_sound(play_sound)


# create title screen
def title_screen():
    texture = arcade.load_texture("Images/snake-title-screen.png")
    arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH,
                                  SCREEN_HEIGHT, texture, 0)
    arcade.draw_text("press A for easy mode\npress V then A for hard mode\npress C for how to play\npress the space bar to quit",
                     SCREEN_WIDTH / 2 - SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / 2.5, arcade.color.WHITE,
                     15, font_name="TIMES NEW ROMAN")


# create end screen
def end_screen(frame):
    global grid, direction, score
    arcade.set_background_color(arcade.color.BLACK)

    if frame < 10:
        game_over_text = arcade.load_texture(
            "Images/Game_over_gif/frame_0" + str(frame) + "_delay-0.11s.gif")
    else:
        game_over_text = arcade.load_texture(
            "Images/Game_over_gif/frame_" + str(frame) + "_delay-0.11s.gif")
    scale = 2
    arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, game_over_text.width * scale,
                                  game_over_text.height * scale, game_over_text, 0)

    # block watermark because cropping is too much work
    arcade.draw_rectangle_filled(540, 136, 140, 20, arcade.color.BLACK)
    arcade.draw_text("Your score is " + str(score) + "\npress any key to play again\npress the space bar to quit",
                     SCREEN_WIDTH / 2 - 100,
                     SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / 4, arcade.color.WHITE, 15, font_name="TIMES NEW ROMAN")

    direction = 0


# create how to play screen
def how_to_play_screen():
    arcade.set_background_color(arcade.color.BLACK)
    controls = arcade.load_texture("Images/controls.png")
    arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, controls.width,
                                  controls.height, controls, 0)
    arcade.draw_text("press A for easy mode\npress V then A for hard mode\npress the space bar to quit", SCREEN_WIDTH / 2 - 150,
                     SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / 2.5, arcade.color.WHITE, 25, font_name="TIMES NEW ROMAN")


# update function
def on_update(delta_time):
    global bug_xPos, bug_yPos, score, high_score, direction, play_screen, game_over, invincibility_powerup_time, invincibility, doublescore, doublescore_powerup_time, powerup_time

    if time.time() - invincibility_powerup_time < powerup_time:
        invincibility = True
    else:
        invincibility_powerup_time =  0
        invincibility = False

    if time.time() - doublescore_powerup_time < powerup_time:
        doublescore = True
    else:
        doublescore_powerup_time =  0
        doublescore = False

    # set direction
    if direction == 1:
        rsnake[len(rsnake) - 1] += 1
    if direction == 2:
        rsnake[len(rsnake) - 1] -= 1
    if direction == 3:
        csnake[len(csnake) - 1] += 1
    if direction == 4:
        csnake[len(csnake) - 1] -= 1

    # increase score when bug is reached, move bug to new location
    if grid[rsnake[len(rsnake) - 1]][csnake[len(csnake) - 1]] == 2:
        crunch = "sounds/Crunch.mp3"
        sound(crunch)
        if doublescore:
            score += 2
        else:
            score += 1
        rsnake.append(rsnake[len(rsnake) - 1])
        csnake.append(csnake[len(csnake) - 1])
        bug_xPos = random.randint(0, COLUMN_COUNT - 1)
        bug_yPos = random.randint(0, ROW_COUNT - 1)
        chance_of_powerup()

    if grid[rsnake[len(rsnake) - 1]][csnake[len(csnake) - 1]] == 4:
        crunch = "sounds/Crunch.mp3"
        sound(crunch)
        if doublescore:
            score += 2
        else:
            score += 1
        rsnake.append(rsnake[len(rsnake) - 1])
        csnake.append(csnake[len(csnake) - 1])
        bug_xPos = random.randint(0, COLUMN_COUNT - 1)
        bug_yPos = random.randint(0, ROW_COUNT - 1)
        chance_of_powerup()
        invincibility_powerup_time = time.time()

    if grid[rsnake[len(rsnake) - 1]][csnake[len(csnake) - 1]] == 5:
        crunch = "sounds/Crunch.mp3"
        sound(crunch)
        score += 2
        rsnake.append(rsnake[len(rsnake) - 1])
        csnake.append(csnake[len(csnake) - 1])
        bug_xPos = random.randint(0, COLUMN_COUNT - 1)
        bug_yPos = random.randint(0, ROW_COUNT - 1)
        chance_of_powerup()
        doublescore = True
        doublescore_powerup_time = time.time()

    # snake movement
    if play_screen:
        for i in range(len(rsnake) - 1):
            rsnake[i] = rsnake[i + 1]
            csnake[i] = csnake[i + 1]
            if i == 0:
                grid[rsnake[i]][csnake[i]] = 0
            else:

                # see if snake hits itself
                for j in range(i - 1):
                    if rsnake[j] == rsnake[i] and csnake[j] == csnake[i] and invincibility == False:
                        if game_over == False:
                            doublescore_powerup_time = False
                            sound_effect = "sounds/Bonk.mp3"
                            sound(sound_effect)
                        game_over = True
                        if score > high_score:
                            high_score = score

                # head of snake
                if i == len(rsnake) - 2:
                    grid[rsnake[i]][csnake[i]] = 3

                # body of snake
                else:
                    grid[rsnake[i]][csnake[i]] = 1

        # game over if snake hits the  boundaries
        if rsnake[len(rsnake) - 1] > ROW_COUNT - 1 or rsnake[len(rsnake) - 1] < 0 or COLUMN_COUNT - 1 < csnake[
            len(rsnake) - 1] or csnake[len(rsnake) - 1] < 0:
            invincibility_powerup_time = 0
            doublescore_powerup_time = 0
            sound_effect = "sounds/Bonk.mp3"
            sound(sound_effect)
            play_screen = False
            direction = 0
            game_over = True
            if score > high_score:
                high_score = score


# rng for powerup pickups
rng = 0
invincibility = False
invincibility_powerup_time = 0

doublescore = False
doublescore_powerup_time = 0
powerup_time = 15


# function for powerup spawning
def chance_of_powerup():
    global rng
    rng = random.randint(1, 20)


# create bug function
def bug():
    global grid, bug_xPos, bug_yPos, rng

    # make sure bug does not spawn in body of snake
    while grid[bug_yPos][bug_xPos] == 1:
        bug_xPos = random.randint(0, COLUMN_COUNT - 2)
        bug_yPos = random.randint(0, ROW_COUNT - 2)

    if rng == 1:
        grid[bug_xPos][bug_yPos] = 4
    elif rng == 2:
        grid[bug_xPos][bug_yPos] = 5
    else:
        grid[bug_yPos][bug_xPos] = 2


# create draw function
def on_draw():
    global score, direction, game_over, how_to_play, song_chosen, play_screen, game_over_image_frame, invincibility
    arcade.start_render()

    # see which screen to draw
    if title:
        title_screen()

    elif game_over:
        end_screen(game_over_image_frame)
        if game_over_image_frame == 17:
            game_over_image_frame = 0
        game_over_image_frame += 1

    elif how_to_play:
        how_to_play_screen()
    else:
        # After the title screen, play song
        if song_chosen == False:
            sound(theme)
            song_chosen = True

        # Draw the grid
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # Figure out what color to draw the box

                # Do the math to figure out where the box is
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                # Determine what to draw on each grid
                if grid[row][column] == 1:
                    color = arcade.color.AMAZON
                    arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                    color = arcade.color.GREEN
                    arcade.draw_rectangle_outline(x, y, WIDTH, HEIGHT, color, 3)
                elif grid[row][column] == 2:
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                    texture = arcade.load_texture("Images/bug.png")
                    arcade.draw_texture_rectangle(x, y, WIDTH,
                                                  HEIGHT, texture, 0)
                elif grid[row][column] == 3:
                    texture = arcade.load_texture("Images/Head.jpg")
                    if direction == 1:
                        arcade.draw_texture_rectangle(x, y, WIDTH,
                                                      HEIGHT, texture, 180)
                    if direction == 2:
                        arcade.draw_texture_rectangle(x, y, WIDTH,
                                                      HEIGHT, texture)
                    if direction == 3:
                        arcade.draw_texture_rectangle(x, y, WIDTH,
                                                      HEIGHT, texture, 90)
                    if direction == 4:
                        arcade.draw_texture_rectangle(x, y, WIDTH,
                                                      HEIGHT, texture, 270)
                elif grid[row][column] == 4:
                    texture = arcade.load_texture("Images/minecraft_golden_apple.png")
                    arcade.draw_texture_rectangle(x, y, WIDTH,
                                                  HEIGHT, texture, 0)

                elif grid[row][column] == 5:
                    texture = arcade.load_texture("Images/double_cherry.jpg")
                    arcade.draw_texture_rectangle(x, y, WIDTH,
                                                  HEIGHT, texture, 0)

                else:
                    texture = arcade.load_texture("Images/grassBlock.png")
                    arcade.draw_texture_rectangle(x, y, WIDTH,
                                                  HEIGHT, texture, 0)

            # draw bug on grid
            bug()

            # draw score
            arcade.draw_text("Score: " + str(score), 20, SCREEN_HEIGHT - 60, arcade.color.BLACK, 18,
                             font_name="COMIC SANS MS")
            arcade.draw_text(str(high_score), 90, SCREEN_HEIGHT - 100,
                             arcade.color.BLACK, 18, font_name="COMIC SANS MS")
            trophy = arcade.load_texture("Images/trophy.png")
            scale = 0.4
            arcade.draw_texture_rectangle(60, SCREEN_HEIGHT - 100, trophy.width * scale,
                                          trophy.height * scale, trophy, 0)

            if invincibility:
                arcade.draw_text("Invincible: " + str(int(31 - (time.time() - invincibility_powerup_time))), SCREEN_WIDTH / 2, SCREEN_HEIGHT - 60,
                                 arcade.color.BLACK, 18, font_name="COMIC SANS MS")

            if doublescore:
                arcade.draw_text("Double Score: " + str(int(31 - (time.time() - doublescore_powerup_time))), 20, SCREEN_HEIGHT - 150,
                                 arcade.color.BLACK, 18, font_name="COMIC SANS MS")


# types of game modes
konamicode = ['u', 'u', 'd', 'd', 'l', 'r', 'l', 'r', 'b', 'a']
hard_mode = ['v', 'a']
easy_mode = ['a']
game_mode = []


def start_game():
    global direction, title, play_screen, how_to_play, game_over, key_press_delay
    direction = 3
    title = False
    play_screen = True
    how_to_play = False
    game_over = False
    key_press_delay = time.time()


def on_key_press(key, modifiers):
    global direction, title, play_screen, game_over, how_to_play, konamicode, hard_mode, easy_mode, game_mode, key_press_delay, fps, theme, score, game_over_image_frame

    if title:
        if key == arcade.key.UP:
            game_mode.append('u')
        elif key == arcade.key.DOWN:
            game_mode.append('d')
        elif key == arcade.key.LEFT:
            game_mode.append('l')
        elif key == arcade.key.RIGHT:
            game_mode.append('r')
        elif key == arcade.key.B:
            game_mode.append('b')
        elif key == arcade.key.A:
            game_mode.append('a')
        elif key == arcade.key.V:
            game_mode.append('v')
            if len(game_mode) >= 2:
                game_mode = ['v']
        elif key == arcade.key.C:
            title = False
            how_to_play = True
            game_mode = []
        elif key == arcade.key.SPACE:
            quit()
        else:
            game_mode = []

        # set game mode based off input
        if game_mode == konamicode:
            theme = "sounds/bloons_theme.mp3"
            fps *= 4
            schedule(fps)
            start_game()

        if game_mode == hard_mode:
            theme = "sounds/hard_theme.mp3"
            fps *= 2
            schedule(fps)
            start_game()

        if game_mode == easy_mode:
            start_game()

    if how_to_play:
        if key == arcade.key.A:
            game_mode.append('a')
        elif key == arcade.key.V:
            game_mode.append('v')
            if len(game_mode) >= 2:
                game_mode = ['v']
        elif key == arcade.key.SPACE:
            quit()
        else:
            game_mode = []
        # set game mode based off input
        if game_mode == hard_mode:
            fps *= 2
            schedule(fps)
            start_game()

        if game_mode == easy_mode:
            start_game()

    # make it so the player can restart after they die
    if game_over:
        game_over_image_frame = 0
        for i in range(len(rsnake)):
            grid[rsnake[i]][csnake[i]] = 0
        rsnake.clear()
        csnake.clear()
        rsnake.append(4)
        rsnake.append(4)
        rsnake.append(4)
        csnake.append(6)
        csnake.append(6)
        csnake.append(6)
        score = 0

        # quit if space bar is pressed when game is over
        if key == arcade.key.SPACE:
            quit()

        start_game()

    # set direction based on input in play screen
    elif play_screen and time.time() - key_press_delay > 1 / fps - 1 / 16:
        if key == arcade.key.W and direction != 2:
            direction = 1
            key_press_delay = time.time()
        if key == arcade.key.S and direction != 1:
            direction = 2
            key_press_delay = time.time()

        if key == arcade.key.D and direction != 4:
            direction = 3
            key_press_delay = time.time()

        if key == arcade.key.A and direction != 3:
            direction = 4
            key_press_delay = time.time()

        if key == arcade.key.SPACE:
            quit()


# create function that determines speed of game
def schedule(fps):
    arcade.schedule(on_update, 1 / fps)

# sets up the game
def setup():
    global grid, fps
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Snake Game")
    schedule(fps)
    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press

    # create body for snake
    rsnake.append(4)
    rsnake.append(4)
    rsnake.append(4)
    csnake.append(6)
    csnake.append(6)
    csnake.append(6)

    # array is simply a list of lists.
    for row in range(ROW_COUNT + 1):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(COLUMN_COUNT + 1):
            grid[row].append(0)  # Append a cell

    arcade.run()


if __name__ == '__main__':
    setup()
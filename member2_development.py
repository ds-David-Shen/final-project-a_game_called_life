# Xavier

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

# set scores
score = 0
high_score = 0

direction = 0

# set if screen is chosen
title = True
play_screen = False
game_over = False
how_to_play = False

# set frame rate
fps = 5

# create key press delay so player cannot break the game by switching direction too quickly
key_press_delay = time.time()

# set if song is chosen
song_chosen = False

# default theme of music
theme = "sounds/maintheme.mp3"

# for gif in game over screen(arcade does not support gifs
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


# create music function for songs
def sound(sound):
    play_sound = arcade.load_sound(sound)
    arcade.play_sound(play_sound)


# create title screen
def title_screen():
    texture = arcade.load_texture("Images/snake-title-screen.png")
    arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH,
                                  SCREEN_HEIGHT, texture, 0)
    arcade.draw_text("press A for easy mode\npress V then A for hard mode\npress C for how to play", SCREEN_WIDTH / 2 - SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / 2.5, arcade.color.WHITE, 15, font_name= "TIMES NEW ROMAN")

# create end screen
def end_Screen(frame):
    global grid, direction, score
    arcade.set_background_color(arcade.color.BLACK)


    if frame < 10:
        game_over_text = arcade.load_texture(
            "Images/Game_over_gif/frame_0"+str(frame)+"_delay-0.11s.gif")
    else:
        game_over_text = arcade.load_texture(
            "Images/Game_over_gif/frame_" + str(frame) + "_delay-0.11s.gif")
    scale = 2
    arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, game_over_text.width * scale,
                                          game_over_text.height * scale, game_over_text, 0)

    # block watermark because cropping is too much work
    arcade.draw_rectangle_filled(540, 136, 140, 20, arcade.color.BLACK)
    arcade.draw_text("Your score is " + str(score) + "\npress any key to play again\npress the space bar to quit", SCREEN_WIDTH / 2 - 100,
                     SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / 4, arcade.color.WHITE, 15, font_name="TIMES NEW ROMAN")

    direction = 0

# create how to play screen
def how_to_play_screen():
    arcade.set_background_color(arcade.color.BLACK)
    controls = arcade.load_texture("Images/controls.png")
    arcade.draw_texture_rectangle(SCREEN_WIDTH / 2,  SCREEN_HEIGHT / 2, controls.width,
                                 controls.height, controls, 0)
    arcade.draw_text("press A for easy mode\npress V then A for hard mode", SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / 2.5, arcade.color.WHITE, 25, font_name= "TIMES NEW ROMAN")

# update function
def on_update(delta_time):
    global bug_xPos, bug_yPos, score, high_score, direction, play_screen, game_over

    # set direction
    if direction == 1:
        rsnake[len(rsnake)-1] += 1
    if direction == 2:
        rsnake[len(rsnake)-1] -= 1
    if direction == 3:
        csnake[len(csnake)-1] += 1
    if direction == 4:
        csnake[len(csnake)-1] -= 1

    # increase score when bug is reached, move bug to new location
    if grid[rsnake[len(rsnake)-1]][csnake[len(csnake)-1]] == 2:
        crunch = "sounds/Crunch.mp3"
        sound(crunch)
        score += 1
        rsnake.append(rsnake[len(rsnake)-1])
        csnake.append(csnake[len(csnake)-1])
        bug_xPos = random.randint(0,COLUMN_COUNT - 1)
        bug_yPos = random.randint(0,ROW_COUNT - 1)
def setup():

    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Snake")
    arcade.set_background_color(arcade.color.BLACK)
    arcade.schedule(on_update, 1/60)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw


    arcade.run()


if __name__ == '__main__':
    setup()

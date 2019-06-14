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
MARGIN = 1

score = 0

direction = 5

# set if screen is chosen
title = True
game_over = False

# set frame rate
fps = 5

# create key press delay so player cannot switch direction too quickly
key_press_delay = time.time()

# set if song is chosen
song_chosen = False

# default theme of music
theme = "music/maintheme.mp3"

# create body of snake
rsnake = []
csnake = []
rsnake.append(4)
rsnake.append(4)
rsnake.append(4)
csnake.append(6)
csnake.append(6)
csnake.append(6)


# Do the math to figure out screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN


grid = []

# create music function for songs
def music(song):
    play_song = arcade.load_sound(song)
    arcade.play_sound(play_song)


# create title screen
def title_screen():
    time.sleep(0.5)
    arcade.set_background_color((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    arcade.draw_text("SnEk", SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2, arcade.color.BLACK, 50)
    arcade.draw_text("press WASD keys\nto play", SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 100, arcade.color.BLACK, 20)
    arcade.draw_text("WASD keys to move", SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 200, arcade.color.BLACK, 20)


# create end screen
def end_Screen():
    global grid, direction
    arcade.set_background_color(arcade.color.WHITE)
    arcade.draw_text("Game over",SCREEN_WIDTH/2 - 150,SCREEN_HEIGHT/2, arcade.color.BLACK,50)
    direction = 0

# update function
def on_update(delta_time):
    global fruit_xPos, fruit_yPos, score, direction, game_over

    # set direction
    if direction == 1:
        rsnake[len(rsnake)-1] += 1
    if direction == 2:
        rsnake[len(rsnake)-1] -= 1
    if direction == 3:
        csnake[len(csnake)-1] += 1
    if direction == 4:
        csnake[len(csnake)-1] -= 1

    # increase score when fruit is reached, move fruit to new location
    if grid[rsnake[len(rsnake)-1]][csnake[len(csnake)-1]] == 2:
        score += 1
        rsnake.append(rsnake[len(rsnake)-1])
        csnake.append(csnake[len(csnake)-1])
        fruit_xPos = random.randint(0,COLUMN_COUNT - 1)
        fruit_yPos = random.randint(0,ROW_COUNT - 1)
        arcade.set_background_color((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # snake movement
    if title == False and game_over == False:
        for i in range(len(rsnake)- 1):
            rsnake[i] = rsnake[i+1]
            csnake[i] = csnake[i+1]
            if i == 0:
                grid[rsnake[i]][csnake[i]] = 0
            else:

                # see if snake hits itself
                for j in range(i - 1):
                    if rsnake[j] == rsnake[i] and csnake[j] == csnake[i]:
                        game_over = True

                # head of snake
                if i == len(rsnake) - 2:
                    grid[rsnake[i]][csnake[i]] = 3

                # body of snake
                else:
                    grid[rsnake[i]][csnake[i]] = 1


# set position of fruit
fruit_xPos = random.randint(0, COLUMN_COUNT - 2)
fruit_yPos = random.randint(0, ROW_COUNT - 2)


# create fruit function
def fruit():
    global grid, fruit_xPos, fruit_yPos
    # make sure fruit does not spawn in body of snake
    while grid[fruit_yPos][fruit_xPos] == 1:
        fruit_xPos = random.randint(0, COLUMN_COUNT - 2)
        fruit_yPos = random.randint(0, ROW_COUNT - 2)
    grid[fruit_yPos][fruit_xPos] = 2


texture = arcade.load_texture("Images/chibi-miku.png")

# create draw function
def on_draw():
    global score, direction, game_over, song_chosen
    arcade.start_render()

    # see which screen to draw based on booleans
    if title:
        title_screen()
    elif game_over:
        end_Screen()
    else:
        # after the title screen, play song
        if song_chosen == False:
            music(theme)
            song_chosen = True

        # game over if snake hits the  boundaries
        if rsnake[len(rsnake)-1] > ROW_COUNT - 1 or rsnake[len(rsnake)-1] < 0 or csnake[len(rsnake)-1] > COLUMN_COUNT - 1 or csnake[len(rsnake)-1] < 0:
            end_Screen()
            direction = 0
            game_over = True

        fruit()
        if game_over:
            pass
        else:
            # Draw the grid
            for row in range(ROW_COUNT):
                for column in range(COLUMN_COUNT):
                    # Figure out what color to draw the box
                    if grid[row][column] == 1:
                        color = arcade.color.GREEN
                    elif grid[row][column] == 2:
                        color = arcade.color.RED
                    else:
                        color = arcade.color.WHITE

                    # Do the math to figure out where the box is
                    x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                    y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                    # Draw the box
                    if grid[row][column] != 3:
                        arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                    else:
                        arcade.draw_texture_rectangle(x, y, WIDTH,
                                                      HEIGHT, texture, 0)
                    if grid[row][column] != 0:
                        arcade.draw_rectangle_outline(x, y, WIDTH, HEIGHT, arcade.color.WHITE, 3)
        # draw score
        arcade.draw_text("Score: "+str(score), 20, SCREEN_HEIGHT - 20, arcade.color.BLACK,18)


# create secret code
konamicode = ['u','u','d','d','l','r','l','r','b','a']
secret = []


def on_key_press(key, modifiers):
    global direction, title, konamicode, secret, key_press_delay, fps, theme

    if title == True:
        if key == arcade.key.UP:
            secret.append('u')
        if key == arcade.key.DOWN:
            secret.append('d')
        if key == arcade.key.LEFT:
            secret.append('l')
        if key == arcade.key.RIGHT:
            secret.append('r')
        if key == arcade.key.B:
            secret.append('b')
        if key == arcade.key.A:
            secret.append('a')

        # if the player does certain inputs in the beginning of the game,
        # play secret theme
        if konamicode == secret:
            theme = "music/Motteke! Sailor Fuku! - Lucky Star Full Opening.mp3"

    # set direction based off key press, create a delay in the key presses
    if title == True and (key == arcade.key.W or key == arcade.key.A or key == arcade.key.S or key == arcade.key.D):
        direction = 3
        title = False
        key_press_delay = time.time()
    if key == arcade.key.W and direction != 0 and direction != 2 and time.time() - key_press_delay > 1/fps - fps/100:
        direction = 1
        key_press_delay = time.time()
    if key == arcade.key.S and direction != 0 and direction != 1 and time.time() - key_press_delay > 1/fps - fps/100:
        direction = 2
        key_press_delay = time.time()

    if key == arcade.key.D and direction != 0 and direction != 4 and time.time() - key_press_delay > 1/fps - fps/100:
        direction = 3
        key_press_delay = time.time()

    if key == arcade.key.A and direction != 0 and direction != 3 and time.time() - key_press_delay > 1/fps - fps/100:
        direction = 4
        key_press_delay = time.time()


def setup():
    global grid, fps
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "SnakeAttempt")
    arcade.set_background_color((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    arcade.schedule(on_update, 1 / fps)
    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press

    # array is simply a list of lists.
    for row in range(ROW_COUNT+1):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(COLUMN_COUNT+1):
            grid[row].append(0)  # Append a cell

    arcade.run()


if __name__ == '__main__':
    setup()
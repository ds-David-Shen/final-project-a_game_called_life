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

    # snake movement
    if play_screen:
        for i in range(len(rsnake)- 1):
            rsnake[i] = rsnake[i+1]
            csnake[i] = csnake[i+1]
            if i == 0:
                grid[rsnake[i]][csnake[i]] = 0
            else:

                # see if snake hits itself
                for j in range(i - 1):
                    if rsnake[j] == rsnake[i] and csnake[j] == csnake[i]:
                        if game_over == False:
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
        if rsnake[len(rsnake)-1] > ROW_COUNT - 1 or rsnake[len(rsnake)-1] < 0 or csnake[len(rsnake)-1] > COLUMN_COUNT - 1 or csnake[len(rsnake)-1] < 0:
            sound_effect = "sounds/Bonk.mp3"
            sound(sound_effect)
            play_screen = False
            direction = 0
            game_over = True
            if score > high_score:
                high_score = score


# create bug function
def bug():
    global grid, bug_xPos, bug_yPos
    # make sure bug does not spawn in body of snake
    while grid[bug_yPos][bug_xPos] == 1:
        bug_xPos = random.randint(0, COLUMN_COUNT - 2)
        bug_yPos = random.randint(0, ROW_COUNT - 2)
    grid[bug_yPos][bug_xPos] = 2


# create draw function
def on_draw():
    global score, direction, game_over, how_to_play, song_chosen, play_screen, game_over_image_frame
    arcade.start_render()

    # see which screen to draw
    if title:
        title_screen()

    elif game_over:
        end_Screen(game_over_image_frame)
        if game_over_image_frame == 17:
            game_over_image_frame = 0
        game_over_image_frame += 1


    elif how_to_play:
        how_to_play_screen()
    else:
        # after the title screen, play song
        if song_chosen == False:
            sound(theme)
            song_chosen = True

        # draw bug
        bug()

        # Draw the grid
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # Figure out what color to draw the box

                # Do the math to figure out where the box is
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

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

                else:
                    texture = arcade.load_texture("Images/grassBlock.png")
                    arcade.draw_texture_rectangle(x, y, WIDTH,
                                                  HEIGHT, texture, 0)

            # draw score
            arcade.draw_text("Score: "+str(score), 20, SCREEN_HEIGHT - 60, arcade.color.BLACK,18, font_name= "COMIC SANS MS")
            arcade.draw_text(str(high_score), 90, SCREEN_HEIGHT - 100,
                             arcade.color.BLACK, 18, font_name= "COMIC SANS MS")
            trophy = arcade.load_texture("Images/trophy.png")
            scale = 0.4
            arcade.draw_texture_rectangle(60, SCREEN_HEIGHT - 100, trophy.width * scale,
                                          trophy.height * scale, trophy, 0)



# create secret code because why not
konamicode = ['u','u','d','d','l','r','l','r','b','a']
hard_mode =['v','a']
secret = []


def on_key_press(key, modifiers):
    global direction, title, play_screen, game_over, how_to_play, konamicode, hard_mode, secret, key_press_delay, fps, theme, score, game_over_image_frame

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
        if key == arcade.key.V:
            secret.append('v')

        # if the player does certain inputs in the beginning of the game,
        # play secret theme and double speed



        if secret == konamicode:
            theme = "sounds/bloonsTheme.mp3"
            fps *= 3
            schedule(fps)

        if secret == hard_mode :
            fps *= 1.5
            schedule(fps)

        # set direction based off key press, create a delay in the key presses
        if key == arcade.key.A:
            direction = 3
            title = False
            play_screen = True
            key_press_delay = time.time()

        if key == arcade.key.C:
            title = False
            how_to_play = True

    if how_to_play:
        if key == arcade.key.A:
            secret.append('a')
        if key == arcade.key.V:
            secret.append('v')
        if secret == hard_mode:
            fps *= 1.5
            schedule(fps)

    if how_to_play and key == arcade.key.A:
        how_to_play = False
        play_screen = True
        direction = 3

    # make it so the player can restart after they die
    if game_over == True:
        game_over_image_frame = 0
        game_over = False
        play_screen = True
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
        direction = 3
        score = 0
        if key == arcade.key.SPACE:
            quit()

    elif play_screen:
        if key == arcade.key.W and direction != 0 and direction != 2 and time.time() - key_press_delay > 1/fps - fps/80:
            direction = 1
            key_press_delay = time.time()
        if key == arcade.key.S and direction != 0 and direction != 1 and time.time() - key_press_delay > 1/fps - fps/80:
            direction = 2
            key_press_delay = time.time()

        if key == arcade.key.D and direction != 0 and direction != 4 and time.time() - key_press_delay > 1/fps - fps/80:
            direction = 3
            key_press_delay = time.time()

        if key == arcade.key.A and direction != 0 and direction != 3 and time.time() - key_press_delay > 1/fps - fps/80:
            direction = 4
            key_press_delay = time.time()


def schedule(fps):
    arcade.schedule(on_update, 1 / fps)

def setup():
    global grid, fps
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Snake")
    schedule(fps)
    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press

    #create body for snake
    rsnake.append(4)
    rsnake.append(4)
    rsnake.append(4)
    csnake.append(6)
    csnake.append(6)
    csnake.append(6)

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
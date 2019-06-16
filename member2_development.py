# Xavier

import arcade
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


# set if screen is chosen
game_over = True
how_to_play = False

# switch between screens
# how_to_play, game_over = game_over, how_to_play

score = 0
# Do the math to figure out screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN

game_over_image_frame = 0
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
    arcade.draw_text("Your score is " + str(score) + "\n press any key\n to play again", SCREEN_WIDTH / 2 - 100,
                     SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / 4, arcade.color.WHITE, 25, font_name="TIMES NEW ROMAN")


# create how to play screen
def how_to_play_screen():
    arcade.set_background_color(arcade.color.BLACK)
    controls = arcade.load_texture("Images/controls.png")
    arcade.draw_texture_rectangle(SCREEN_WIDTH / 2,  SCREEN_HEIGHT / 2, controls.width,
                                 controls.height, controls, 0)
    arcade.draw_text("press A to start", SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / 2.5, arcade.color.WHITE, 25, font_name= "TIMES NEW ROMAN")

def on_update(delta_time):
    pass


def on_draw():
    arcade.start_render()
    global game_over_image_frame
    if game_over:
        end_Screen(game_over_image_frame)
        if game_over_image_frame == 17:
            game_over_image_frame = 0
        game_over_image_frame += 1
        time.sleep(0.11)
    if how_to_play:
        how_to_play_screen()
    # how_to_play_screen()

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
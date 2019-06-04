import arcade
import time
import os
from PIL import Image
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)
# Set how many rows and columns we will have
ROW_COUNT = 20
COLUMN_COUNT = 20

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 0#change to 1 when editing code
monkeybox = 150
# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN + monkeybox
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN

lives = 100
cash = 202

num_of_balloons = 5
balloons_per_round = 5
rounds = 0
round_Happens = False

round_start = time.time()
grid = []

rowpath = []
columnpath = []
monkeyList = []
monkey_chosen = 0

balloons_on_square = []

def music():
    #place song here
    pass

def on_update(delta_time):
    global rounds
    global balloons_per_round
    global num_of_balloons
    global round_Happens
    global lives
    global round_start
    if title:
        round_start = time.time()
    else:
        music()
        if time.time() - round_start > 10 and round_Happens == False and title == False:
            # print(time.time() - round_start)
            round_Happens = True

        if balloons_per_round == 0:
            round_Happens = False
            rounds += 1
            # print(rounds)
            num_of_balloons += 5
            balloons_per_round = num_of_balloons
            round_start = time.time()
        checked = [False] * len(rowpath)
        if round_Happens:
            if rounds == 1:
                rounds += 1
                pass
            else:

                # time.sleep(1/10)
                for i in range(len(rowpath)):
                    x = rowpath[i]
                    y = columnpath[i]
                    if i == 0:
                        grid[x][y] = 7
                    if i < len(rowpath) - 1:
                        x1 = rowpath[i + 1]
                        y1 = columnpath[i + 1]
                    if grid[x][y] == 7 and i != len(rowpath) - 1 and checked[i] == False:
                        if grid[x1][y1] == 6:
                            print("hit")

                        grid[x1][y1] = 7
                        grid[x][y] = 1

                        checked[i + 1] = True

                    elif grid[x][y] == 7 and i == len(rowpath) - 1 and checked[i] == False:
                        lives -= 1
                        balloons_per_round -=1
                        if lives == 0:
                            exit()



#create function for resizing image using pil(keeps it higher resolution)
def resizeImage(xpos, ypos, xsize,ysize, image):
    size = xsize,ysize
    im = Image.open(image)
    im_resized = im.resize(size, Image.ANTIALIAS)
    im_resized.save(image,"PNG")
    image = arcade.load_texture(image)
    arcade.draw_texture_rectangle(xpos, ypos, xsize, ysize, image)

title = True
def titleScreen():
    #make title screen
    resizeImage(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, "Images/TitleScreen.png", )
    arcade.draw_rectangle_filled(375,190, 90, 120, arcade.color.WHITE)
    arcade.draw_text("7",340,140,arcade.color.BLACK,120)


def on_draw():
    global title
    arcade.start_render()
    if title:
        titleScreen()
    # Draw the grid
    else:
        track()
        global round_Happens
        global lives
        global rounds
        global cash

        on_update(time.sleep(0.1))


        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # print(grid[ROW_COUNT-row-1][column],end="")
                if grid[row][column] == 1:
                    color = arcade.color.BEIGE
                elif grid[row][column] == 7:
                    color = arcade.color.PURPLE

                elif grid[row][column] == 2:
                    color = arcade.color.RED
                    if grid[row][column+1] == 7:
                        grid[row][column+1] = 6
                        cash += 1
                    elif grid[row][column-1] == 7:
                        grid[row][column-1] = 6
                        cash += 1
                    elif grid[row+1][column] == 7:
                        grid[row+1][column] = 6
                        cash += 1
                    elif grid[row-1][column] == 7:
                        grid[row-1][column] = 6
                        cash += 1



                elif grid[row][column] == 3:
                    color = arcade.color.BLUE
                elif grid[row][column] == 4:
                    color = arcade.color.GREEN
                elif grid[row][column] == 5:
                    color = arcade.color.YELLOW
                elif grid[row][column] == 6:
                    color = arcade.color.BLACK
                    grid[row][column] = 0

                else:
                    color = arcade.color.WHITE

                # Do the math to figure out where the box is
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                # Draw the box
                arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)
        #     print()
        # print()

        monkeybox_outline = 2
        arcade.draw_rectangle_filled(SCREEN_WIDTH-monkeybox/2, SCREEN_HEIGHT/2, monkeybox, SCREEN_HEIGHT,
                                     arcade.color.BEIGE)
        arcade.draw_rectangle_outline(SCREEN_WIDTH - monkeybox / 2, SCREEN_HEIGHT / 2, monkeybox - monkeybox_outline,
                                      SCREEN_HEIGHT - monkeybox_outline,
                                     arcade.color.BLACK)
        arcade.draw_text("Towers", SCREEN_WIDTH-monkeybox/2-40, SCREEN_HEIGHT-20, arcade.color.BLACK)
        arcade.draw_text("Lives:"+str(lives), SCREEN_WIDTH - monkeybox / 2 - 40, SCREEN_HEIGHT - 350, arcade.color.BLACK)
        arcade.draw_text("Cash:"+str(cash), SCREEN_WIDTH - monkeybox / 2 - 40, SCREEN_HEIGHT - 380, arcade.color.BLACK)
        arcade.draw_text("round: "+str(rounds), 20, SCREEN_HEIGHT - 20, arcade.color.BLACK)
        for i in range(4):
            if monkeyList[i] == 0:
                color = arcade.color.RED
            elif monkeyList[i] == 1:
                color = arcade.color.BLUE
            elif monkeyList[i] == 2:
                color = arcade.color.GREEN
            else:
                color = arcade.color.YELLOW
            x = SCREEN_WIDTH-monkeybox/2
            y = SCREEN_HEIGHT- 80 - 60*i
            arcade.draw_rectangle_filled(x, y, 60, 60, color)
            arcade.draw_rectangle_outline(x, y, 60,60, arcade.color.BLACK)

def on_key_press(key, modifiers):
    global round_Happens

    if key == arcade.key.F and round_Happens == False and title == False:

        round_Happens = True


def on_key_release(key, modifiers):
    pass


monkeyClicked = -1


def track():
    grid[0][6] = 1
    rowpath.append(0)
    columnpath.append(6)
    grid[1][6] = 1
    rowpath.append(1)
    columnpath.append(6)
    grid[2][6] = 1
    rowpath.append(2)
    columnpath.append(6)
    grid[3][6] = 1
    rowpath.append(3)
    columnpath.append(6)
    grid[4][6] = 1
    rowpath.append(4)
    columnpath.append(6)
    grid[5][6] = 1
    rowpath.append(5)
    columnpath.append(6)
    grid[6][6] = 1
    rowpath.append(6)
    columnpath.append(6)
    grid[6][7] = 1
    rowpath.append(6)
    columnpath.append(7)
    grid[6][8] = 1
    rowpath.append(6)
    columnpath.append(8)
    grid[6][9] = 1
    rowpath.append(6)
    columnpath.append(9)
    grid[6][10] = 1
    rowpath.append(6)
    columnpath.append(10)
    grid[6][11] = 1
    rowpath.append(6)
    columnpath.append(11)
    grid[6][12] = 1
    rowpath.append(6)
    columnpath.append(12)
    grid[6][13] = 1
    rowpath.append(6)
    columnpath.append(13)
    grid[5][13] = 1
    rowpath.append(5)
    columnpath.append(13)
    grid[4][13] = 1
    rowpath.append(4)
    columnpath.append(13)
    grid[3][13] = 1
    rowpath.append(3)
    columnpath.append(13)
    grid[2][13] = 1
    rowpath.append(2)
    columnpath.append(13)
    grid[2][14] = 1
    rowpath.append(2)
    columnpath.append(14)
    grid[2][15] = 1
    rowpath.append(2)
    columnpath.append(15)
    grid[2][16] = 1
    rowpath.append(2)
    columnpath.append(16)
    grid[3][16] = 1
    rowpath.append(3)
    columnpath.append(16)
    grid[4][16] = 1
    rowpath.append(4)
    columnpath.append(16)
    grid[5][16] = 1
    rowpath.append(5)
    columnpath.append(16)
    grid[6][16] = 1
    rowpath.append(6)
    columnpath.append(16)
    grid[7][16] = 1
    rowpath.append(7)
    columnpath.append(16)
    grid[8][16] = 1
    rowpath.append(8)
    columnpath.append(16)
    grid[9][16] = 1
    rowpath.append(9)
    columnpath.append(16)
    grid[10][16] = 1
    rowpath.append(10)
    columnpath.append(16)
    grid[11][16] = 1
    rowpath.append(11)
    columnpath.append(16)
    grid[11][15] = 1
    rowpath.append(11)
    columnpath.append(15)
    grid[11][14] = 1
    rowpath.append(11)
    columnpath.append(14)
    grid[11][13] = 1
    rowpath.append(11)
    columnpath.append(13)
    grid[11][12] = 1
    rowpath.append(11)
    columnpath.append(12)
    grid[11][11] = 1
    rowpath.append(11)
    columnpath.append(11)
    grid[11][10] = 1
    rowpath.append(11)
    columnpath.append(10)
    grid[11][9] = 1
    rowpath.append(11)
    columnpath.append(9)
    grid[11][8] = 1
    rowpath.append(11)
    columnpath.append(8)
    grid[11][7] = 1
    rowpath.append(11)
    columnpath.append(7)
    grid[11][6] = 1
    rowpath.append(11)
    columnpath.append(6)
    grid[11][5] = 1
    rowpath.append(11)
    columnpath.append(5)
    grid[11][4] = 1
    rowpath.append(11)
    columnpath.append(4)
    grid[11][3] = 1
    rowpath.append(11)
    columnpath.append(3)
    grid[11][2] = 1
    rowpath.append(11)
    columnpath.append(2)
    grid[12][2] = 1
    rowpath.append(12)
    columnpath.append(2)
    grid[13][2] = 1
    rowpath.append(13)
    columnpath.append(2)
    grid[14][2] = 1
    rowpath.append(14)
    columnpath.append(2)
    grid[15][2] = 1
    rowpath.append(15)
    columnpath.append(2)
    grid[16][2] = 1
    rowpath.append(16)
    columnpath.append(2)
    grid[16][3] = 1
    rowpath.append(16)
    columnpath.append(3)
    grid[16][4] = 1
    rowpath.append(16)
    columnpath.append(4)
    grid[16][5] = 1
    rowpath.append(16)
    columnpath.append(5)
    grid[16][6] = 1
    rowpath.append(16)
    columnpath.append(6)
    grid[16][7] = 1
    rowpath.append(16)
    columnpath.append(7)
    grid[16][8] = 1
    rowpath.append(16)
    columnpath.append(8)
    grid[16][9] = 1
    rowpath.append(16)
    columnpath.append(9)
    grid[16][10] = 1
    rowpath.append(16)
    columnpath.append(10)
    grid[17][10] = 1
    rowpath.append(17)
    columnpath.append(10)
    grid[18][10] = 1
    rowpath.append(18)
    columnpath.append(10)
    grid[19][10] = 1
    rowpath.append(19)
    columnpath.append(10)
    # print(rowpath)
    # print(columnpath)
    # exit(0)
    # [0, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 6, 5, 4, 3, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 12, 13, 14, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16, 17, 18, 19]
    # [6, 6, 6, 6, 6, 6, 6, 7, 8, 9, 10, 11, 12, 13, 13, 13, 13, 13, 14, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 2, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def on_mouse_press(x, y, button, modifiers):

    global monkeyClicked
    global title
    global cash
    # Change the x/y screen coordinates to grid coordinates
    column = x // (WIDTH + MARGIN)
    row = y // (HEIGHT + MARGIN)


    # Make sure we are on-grid. It is possible to click in the upper right
    # corner in the margin and go to a grid location that doesn't exist
    if row < ROW_COUNT and column < COLUMN_COUNT:
        # if grid[row][column] == 1:
        #     print(f"grid[{row}][{column}] = 1")
        #     print(f"rowpath.append({row})")
        #     print(f"columnpath.append({column})")
        # Flip the location between 1 and 0.
        # if grid[row][column] == 0:
        #     grid[row][column] = 1
        if grid[row][column] == 0 and monkeyClicked == 0:
            if cash<200:
                print("broke")
            else:
                grid[row][column] = 2
                cash -= 1#change back to 200 later
        elif grid[row][column] == 0 and monkeyClicked == 1 and cash >= 360:
            grid[row][column] = 3
            cash -= 360
        elif grid[row][column] == 0 and monkeyClicked == 2 and cash >= 350:
            grid[row][column] = 4
            cash -= 350
        elif grid[row][column] == 0 and monkeyClicked == 3 and cash >= 500:
            grid[row][column] = 5
            cash -= 500


    if x > SCREEN_WIDTH - monkeybox + 42 and x < SCREEN_WIDTH - 42:
        # print("in the monkey box")
        monkeyClicked = int(6.1+5/60-(y)/60)
    else:
        monkeyClicked = -1
    if monkeyClicked != -2:
        title = False


def setup():
    global grid

    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Bloons Tower Defense 7")
    arcade.set_background_color(arcade.color.BLACK)
    arcade.schedule(on_update, 1/60)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_mouse_press = on_mouse_press

    # array is simply a list of lists.
    for row in range(ROW_COUNT):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(COLUMN_COUNT):
            grid[row].append(0)  # Append a cell

    for i in range(4):
        monkeyList.append(i)

    arcade.run()


if __name__ == '__main__':
    setup()

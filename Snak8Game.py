import tkinter
import random
import os

# ---------------- GAME SETTINGS ----------------
ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

# ---------------- HIGH SCORE FILE (SAFE PATH) ----------------
HIGH_SCORE_FILE = os.path.join(os.path.dirname(__file__), "highscore.txt")

try:
    with open(HIGH_SCORE_FILE, "r") as file:
        high_score = int(file.read())
except:
    high_score = 0


# ---------------- TILE CLASS ----------------
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# ---------------- WINDOW ----------------
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(
    window,
    bg="black",
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    highlightthickness=0,
)
canvas.pack()

window.update()

# Center window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = (screen_width // 2) - (window_width // 2)
window_y = (screen_height // 2) - (window_height // 2)

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")


# ---------------- RESET GAME ----------------
def reset_game():
    global snake, food, snake_body
    global velocityX, velocityY
    global score, game_over, game_state, paused

    snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
    food = Tile(
        random.randint(0, COLS - 1) * TILE_SIZE,
        random.randint(0, ROWS - 1) * TILE_SIZE
    )

    snake_body = []
    velocityX = 1
    velocityY = 0

    score = 0
    game_over = False
    game_state = "playing"
    paused = False


# ---------------- INITIAL STATE ----------------
snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)

snake_body = []
velocityX = 0
velocityY = 0

score = 0
game_over = False
game_state = "start"
paused = False


# ---------------- INPUT ----------------
def change_direction(e):
    global velocityX, velocityY, game_state, paused

    # PAUSE
    if e.keysym.lower() == "p" and game_state == "playing" and not game_over:
        paused = not paused
        return

    # START
    if game_state == "start":
        if e.keysym == "space":
            reset_game()
        return

    # RESTART
    if game_over:
        if e.keysym == "Return":
            reset_game()
        return

    # MOVEMENT
    if e.keysym == "Up" and velocityY != 1:
        velocityX = 0
        velocityY = -1

    elif e.keysym == "Down" and velocityY != -1:
        velocityX = 0
        velocityY = 1

    elif e.keysym == "Left" and velocityX != 1:
        velocityX = -1
        velocityY = 0

    elif e.keysym == "Right" and velocityX != -1:
        velocityX = 1
        velocityY = 0


# ---------------- GAME LOGIC ----------------
def move():
    global snake, food, snake_body
    global score, game_over, high_score

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

    # DETECTS IF IT HITS A WALL IS GAME OVER
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return

    # IF IT HITS ITSELF IS GAMEOVER
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    # FOOD EAT
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))

        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE

        score += 1

        # SAVE HIGH SCORE
        if score > high_score:
            high_score = score
            try:
                with open(HIGH_SCORE_FILE, "w") as file:
                    file.write(str(high_score))
            except:
                pass

    # MOVE BODY
    for i in range(len(snake_body) - 1, -1, -1):
        if i == 0:
            snake_body[i].x = snake.x - velocityX * TILE_SIZE
            snake_body[i].y = snake.y - velocityY * TILE_SIZE
        else:
            snake_body[i].x = snake_body[i - 1].x
            snake_body[i].y = snake_body[i - 1].y


# ---------------- DRAW ----------------
def draw():
    global game_state

    if game_state == "playing" and not paused:
        move()

    canvas.delete("all")

    # BORDER
    canvas.create_rectangle(
        0, 0, WINDOW_WIDTH, WINDOW_HEIGHT,
        outline="white",
        width=3
    )

    # FOOD
    canvas.create_rectangle(
        food.x, food.y,
        food.x + TILE_SIZE,
        food.y + TILE_SIZE,
        fill="white"
    )

    # SNAKE HEAD
    canvas.create_rectangle(
        snake.x, snake.y,
        snake.x + TILE_SIZE,
        snake.y + TILE_SIZE,
        fill="limegreen"
    )

    # SNAKE BODY
    for tile in snake_body:
        canvas.create_rectangle(
            tile.x, tile.y,
            tile.x + TILE_SIZE,
            tile.y + TILE_SIZE,
            fill="limegreen"
        )

    # START SCREEN
    if game_state == "start":
        canvas.create_text(
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 - 40,
            text="SNAKE",
            fill="white",
            font=("Arial", 40, "bold")
        )

        canvas.create_text(
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 + 10,
            text="Press SPACE to Start",
            fill="white",
            font=("Arial", 20, "bold")
        )

    # GAME OVER SCREEN
    elif game_over:
        canvas.create_text(
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 - 60,
            text="GAME OVER",
            fill="red",
            font=("Arial", 34, "bold")
        )

        canvas.create_text(
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 - 10,
            text=f"Score: {score}",
            fill="white",
            font=("Arial", 18)
        )

        canvas.create_text(
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 + 20,
            text=f"Best: {high_score}",
            fill="gold",
            font=("Arial", 18, "bold")
        )

        canvas.create_text(
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 + 70,
            text="Press ENTER to Restart",
            fill="white",
            font=("Arial", 18, "bold")
        )

    # GAME PLAYING
    else:
        canvas.create_text(
            WINDOW_WIDTH / 2,
            20,
            text=f"Score: {score}   Best: {high_score}",
            fill="white",
            font=("Arial", 14, "bold")
        )

        if paused:
            canvas.create_text(
                WINDOW_WIDTH / 2,
                WINDOW_HEIGHT / 2,
                text="PAUSED\nPress P to Resume",
                fill="yellow",
                font=("Arial", 24, "bold")
            )

    window.after(100, draw)


# ---------------- START GAME ----------------
draw()
window.bind("<KeyRelease>", change_direction)
window.mainloop()
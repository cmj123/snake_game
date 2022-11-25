import tkinter as tk
from PIL import Image, ImageTk
import time

MOVE_INCREMENT = 20
MOVES_PER_SECOND = 5
GAME_SPEED = 1000 // MOVES_PER_SECOND

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620,background='black',highlightthickness=0)

        # Initialise snake positions
        self.snake_positions = [(100,100), (80,100), (60,100)]
        self.food_position = (200, 100)
        self.score = 0
        self.direction = "Right"
        self.bind_all("<Key>", self.on_key_press)

        # Load images for food and snake
        self.load_assets()
        # Create snake and food object
        self.create_objects()

        self.after(75, self.perform_actions)

    def load_assets(self):
        try:
            self.snake_body_image = Image.open("./assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print(error)
            root.destroy()

    def create_objects(self):
        # create score visual
        self.create_text(
            45,12,text=f"Score : {self.score}", tag="score", fill="#fff", font=("TkDefaultFont",14)
        )

        # create snake visuals
        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position, image=self.snake_body, tag='snake')

        # create food visual
        self.create_image(*self.food_position, image=self.food, tag='food')

        # create game boundaries line
        self.create_rectangle(7, 27, 593,613, outline="#525d69")

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]

        if self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == "Down":
            new_head_position = (head_x_position , head_y_position + MOVE_INCREMENT)
        elif self.direction == "Up":
            new_head_position = (head_x_position , head_y_position - MOVE_INCREMENT)


        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    def perform_actions(self):
        if self.check_collisions():
            return

        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]

        return (
            head_x_position in (0, 600-MOVE_INCREMENT)
            or head_y_position in (20,620)
            or (head_x_position, head_y_position) in self.snake_positions[1:]
        )

    def on_key_press(self, e):
        new_direction = e.keysym

        all_directions = ("Up","Down","Right", "Left")
        opposites = ({"Up", "Down"}, {"Right", "Left"})

        if (
            new_direction in all_directions 
            and {new_direction, self.direction} not in opposites
        ):
            self.direction = new_direction

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"
            )

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score}", tag="score")


            

root = tk.Tk()
root.title("Snake")
root.resizable(False, False)

# Create an instance of Snake
board = Snake()
board.pack()

root.mainloop()
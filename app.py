import tkinter as tk
from PIL import Image, ImageTk

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620,background='black',highlightthickness=0)

        # Initialise snake positions
        self.snake_positions = [(100,100), (80,100), (60,100)]
        self.food_position = (200, 100)
        self.score =0

        # Load images for food and snake
        self.load_assets()
        # Create snake and food object
        self.create_objects()

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
            

root = tk.Tk()
root.title("Snake")
root.resizable(False, False)

# Create an instance of Snake
board = Snake()
board.pack()

root.mainloop()
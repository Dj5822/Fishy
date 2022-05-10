# Imports
import random
import time
from tkinter import *


class GUI:
    """Creates all screens required in the game."""

    CANVAS_WIDTH = 800
    CANVAS_HEIGHT = 600
    BUTTON_WIDTH = 10
    BUTTON_HEIGHT = 2

    def __init__(self):
        """Construct the GUI."""
        """Create main menu, instruction and game screen."""
        self.window = Tk()
        self.window.title(string='Fishy')
        self._main_menu = MainMenu(self)
        self._instruction_screen = InstructionScreen(self)
        self._game_screen = GameScreen(self)
        self._game_over_screen = GameOverScreen(self)
        self.navigate_to_menu()
        self.window.mainloop()

    def navigate_to_menu(self):
        """Show the menu screen.

        :return: None
        """
        self._instruction_screen.hide_instruction_screen()
        self._game_over_screen.hide_game_over_screen()
        self._main_menu.show_main_menu_screen()
        self._game_screen.hide_game_screen()

    def navigate_to_instruction_screen(self):
        """Show the instruction screen.

        :return: None
        """
        self._instruction_screen.show_instruction_screen()
        self._main_menu.hide_main_menu_screen()
        self._game_screen.hide_game_screen()

    def navigate_to_game_screen(self):
        """Show the game screen.

        :return: None
        """
        self._instruction_screen.hide_instruction_screen()
        self._game_over_screen.hide_game_over_screen()
        self._main_menu.hide_main_menu_screen()
        self._game_screen.show_game_screen()
        self._game_screen.start_game()

    def navigate_to_gameover_screen(self, message):
        """Show the game over screen.

        :param message: win or lose
        :return: None
        """
        self._game_screen.hide_game_screen()
        self._game_over_screen.show_game_over_screen(message)


class MainMenu:
    """Display the main menu screen."""

    def __init__(self, gui):
        """Construct the main menu.

        :param gui:
        """
        self.window = gui.window
        self._main_menu_canvas = Canvas(self.window,
                                        width=GUI.CANVAS_WIDTH,
                                        height=GUI.CANVAS_HEIGHT,
                                        background="light blue")

        # Display title of game.
        self._game_title = self._main_menu_canvas.create_text(
            GUI.CANVAS_WIDTH / 2,
            GUI.CANVAS_HEIGHT / 4,
            text="Fishy",
            fill="black",
            font='Helvetica 50 bold')

        # Start game button
        start_button = Button(self._main_menu_canvas,
                              text="Start game",
                              height=GUI.BUTTON_HEIGHT,
                              width=GUI.BUTTON_WIDTH,
                              command=gui.navigate_to_game_screen)
        start_button.place(x=GUI.CANVAS_WIDTH / 2.2,
                           y=GUI.CANVAS_HEIGHT / 2.2)

        # Instruction button
        instruction_button = Button(
            self._main_menu_canvas,
            text="Instructions",
            height=GUI.BUTTON_HEIGHT,
            width=GUI.BUTTON_WIDTH,
            command=gui.navigate_to_instruction_screen)
        instruction_button.place(x=GUI.CANVAS_WIDTH / 2.2,
                                 y=GUI.CANVAS_HEIGHT / 1.7)

        # Exit button
        exit_button = Button(self._main_menu_canvas,
                             text="Exit",
                             height=GUI.BUTTON_HEIGHT,
                             width=GUI.BUTTON_WIDTH,
                             command=self.window.destroy)
        exit_button.place(x=GUI.CANVAS_WIDTH / 2.2,
                          y=GUI.CANVAS_HEIGHT / 1.4)

    def show_main_menu_screen(self):
        """Display main menu canvas.

        :return: None
        """
        # Main menu canvas is packed and created
        self._main_menu_canvas.pack()

    def hide_main_menu_screen(self):
        """Hide the main menu screen.

        :return: None
        """
        self._main_menu_canvas.pack_forget()


class InstructionScreen:
    """Display the instruction screen."""

    def __init__(self, gui):
        """Display the instruction screen.

        :param gui:
        """
        # Creates and places instruction canvas
        self._instruction_canvas = Canvas(gui.window,
                                          width=GUI.CANVAS_WIDTH,
                                          height=GUI.CANVAS_HEIGHT,
                                          background="light blue")

        self._instruction_canvas.create_text(GUI.CANVAS_WIDTH / 2,
                                             GUI.CANVAS_HEIGHT / 4,
                                             text="Instructions:\n"
                                                  "You are the orange blob. "
                                                  "Use arrow keys to move up"
                                                  " ,down, left, and right.\n"
                                                  "Eat smaller fishes to grow"
                                                  " and avoid bigger fishes"
                                                  " as you will be eaten "
                                                  "\nEnjoy!",
                                             fill="black",
                                             font='Helvetica 15 bold')

        # Button to go back to main menu
        exit_instruction_button = Button(self._instruction_canvas,
                                         text="Back",
                                         height=GUI.BUTTON_HEIGHT,
                                         width=GUI.BUTTON_WIDTH,
                                         command=gui.navigate_to_menu)

        exit_instruction_button.place(x=GUI.CANVAS_WIDTH / 2.2,
                                      y=GUI.CANVAS_HEIGHT / 1.4)

    def show_instruction_screen(self):
        """Display the instructions for fishy.

        :return: None
        """
        self._instruction_canvas.pack()

    def hide_instruction_screen(self):
        """Hide the instruction screen.

        :return: None
        """
        self._instruction_canvas.pack_forget()


class GameScreen:
    """Make the game screen.

    Enemies will be spawned every second until SPAWN LIMIT is reached.
    Each enemy will move in a certain direction.
    """

    SPAWN_LIMIT = 20
    RESET_X = 700
    RESET_Y = 200
    RESET_SIZE = 25

    def __init__(self, gui):
        """Create the game screen.

        :param gui:
        """
        # Creates and places game canvas.
        self._game_canvas = Canvas(gui.window, width=GUI.CANVAS_WIDTH,
                                   height=GUI.CANVAS_HEIGHT,
                                   background="light blue")
        self.gui = gui
        self.window = gui.window
        self._enemy_list = []
        self._continue_game = False

        # Creates the player.
        self._player = PlayerFish(self._game_canvas, GameScreen.RESET_X,
                                  GameScreen.RESET_Y, GameScreen.RESET_SIZE)

        # Key binding
        self._game_canvas.focus_set()
        self._game_canvas.bind('<Up>', self._player.move_up)
        self._game_canvas.bind('<Right>', self._player.move_right)
        self._game_canvas.bind('<Down>', self._player.move_down)
        self._game_canvas.bind('<Left>', self._player.move_left)

        # Creates and moves the NPC fish
        self._enemy_creator()
        self._move_enemies()

        # Enable collision detection
        self._collision_detection()

    def show_game_screen(self):
        """Display the game screen.

        :return: None
        """
        self._game_canvas.pack()

    def hide_game_screen(self):
        """Hide the game screen.

        :return: None
        """
        self._game_canvas.pack_forget()

    def _enemy_creator(self):
        """Generate the enemy fish left and right side.

        :return: None
        """
        if self._continue_game:
            if len(self._enemy_list) < GameScreen.SPAWN_LIMIT:
                random_num = random.randint(0, GUI.CANVAS_HEIGHT)
                spawn_left = random.randint(0, 1)
                # The lowest number of the 3 is generated
                size = min(random.randint(EnemyFish.MIN_SIZE,
                                          EnemyFish.MAX_SIZE),
                           random.randint(EnemyFish.MIN_SIZE,
                                          EnemyFish.MAX_SIZE),
                           random.randint(EnemyFish.MIN_SIZE,
                                          EnemyFish.MAX_SIZE))
                if spawn_left:
                    self._enemy_list.append(EnemyFish(self._game_canvas,
                                                      -size,
                                                      random_num, size, 1))
                else:
                    self._enemy_list.append(EnemyFish(self._game_canvas,
                                                      GUI.CANVAS_WIDTH + size,
                                                      random_num, size, -1))
        # Refresh
        self.window.after(1000, self._enemy_creator)

    def _collision_detection(self):
        """Detect if the player has touched/collided with the enemy fish.

        :return: None
        """
        if self._continue_game:
            collision_list = self._player.detect_collision()
            if len(collision_list) > 0:
                for col in collision_list:
                    for enemy in self._enemy_list:
                        if enemy.fish == col:
                            if self._player.size >= GUI.CANVAS_WIDTH:
                                # Display message when game is won.
                                self.game_over("YOU WON!!! :)")
                            elif enemy.size <= self._player.size:
                                self._player.enlarge(enemy.size)
                                enemy.reset()
                            else:
                                # Display message when game is lost.
                                self.game_over("You lost :(")
        # Refresh
        self.window.after(10, self._collision_detection)

    def _move_enemies(self):
        """Movement of the enemy fish.

        :return: None
        """
        if self._continue_game:
            for enemy in self._enemy_list:
                enemy.move()
        self._game_canvas.after(10, self._move_enemies)

    def start_game(self):
        """Start the game.

        :return: None
        """
        # Create enemies
        self._continue_game = True

    def game_over(self, message):
        """When game is won or lost, display message and clear screen.

        :param message: Message of whether it is a win or a loss.
        :return: None
        """
        self._continue_game = False
        self._game_canvas.delete("all")
        self._player.reset(GameScreen.RESET_X, GameScreen.RESET_Y,
                           GameScreen.RESET_SIZE)
        self._player.size = GameScreen.RESET_SIZE
        self._enemy_list.clear()
        self.gui.navigate_to_gameover_screen(message)

    def back_to_menu(self):
        """Goes back to the main menu using the navigation method.

        :return: None
        """
        self._game_canvas.delete("all")
        self.gui.navigate_to_menu()


class GameOverScreen:
    """Displays the game over screen."""

    def __init__(self, gui):
        """Create the game over screen.

        :param gui:
        """
        self._gameover_canvas = Canvas(gui.window, width=GUI.CANVAS_WIDTH,
                                       height=GUI.CANVAS_HEIGHT,
                                       background="light blue")

        self._gameover_canvas.create_text(GUI.CANVAS_WIDTH / 2,
                                          GUI.CANVAS_HEIGHT / 4,
                                          text="Game over")

        self._gameover_message = self._gameover_canvas.create_text(
            GUI.CANVAS_WIDTH / 2,
            GUI.CANVAS_HEIGHT / 3,
            text="-")

        self._back_button = Button(self._gameover_canvas,
                                   text="Back to Menu",
                                   height=GUI.BUTTON_HEIGHT,
                                   width=GUI.BUTTON_WIDTH,
                                   command=gui.navigate_to_menu)

        self._restart_button = Button(self._gameover_canvas,
                                      text="Restart",
                                      height=GUI.BUTTON_HEIGHT,
                                      width=GUI.BUTTON_WIDTH,
                                      command=gui.navigate_to_game_screen)

        self._back_button.place(x=GUI.CANVAS_WIDTH / 2.2,
                                y=GUI.CANVAS_HEIGHT / 1.4)
        self._restart_button.place(x=GUI.CANVAS_WIDTH / 2.2,
                                   y=GUI.CANVAS_HEIGHT / 2.4)

    def show_game_over_screen(self, message):
        """Display the instructions for fishy.

        Forgets main menu canvas and packs instruction canvas.
        Has a button which can go back to main menu canvas.
        :return:
        """
        self._gameover_canvas.itemconfig(self._gameover_message, text=message)
        self._gameover_canvas.pack()

    def hide_game_over_screen(self):
        """Hides the game screen.

        :return: None
        """
        self._gameover_canvas.pack_forget()


class PlayerFish:
    """Creates the player which is the fish."""

    # Refresh rate is how often player and fish updates position.
    MOVEMENT_SPEED = 8

    def __init__(self, canvas, x_position, y_position, size):
        """Create the player fish which can be moved.

        :param canvas: fish
        :param x_position: the horizontal position of fish
        :param y_position: the vertical position of fish
        :param size: size of fish
        """
        self.canvas = canvas
        self._speed_vertical = PlayerFish.MOVEMENT_SPEED
        self._speed_horizontal = PlayerFish.MOVEMENT_SPEED
        self.size = size
        self.x_position = x_position
        self.y_position = y_position

        self.fish = self.canvas.create_rectangle((
            self.x_position,
            self.y_position,
            self.x_position + self.size,
            self.y_position + self.size),
            fill="orange")

    def reset(self, x_position, y_position, size):
        """Reset player.

        :param x_position: horizontal position of the fish
        :param y_position: vertical position of the fish
        :param size: size of the fish
        :return: None
        """
        self.size = size
        self.x_position = x_position
        self.y_position = y_position
        self.fish = self.canvas.create_rectangle((
            self.x_position,
            self.y_position,
            self.x_position + self.size,
            self.y_position + self.size),
            fill="orange")

    def move_up(self, event):
        """Move the fish up.

        :param event: Move up
        :return: None
        """
        if self.y_position > 0:
            self.y_position -= PlayerFish.MOVEMENT_SPEED
            self.canvas.move(self.fish, 0, -PlayerFish.MOVEMENT_SPEED)

    def move_right(self, event):
        """Move the fish right.

        :param event: move right
        :return: None
        """
        if self.x_position < GUI.CANVAS_WIDTH - self.size:
            self.x_position += PlayerFish.MOVEMENT_SPEED
            self.canvas.move(self.fish, PlayerFish.MOVEMENT_SPEED, 0)

    def move_down(self, event):
        """Move the fish down.

        :param event: move down
        :return: None
        """
        if self.y_position < GUI.CANVAS_HEIGHT - self.size:
            self.y_position += PlayerFish.MOVEMENT_SPEED
            self.canvas.move(self.fish, 0, PlayerFish.MOVEMENT_SPEED)

    def move_left(self, event):
        """Move the fish left.

        :param event: move left
        :return: None
        """
        if self.x_position > 0:
            self.x_position -= PlayerFish.MOVEMENT_SPEED
            self.canvas.move(self.fish, -PlayerFish.MOVEMENT_SPEED, 0)

    def detect_collision(self):
        """Detect if the fish are overlapping each other.

        :return: None
        """
        p = self.canvas.coords(self.fish)
        collisions = list(self.canvas.find_overlapping(
            p[0], p[1], p[2], p[3]))
        collisions.remove(self.fish)
        return collisions

    def enlarge(self, amount):
        """Increase size of player as it overlap with smaller fish.

        :param amount: The amount of growth
        :return: None
        """
        self.size = self.size + amount/4
        self.canvas.delete(self.fish)

        self.fish = self.canvas.create_rectangle((
            self.x_position,
            self.y_position,
            self.x_position + self.size,
            self.y_position + self.size),
            fill="orange")


class EnemyFish:
    """Creates the enemy fish."""

    MOVEMENT_SPEED = 50
    MIN_SIZE = 10
    MAX_SIZE = 200

    def __init__(self, canvas, x_position, y_position, size, direction):
        """Create the enemy fish.

        :param canvas: Fish
        :param x_position: horizontal position
        :param y_position: vertical position
        :param size: size of fish
        :param direction: left or right
        """
        self.canvas = canvas
        self.size = size

        self._current_time = time.time()

        # -1 for left movement, 1 for right movement
        self._direction = direction

        self.fish = self.canvas.create_rectangle((
            x_position,
            y_position,
            x_position + self.size,
            y_position + self.size),
            fill="blue")

        self.move()

    def move(self):
        """Movement of the enemy fish.

        :return: None
        """
        # displacement = velocity * change in time
        self.canvas.move(self.fish, (time.time() - self._current_time) *
                         self._direction * EnemyFish.MOVEMENT_SPEED, 0)
        self._current_time = time.time()

        # check if the enemy has moved off the screen
        if self._direction == -1 and self.canvas.coords(
                self.fish)[0] < -self.size:
            self.reset()
        elif self._direction == 1 and self.canvas.coords(self.fish)[0] > \
                GUI.CANVAS_WIDTH + self.size:
            self.reset()

    def reset(self):
        """Reset game after win or loss.

        :return: None
        """
        random_num = random.randint(0, GUI.CANVAS_HEIGHT)
        spawn_left = random.randint(0, 1)
        self.size = min(random.randint(EnemyFish.MIN_SIZE,
                                       EnemyFish.MAX_SIZE),
                        random.randint(EnemyFish.MIN_SIZE,
                                       EnemyFish.MAX_SIZE),
                        random.randint(EnemyFish.MIN_SIZE,
                                       EnemyFish.MAX_SIZE))
        self.canvas.delete(self.fish)
        if spawn_left:
            self._direction = 1
            self.fish = self.canvas.create_rectangle((
                -self.size,
                random_num,
                -self.size + self.size,
                random_num + self.size),
                fill="blue")
        else:
            self._direction = -1
            self.fish = self.canvas.create_rectangle((
                GUI.CANVAS_WIDTH + self.size,
                random_num,
                GUI.CANVAS_WIDTH + self.size + self.size,
                random_num + self.size),
                fill="blue")


GUI()

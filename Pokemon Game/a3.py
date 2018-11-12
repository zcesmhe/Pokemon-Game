#!/usr/bin/env python3
################################################################################
#
#   CSSE1001/7030 - Assignment 3
#
#   Student Username: s4442951
#
#   Student Name: Mounir Hedna
#
################################################################################

# VERSION 1.0.1

################################################################################
#
# The following is support code. DO NOT CHANGE.

from a3_support import *
import tkinter as tk
from tkinter import messagebox
import random
import math

# End of support code
################################################################################
# Write your code below
################################################################################

# Write your classes here (including import statements, etc.)


class SimpleTileApp(object):
    def __init__(self, master):
        """
        Constructor(SimpleTileApp, tk.Frame)
        """
        self._master = master
        master.title("Simple Tile Game")

        self._game = SimpleGame()

        self._game.on('swap', self._handle_swap)
        self._game.on('score', self._handle_score)

        self._grid_view = TileGridView(
            master, self._game.get_grid(),
            width=GRID_WIDTH, height=GRID_HEIGHT, bg='black')
        self._grid_view.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        #Task 1 Start
        self._player = SimplePlayer()
        self._status_bar = SimpleStatusBar(master)
        self._status_bar.set_num_swaps(self._player.get_swaps())
        self._status_bar.set_score(self._player.get_score())
        self._status_bar.pack(side=tk.TOP, expand=True, fill=tk.X, padx=10,
                              pady=10)

        self._reset_status_btn = tk.Button(master, text="Reset Status",
                                           command = self.reset_status)

        self._reset_status_btn.pack(side=tk.BOTTOM, padx=10, pady=10)

        menubar = tk.Menu(master)
        master.config(menu=menubar)

        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Game", command=self.new_game)
        filemenu.add_command(label="Exit", command=self.exit_game)
        #Task 1 End

    def new_game(self):
        """Starts a new game by resetting tiles and statusbar.

        SimpleTileApp.new_game() -> None
        """
        if self._grid_view.is_resolving():
            messagebox.showerror("Grid is still resolving!")

        else:
            self._game.reset()
            self.reset_status()
            self._grid_view.draw()

    def exit_game(self):
        """Exits the game.

        SimpleTileApp.exit_game() -> None
        """
        self._master.destroy()


            
    def reset_status(self):
        """Resets the players status and updates the StatusBar

        SimpleTileApp.reset_status() -> None
        """
        self._player.reset_score()
        self._player.reset_swaps()
        self._status_bar.set_num_swaps(0)
        self._status_bar.set_score(0)
        

    def _handle_swap(self, from_pos, to_pos):
        """
        Run when a swap on the grid happens.
        """
        self._player.record_swap()
        self._status_bar.set_num_swaps(self._player.get_swaps())
        print("SimplePlayer made a swap from {} to {}!".format(
            from_pos, to_pos))

    def _handle_score(self, score):
        """
        Run when a score update happens.
        """
        self._player.add_score(score)
        self._status_bar.set_score(self._player.get_score())
        print("SimplePlayer scored {}!".format(score))

class SimplePlayer(object):

    def __init__(self):
        """Constructor: SimplePlayer()
        """
        self._score = 0
        self._swaps = 0

    def add_score(self, score):
        """Adds a score to the players score and returns the new score.

        SimplePlayer.add_score(int) -> int
        """
        self._score += score
        return self._score

    def get_score(self):
        """Returns a players score.

        SimplePlayer.get_score() -> int
        """
        return self._score

    def reset_score(self):
        """Resets a players score.

        SimplePlayer.reset_score() -> None
        """
        self._score = 0

    def record_swap(self):
        """Records a swap for the player and returns new swap count.

        SimplePlayer.record_swap() -> int
        """
        self._swaps += 1
        return self._swaps

    def get_swaps(self):
        """Returns the players swap count.

        SimplePlayer.get_swaps() -> int
        """

        return self._swaps

    def reset_swaps(self):
        """Resets the players swap count.

        SimplePlayer.reset_swaps() -> None
        """
        self._swaps = 0

class SimpleStatusBar(tk.Frame):

    def __init__(self, parent):
        """Constrcutor: SimpleStatusBar(tk.Widget)
        """
        super().__init__(parent)

        self._swaps_lbl = tk.Label(self, text="Number of Swaps: ")
        self._swaps_lbl.pack(side=tk.LEFT)

        self._score_lbl = tk.Label(self, text="Score: ")
        self._score_lbl.pack(side=tk.RIGHT)

    def set_num_swaps(self, num_swaps):
        """Sets the swaps label to show num_swaps.

        SimpleStatusBar.set_num_swaps(integer) -> None
        """
        self._swaps_lbl.config(text="Number of Swaps: {}".format(num_swaps))

    def set_score(self, score):
        """Sets the score label to show score.

        SimpleStatusBar.set_score(integer) -> None
        """
        self._score_lbl.config(text="Score: {}".format(score))

class Character(object):

    def __init__(self, max_health):
        """Constructs the character with a max health to start with.

        Constructor: Character(int)
        """
        self._max_health = max_health
        self._current_health = max_health

    def get_max_health(self):
        """Returns the maximum health of a character.

        Character.get_max_health() -> int
        """
        return self._max_health

    def get_health(self):
        """Return the characters current health.

        Character.get_health() -> int
        """
        return self._current_health

    def lose_health(self, amount):
        """Decreases a characters health by amount, cannot go below zero.

        Character.lose_health(int) -> None
        """
        if amount >= self._current_health:
            self._current_health = 0

        else:
            self._current_health -= amount
            

    def gain_health(self, amount):
        """Increases a characters health by amount, cannot go above max health.

        Character.gain_health(int) -> None
        """
        if (self._current_health + amount) > self._max_health:
            self._current_health = self._max_health

        else:
            self._current_health += amount

    def reset_health(self):
        """Resets that characters health to max health.

        Character.reset_health() -> None
        """
        self._current_health = self._max_health

class Enemy(Character):

    def __init__(self, type, max_health, attack):
        """Constructs an enemy with max health, type and attack range.

        Constructor: Enemy(String, int, (int,int))
        """
        super().__init__(max_health)
        self._type = type
        self._attack = attack


    def get_type(self):
        """Returns the enemy type.

        Enemy.get_type() -> String
        """
        return self._type

    def attack(self):
        """Returns a random integer in enemys attack range.

        Enemy.attack() -> int
        """
        return random.randint(self._attack[0], self._attack[1])

class Player(Character):

    def __init__(self, max_health, swaps_per_turn, base_attack):
        """Constructs a human player with max health, number of swaps the player
        makes and the players base attack

        Constructor: Player(int, int, int)
        """
        super().__init__(max_health)
        self._max_swaps = swaps_per_turn
        self._swaps_per_turn = swaps_per_turn
        self._base_attack = base_attack
        self._wins = 0

        #All types and their weaknesses
        self._weaknesses = {"fire" : "water",
                            "water" : "ice",
                            "ice" : "fire",
                            "poison" : None,
                            "psychic" : None,
                            "coin" : None,
                            None : None}

    def win(self):
        """Increases player wins by 1.

        Player.win() -> None
        """
        self._wins += 1

    def reset_wins(self):
        """Resets a players wins to zero.

        Player.reset_wins() -> None
        """
        self._wins = 0

    def get_wins(self):
        """Returns the players number of wins.

        Player.get_wins() -> int
        """
        return self._wins

    def record_swap(self):
        """Decreases a players swap count by 1 and returns new value.
        Cannot go below zero.

        Player.record_swap() -> int
        """
        if self._swaps_per_turn > 0:
            self._swaps_per_turn -= 1
            return self._swaps_per_turn
        else:
            return 0

    def get_swaps(self):
        """Returns the players swap count.

        Player.get_swaps() -> int
        """
        return self._swaps_per_turn

    def reset_swaps(self):
        """Resets the players swap count to the maximum swap count.

        Player.reset_swaps() -> None
        """
        self._swaps_per_turn = self._max_swaps

    def attack(self, runs, defender_type):
        """Takes a list of Run instances and a defender type. Returns a list of
        pairs of (type, damage). Then compares the damage type with enemy type,
        damage is then scaled depending if it is weak/strong against that type.
        Also gives bonus for more multiple runs of the same type.

        Player.attack(list<Run>, string) -> list<(string, int)>
        """
        damages = []
        #Number of occurences of a type in a run
        type_occurences = {"fire" : 0,
                           "poison" : 0,
                           "water" : 0,
                           "coin" : 0,
                           "psychic" : 0,
                           "ice" : 0}
        #Calculates damage
        for r in runs:
            tile = r.__getitem__(r.find_dominant_cell())
            type = tile.get_type()
            type_occurences[type] += 1
            tiles_in_run = len(r)
            longest_straight_in_run = r.get_max_dimension()
            damages += [(type, tiles_in_run*
                        longest_straight_in_run*self._base_attack)]

        damage_bonus = []
        BONUS = 1.2

        #Applies bonus for multiple instances of same type in a run
        for d in damages:
            damage_type = d[0]
            damage = d[1]
            if type_occurences[damage_type] != 0:
                damage = math.ceil(damage*BONUS**type_occurences[damage_type])
                damage_bonus += [(damage_type, damage)]

        result = []
        #Applies bonus based on weaknesses
        for d in damage_bonus:
            damage = d[1]
            damage_type = d[0]
            
            if damage_type == defender_type:
                damage = math.ceil(damage*0.8)

            elif damage_type == self.get_weakness(defender_type):
                damage = math.ceil(damage*BONUS)

            elif damage_type == "coin":
                damage *= 2

            else:
                damage = damage

            result += [(damage_type, damage)]

        return result
        

    def get_weakness(self, type):
        """Returns the weakness type of the enemy.

        Enemy.get_weakness(string) -> string
        """
        return self._weaknesses[type]

    def total_damage(self, damage):
        """Sums up the total damage calculated from damage bonus.


        Player.total_damage(list<(string,int)>, Enemy) -> int
        """
        total = 0
        for d in damage:
            damage = d[1]
            total += damage

        return total
            

class VersusStatusBar(tk.Frame):

    def __init__(self, master):
        """Constructor : VersusStatusBar(tk.Widget)"""
        super().__init__(master)

        #Setting up all labels for status bar

        self._level_lbl = tk.Label(self, text="Current Level: ")
        self._level_lbl.pack(side=tk.TOP)

        self._health_frame = tk.Frame(self)
        self._health_frame.pack(side=tk.BOTTOM, expand=True,
                                fill=tk.BOTH)

        self._player_health_lbl = tk.Label(self._health_frame,
                                           text="Player Health: ")
        self._player_health_lbl.pack(side=tk.LEFT)

        self._player_health_bar = tk.Canvas(self._health_frame,
                                            width=100, height=20)
        self._player_health_bar.create_rectangle(0,0,100,20,
                                                 fill="red", outline="")
        self._player_health_bar.pack(side=tk.LEFT)
        

        self._swaps_lbl = tk.Label(self._health_frame, text="Swaps: : ")
        self._swaps_lbl.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self._enemy_health_bar = tk.Canvas(self._health_frame,
                                           width=100, height=20)
        self._enemy_health_bar.pack(side=tk.RIGHT)

        self._enemy_health_lbl = tk.Label(self._health_frame,
                                          text="Enemy Health: ")
        self._player_health_bar.create_rectangle(0,0,100,20,
                                                 fill="red", outline="")
        self._enemy_health_lbl.pack(side=tk.RIGHT)


    def set_current_level(self, level):
        """Sets the level label equal to level.

        VersusStatusBar.set_current_level(int) -> None
        """
        self._level_lbl.config(text="Current Level: {}".format(level))

    def set_player_health(self, player):
        """Sets the player health label to health.

        VersusStatusBar.set_player_health(Player) -> None
        """
        self._player_health_lbl.config(text="Player Health: {}"
                                       .format(player.get_health()))
        new_health_bar = (player.get_health()/player.get_max_health())*100
        self._player_health_bar.delete("all")
        self._player_health_bar.create_rectangle(0,0,100,20,
                                                 fill="red", outline="")
        self._player_health_bar.create_rectangle(0,0,new_health_bar,20,
                                                 fill="green", outline="")

    def set_player2_health(self, player):
        """Sets the player 2 health label to health.

        VersusStatusBar.set_player_health(Player) -> None
        """
        self._enemy_health_lbl.config(text="Player 2 Health: {}"
                                      .format(player.get_health()))
        new_health_bar = (player.get_health()/player.get_max_health())*100
        self._enemy_health_bar.delete("all")
        self._enemy_health_bar.create_rectangle(0,0,100,20,
                                                fill="red", outline="")
        self._enemy_health_bar.create_rectangle(0,0,new_health_bar,20,
                                                fill="green", outline="")
        

    def set_enemy_health(self, enemy):
        """Sets the enemy health label to health.

        VersusStatusBar.set_enemy_health(Enemy) -> None
        """
        self._enemy_health_lbl.config(text="Enemy Health: {}"
                                      .format(enemy.get_health()))
        new_health_bar = (enemy.get_health()/enemy.get_max_health())*100
        self._enemy_health_bar.delete("all")
        self._enemy_health_bar.create_rectangle(0,0,100,20,
                                                fill="red", outline="")
        self._enemy_health_bar.create_rectangle(0,0,new_health_bar,20,
                                                fill="green", outline="")

    def set_num_swaps(self, swaps):
        """Sets the swaps label equal to swaps.

        VersusStatusBar.set_swaps(int) -> None
        """
        self._swaps_lbl.config(text="Swaps: {}".format(swaps))

class ImageTileGridView(TileGridView):

    def __init__(self, master, grid, *args, width=GRID_WIDTH,
                 height=GRID_HEIGHT,
                 cell_width=GRID_CELL_WIDTH, cell_height=GRID_CELL_HEIGHT,
                 **kwargs):
        """
        Constructor(tk.Frame, TileGrid, *, int, int, int, int, *)

        :param master: The tkinter master widget/window.
        :param width: Total width of the grid.
        :param height: Total height of the grid.
        :param cell_width: Width of each cell.
        :param cell_height: Height of each cell.
        """

        #Storing image files in a dictionary

        self._images = {"red" : tk.PhotoImage(file="fire.gif"),
                        "green" : tk.PhotoImage(file="poison.gif"),
                        "blue" : tk.PhotoImage(file="water.gif"),
                        "gold" : tk.PhotoImage(file="coin.gif"),
                        "purple" : tk.PhotoImage(file="psychic.gif"),
                        "light sky blue" : tk.PhotoImage(file="ice.gif")}
                        
        
        super().__init__(master, grid, *args, width=GRID_WIDTH,
                 height=GRID_HEIGHT,
                 cell_width=GRID_CELL_WIDTH, cell_height=GRID_CELL_HEIGHT,
                 **kwargs)
        

    def draw_tile_sprite(self, xy_pos, tile, selected):
        """Draws the sprite for the given tile at given (x, y) position.

        TileGridView.undraw_tile_sprite(TileGridView, (int, int), Tile, bool)
                                                                    -> None"""
        colour = tile.get_colour()

        img = self._images[colour]

        width, height = self._calculate_tile_size(xy_pos, selected)

        x, y = xy_pos
        return self.create_image(x, y, image=img)

class SinglePlayerTileApp(SimpleTileApp):

    def __init__(self, master):
        """Constructor: SinglePlayerTileApp(tk.Frame)"""
        self._master = master
        master.title("Single Player Tile App")

        self._status_bar = VersusStatusBar(master)
        self._status_bar.pack(side=tk.TOP, expand=True, fill=tk.X, padx=10,
                                pady=10)

        self._current_level = 1
        master.title("Tile Game - Level {}".format(self._current_level))

        self._player = Player(PLAYER_BASE_HEALTH, SWAPS_PER_TURN,
                              PLAYER_BASE_ATTACK)

        self._enemy = self.generate_enemy()        

        self._status_bar.set_num_swaps(self._player.get_swaps())
        self._status_bar.set_player_health(self._player)
        self._status_bar.set_current_level(self._current_level)
        self._status_bar.set_enemy_health(self._enemy)

        self._game = SimpleGame()

        self._game.on('swap_resolution', self._handle_swap_resolution)
        
        self._game.on('runs', self._handle_runs)

        self._game.on('swap', self._handle_swap)

        self._start_of_level = True

        self._player_frame = tk.Frame(master)
        self._player_canvas = tk.Canvas(self._player_frame,width=100,height=100)
        self._player_image = tk.PhotoImage(file="player.gif")
        self._player_canvas.create_image((50,50), image=self._player_image)
        self._player_canvas.pack(side=tk.TOP)
        self._player_lbl = tk.Label(self._player_frame, text="Player")
        self._player_lbl.pack()
        self._player_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        #Enemy images based on their type

        self._enemy_images = {"fire" : tk.PhotoImage(file="fire_enemy.gif"),
                              "poison" : tk.PhotoImage(file="poison_enemy.gif"),
                              "water" : tk.PhotoImage(file="water_enemy.gif"),
                              "psychic":tk.PhotoImage(file="psychic_enemy.gif"),
                              "ice" : tk.PhotoImage(file="ice_enemy.gif")}
        
        self._enemy_frame = tk.Frame(master)
        self._enemy_canvas = tk.Canvas(self._enemy_frame, width=100,height=100)
        self._enemy_image = self._enemy_images[self._enemy.get_type()]
        self._enemy_canvas.create_image((50,50), image=self._enemy_image)
        self._enemy_canvas.pack(side=tk.TOP)
        self._enemy_lbl = tk.Label(self._enemy_frame, text="Enemy Type: {}"
                                   .format(self._enemy.get_type().title()))
        self._enemy_lbl.pack()

        self._enemy_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self._grid_view = ImageTileGridView(
            master, self._game.get_grid(),
            width=GRID_WIDTH, height=GRID_HEIGHT, bg="black")
        self._grid_view.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        
        self.menubar = tk.Menu(master)
        master.config(menu=self.menubar)

        filemenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Game", command=self.new_game)
        filemenu.add_command(label="Exit", command=self.exit_game)

        
    
    def create_animation_stepper(self, master, steps, delay, callback=None):
        def stepper():
            try:
                next(steps)
                if delay is not None:
                    self._master.after(delay, stepper)
            except StopIteration:
                if callback:
                    callback()
        return stepper

    def animate_health(self, master, character, amount):
        def done():
            pass

        def run_animation():
            def _anim():
                
                for i in range(0, amount):  
                    self._status_bar.set_enemy_health(self._enemy)
                    self._status_bar.set_player_health(self._player)
                    yield

                character.lose_health(amount)
                
            stepper=self.create_animation_stepper(self._master,_anim(),10,done)
            stepper()

        run_animation()
    
        
    def exit_game(self):
        """Exits the game.

        SinglePlayerTileApp.exit_game() -> None
        """
        yes = messagebox.askyesno("Exit Game",
                                  "Are you sure you want to exit the game?")

        if yes:
            self._master.destroy()

    def set_enemy_image(self, type):
        """Sets an enemys image depending on their type

        SinglePlayerTileApp.set_enemy_image(string) -> None
        """
        self._enemy_canvas.delete("all")
        self._enemy_image = self._enemy_images[type]
        self._enemy_canvas.create_image((50,50), image=self._enemy_image)
        self._enemy_lbl.config(text="Enemy Type: {}"
                               .format(self._enemy.get_type().title()))

    def new_game(self):
        """Resets the game, returns player and enemy to full health and level
        to 1.

        SinglePlayerTileApp.new_game() -> None
        """
        yes = messagebox.askyesno("New Game",
                                  "Would you like to start a new game?")
        if yes:
            self.reset_game()

    def reset_game(self):
        """Resets the game back to level one and reinitialises all characters.

        SinglePlayerTileApp.reset_game() -> None
        """
        self._start_of_level = True
        self._player.reset_health()
        self._player.reset_swaps()
        self._game.reset()
        self._grid_view.draw()
        self.reset_level()
        self._master.title("Tile Game - Level {}"
                               .format(self._current_level))
        self._enemy = self.generate_enemy()
        self._status_bar.set_num_swaps(self._player.get_swaps())
        self._status_bar.set_player_health(self._player)
        self._status_bar.set_current_level(self._current_level)
        self._status_bar.set_enemy_health(self._enemy)
        self.set_enemy_image(self._enemy.get_type())        

    def next_level(self):
        """Starts the next level of the game.

        SinglePlayerTileApp.next_level() -> None
        """

        self._current_level += 1
        self._master.title("Tile Game - Level {}".format(self._current_level))
        self._game.reset()
        self._grid_view.draw()
        self._start_of_level = True
        self._enemy = self.generate_enemy()
        self._player.reset_health()
        self._player.reset_swaps()
        self._status_bar.set_num_swaps(self._player.get_swaps())
        self._status_bar.set_player_health(self._player)
        self.set_enemy_image(self._enemy.get_type())
        self._status_bar.set_current_level(self._current_level)
        self._status_bar.set_enemy_health(self._enemy)

        
    def reset_level(self):
        """Sets the level back to 1.

        SinglePlayerTileApp.reset_level() -> None
        """
        self._current_level = 1
        self._start_of_level = True
        self._master.title("Tile Game - Level {}".format(self._current_level))

    def _handle_swap(self, from_pos, to_pos):
        """
        Run when a swap on the grid happens.
        """
                     
        if self._start_of_level:
            self._start_of_level = False
                
        self._player.record_swap()
        self._status_bar.set_num_swaps(self._player.get_swaps())
        print("Player made a swap from {} to {}!".format(
        from_pos, to_pos))

            
    def _handle_swap_resolution(self, from_pos, to_pos):
        """
        Handles the resolution of a swap (after all runs have been resolved).

        Emits swap_resolution.

        SimpleGame._handle_swap_resolution(SimpleGame, (int, int), (int, int))
                                                                        -> None
        """
        if self._start_of_level:
            pass
        else:
            damage_taken = self._enemy.attack()
            print("Player took {} damage!".format(damage_taken))
            self._player.lose_health(damage_taken)
            #self.animate_health(self._master, self._player, damage_taken)
            self._status_bar.set_player_health(self._player) #Hide this 
            if self._player.get_health() == 0:
                yes=messagebox.askyesno("Game Over! You have died!"
                                        ,"Would you like to start a new game?")
                if yes:
                    self.reset_game()

                else:
                    self._master.destroy()

        if self._player.get_swaps() == 0:
            yes = messagebox.askyesno("Game Over! You have run out of swaps!"
                                      , "Would you like to start a new game?")

            if yes:
                self.reset_game()
            else:
                self._master.destroy()

    def _handle_runs(self, runs):
        attack = self._player.attack(runs, self._enemy.get_type())
        damage = self._player.total_damage(attack)
        self._enemy.lose_health(damage) #Hide this
        self._status_bar.set_enemy_health(self._enemy) #Hide this
        #self.animate_health(self._master, self._enemy, damage)
        print("Player did {} damage!".format(damage))
        if self._enemy.get_health() == 0:
            messagebox.showinfo(title="Level Complete!",
                                message=
                                "Congratulations you have completed level {}!"
                                .format(self._current_level))
            self.next_level()        
        

    def generate_enemy(self):
        """Randomly generates an enemy.

        SinglePlayerTileApp.generate_enemy_type() -> Enemy
        """
        random_num = random.randint(0,4)
        type = None

        #Each type has an equal probability of occuring

        if random_num < 1:
            type = "fire"
        elif random_num < 2:
            type = "water"
        elif random_num < 3:
            type = "poison"
        elif random_num < 4:
            type = "psychic"
        else:
            type = "ice"

        stats = generate_enemy_stats(self._current_level)

        enemy = Enemy(type, stats[0], stats[1])
        
        return enemy

class MultiPlayerTileApp(SinglePlayerTileApp):

    def __init__(self, master):
        """Constructor: MultiPlayerTileApp(tk.Widget)"""
        super().__init__(master)
        self._master = master
        master.title("MultiPlayer Tile App")
        
        self._num_turns_lbl = self._status_bar._swaps_lbl
        self._num_turns = 0
        self._num_turns_lbl.config(text="Number of Turns: {}"
                                   .format(self._num_turns))
        
        self._turn_lbl = self._status_bar._level_lbl
        self._player2 = Player(PLAYER_BASE_HEALTH, SWAPS_PER_TURN,
                              PLAYER_BASE_ATTACK)
        #Changes enemy health bar to another player health bar
        self._player2_health_bar = self._status_bar._enemy_health_lbl
        self._player2_health_bar.config(text="Player 2 Health: {}"
                                            .format(self._player2.get_health()))
        
        self._player1_health_bar = self._status_bar._player_health_lbl
        self._player1_health_bar.config(text="Player 1 Health: {}"
                                            .format(self._player.get_health()))
        self._player1_turn = True
        self._player_turn = None
        if self._player1_turn:
            self._player_turn = 1
        else:
            self._player_turn = 2

        self._turn_lbl.config(text="Player {} Turn"
                              .format(self._player_turn))
                
        self._player_lbl.config(text="Player 1 Score: {}"
                                .format(self._player.get_wins()))
        self._enemy_canvas.delete("all")
        self._player2_image = tk.PhotoImage(file="player2.gif")
        self._player2_canvas = self._enemy_canvas
        self._player2_canvas.create_image((50,50), image=self._player2_image)
        self._player2_lbl = self._enemy_lbl
        self._player2_lbl.config(text="Player 2 Score: {}"
                                 .format(self._player2.get_wins()))

        game_mode_menu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="Game Modes", menu=game_mode_menu)
        game_mode_menu.add_command(label="Single Player",
                                   command=self.single_player_game)
    
    def animate_health(self, master, character, amount):
        def done():
            pass

        def run_animation():
            def _anim():
                
                for i in range(0, amount):
                    character.lose_health(1)
                    self._status_bar.set_player2_health(self._player2)
                    self._status_bar.set_player_health(self._player)
                    yield
                
            stepper=self.create_animation_stepper(self._master,_anim(),10,done)
            stepper()

        run_animation()
        

    def new_game(self):
        """Resets the game, returns player and enemy to full health and level
        to 1.

        MultiPlayerTileApp.new_game() -> None
        """
        yes = messagebox.askyesno("New Game",
                                  "Would you like to start a new game?")
        if yes:
            self._start_of_level = True
            self._game.reset()
            self._grid_view.draw()
            self._player.reset_health()
            self._player2.reset_health()
            self._player.reset_wins()
            self._player2.reset_wins()
            self._player1_health_bar.config(text="Player 1 Health: {}"
                                            .format(self._player.get_health()))
            self._player2_health_bar.config(text="Player 2 Health: {}"
                                            .format(self._player2.get_health()))
            self._player_lbl.config(text="Player 1 Score: {}"
                                    .format(self._player.get_wins()))

    def single_player_game(self):
        """Closes multiplayer game and recreates a single player game in
           new window.

        MultiplayerTileApp.single_player_game() -> None
        """
        self._master.destroy()
        root = tk.Tk()
        app = TileApp(root)
        root.mainloop()
        

    def get_current_player(self):
        """Returns the player who is currently taking their turn.

        MultiPlayerTileApp.get_current_player() -> Player
        """
        if self._player1_turn:
            return self._player
        else:
            return self._player2

    def player_is_dead(self):
        """Returns True if a player has died.

        MultiPlayerTileApp.player_is_dead() -> Boolean
        """
        if self._player.get_health() == 0:
            return True
        elif self._player2.get_health() == 0:
            return True
        else:
            return False

    def next_player(self):
        """Changes the players turn to the next player.

        MultiPlayerTileApp.next_player() -> None
        """
        if self._player1_turn:
            self._player_turn = 2

        else:
            self._player_turn = 1

    def _handle_swap(self, from_pos, to_pos):
        """
        Run when a swap on the grid happens.
        """
        if self._start_of_level:
            self._start_of_level = False
        print("Player {} made a swap from {} to {}!"
              .format(self._player_turn,
            from_pos, to_pos))

        self._num_turns += 1
        self._num_turns_lbl.config(text="Number of Turns: {}"
                                   .format(self._num_turns))

    def _handle_swap_resolution(self, from_pos, to_pos):
        """
        Handles the resolution of a swap (after all runs have been resolved).

        Emits swap_resolution.

        SimpleGame._handle_swap_resolution(SimpleGame, (int, int), (int, int))
                                                                        -> None
        """
        if self._start_of_level:
            pass
        
        elif self.player_is_dead():
            if self._player1_turn:
                self._player.win()
            else:
                self._player2.win()
                
            self._player_lbl.config(text="Player 1 Score: {}"
                                    .format(self._player.get_wins()))
            self._player2_lbl.config(text="Player 2 Score: {}"
                                     .format(self._player2.get_wins()))
            
            yes = messagebox.askyesno("Player {} Wins!"
                                      .format(self._player_turn)
                                      , "Would you like to play another game?")
            
            if yes:
                self._game.reset()
                self._grid_view.draw()
                self._player.reset_health()
                self._player2.reset_health()
                self._player1_turn = True
                self._player_turn= 1
                self._start_of_level = True
                self._status_bar.set_player_health(self._player)
                self._status_bar.set_player2_health(self._player2)
                self._turn_lbl.config(text="Player {} Turn"
                                      .format(self._player_turn))
                self._num_turns = 0
                self._num_turns_lbl.config(text="Number of Turns: {}"
                                           .format(self._num_turns))
            else:
                self._master.destroy()

        else:
            
            if self._player1_turn:
                self.next_player()
                self._turn_lbl.config(text="Player {} Turn"
                                      .format(self._player_turn))
                self._player1_turn = False 
            else:
                self.next_player()
                self._turn_lbl.config(text="Player {} Turn"
                                      .format(self._player_turn))
                self._player1_turn = True


    def _handle_runs(self, runs):
        if self._player1_turn:
            
            attack = self._player.attack(runs, None)
            damage = self._player.total_damage(attack)
            #self.animate_health(self._master, self._player2, damage)
            self._player2.lose_health(damage)
            self._status_bar.set_player2_health(self._player2)
            print("Player {} did {} damage!".format(self._player_turn, damage))

        else:
            attack = self._player2.attack(runs, None)
            damage = self._player2.total_damage(attack)
            #self.animate_health(self._master, self._player, damage)
            self._player.lose_health(damage)
            self._status_bar.set_player_health(self._player)
            print("Player {} did {} damage!".format(self._player_turn, damage))
            

class TileApp(SinglePlayerTileApp):

    def __init__(self, master):
        super().__init__(master)

        self._master = master
        
        game_mode_menu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="Game Modes", menu=game_mode_menu)
        game_mode_menu.add_command(label="Multiplayer",
                                   command=self.multiplayer_game)

    def multiplayer_game(self):
        """Creates a multiplayer game

        TileApp.multiplayer_game() -> None
        """
        yes=messagebox.askyesno("Switch to Multiplayer"
                                ,"Are you sure you want to change game modes?")
        
        if yes:
            self._master.destroy()
            root = tk.Tk()
            app = MultiPlayerTileApp(root)
            root.mainloop()
         
        

def task1():
    root = tk.Tk()
    app = SimpleTileApp(root)
    root.mainloop()

def task2():
    root = tk.Tk()
    app = SinglePlayerTileApp(root)
    root.mainloop()


def task3():
    root = tk.Tk()
    app = TileApp(root)
    root.mainloop()


def main():
    # Choose relevant task to run
    task3()


if __name__ == '__main__':
    main()

from game_character import GameCharacter
from eyes import Eyes


# The Pinky class extends GameCharacter, so methods defined in GameCharacter
# are inherited by objects of class Pinky.
class Pinky(GameCharacter):
    def __init__(self, maze, pacman, game_controller):
        self.CHAR_WIDTH = 100
        self.CHAR_HEIGHT = 100
        self.maze = maze
        self.pacman = pacman
        self.gc = game_controller
        self.x = maze.WIDTH/2
        self.y = maze.TOP_HORIZ
        self.velocity = 1
        self.x_add = self.velocity
        self.y_add = 0
        self.eyes = Eyes()
        self.looking = (0, 0)
        self.WIN_PROXIMITY = 80
        self.WALL_TOLERANCE = 2

    def draw_self(self, x, y):
        """Draw Pinky to the screen"""
        noStroke()
        fill(1.0, 0.5, 0.6)
        ellipse(x, y, 100, 100)
        bottom_half = createShape()
        bottom_half.beginShape()
        bottom_half.vertex(x, y)
        bottom_half.vertex(x+100, y)
        bottom_half.vertex(x+100, y+50)
        bottom_half.vertex(x+50, y+25)
        bottom_half.vertex(x, y+50)
        bottom_half.endShape()
        shape(bottom_half, -50, 0)

        self.eyes.display(x, y - 15, self.looking)

    def update(self):
        """Carry out necessary updates for each frame before
        drawing to screen"""
        # Check if Pinky is at an intersection
        on_vert = (
            (abs(self.x - self.maze.LEFT_VERT) < self.WALL_TOLERANCE) or
            (abs(self.x - self.maze.RIGHT_VERT) < self.WALL_TOLERANCE)
                   )
        on_horz = (
            (abs(self.y - self.maze.TOP_HORIZ) < self.WALL_TOLERANCE) or
            (abs(self.y - self.maze.BOTTOM_HORIZ) < self.WALL_TOLERANCE)
                   )

        # Check whether Pinky is up or down/left or right of Pacman
        up_down_part = self.pacman.y - self.y
        left_right_part = self.pacman.x - self.x

        # Update Pinky's eyes to look at Pacman
        self.update_eyes(up_down_part, left_right_part)

        # If Pinky gets close to Pacman, tell the GameController
        # that Pinky wins
        if (abs(up_down_part) < self.WIN_PROXIMITY and
                abs(left_right_part) < self.WIN_PROXIMITY):
            self.gc.pinky_wins = True
        
        # TODO:
        # PROBLEM 2: Make Pinky chase Pacman!
        # Study the code above and below these lines to understand how
        # Pinky's movements are calculated, and how Pinky's position with
        # respect to Pacman is represented.
        # Pinky should decide at each intersection whether to go left, right
        # up or down depending on which direction Pacman is further away in.
        # START CODE CHANGES

        # make Pinky chase Pacman while avoiding walls

        
        if on_vert or on_horz:
            # figure out where Pacman is
            up_down_part = self.pacman.y - self.y
            left_right_part = self.pacman.x - self.x

            # define bounds
            left = self.maze.LEFT_VERT
            right = self.maze.RIGHT_VERT
            top = self.maze.TOP_HORIZ
            bottom = self.maze.BOTTOM_HORIZ

         # try moving in the direction of Pacman if its within bounds
        if on_horz and abs(left_right_part) > abs(up_down_part):
            if left_right_part > 0 and self.x + self.velocity <= right:
                self.x_add = self.velocity
                self.y_add = 0
            elif left_right_part < 0 and self.x - self.velocity >= left:
                self.x_add = -self.velocity
                self.y_add = 0

        # move up/down only if on a valid vertical path
        elif on_vert:
            if up_down_part > 0 and self.y + self.velocity <= bottom:
                self.x_add = 0
                self.y_add = self.velocity
            elif up_down_part < 0 and self.y - self.velocity >= top:
                self.x_add = 0
                self.y_add = -self.velocity

            else:
                # try moving up or down
                if up_down_part > 0 and self.y + self.velocity <= bottom:
                    self.x_add = 0
                    self.y_add = self.velocity
                elif up_down_part < 0 and self.y - self.velocity >= top:
                    self.x_add = 0
                    self.y_add = -self.velocity

        self.x += self.x_add
        self.y += self.y_add



    def update_eyes(self, up_down_part, left_right_part):
        """Set self.looking value based on position of Pinky w/r/t Pacman"""
        if up_down_part and abs(up_down_part) > 5:
            y = up_down_part/abs(up_down_part)
        else:
            y = 0
        if left_right_part and abs(left_right_part) > 5:
            x = left_right_part/abs(left_right_part)
        else:
            x = 0
        self.looking = (x, y)
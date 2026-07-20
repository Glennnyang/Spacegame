from graphics import *
import random
import time


def main():
    # Create the window
    win = GraphWin("my window", 900, 800)
    background_image = Image(Point(400, 400), "meesaa.png")  # Centered at the middle of the window
    background_image.draw(win)
    
    # Create and draw the plane object
    hero = Plane(450, "black")
    hero.draw(win)

    # Display the score at the top right
    score = 0
    missed_obstacles= 0
    score_display = Text(Point(750, 30), "Score: {}".format(score))
    score_display.setSize(16)
    score_display.setTextColor("orange")
    score_display.draw(win)

    #Display missed balls at top left
    missed_display = Text(Point(50, 30), "Missed: {}".format(missed_obstacles))
    missed_display.setSize(16)
    missed_display.setTextColor("red")
    missed_display.draw(win)

    # Lists to hold projectiles and obstacles
    projectiles = []
    obstacles = []

    last_obstacle_time = time.time()  # Store the last time we added an obstacle


    while not win.isClosed():
        current_time = time.time()

        # Check if 3 second has passed since last obstacle drop
        if current_time - last_obstacle_time >= 3:
            # Drop a new obstacle at a random x position
            new_obstacle = Obstacle(random.randint(0, 780), 0, "pink")
            obstacles.append(new_obstacle)
            new_obstacle.draw(win)
            last_obstacle_time = current_time  # Update the last obstacle time

        # Move the obstacles down
        for obs in obstacles[:]:
            obs.down_movement()
            # Check if the obstacle crosses the plane's height
            if obs.crosses_plane():
                obs.remove(win)
                obstacles.remove(obs)
                missed_obstacles += 1
                missed_display.setText("Missed: {}".format(missed_obstacles))
                # End the game if 3 obstacles are missed
                if missed_obstacles >= 3:
                    display_final_score(win, score)
                    win.close() 
                    return


        # # Move the obstacles down
        # for obs in obstacles:
        #     obs.down_movement()

        # Check for projectile movement
        for proj in projectiles:
            proj.up_movement()

        # Check for collisions between projectiles and obstacles
        for proj in projectiles[:]:
            for obs in obstacles[:]:
                if proj.collides_with(obs):
                    proj.remove(win)
                    obs.remove(win)
                    projectiles.remove(proj)
                    obstacles.remove(obs)


                    score+=1
                    score_display.setText("Score: {}".format(score))
                    break  # Break to avoid modifying lists while iterating

        # Check for collisions between the plane and obstacles
        for obs in obstacles:
            if hero.collides_with(obs):
                # Display the final score and exit the game
                display_final_score(win, score)
                win.close()
                return
            
        # Checks for highest score    
        if score == 25:
            display_final_score(win,score)
            win.close()
            return

        # Check for key presses to move the plane
        key = win.checkKey()
        if key == 'Left':
            hero.move_left()
        elif key == 'Right':
            hero.move_right()

        # Check if the user clicked the left mouse button to fire a projectile
        click_point = win.checkMouse()  # Get the point where the mouse was clicked
        if click_point:
            hero.fire_projectile(projectiles, win)
    
        time.sleep(0.05)
       

def display_final_score(win, score):
    #Display the final score at the center of the screen.
    final_score_text = Text(Point(400, 400),"Final Score: {}".format(score))
    if score == 25:
        final_score_text = Text(Point(400,400),"    Congrats, Highest Score Achieved")
    final_score_text.setSize(36)
    final_score_text.setStyle("bold")
    final_score_text.setTextColor("red")
    final_score_text.draw(win)
    time.sleep(3)  # Wait for 3 seconds before closing the window


class Obstacle:
    '''Class containing the obstacles which have to be shot by the projectiles'''
    def __init__(self, posX, posY, color):
        self.posX = posX
        self.posY = posY
        self.velocity = 3  # Set initial velocity for obstacle fall
        self.circle = Circle(Point(posX, posY), 10)
        self.circle.setFill(color)

    def draw(self, win):
        self.circle.draw(win)

    def down_movement(self):
        # Move the obstacle downwards
        self.circle.move(0, self.velocity)
    
    def crosses_plane(self):
        # Check if the obstacle has crossed the plane's height
        return self.circle.getCenter().getY() > 790

    def remove(self, win):
        self.circle.undraw()  # Remove the obstacle from the window

class Plane:
    '''This class contains the plane object which will be used to fire projectiles at obstacles'''
    def __init__(self, posX, color):
        self.posX = posX
        self.posY = 700  # Y-coordinate for the plane
        self.plane = Image(Point(posX + 10, self.posY + 10), "plane.png")  # Load GIF image of the plane

    def move_left(self):
        if self.posX > 20:  # Prevent moving out of bounds
            self.posX -= 12
            self.plane.move(-12, 0)

    def move_right(self):
        if self.posX < 760:  # Prevent moving out of bounds
            self.posX += 12
            self.plane.move(12, 0)

    def fire_projectile(self, projectiles, win):
        '''Fires a projectile from the plane'''
        new_projectile = Projectile(self.posX+5, self.posY, "white")  # Centered based on new plane image
        projectiles.append(new_projectile)
        new_projectile.draw(win)

    def collides_with(self, obstacle):
        '''Check if the plane collides with an obstacle'''
        plane_x1 = self.posX - 10
        plane_x2 = self.posX + 10
        plane_y1 = self.posY - 10
        plane_y2 = self.posY + 10

        obs_center = obstacle.circle.getCenter()
        obs_x, obs_y = obs_center.getX(), obs_center.getY()
        obs_radius = 10

        # Check if the obstacle's circle overlaps with the plane's bounding box
        if (plane_x1 - obs_radius <= obs_x <= plane_x2 + obs_radius and
                plane_y1 - obs_radius <= obs_y <= plane_y2 + obs_radius):
            return True
        return False

    def draw(self, win):
        self.plane.draw(win)

class Projectile:
    '''Class for projectiles fired by the plane'''
    def __init__(self, posX, posY, color):
        self.posX = posX
        self.posY = posY
        self.bullet = Oval(Point(posX - 10, posY - 20), Point(posX, posY))
        self.bullet.setFill(color)

    def draw(self, win):
        self.bullet.draw(win)

    def up_movement(self):
        move = -10
        self.bullet.move(0, move)

    def collides_with(self, obstacle):
        '''Check if the projectile collides with an obstacle'''
        # Get the bounding box of the projectile and the obstacle
        proj_x1, proj_y1 = self.bullet.getP1().getX(), self.bullet.getP1().getY()
        proj_x2, proj_y2 = self.bullet.getP2().getX(), self.bullet.getP2().getY()

        obs_x1, obs_y1 = obstacle.circle.getCenter().getX() - 10, obstacle.circle.getCenter().getY() - 10
        obs_x2, obs_y2 = obstacle.circle.getCenter().getX() + 10, obstacle.circle.getCenter().getY() + 10

        # Check if the bounding boxes overlap
        if proj_x1 < obs_x2 and proj_x2 > obs_x1 and proj_y1 < obs_y2 and proj_y2 > obs_y1:
            return True
        return False

    def remove(self, win):
        '''Remove the projectile from the window'''
        self.bullet.undraw()

main()

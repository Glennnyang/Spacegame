Game project 
#about space_game
space_game is a simple 2D game consisting of an aeroplane located at the base of the screen which shoots down upstacles. The main aim of the game is to shoot 25 incoming obstacles from above

#game rules
space_game's user is in control of the aeroplane object which can move left or right along the horizontal axis of the screen.
The user can then fire projectiles which are randomly incoming from above.
To move the plane left or right, the user has to use the left arrow key and the right arrow key respectively on the keyboard.
To fire a projectile, the user has to click the left click on the computer mouse.

#success and failure conditions
Failure occurs in two conditions
The first condition is when an obstacle touches the core of the plane object(if it touches the wings, the plane will be unafected).
The second condition is when a total of three obstacles bypass the plane and are not shot down.
In both cases above, after failure, a message is displayed on the screen's center showing the user's total score. The game then shuts down automatically after 3 seconds.

Success occurs when the user succeeds to shoot down a total of 25 objects, after which a congratulations message displays on the screen, and the game shuts down 3 seconds later.

#game requirements
Python 3.x
graphics.py module (John Zelle's graphics library)
Download from: graphics.py module
Assets:
meesaa.png – Background image (900x800 recommended).
plane.png – Plane image (in GIF or png format).

#How to Run
Ensure you have Python and the graphics.py module installed.
Place the following files in the same directory:
The game script (PlaneShooter.py).
meesaa.png (background image).
plane.png (plane image).

Run the code:
python space_game.py


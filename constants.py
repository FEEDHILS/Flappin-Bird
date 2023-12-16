import pygame
### CONSTANTS ###

# MAIN.
W = 640 # Width of Screen
H = 720 # Height

# PLAYER CONSTANTS.
PLAYERDAMPING = .1 # Damping just slows velocity change.
PLAYERJUMPHEIGHT = 100 
GRAVITY = 5
PLAYERMAXVELOCITY = [300, 300]
BOTTOMCOLLISION = H
MAXDASHLENGTH = 200

# PIPE CONSTANTS.
GAP = [125, 225] # Min and max amount of space between pipes.
MAXOFFSET = [185, H-185] # Beyound that, the player would be able to see sprite blank space
 

### CUSTOM EVENTS ###

# PLAYER EVENTS.
DASHRELOAD = pygame.USEREVENT+1
PLAYERENABLEGRAVITY = pygame.USEREVENT+2
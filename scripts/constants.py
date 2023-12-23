import pygame
### CONSTANTS ###

# MAIN.
W = 640 # Width of Screen
H = 720 # Height
FONT = "fonts/dpcomic.ttf"
BUTTONCOLOR = pygame.color.Color( (29,26,49) )


# PLAYER CONSTANTS.
PLAYERDAMPING = .1 # Damping just slows velocity change.
PLAYERJUMPHEIGHT = 100 
GRAVITY = 7
PLAYERMAXVELOCITY = [300, 300]
BOTTOMCOLLISION = H-10
MAXDASHLENGTH = 200
MINDASHLENGTH = 125
# PIPE CONSTANTS.
GAP = [125, 225] # Min and max amount of space between pipes.
MAXOFFSET = [100, H-150] # Beyound that, the player would be able to see sprite blank space
 

### CUSTOM EVENTS ###
TIMER = pygame.USEREVENT+15

# PLAYER EVENTS.
DASHRELOAD = pygame.USEREVENT+1
PLAYERENABLEGRAVITY = pygame.USEREVENT+2
PLAYERDEAD = pygame.USEREVENT+8
SCOREUP = pygame.USEREVENT+9

# PIPE EVENTS.
SPAWNPIPE = pygame.USEREVENT+3

# LEVEL EVENTS.
LOADLEVEL = pygame.USEREVENT+4
RELOADLEVEL = pygame.USEREVENT+5
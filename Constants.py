#SCREEN VARIABLES
SCREEN_W = 800
SCREEN_H = 600

#DIRECTIONS
DIR_INVALID = -1
DIR_UP = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_RIGHT = 3
DIR_NONE = 4

#OBJECT TYPES
BASE_OBJECT = 0
LEVEL_OBJECT = 1
PLAYER = 2
GROUP_OBJECT = 3
CRANE_OBJECT = 4

#BEHAVIORS
NOTHING = 0
PICKUP = 1
PLACE = 2
TURN_ON = 3

#STATES FOR GROUP OBJECTS
OFF = 0
ON = 1

#MOVE TO POINTS
CENTER = 0
TOP_LEFT = 1
MID_TOP = 2
TOP_RIGHT = 3
MID_RIGHT = 4
BOT_RIGHT = 5
MID_BOT = 6
BOT_LEFT = 7
MID_LEFT = 8

#JUMP STATES
NOT_JUMPING = 0
JUMP_DELAY = 1
JUMP = 2

#GUI OBJECT TYPES
GUI_OBJ = 0
TXT_BOX = 1
LIST_BOX = 2

#Names for indicies inside tuple stored in dest list
X = 0
Y = 1
WAIT = 2
ACTION = 3

#Input Types
KEY = 0
MOUSE = 1
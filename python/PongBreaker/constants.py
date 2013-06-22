X = 0
Y = 1

XLEN = 0
YLEN = 1

MIN = 0
MAX = 1

START = 0
END = 1

PLAYER = 0
VALUE = 1

LOWER = 0
UPPER = 1

RIGHT = 0
LEFT = 1

NAME = 0
DIRECTION = 1

GOAL = 2

TYPE = 0
DETAILS = 1

BRICK = 1
OUT = 2

MENU = 0
GAME = 1
EDITOR = 2

STOP = 5
CONTINUE = 6
BACK = 7
GAMEOVER = 8

SETTINGS = 3
RULES = 4

DIMENSIONS = 0
PLAYERS = 0
MODE = 1
SCREENSIZE = 2
WINDOW = 3


FPS = 40
FRICTION = 0.7
SCORE_BUFFER = 20
MENU_DIMENSIONS = (640,480)
MENU_POSITION = (0,224) #(320, 352)
RACKET_THICKNESS = 5
BALL_SPAWN_OFFSET = 25

RACKET_BUFFER = 10
brickZoneBuffer = 40
brickCount = [30,30]


RACKET_SCREEN_RATIO = 12
BRICK_SCREEN_RATIO = 40
BALL_SCREEN_RATIO = 53
BRICKZONE_SCREEN_RATIO = 4/3.
bzbufferScreenRatio = 8  



RULES = "\n\n\
#######################################################\n\
#                        RULES                        #\n\
#######################################################\n\
#                                                     #\n\
#     Losing ANY ball from your side is -3 points     #\n\
#                                                     #\n\
#        Hitting a ball captures it temporarily,      #\n\
#              by turning it your colour              #\n\
# You can only score points with balls of your colour #\n\
#                                                     #\n\
#    Losing captured balls only affects the ball's    #\n\
#    original owner, UNLESS it's lost on your side,   #\n\
#        in which case both of you lose points        #\n\
#                                                     #\n\
#                     GOOD LUCK!                      #\n\
#                                                     #\n\
#                  Player Controls:                   #\n\
#                P1 - Green     {Q,A}                 #\n\
#                P2 - Orange  {UP,DOWN}               #\n\
#                P3 - Blue      {C,V}                 #\n\
#                 P4 - Red      {J,K}                 #\n\
#                                                     #\n\
#                                                     #\n\
#                     GAME MODES:                     #\n\
#                                                     #\n\
#                    - ALL v ALL -                    #\n\
#                Every man for himself!               #\n\
#                                                     #\n\
#                      - TEAM -                       #\n\
#                   Players 1 and 2                   #\n\
#                         vs                          #\n\
#                   Players 3 and 4                   #\n\
#            (Get your ball past the other            #\n\
#              team to score more points!)            #\n\
#                                                     #\n\
#                      - COOP -                       #\n\
#                Cooperate for points,                #\n\
#            you succeed or fail together!            #\n\
#        (Standard BrickBreaker when 1 player)        #\n\
#                                                     #\n\
#                      - TIMED -                      #\n\
#                  Timed cooperation,                 #\n\
#              what's the best score you              #\n\
#                can get in 5 minutes?                #\n\
#                                                     #\n\
#                     BRICK TYPES:                    #\n\
#         Blue:   Normal            (1 point)         #\n\
#         Green:  Double-Strength  (2 points)         #\n\
#         Red:    Next Level       (4 points)         #\n\
#######################################################\n\n"


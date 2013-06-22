from constants import X, Y, MIN, MAX, SCORE_BUFFER, BALL_SCREEN_RATIO, BALL_SPAWN_OFFSET, RACKET_SCREEN_RATIO, RACKET_THICKNESS, RACKET_BUFFER, BRICK_SCREEN_RATIO, BRICKZONE_SCREEN_RATIO

def halfway( start, end ):
        return end/2 + start/2

class Window:
        def __init__( self, size=0 ):
                self.sizeMap = {0:320, 1:480, 2:640}
                self.changeSize( self.sizeMap[size] )
                
        def changeSize( self, newSize ):
                self.activeSize = newSize
                self.build()
                
        def build( self ):
                self.screenDimensions = [self.activeSize, self.activeSize+SCORE_BUFFER]
                self.screenSize = [[0,self.screenDimensions[X]], [SCORE_BUFFER,self.screenDimensions[Y]]]
                self.activeWidth = self.screenSize[X][MAX] - self.screenSize[X][MIN]
                self.activeHeight = self.screenSize[Y][MAX] - self.screenSize[Y][MIN]
                
                self.ballDimensions = [self.activeWidth/BALL_SCREEN_RATIO, self.activeHeight/BALL_SCREEN_RATIO]
                self.racketDimensions = [[self.activeWidth/RACKET_SCREEN_RATIO, RACKET_THICKNESS], [RACKET_THICKNESS, self.activeHeight/RACKET_SCREEN_RATIO]]
                self.brickDimensions = [self.activeWidth/BRICK_SCREEN_RATIO, self.activeHeight/BRICK_SCREEN_RATIO]
                self.brickZoneDimensions = [int( self.activeWidth/BRICKZONE_SCREEN_RATIO ), int( self.activeHeight/BRICKZONE_SCREEN_RATIO )]
                
                buffer = [(self.activeWidth - self.brickZoneDimensions[X])/2, (self.activeHeight - self.brickZoneDimensions[Y])/2 + SCORE_BUFFER]
                self.brickZone = [[buffer[X], self.brickZoneDimensions[X] + buffer[X]], [buffer[Y], self.brickZoneDimensions[Y] + buffer[Y]]]

                
                self.racketPosition = [[ self.screenSize[X][MIN] + RACKET_BUFFER, halfway( self.screenSize[Y][MIN], self.screenSize[Y][MAX] ) ],
                                       [ self.screenSize[X][MAX] - RACKET_BUFFER, halfway( self.screenSize[Y][MIN], self.screenSize[Y][MAX] ) ],
                                       [ halfway( self.screenSize[X][MIN], self.screenSize[X][MAX] ), self.screenSize[Y][MIN] + RACKET_BUFFER ],
                                       [ halfway( self.screenSize[X][MIN], self.screenSize[X][MAX] ), self.screenSize[Y][MAX] - RACKET_BUFFER ]]
                                       
                self.ballPosition = [[ self.screenSize[X][MIN] + BALL_SPAWN_OFFSET, halfway( self.screenSize[Y][MIN], self.screenSize[Y][MAX] ) ],
                                     [ self.screenSize[X][MAX] - BALL_SPAWN_OFFSET, halfway( self.screenSize[Y][MIN], self.screenSize[Y][MAX] ) ],
                                     [ halfway( self.screenSize[X][MIN], self.screenSize[X][MAX] ), self.screenSize[Y][MIN] + BALL_SPAWN_OFFSET ],
                                     [ halfway( self.screenSize[X][MIN], self.screenSize[X][MAX] ), self.screenSize[Y][MAX] - BALL_SPAWN_OFFSET ]]
                                     
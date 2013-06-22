import pygame
from score import EditorMode
from brick import MapBuilder
from core import Screen, Controller
from constants import X, Y, MAX, MIN, CONTINUE, BACK, STOP, LEFT, EDITOR, WINDOW, SCORE_BUFFER
#from settings import BRICKZONE, bzone_length_y, bzone_length_x, ScreenDimensions, scoreBuffer

class EditorScreen( Screen ):
        def __init__( self, dimensions, brickZoneDetails ):
                Screen.__init__( self, dimensions )
                
                self.brickZone = brickZoneDetails[0]
                self.brickZoneDimensions = brickZoneDetails[1]
                
                brick_len_x = self.brickZone[X][MAX] - self.brickZone[X][MIN]
                brick_len_y = self.brickZone[Y][MAX] - self.brickZone[Y][MIN]
                
                pygame.draw.rect( self.background, pygame.Color("grey"), (self.brickZone[X][MIN],self.brickZone[Y][MIN], brick_len_x, brick_len_y), 0 )
                #self.recLines( bzone_length_y/2, bzone_length_y/2, Y )
                #self.recLines( bzone_length_x/2, bzone_length_x/2, X )
                self.recVert()
                self.recHor()
                
                
                pygame.draw.rect( self.background, pygame.Color("green"), (0,0,dimensions[X], SCORE_BUFFER), 0 )
                self.screen.blit( self.background, (0,0))
                      
        
        def recVert( self, depth=1, width=None, inc=None):
                base = self.brickZone[X][MIN]
                if width == None: width = self.brickZoneDimensions[X]/2
                if inc == None: inc = self.brickZoneDimensions[X]/2
                
                for y in range(self.brickZone[Y][MIN], self.brickZone[Y][MAX], 10):
                        pygame.draw.line( self.background, pygame.Color("white"), (base+width,y), (base+width,y+3))
                        
                if depth < 3: 
                        inc = inc/2
                        self.recVert( depth+1, width-inc, inc )
                        self.recVert( depth+1, width+inc, inc )
                        
                
        def recHor(self, depth=1, height=None, inc=None):
                base = self.brickZone[Y][MIN]
                if height == None: height = self.brickZoneDimensions[Y]/2
                if inc == None: inc = self.brickZoneDimensions[Y]/2
                
                for x in range(self.brickZone[X][MIN], self.brickZone[X][MAX], 10):
                        pygame.draw.line( self.background, pygame.Color("white"), (x,base+height), (x+3,base+height))
                        
                if depth < 3: 
                        inc = inc/2
                        self.recHor( depth+1, height-inc, inc )
                        self.recHor( depth+1, height+inc, inc )
        
        '''Not Working...
        def recLines( self, distance, increment, axis, depth=1 ):
                base = self.brickZone[1-axis][MIN]
                for n in range(self.brickZone[axis][MIN], self.brickZone[axis][MAX], 10):
                        pygame.draw.line( self.background, pygame.Color("white"), (n,base+distance), (n+3,base+distance))
                        
                if depth < 3: 
                        inc = increment/2
                        self.recLines( distance-inc, inc, axis, depth+1 )
                        self.recLines( distance+inc, inc, axis, depth+1 )
        '''

class EditorController( Controller ):
        def __init__( self, settings ):
                self.window = settings[WINDOW]
                Controller.__init__( self, EditorScreen( self.window.screenDimensions, [self.window.brickZone, self.window.brickZoneDimensions] ) )
                self.type = EDITOR
                
                self.bricks = []
                self.mapper = MapBuilder( self.window.brickDimensions, [self.window.brickZone, self.window.brickZoneDimensions])
                self.mapper.newTemplate()
                self.score = EditorMode( "black", (self.window.screenDimensions[0]/2, SCORE_BUFFER/2), 0, self )
                
        def getAgents( self ):
                return self.bricks + [self.score]
                
                
        def handleEvents( self, events ):
                for event in events:
                        if( event.type == pygame.QUIT ):
                                return STOP
                                
                        elif( event.type == pygame.KEYDOWN ): 
                                if( event.key == pygame.K_c ):
                                        self.mapper.newTemplate()
                                        self.bricks = []
                                
                                elif( event.key == pygame.K_o ):
                                        self.bricks = self.mapper.loadTemplate( int(raw_input( "Load which level?: " )) )
                                
                                elif( event.key == pygame.K_s ):
                                        self.mapper.saveTemplate()
                                        return BACK
                                        
                                elif( event.key == pygame.K_q ):
                                        save = raw_input( "Do you want to save? (y/n): " )
                                        if {'y':True, 'n':False}[save]: self.mapper.saveTemplate()
                                        return BACK
                                        
                                
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == LEFT: removeBrick = False
                                else: removeBrick = True
                                self.bricks = self.mapper.scrollTemplate( (event.pos[0]+4,event.pos[1]+4), removeBrick )
                                
                return CONTINUE
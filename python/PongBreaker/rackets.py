from player import Player
from core import Mover, pygame
from constants import X, Y, XLEN, YLEN, NAME, DIRECTION


class Racket( Mover ):
        def __init__( self, axis, color, position, dimensions, screenSize ):
                Mover.__init__( self, screenSize )
                self.image = pygame.Surface( dimensions )
                self.rect = pygame.Rect( 0, 0, dimensions[XLEN], dimensions[YLEN] )
                self.startPos = position
                
                self.accelerate = False
                self.acceleration = 0.2
                self.decRate = 0.3
                
                self.velMax = [[-2,2],[-2,2]]
                self.direction = -1
                self.color = color
                self.axis = axis
                
                self.start()
                
        def start( self ):
                pygame.draw.rect( self.image, pygame.Color( self.color ), self.rect )
                self.rect.center = self.startPos
                
        def move( self ):
                velocity = self.velocity[self.axis]
                        
                if( self.accelerate == True ):
                        if( self.direction >= 0 ):
                                deltaV = self.acceleration * [-1,1][self.direction]
                                velocity += deltaV
                        
                        
                elif( int(abs(velocity)) > 0.04 ):
                        velocity -= self.decRate * [-1,1][self.direction]
                
                else: velocity = 0
                
                self.velocity[self.axis] = velocity


                

         
class RacketController():
        def __init__( self, racketPosition, ballPosition ):
                self.keyMap = {}
                self.racketDetails = [
                        {"axis": Y, "color": "green", "keys": (pygame.K_q, pygame.K_a),"position": racketPosition[0], "ballposition": ballPosition[0] },
                        {"axis": Y, "color": "orange", "keys": (pygame.K_UP, pygame.K_DOWN), "position": racketPosition[1], "ballposition": ballPosition[1] },
                        {"axis": X, "color": "blue", "keys": (pygame.K_c, pygame.K_v), "position": racketPosition[2], "ballposition": ballPosition[2] },
                        {"axis": X, "color": "red", "keys": (pygame.K_j, pygame.K_k), "position": racketPosition[3], "ballposition": ballPosition[3] } ]
                
        
        def buildRackets( self, playerCount, racketDimensions, screenSize ):
                rackets = []
                players = []
                walls = [True,True,True,True]
                
                for p in range( playerCount ):
                        axis = self.racketDetails[p]['axis']
                        rackets.append( Racket( axis, self.racketDetails[p]['color'], self.racketDetails[p]['position'], racketDimensions[axis], screenSize ) )
                        players.append( Player( p, rackets[p] ) )
                        walls[p] = False
                
                        #{ pygame.K_UP: [<racket0.obj>,0], pygame.K_DOWN: [<racket0.obj>,1], ... }
                        #directions: 0 = axis negative (up, left), 1 = axis positive (down, right)
                        keys = self.racketDetails[p]['keys']
                        for k in range( len( keys )):
                                self.keyMap[ keys[k] ] = [ rackets[p], k ] # EXPLAIN
        
                return [players,walls,rackets]
                
        def move( self, key, keyDown ):
                if( key in self.keyMap ):
                        agent = self.keyMap[key]
                        
                        if( keyDown ):
                                agent[NAME].direction = agent[DIRECTION]
                                agent[NAME].accelerate = True
                        else:
                                agent[NAME].accelerate = False


       
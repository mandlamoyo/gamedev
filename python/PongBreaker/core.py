import pygame
from pygame.sprite import Sprite
from constants import X, Y, LOWER, UPPER, START, END


class Screen:
        def __init__( self, dimensions ):
                self.screen = pygame.display.set_mode( dimensions )
                self.background = pygame.Surface( dimensions )
                self.background.fill( pygame.Color("black"))
                pygame.font.init()
                
        def render( self, agents ):
                sprites = pygame.sprite.RenderClear( agents )
                sprites.update()
                sprites.draw( self.screen )
                pygame.display.flip()
                sprites.clear( self.screen, self.background )
                
class Controller:
        def __init__( self, screen ):
                self.screen = screen
                
        def getAgents( self ):
                return None
                
        def update( self ):
                pass
                
        def render( self ):
                agents = filter( lambda x:x!=None, self.getAgents() )
                self.screen.render( agents )
                
        def handleEvents( self, events ):
                pass

class Agent( Sprite ):
        def __init__( self ):
                Sprite.__init__( self )

        def update( self ):
                pass

                
class Brick( Agent ):
        pass
        
        
class Mover( Agent ):
        def __init__( self, screenSize ):
                Agent.__init__( self )
                self.velocity = [0,0]
                self.velMax = [[-3,3],[-3,3]]
                self.boundary = screenSize
        
        def move( self ):
                pass

        def checkVelocity( self ):
                # Limit velocity to max velocity
                if( self.velocity[X] < self.velMax[X][LOWER] ): self.velocity[X] = self.velMax[X][LOWER]
                if( self.velocity[X] > self.velMax[X][UPPER] ): self.velocity[X] = self.velMax[X][UPPER]
                if( self.velocity[Y] < self.velMax[Y][LOWER] ): self.velocity[Y] = self.velMax[Y][LOWER]
                if( self.velocity[Y] > self.velMax[Y][UPPER] ): self.velocity[Y] = self.velMax[Y][UPPER]
                
        def update( self ):
                self.move()
                self.checkVelocity()
                self.rect.move_ip( self.velocity[X], self.velocity[Y] )
                
                self.rect.top = max( self.boundary[Y][START], self.rect.top )
                self.rect.bottom = min( self.boundary[Y][END], self.rect.bottom )
                self.rect.left = max( self.boundary[X][START], self.rect.left )
                self.rect.right = min( self.boundary[X][END], self.rect.right )
                
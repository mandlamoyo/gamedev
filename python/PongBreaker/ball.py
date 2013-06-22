from math import floor
from core import Mover
from core import pygame
from random import randint, random
from constants import XLEN, YLEN, X, Y, START, END, MIN, MAX, BRICK, OUT, FRICTION, SCORE_BUFFER


class Ball ( Mover ):
        def __init__( self, position, player, controller, dimensions, screenSize ):
                Mover.__init__( self, screenSize )
                self.velMax = [[-2.25,2.25],[-2.25,2.25]]
                
                dimensions = controller.window.ballDimensions
                self.image = pygame.Surface( dimensions )
                pygame.draw.circle( self.image, pygame.Color( player.racket.color ), (dimensions[XLEN]/2,dimensions[YLEN]/2),dimensions[XLEN]/2)
                self.rect = self.image.get_rect()
                
                self.position = position
                self.reposition( position )
                
                
                self.controller = controller
                self.id = randint(0,999)
                self.isAsleep = 0
                self.lastHit = -1
                self.chanceVel = [0,0]
                
                self.dimensions = dimensions
                self.startPos = [position[0] + 4, position[1]]
                
                self.owner = player
                self.player = player
                
                self.serve()
        
        def movePosition( self, velocity ):
                self.position[0] += velocity[0]
                self.position[1] += velocity[1]
                self.rect.center = (int(self.position[0]),int(self.position[1]))
        
        def reposition( self, newPos ):
                self.position = newPos
                self.rect.center = self.position
        
        def transfer( self, player ):
                if player == self.owner or not self.controller.score.harsh: color = pygame.Color( player.racket.color )
                else: color = tuple( [c/2 for c in pygame.Color( player.racket.color )] )
                
                pygame.draw.circle( self.image, color, (self.dimensions[XLEN]/2,self.dimensions[YLEN]/2),self.dimensions[XLEN]/2)
                self.player = player
        
        def serve( self ):
                self.transfer( self.owner )
                dirX = (self.boundary[X][END]/2 + self.boundary[X][START]/2 ) - (self.startPos[X])
                dirY = (self.boundary[Y][END]/2 + self.boundary[Y][START]/2 ) - (self.startPos[Y])
                
                if self.player.racket.axis==1:
                        normX = dirX/abs(dirX)
                        normY = randint(-1,0)+random()
                
                else: 
                        normX = randint(-1,0)+random()
                        normY = dirY/abs(dirY)
                
                
                self.velocity = [normX,normY]
                
                self.reposition( self.startPos[:] )
        
        def update( self ):
                points = [0,[None,0]]
                
                self.checkVelocity()
                self.movePosition( self.velocity ) 
                scorePacket = { 'active': False, 'owner': self.owner.pid, 'player': self.player.pid, 'type': None, 'side': None, 'points': 0 }
                
                #Check player collisions
                for player in self.controller.players:
                        if( self.rect.colliderect( player.racket.rect ) ):
                                axis = player.racket.axis
                                self.velocity[1-axis] *= -1
                                
                                self.velocity[axis] += player.racket.velocity[axis]*FRICTION
                                
                                self.rect.x += self.velocity[1-axis]
                                self.transfer( player )
                
                
                #Have a brickzone: only check for brick collisions when ball is in zone
                #Better yet, divide bricks up into zones, only that zone gets checked
                for brick in self.controller.bricks:
                        if( self.rect.colliderect( brick.rect ) ):
                                directions = { 0:'up', 1:'down', 2:'left', 3:'right' }
                                diff = min( [[abs(self.rect.left - brick.rect.right),2], [abs(self.rect.right - brick.rect.left),3], [abs(self.rect.top - brick.rect.bottom), 0], [abs(self.rect.bottom - brick.rect.top), 1] ] )
                                
                                if brick.id != self.lastHit:
                                        if diff[1] < 2:
                                                self.velocity[1] *= -1
                                                
                                        else:
                                                self.velocity[0] *= -1
                                        
                                        scorePacket['active'] = True
                                        scorePacket['type'] = BRICK
                                        scorePacket['points'] += brick.hit( self )
                                        
                                self.lastHit = brick.id
                                
                if( self.rect.left < self.boundary[X][START] ):
                        if( self.controller.walls[0] ):
                                self.velocity[X] *= -1
                                self.rect.left = self.boundary[X][START] + 1
                        else:
                                self.serve()
                                scorePacket['active'] = True
                                scorePacket['type'] = OUT
                                scorePacket['side'] = 0
                                
                if( self.rect.right > self.boundary[X][END] ):
                        if( self.controller.walls[1] ):
                                self.velocity[X] *= -1
                                self.rect.right = self.boundary[X][END] - 1
                        else:
                                self.serve()
                                scorePacket['active'] = True
                                scorePacket['type'] = OUT
                                scorePacket['side'] = 1
                                
                if( self.rect.top < self.boundary[Y][START] ):
                        if( self.controller.walls[2] ):
                                self.velocity[Y] *= -1
                                self.rect.top = self.boundary[Y][START] + 1
                        else:
                                self.serve()
                                scorePacket['active'] = True
                                scorePacket['type'] = OUT
                                scorePacket['side'] = 2
                                
                if( self.rect.bottom > self.boundary[Y][END] ):
                        if( self.controller.walls[3] ):
                                self.velocity[Y] *= -1
                                self.rect.bottom = self.boundary[Y][END] - 1 
                        else: 
                                self.serve()
                                scorePacket['active'] = True
                                scorePacket['type'] = OUT
                                scorePacket['side'] = 3
                
                if scorePacket['active']: self.controller.score.changeScore( scorePacket )
                
                        
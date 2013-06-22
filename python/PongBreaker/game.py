import pygame
from ball import Ball
from time import sleep
from score import MODES
from player import Player
from brick import MapBuilder
from core import Screen, Controller
from rackets import RacketController
from constants import X, STOP, CONTINUE, GAMEOVER, GOAL, GAME, BACK, SCORE_BUFFER, PLAYERS, MODE, SCREENSIZE, WINDOW


WALLS = 1
RACKETS = 2

class GameScreen( Screen ):
        def __init__( self, dimensions ):
                Screen.__init__( self, dimensions )
                
                pygame.draw.rect( self.background, pygame.Color("yellow"), (0,0,dimensions[X], SCORE_BUFFER), 0 )
                self.screen.blit( self.background, (0,0))
                self.wait = True
                
        def setWait( self ):
                self.wait = True
                
        def render( self, agents ):
                sprites = pygame.sprite.RenderClear( agents )
                sprites.update()
                sprites.draw( self.screen )
                pygame.display.flip()
                
                if self.wait: 
                        sleep(3)
                        self.wait = False
                        
                sprites.clear( self.screen, self.background )
                
                #running = controller.update( pygame.event.get() )
                
                
                
class GameController( Controller ):
        def __init__( self, settings ):
                self.window = settings[WINDOW]
                Controller.__init__( self, GameScreen( self.window.screenDimensions ) )
                
                self.level = 1
                self.type = GAME
                self.nextLevel = None
                self.playerCount = settings[PLAYERS] + 1
                self.mapper = MapBuilder( self.window.brickDimensions, [self.window.brickZone, self.window.brickZoneDimensions])
                self.score = MODES[settings[MODE]]( "black", (self.window.screenDimensions[X]/2, SCORE_BUFFER/2), self.playerCount, self )
                
                '''
                for p in range( self.playerCount ):
                        axis = racketDetails[p]['axis']
                        self.rackets.append( Racket( axis, racketDetails[p]['color'], racketDetails[p]['position'], self.window.racketDimensions[axis], self.window.screenSize ) ) #racketDetails[p]['axis']( racketDetails[p]['color'], racketDetails[p]['position'], self.window. ) )
                        self.players.append( Player( p, self.rackets[p] ) )
                        self.walls[p] = False
                '''
                
                self.racketMover = RacketController( self.window.racketPosition, self.window.ballPosition )
                results = self.racketMover.buildRackets( self.playerCount, self.window.racketDimensions, self.window.screenSize )
                
                self.bricks = []
                self.walls = results[WALLS]
                self.rackets = results[RACKETS]
                self.players = results[PLAYERS]
                self.balls = [ Ball( self.racketMover.racketDetails[p]['ballposition'], self.players[p], self, self.window.ballDimensions, self.window.screenSize ) for p in range( self.playerCount ) ]
        
        
                self.gameOver = False
                self.start()
        
        def start( self ):
                self.bricks = self.getLevel( self.level )
                self.nextLevel = len([brick for brick in self.bricks if brick.type == GOAL])
                for racket in self.rackets: racket.start()
                for ball in self.balls: ball.serve()
        
        def getLevel( self, number ):
                return self.mapper.getLevel( number )
                
        def getAgents( self ):
                return self.rackets + self.balls + self.bricks + [self.score]
                
        def getScores( self ):
                return self.score.getScores()
                
        def update( self ):
                for agent in self.getAgents():
                        agent.update()
                
                
                # Level checking/updating
                tempBricks = []
                nextLevel = self.nextLevel
                
                # Subtract one from the total number of goal bricks for every goal brick encountered
                for brick in self.bricks:
                        if brick.isAlive:
                                if brick.type == GOAL: 
                                        nextLevel -= 1
                                tempBricks.append( brick )
                        
                # If there is a goal brick unaccounted for (it has been hit), then move to the next level       
                if nextLevel:
                        self.level += 1
                        self.start()
                        
                        if len( self.bricks ) == 0: self.gameOver = True
                        else: self.screen.setWait() #return WAIT
                # otherwise, update/reset values for next iteration
                else: 
                        self.bricks = tempBricks
                        #self.nextLevel = nextLevel
                #self.bricks = [ brick for brick in self.bricks if brick.isAlive == True ]
                        
                
        def handleEvents( self, events ):
                if self.gameOver: return GAMEOVER
                
                for event in events:
                        if( event.type == pygame.QUIT ):
                                return STOP
                                
                        elif( event.type == pygame.KEYDOWN ): 
                                if event.key == pygame.K_BACKSPACE:
                                        return BACK
                                
                                elif event.key == pygame.K_f:
                                        return GAMEOVER
                                
                                self.racketMover.move( event.key, True )
                        elif( event.type == pygame.KEYUP ):
                                self.racketMover.move( event.key, False )
                                
                return CONTINUE
from core import Sprite
from core import pygame
from constants import GAME, EDITOR, OUT, BRICK


SCORE = 0
LIVES = 1
TIME = 1

class Mode( Sprite ):
        def __init__( self, color, position, playerCount, controller, score=None, harsh=False ):
                pygame.sprite.Sprite.__init__( self )
                self.color = pygame.Color( color )
                self.score = score
                self.playerCount = playerCount
                self.negativeScores = False
                self.controller = controller
                
                self.font = pygame.font.Font( None, 24 )
                self.renderText()
                self.rect = self.image.get_rect()
                self.rect.center = position
                self.harsh = harsh
                
        def renderText( self ):
                pass
                #self.image = self.font.render( "", True, self.color )
        
        def validateScore( self ):
                for side in range(len(self.score)):
                        if self.score[side] < 0 and not self.negativeScores: 
                                self.score[side] = 0
                
                self.renderText()
        
        def changeScore( self, scorePacket ):
                pass
                
        def getScores( self, title="PLAYER" ):
                scores = [[ self.score[i], title + " " + str(i+1) ] for i in range(len(self.score)) ]
                scores.sort( reverse=True )
                return [[ str(n+1) + ": " + scores[n][1] + " --- ", scores[n][0] ] for n in range(len(scores)) ]
                
                
class StandardMode( Mode ): #2+ players
        def __init__( self, color, position, playerCount, controller, harsh=False ):
                Mode.__init__( self, color, position, playerCount, controller, [0,0,0,0] )
                self.mode = 'standard'
                
        def renderText( self ):
                text = ""
                for p in range( self.playerCount ): text += "P%(pn)d: {%(n)d}         " % {'pn':p+1, 'n':p}
                self.image = self.font.render( text.format( *self.score ), True, self.color )

        def changeScore( self, scorePacket ):
                if scorePacket['type'] == OUT:
                        if self.harsh: self.score[scorePacket['owner']] -= 2
                        self.score[scorePacket['side']] -= 3
                
                elif scorePacket['type'] == BRICK:
                        self.score[scorePacket['player']] += scorePacket['points']
                        
                self.validateScore()
                
                
class TeamMode( Mode ): #4 players
        def __init__( self, color, position, playerCount, controller ):
                Mode.__init__( self, color, position, playerCount, controller, [0,0] )
                self.teams = [0,0,1,1]
                self.mode = 'team'
                
        def renderText( self ):
                text = ""
                for t in range(len( self.score )): text += "Team %(tn)d: {%(n)d}         " % {'tn':t+1, 'n':t}
                print self.score
                self.image = self.font.render( text.format( *self.score ), True, self.color )
                
        def changeScore( self, scorePacket ):
                if scorePacket['type'] == OUT:
                        self.score[self.teams[scorePacket['side']]] -= 3
                
                        #goal scoring
                        if self.teams[scorePacket['player']] != self.teams[scorePacket['side']]:
                                self.score[self.teams[scorePacket['player']]] += 1
                
                elif scorePacket['type'] == BRICK:
                        self.score[self.teams[scorePacket['player']]] += scorePacket['points']
                        
                self.validateScore()
                
        def getScores( self ):
                return Mode.getScores( self, 'TEAM' )
        
        def changeTeams( self, player, newTeam ):
                self.teams[player] = newTeam
                self.score = [ 0 for i in range(len(set(self.teams))) ]
                
                
class CoopMode( Mode ): #also singleplayer, any number of players
        def __init__( self, color, position, playerCount, controller ):
                Mode.__init__( self, color, position, playerCount, controller, [0,3*playerCount] )
                self.mode = 'coop'
                
        def renderText( self ):
                self.image = self.font.render( "Score: {0}         Lives: {1}".format( *self.score ), True, self.color )
                
        def changeScore( self, scorePacket ):
                if scorePacket['type'] == OUT:
                        self.score[LIVES] -= 1
                
                elif scorePacket['type'] == BRICK:
                        self.score[SCORE] += scorePacket['points']
                
                
                self.validateScore()
                if self.score[LIVES] <= 0: self.controller.gameOver = True
                
        def getScores( self ):
                return [["YOUR SCORE: ", self.score[SCORE]]]
                
class TimedMode( Mode ): #same as coopmode? but time instead of lives... any number of players
        def __init__( self, color, position, playerCount, controller ):
                Mode.__init__( self, color, position, playerCount, controller, [0,1000] )
                self.mode = 'timed'
                
        def renderText( self ):
                self.image = self.font.render( "Score: {0}         Time: {1}".format( *self.score ), True, self.color )
        
        def changeScore( self, scorePacket ):
                if scorePacket['type'] == OUT:
                        self.score[SCORE] -= 3
                
                elif scorePacket['type'] == BRICK:
                        self.score[SCORE] += scorePacket['points']
        
                self.validateScore()
                
        def getScores( self ):
                return [["YOUR SCORE: ", self.score[SCORE]]]
                
        def update( self ):
                self.score[TIME] -= 1
                self.validateScore()
                if self.score[TIME] <= 0: self.controller.gameOver = True
                
      
                
class EditorMode( Mode ):
        def renderText( self ):
                self.image = self.font.render( "'c' - clear | 'o' - open | 's' - save | 'q' - quit", True, self.color )
                
                
MODES = [StandardMode, TeamMode, CoopMode, TimedMode]
        
''' OBSOLETE                 
class Score( Sprite ):
        def __init__( self, color, position, mode ):
                pygame.sprite.Sprite.__init__( self )
                self.color = pygame.Color( color )
                self.score = [0,0,0,0]
                self.mode = mode
                self.gameMode = gmode
                
                self.font = pygame.font.Font( None, 24 )
                self.render_text()
                self.rect = self.image.get_rect()
                self.rect.center = position
                
                
        def render_text( self ):
                if self.mode == GAME: self.image = self.font.render( "P1: {0}         P2: {1}         P3: {2}         P4: {3}".format( *self.score ), True, self.color )
                if self.mode == EDITOR: self.image = self.font.render( "'c' - clear | 'o' - open | 's' - save | 'q' - quit", True, self.color )
                
        def change_scoreOLD( self, side, quantity ):
                self.score[side] += quantity
                if self.score[side] < 0 and not NEGATIVE_SCORES: 
                        self.score[side] = 0
                
                self.render_text()
        
        def changeScore( self, scorePacket ):
                #STANDARD MODE
                if scorePacket['type'] == OUT:
                        if HARSH: self.score[scorePacket['owner']] -= 2
                        self.score[scorePacket['side']] -= 3
                
                elif scorePacket['type'] == BRICK:
                        self.score[scorePacket['player']] += scorePacket['points']
                        
                #2V2
                
'''

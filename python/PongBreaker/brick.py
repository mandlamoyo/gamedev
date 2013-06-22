import os
import csv
from random import randint
from core import Agent, pygame
from constants import X, Y, XLEN, YLEN



BRICKTYPES = [
        { "color": "blue", "health": 1, "points": 1, "type": "basic" },
        { "color": "green", "health": 2, "points": 2, "type": "reinforced" },
        { "color": "red", "health": 1, "points": 4, "type": "goal" }
]

class Brick( Agent ):
        def __init__( self, position, brickType, dimensions ):
                Agent.__init__( self )
                self.image = pygame.Surface( dimensions )
                self.rect = pygame.Rect( 0, 0, dimensions[XLEN], dimensions[YLEN] )
                pygame.draw.rect( self.image, pygame.Color( BRICKTYPES[brickType]["color"] ), self.rect )
                self.rect.center = position
                self.position = position
                
                self.id = randint(1000,1000000)
                self.type = brickType
                self.color = BRICKTYPES[brickType]["color"]
                self.points = BRICKTYPES[brickType]["points"]
                self.health = BRICKTYPES[brickType]["health"]
                self.maxHealth = BRICKTYPES[brickType]["health"]
                self.lastHitPlayer = None
                self.isAlive = True
                
        def hit( self, ball ):
                if( self.health > 0 ): self.lastHitPlayer = ball.player
                
                self.health -= 1
                
                if( self.health <= 0 ): 
                        self.isAlive = False
                        return self.points
                
                ##else:
                        ##hFrac = self.health/float(self.maxHealth)
                        ##color = tuple( [int(c*hFrac) for c in pygame.Color( self.color )] )
                        ##print pygame.Color( self.color )
                        ##print color
                        
                        ##pygame.draw.rect( self.image, pygame.Color( 'purple' ), self.rect )
                        ##self.rect.center = self.position
                        
                return 0
                
    
class MapBuilder:
        def __init__( self, brickDimensions, brickZoneDetails ):
                self.template = None
                self.brickDimensions = brickDimensions
                self.brickZone = brickZoneDetails[0]
                self.brickZoneDimensions = brickZoneDetails[1]
                
        def newTemplate( self ):
                brickCount = [self.brickZoneDimensions[X]/self.brickDimensions[X], self.brickZoneDimensions[Y]/self.brickDimensions[Y]]
                self.template = [[0 for i in range(brickCount[X])] for j in range(brickCount[Y])]
                
        def scrollTemplate( self, coords, remove=False ):
                position = self.getPosFromCoords( coords )
                if 0 <= position[1] < len( self.template ) and 0 <= position[0] < len( self.template[0] ):
                        if remove: self.template[position[1]][position[0]] = 0
                        else: self.template[position[1]][position[0]] = (self.template[position[1]][position[0]] + 1)%(len(BRICKTYPES)+1)
                        
                return self.buildMap( self.template )
                
        def loadTemplate( self, level ):
                levelMap = self.loadMap( level )
                self.template = levelMap
                return self.buildMap( self.template )
        
        def saveTemplate( self, level=1 ):
                while True:
                        levelpathname = 'levels/level' + str(level) + '.csv'
                        if not os.path.isfile( levelpathname ): break
                        level += 1
                        
                with open(levelpathname,'wb') as f:
                        writer = csv.writer(f)
                        writer.writerows(self.template)
                
                
        def getCoords( self, position ):
                origin = [self.brickZone[0][0]+self.brickDimensions[0]/2, self.brickZone[1][0]+self.brickDimensions[1]/2]
                return [origin[0] + (position[0]*self.brickDimensions[0]), origin[1] + (position[1]*self.brickDimensions[1])]

                
        def getPosFromCoords( self, coords ):
                origin = [self.brickZone[0][0]+self.brickDimensions[0]/2, self.brickZone[1][0]+self.brickDimensions[1]/2]
                xdiff = coords[0] - origin[0]
                return ( (coords[0] - origin[0])/8, (coords[1] - origin[1])/8 )
        
        def loadMap( self, level ):
                levelMap = []
                levelpathname = 'levels/level' + str(level) + '.csv'
                if not os.path.isfile( levelpathname ): return False
                
                with open(levelpathname,'rb') as f:
                        reader = csv.reader(f)
                        for row in reader:
                                levelMap.append([int(value) for value in row])
                                
                return levelMap
        
        
        def buildMap( self, levelMap ):
                brickArray = []

                for j in range(len(levelMap)):
                        for i in range(len(levelMap[j])):
                                if levelMap[j][i] > 0:
                                        brickArray.append( Brick( self.getCoords( [i,j] ), levelMap[j][i]-1, self.brickDimensions ) )
                                        
                return brickArray
        
        
        def getLevel( self, level ):
                levelMap = self.loadMap( level )
                if levelMap: return self.buildMap( levelMap )
                return []
        

                        

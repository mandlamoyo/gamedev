import pygame
from window import Window
from core import Screen, Controller, Sprite
from constants import X, Y, MENU, GAME, EDITOR, SETTINGS, RULES, STOP, CONTINUE, BACK, PLAYERS, DIMENSIONS, MODE, SCREENSIZE, WINDOW, MENU_DIMENSIONS, MENU_POSITION, RULES

PLAYER = 0
VALUE = 1

DISPLAY = 0
DIMENSIONS = 1
SCORES = 2

DEFAULT = 0
POSITION = 1
TOTAL = 2
IMAGE = 3

imageMap = [None,{0: "allvall", 1: "team", 2: "coop", 3: "timed" }]

class Scores( Sprite ):
        def __init__( self, score, offset ):
                Sprite.__init__( self )
                
                score.sort( reverse=True )
                text = score[PLAYER] + str( score[VALUE] )
                
                #for n in range(len(scores)):
                #        text += scores[n][PLAYER] + str( scores[n][VALUE] ) + "\n"

                self.font = pygame.font.Font( None, 50 )        
                self.image = self.font.render( text, True, pygame.Color( "white" ) )
                self.rect = self.image.get_rect()
                self.rect.center = (MENU_DIMENSIONS[X]/2,265 + offset) #MENU_POSITION
                
class Pointer( Sprite ):
        def __init__( self, image, positionMap, position, visible=True ):
                Sprite.__init__( self )
                self.image = pygame.image.load( image )
                self.image = self.image.convert_alpha()
                
                self.visible = visible
                self.positionMap = positionMap

                self.position = positionMap[position]
                self.rect = self.image.get_rect()
                self.rect.center = self.position
             
                
        def setPosition( self, option ): #translates option to coords!
                if option < len( self.positionMap ):
                        self.position = self.positionMap[option]
                        self.rect.center = self.position
                

class Value( Sprite ):
        def __init__( self, value, position, maximum=4, vmap=None ):
                Sprite.__init__( self )
                
                if vmap: self.vmap = vmap
                else: self.vmap = {0:"one", 1:"two", 2:"three", 3:"four"}
                
                self.value = value
                self.maximum = maximum
                self.position = position
                self.loadImage( self.value )
                
         
        def loadImage( self, value ):
                image = "images/" + self.vmap[value] + ".gif"
                self.image = pygame.image.load( image )
                self.image = self.image.convert_alpha()
               
                self.rect = self.image.get_rect()
                self.rect.center = self.position
                
        def changeValue( self, newValue ):
                self.value = newValue%self.maximum
                self.loadImage( self.value )
                
        def getValue( self ):
                return self.value
                
class MenuScreen( Screen ):
        def __init__( self, dimensions ):
                Screen.__init__( self, dimensions )
                
                title = pygame.image.load("images/title.gif")
                title = title.convert_alpha()
                
                self.background.blit( title, (0,0))
                self.screen.blit( self.background, (0,0))
               
                

menu1 = { 'image': "images/menu1.gif", 'options': ['game','settings','rules','editor'], 'subOptions': {}, 'positionMap': [(92,261),(92,310),(92,359),(92,422)], 'subPositionMap': [(92,261),(92,310),(92,359),(92,422)], 'valueDetails': [] }

menu2 = { 'image': "images/menu2.gif", 'options': ['players','mode', 'screensize', 'back'], 'subOptions': {'players':[1,2,3,4],'mode':[1,2,3,4],'screensize':[1,2,3]}, 'positionMap': [(92,261),(92,310),(92,359),(92,422)], 'subPositionMap': [(502,283),(502,333),(502,381)], 'valueDetails': [(0,(503,261),4,0),(2,(503,311),4,1),(0,(503,359),3,0)] }

menu3 = { 'image': "images/menu3.gif", 'options': ['main'], 'subOptions': {}, 'positionMap': [(92,422)], 'subPositionMap': [(92,422)], 'valueDetails': [] }

class Menu( Sprite ):
        def __init__( self, type, menuSettings ):
                Sprite.__init__( self )
        
                self.image = pygame.Surface( (640,256) )
                self.image = pygame.image.load( menuSettings['image'] )
                self.image = self.image.convert_alpha()
                self.type = type
                
                #self.position = MENU_CENTRE
                #self.rect = self.image.get_rect()
                #self.rect.center = self.position
                
                self.options = menuSettings['options']
                self.subOptions = menuSettings['subOptions']
                self.positionMap = menuSettings['positionMap']
                self.subPositionMap = menuSettings['subPositionMap']
                self.values = [ Value(v[DEFAULT],v[POSITION],v[TOTAL],imageMap[v[IMAGE]]) for v in menuSettings['valueDetails'] ]

                
                self.settings = { PLAYERS: 0, MODE: 2, SCREENSIZE: 0, WINDOW: None }
                
        def setOption( self, option, newSetting ):
                #value = newSetting + 1
                self.settings[option] = newSetting
                self.values[option].changeValue( newSetting )
                #self.settings[option] = newSetting
                #self.values[option].changeValue( newSetting )
                
        def getOption( self, option ):
                return self.settings[option] #self.settings[self.options[option]] #
  

        
#self.options = { 0: GAME, 1: SETTINGS, 2: RULES, 3: EDITOR }
#positionMap = {0: (0,0), 1: (0,0), 2: (0,0), 3: (0,0) }
#defaultSettings = { PLAYERS: 1, MODE: 1, SCREENSIZE: 1 }

class MenuController( Controller ):
        def __init__( self, settings ): #display='main', dimensions=MENU_DIMENSIONS ):
                Controller.__init__( self, MenuScreen( settings[DIMENSIONS] ))
                self.type = MENU
                
                if len( settings ) == 3: self.scores = settings[SCORES]
                else: self.scores = None
                
                self.menuStack = []
                self.menuList = {'main':menu1, 'settings':menu2, 'scores':menu3}
                self.menu = Menu( settings[DISPLAY], self.menuList[ settings[DISPLAY] ] )
                self.screen.screen.blit( self.menu.image, MENU_POSITION )
                
                self.initGame = 0
                self.currentOption = 0
                self.onSubOption = False #Selecting a suboption? (As opposed to a main option)
                
                
                
                self.pointer = Pointer( "images/pointer.gif", self.menu.positionMap, self.currentOption )
                self.subPointer = Pointer( "images/subpointer.gif", self.menu.subPositionMap, self.currentOption, visible=False ) #change to "images/subpointer.gif"
                
                self.selected = None
                
                
        def getAgents( self ):
                agents = filter( lambda x: x.visible==True, [self.pointer, self.subPointer] ) + self.menu.values
                if self.menu.type == 'scores': 
                        for i in range(len(self.scores)):
                                agents.append( Scores( self.scores[i], 35*i ))
                        
                return agents
                
        def update( self ):
                if self.selected:
                        self.changeMenu( self.selected )
                        self.selected = None
        
                self.pointer.setPosition( self.currentOption )
                self.subPointer.setPosition( self.currentOption )
           
        def changeMenu( self, menuName ):
                if menuName == 'game' or menuName == 'editor':
                        self.initGame = {'game':GAME, 'editor':EDITOR}[menuName]
                        
                elif menuName == 'rules':
                        print RULES
        
                else:
                        if menuName == 'back': 
                                settings = self.menu.settings
                                self.menu = self.menuStack.pop()
                                self.menu.settings = settings
                        else:
                                if self.menu: self.menuStack.append( self.menu )
                                self.menu = Menu( menuName, self.menuList[menuName] )

                                
                        self.pointer = Pointer( "images/pointer.gif", self.menu.positionMap, self.currentOption )
                        self.subPointer = Pointer( "images/subpointer.gif", self.menu.subPositionMap, self.currentOption, visible=False )
                        self.screen.screen.blit( self.menu.image, MENU_POSITION )
                        self.currentOption = 0
                        
        def toggleSubOption( self ):
                if self.onSubOption:
                        self.onSubOption = False
                        self.subPointer.visible = False
                        return False
                else:
                        self.onSubOption = True
                        self.subPointer.visible = True
                        return True
                        

                        
        def handleEvents( self, events ):
                if self.initGame: 
                        self.menu.settings[WINDOW] = Window( self.menu.settings[SCREENSIZE] )
                        return [self.initGame, self.menu.settings]
                
                for event in events:
                        if( event.type == pygame.QUIT ):
                                return STOP
                                
                        elif( event.type == pygame.KEYDOWN ): 
                                if( event.key == pygame.K_UP or event.key == pygame.K_DOWN ):
                                        adjustment = {pygame.K_UP:-1, pygame.K_DOWN:1}[event.key]
                                        
                                        if self.onSubOption:
                                                self.menu.setOption( self.currentOption, (self.menu.getOption( self.currentOption ) - adjustment)%len( self.menu.subOptions[self.menu.options[self.currentOption]] ) )
                                                #print self.currentOption, self.menu.getOption( self.currentOption ), self.menu.settings[self.currentOption]
                                        else:
                                                newPosition = (self.currentOption + adjustment)%len(self.menu.options)
                                                self.currentOption = newPosition
                                                
                                        
                                elif( event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT ): 
                                        if self.menu.subOptions and self.menu.options[self.currentOption] in self.menu.subOptions: 
                                                currentSetting = self.toggleSubOption()

                                        elif event.key == pygame.K_RIGHT: self.selected = self.menu.options[self.currentOption]
                                        
                                elif( event.key == pygame.K_RETURN ):
                                        if self.menu.subOptions and self.currentOption in self.menu.subOptions: continue
                                        else:
                                                self.selected = self.menu.options[self.currentOption]
                                                #print self.menu.options[self.currentOption]
                                        
                                elif( event.key == pygame.K_u ):
                                        self.pointer.visible = not self.pointer.visible
                                        
                return CONTINUE
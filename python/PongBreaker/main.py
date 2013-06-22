#!/usr/bin/env python
from core import pygame
from game import GameController
from editor import EditorController
from menu import MenuController
from constants import FPS, TYPE, DETAILS, MENU, GAME, EDITOR, STOP, CONTINUE, BACK, MENU_DIMENSIONS, GAMEOVER



def main():
        pygame.init() 
        clock = pygame.time.Clock()
        controllerStack = []
        menuSettings = ['main',MENU_DIMENSIONS]
        
        controller = MenuController( menuSettings )
        controllerType = {GAME: GameController, EDITOR: EditorController, MENU: MenuController}
        running = True
        
        while running:
                clock.tick(FPS)
                pygame.display.set_caption("PONG - {0:2f} fps".format( clock.get_fps() ))

                controller.render()
                state = controller.handleEvents( pygame.event.get() )
                
                
                if isinstance( state, list ):
                        controller = controllerType[state[TYPE]]( state[DETAILS] )
                
                elif state == STOP: running = False
                elif state == CONTINUE: controller.update()
                elif state == GAMEOVER:
                        scores = controller.getScores()
                        controller = MenuController( ['scores', MENU_DIMENSIONS, scores] )
                        
                elif state == BACK: 
                        controller = MenuController( menuSettings )

                        
                        
'''                     
def main():
        player_count = 0
        mode = {'y':EDITOR, 'n':MAIN}[raw_input( "Level editor? (y/n): " )]
        
        if mode == MAIN:
                player_count = int( raw_input( "How many players?: " ) )
                while (0 < player_count <= 4) != True: player_count = int( raw_input( "Invalid number, try again: " ) )
        
                print RULES
                
        runGame( player_count, mode )

def runGame( player_count, mode ):
        screen = pygame.display.set_mode((ScreenDimensions[0],ScreenDimensions[1]))
        clock = pygame.time.Clock()
        pygame.font.init()
        controller = Controller( player_count, mode )
        background = pygame.Surface([ScreenDimensions[0],ScreenDimensions[1]])
        
        #Background details
        background.fill( pygame.Color("black"))
        
        pygame.draw.rect( background, pygame.Color("yellow"), (0,0,ScreenDimensions[0],scoreBuffer), 0 )
        brick_len_x = BRICKZONE[X][MAX] - BRICKZONE[X][MIN]
        brick_len_y = BRICKZONE[Y][MAX] - BRICKZONE[Y][MIN]
        
        if mode == EDITOR: 
                pygame.draw.rect( background, pygame.Color("grey"), (BRICKZONE[X][MIN],BRICKZONE[Y][MIN], brick_len_x, brick_len_y), 0 )
                recVert()   
                recHor()
                
        screen.blit( background, (0,0))
        
        
        #Setup
        agents = filter( lambda x:x!=None, controller.getAgents() )
        sprites = pygame.sprite.RenderClear( agents )
        sprites.draw( screen )
        pygame.display.flip()
        
        
        sprites.clear( screen, background )
        
        running = WAIT
        
        while running:
                
                pygame.display.set_caption("PONG - {0:2f} fps".format( clock.get_fps()))
        
                agents = filter( lambda x:x!=None, controller.getAgents() )
                sprites = pygame.sprite.RenderClear( agents )
                sprites.update()
                sprites.draw( screen )
                pygame.display.flip()
                if running == WAIT: sleep(3)
                sprites.clear( screen, background )
                
                running = controller.update( pygame.event.get() )
'''                
                
                
if __name__ == "__main__":
        main()
        

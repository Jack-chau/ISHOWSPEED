import customtkinter as ctk
from sidebar.menuPage import SwitchMenu
from mydocker.myDockerPage import MyDockerPage
from myansible.myAnsiblePage import MyAnsiblePage
import pygame
# import threading

def main() :
    app = Notorious()
    app.mainloop()

class Notorious( ctk.CTk ) :
    def __init__( self ) :
        super( ).__init__( )
        ctk.set_appearance_mode( 'light' )
        ctk.set_default_color_theme( './theme/rime.json' )
        ctk.set_widget_scaling( 1.0 )
        # root window size
        self.title( "ISHOWSPEED" )
        self.geometry( f'{1800}x{1200}+{180}+{80}' )
        # self.resizable( False, False )

# Default Page
        # thread1 = threading.Thread( target = self.docker_page )
        # thread1.start()
        self.docker_page()
# Music
        # thread2 = threading.Thread( target = self.play_music )
        # thread2.start()
        # self.play_music()
    
        # define grid ( 10 column * 4 row )
        self.grid_columnconfigure( 0, weight = 0 )
        self.grid_columnconfigure( 1, weight = 0 )
        self.grid_columnconfigure( 2, weight = 2 )
        self.grid_columnconfigure( 3, weight = 1 )
        self.grid_columnconfigure( 4, weight = 15 )
        self.grid_columnconfigure( 5, weight = 1 )
        self.grid_columnconfigure( 6, weight = 2 )
        self.grid_columnconfigure( 7, weight = 1 )
        self.grid_columnconfigure( 8, weight = 1 )
        self.grid_columnconfigure( 9, weight = 1 )
        self.grid_rowconfigure( ( 0, 1, 2 ), weight = 1 )
        self.grid_rowconfigure( 3, weight = 1)

        # Menu Frame

        self.switch_menu = SwitchMenu( self )

        self.switch_menu.docker_btn.configure( command = lambda : self.switch_page( indicator = self.switch_menu.docker_btn , page = self.docker_page ) )
        self.switch_menu.docker_label.configure( command = lambda : self.switch_page( indicator = self.switch_menu.docker_btn , page = self.docker_page ) )
        self.switch_menu.ansible_btn.configure( command = lambda : self.switch_page( indicator = self.switch_menu.ansible_btn , page = self.ansible_page ) )
        self.switch_menu.ansible_label.configure( command = lambda : self.switch_page( indicator = self.switch_menu.ansible_btn , page = self.ansible_page ) )

    def docker_page( self ) : 
        self.DockerPage = MyDockerPage( self )

    def ansible_page( self ) :
        self.AnsiblePage = MyAnsiblePage( self )

    def switch_page( self, indicator, page ) :
        self.switch_menu.docker_btn.configure( fg_color = 'transparent' )
        self.switch_menu.ansible_btn.configure( fg_color = 'transparent' )
        # self.switch_menu.logging_btn.configure( fg_color = 'transparent' )
        # self.switch_menu.schedule_btn.configure( fg_color = 'transparent' )
        # self.switch_menu.github_btn.configure( fg_color = 'transparent' )
        indicator.configure( fg_color = self.switch_menu.selected_color, hover_color = self.switch_menu.selected_color )
        # thread3 = threading.Thread( target = page )
        # thread3.start()
        page()

    
    def play_music( self ) :
        pygame.mixer.init()
        pygame.mixer.music.load( "./Music/cso.mp3" )
        pygame.mixer.music.play( loops = 0 )

if __name__ == "__main__":   
    main()

      
import customtkinter as ctk
from CTkTable import *
# Menu Bar
from sidebar.features import Clock, Appearance, Progressbar
from datetime import datetime
# Frames
from myansible.frames.inventoryTab import AnsibleInventoryTab
from myansible.frames.playbookTab import AnsiblePlaybookTab

class AnsibleMainFrame( ctk.CTkFrame ) :
    def __init__( self, master ) :
        super( ).__init__( master )

    def ansible_frame( self ) :
###SideBar

    # Ansible Sidebar Frame
        self.ansible_sidebar = ctk.CTkFrame( 
            self.master, 
            width = 100, 
            corner_radius = 0 
        )
        self.ansible_sidebar.grid( 
            row = 0, 
            rowspan = 4,
            columnspan = 2,
            column = 2, 
            sticky = 'nsew' 
        )

    # Sidebar
        self.page_label = ctk.CTkLabel( 
            self.ansible_sidebar, 
            text = "Ansible Page", 
            font = ctk.CTkFont("Segoe Script", 30 ),
        )
        self.page_label.pack( 
            side = 'top',
            pady = ( 40, 30 ),
            padx = ( 50, 50 ),
        )

        # Clock
        self.date_label = Clock( self.ansible_sidebar ).date_label
        self.date_label.pack(
            side = 'top',
            pady = ( 100, 0 )
        )
        self.day_label = Clock( self.ansible_sidebar ).day_label
        self.day_label.pack(
            side = 'top',
        )
        self.time_label = Clock( self.ansible_sidebar ).time_label
        self.time_label.pack(
            side = 'top',
            pady = ( 15 , 0)
        )
        
    # Appearance
        self.appearance_label = Appearance( self.ansible_sidebar ).appearance_label
        self.appearance_label.configure( 
            font = ctk.CTkFont("Segoe Script", 25 )
        )
        self.appearance_label.pack( 
            side = 'top',
            pady = ( 250, 20 )
        )

        self.appearance_option_menu = Appearance( self.ansible_sidebar ).appearance_optionmenu
        self.appearance_option_menu.configure(
            width = 200,
            height = 50, 
            font = ctk.CTkFont("Segoe Script", 25 ),
            dropdown_font = ctk.CTkFont("Segoe Script", 25 ),
        )
        self.appearance_option_menu.pack( 
            side = 'top',
            pady = ( 20, 20 )
        )

        self.scale_label = Appearance( self.ansible_sidebar ).scale_label
        self.scale_label.configure( 
            font = ctk.CTkFont("Segoe Script", 25 )
        )
        self.scale_label.pack( 
            side = 'top',
            pady = ( 20, 20 )
        )

        self.scale_optionmenu = Appearance( self.ansible_sidebar ).scale_optionmenu
        self.scale_optionmenu.configure(
            width = 200,
            height = 50,
            font = ctk.CTkFont("Segoe Script", 25 ),
            dropdown_font = ctk.CTkFont("Segoe Script", 25 ),
        )
        self.scale_optionmenu.pack( )

############ Ansible tab 

        # Ansible Tab Frame
        self.ansible_frame = ctk.CTkFrame(
            self.master,
            width = 300 ,
            corner_radius = 0,
        )
        self.ansible_frame.grid( 
            row = 0, 
            column = 4,
            columnspan = 3,
            rowspan = 2,
            sticky = 'nsew',
        )

        self.ansible_application = ctk.CTkLabel(
            self.ansible_frame,
            text = "Ansible Applicaiton",
            font = ctk.CTkFont(
                family="Courier New",
                size=25,
                weight="bold",
                slant="italic",
                overstrike=False
            )
        )

        self.ansible_application.pack(
            fill = 'both',
            pady = (30,10),
            padx = ( 10, 10 )
        )

        self.ansible_tab = ctk.CTkTabview(
            self.ansible_frame ,
            width = 900,
            height = 200,
            anchor = "nw",
            # border_width = 2
        )
        self.ansible_tab.pack(
            fill = 'both',
            expand = True,
            padx = ( 50, 50) ,
            pady = ( 0, 20 ),
            
        )

        self.ansible_tab._segmented_button.configure(
            font = ( "Helventica bold", 15 ),
            width = 500,
            height =30,
            dynamic_resizing = False, 

        )
# Docker tabs
        self.inventory_tab = AnsibleInventoryTab( self.ansible_tab )
        self.playbook_tab = AnsiblePlaybookTab( self.ansible_tab )

#CLI output frame
    # Text Box Frame
        self.ansible_textbox_frame = ctk.CTkFrame( 
            self.master, 
            corner_radius = 0,
            border_width = 0, 
        )
        self.ansible_textbox_frame.grid( 
            row = 2, 
            rowspan = 2, 
            column = 4,
            columnspan = 3,
            sticky = 'nsew',
        )
    # Textbox
        self.ansible_textbox = ctk.CTkTextbox( 
            self.ansible_textbox_frame,
            corner_radius = 0,
            border_width = 0,
            font = ctk.CTkFont( size=15, weight='bold' )
        )
        self.ansible_textbox.pack(
            side = 'top',
            padx = ( 50, 50 ),
            pady = ( 0, 0 ),
            expand = True,
            fill = 'both',
        )
        
    # Progress bar
        self.progressbar = Progressbar( self.ansible_textbox_frame ).progressbar
        self.progressbar.pack(
            side = 'top',
            fill = 'both',
            padx = (10,10),
            pady = (10,10),
        )
        self.progressbar.set( 0 )
        # self.progressbar.forget()
'''
# Remark
### Note Frame
        self.note_frame = ctk.CTkFrame( 
            self.master, 
            width = 400,
            # border_width = 2,
        )
        self.note_frame.grid( 
            row = 0, 
            column = 7,
            columnspan = 2,
            rowspan = 2,
            sticky = 'nsew',
        )

# Remark
        self.remark_tab = ctk.CTkTabview(
            self.note_frame,
            width = 400,
            height = 500,
        )
        self.remark_tab.pack(
            fill = 'both' ,
            expand = True,
            side = 'top',
            padx = ( 0, 0  ),
            pady = ( 0, 0 )
        )

# # Tab choice
        self.remark_tab.add( 'Remarks' )

        self.remark_frame = ctk.CTkScrollableFrame(
            self.remark_tab.tab( 'Remarks' ),
            height = 750,
            width = 380,
        )
        self.remark_frame.grid(
            row = 0,
            column = 0,
            columnspan = 4,
            rowspan = 2,
            padx= ( 10, 0 ),
            pady = ( 10, 0 ),
            sticky = "nsew" 
        )

        self.remark_label = ctk.CTkLabel(
            self.remark_frame,
            text = "Docker Management: ",
            font = ( "Comic Sans MS", 30 ),
            # width = 800,
        )
        self.remark_label.grid(
            row = 0, 
            column = 0, 
            columnspan = 4,
            padx = ( 10, 0 ), 
            pady = ( 20, 0 ), 
            sticky = "nsew",
        )
        self.remark = ctk.CTkTextbox(
            self.remark_frame, 
            font = ( "Comic Sans MS", 25 ),
            width = 400,
            height = 700,
            fg_color = ["#C0C8CE", "#2B2D2F"],
        )
        self.remark.grid(
            row = 2,
            rowspan = 2,
            column = 0, 
            columnspan = 4,
            padx = ( 10, 0 ), 
            pady = ( 20, 0 ), 
            sticky = "nsew",
        )
        self.remark.insert( 
            "0.0",
            "Welcome to Docker Management Tool!\n\n"
        )


# Music Player Frame
        self.music_frame = ctk.CTkFrame( 
            self.master, 
            width = 800,
            height = 200,
            corner_radius = 0,
        )
        self.music_frame.grid( 
            row = 2,
            column = 6,
            columnspan = 4,
            rowspan = 2,
            sticky = 'nsew',
        )

        self.remark_label = ctk.CTkLabel(
            self.music_frame,
            text = "Music Player ",
            font = ( "Comic Sans MS", 25 ),
        )
        self.remark_label.grid(
            row = 0,
            column = 0, 
            columnspan = 2,
            padx = ( 0, 0 ), 
            pady = ( 20, 0 ), 
            sticky = "nsew",
        )

        self.music_menu = ctk.CTkOptionMenu( 
            self.music_frame,
            values = [  "The Beginning of The War", 
                        "All girl are the same",
                        "Hate me",
                        "21",
                        "When I grow up",
                        "Ruthless",
                        "Let You Down",
                        "Leave Me Alone",
                    ],
            width = 300,
            height = 50,
            dynamic_resizing = False,
            font = ctk.CTkFont( size=20,  ),
            anchor = "center"
        )


        self.music_menu.grid( 
            row = 1,
            column = 0,
            columnspan = 2,
            # sticky = "nsew",
            padx = ( 200, 0 ), 
            pady = ( 80, 0 ), 
        )
'''
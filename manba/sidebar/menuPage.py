import customtkinter as ctk
from PIL import Image, ImageTk
from mydocker.myDockerPage import MyDockerPage
from myansible.myAnsiblePage import MyAnsiblePage

class SwitchMenu( ctk.CTkFrame ) :
   def __init__( self, master ) :
      super().__init__( master )

# Variable Initiation
      self.menu_bg_color = ["#6E8BA4", "#4A5D6B"]
      self.selected_color = ["#5F7A8E", "#3A4A54"]
      self.icon_width = 50
      self.icon_height = 50
      self.btn_width = 30
      self.btn_height = 50
      self.label_width = 250
      self.label_height = 10
      self.font_style = ( "Comic Sans MS", 30 )
     
# Icon Location
      self.menu_icon = ctk.CTkImage( 
            light_image = Image.open( "images/resized_images/menu.png" ), 
            dark_image = Image.open( "images/resized_images/menu.png" ), 
            size=( self.icon_width, self.icon_height )
      )
      self.docker_icon = ctk.CTkImage( 
            light_image = Image.open( 'images/resized_images/docker.png' ),
            dark_image = Image.open( "images/resized_images/docker.png" ), 
            size=( self.icon_width, self.icon_height )
      )
      self.ansible_icon = ctk.CTkImage( 
            light_image = Image.open( 'images/resized_images/ansible.png' ),
            dark_image = Image.open( "images/resized_images/ansible.png" ), 
            size=( self.icon_width, self.icon_height )
      )
      self.close_icon = ctk.CTkImage( 
            light_image = Image.open( 'images/resized_images/close.png' ),
            dark_image = Image.open( "images/resized_images/close.png" ), 
            size=( self.icon_width , self.icon_height )
      )

# Menu frame
      self.menu_frame = ctk.CTkFrame( master, width = 150, fg_color = self.menu_bg_color, corner_radius = 0 )
      self.menu_frame.grid( row = 0, column = 1, rowspan = 4, sticky = 'nsew' )
      self.menu_frame.grid_columnconfigure( 0, weight = 0 )
      self.menu_frame.grid_columnconfigure( 1, weight = 10 )
      self.menu_frame.rowconfigure( 0, weight = 3 )

      # Button Frame
      self.button_frame = ctk.CTkFrame( 
            self.menu_frame, 
            fg_color = self.menu_bg_color, 
      )
      self.button_frame.grid( row = 0, column = 0, sticky = 'nsew' )

      # Buttons
      self.menu_btn = ctk.CTkButton( 
            self.button_frame, 
            image = self.menu_icon, 
            text='' , 
            width=self.btn_width,
            height = self.btn_height,
            # fg_color='transparent', 
            # hover_color = self.selected_color,
            corner_radius=0,
            command = self.extend_menu_bar
      )
      self.menu_btn.pack( side = 'top', expand = True, fill = 'both' )

      self.blank_btn_1 = ctk.CTkButton( 
            self.button_frame,
            text = '',
            fg_color = self.menu_bg_color, 
            hover_color = 'red',
            width = self.btn_width ,
            height = 160,
            state = "disabled",
      )
      self.blank_btn_1.pack( side = 'top', expand = True, fill = 'both' )

      self.docker_btn = ctk.CTkButton( 
            self.button_frame, 
            image = self.docker_icon,
            width = self.btn_width,
            height = self.btn_height,
            text='' ,
            # fg_color=self.selected_color,
            # hover_color = self.selected_color,
            corner_radius=0,
            # command = lambda : self.switch_page( indicator = self.docker_btn ) 
      )
      self.docker_btn.pack( side = 'top', expand = True, fill = 'both' )

      self.ansible_btn = ctk.CTkButton( 
            self.button_frame,
            image = self.ansible_icon,
            width = self.btn_width, 
            height = self.btn_height,
            text='' ,
            fg_color='transparent',
            # hover_color = self.selected_color,
            corner_radius=0,
            # command = lambda : self.switch_page( indicator = self.ansible_btn ) 
      )
      self.ansible_btn.pack( side = 'top', expand = True, fill = 'both' )
                  
      self.logging_btn = ctk.CTkButton( 
            self.button_frame, 
            # image = self.logging_icon, 
            width = self.btn_width, 
            height = self.btn_height,
            text='' , 
            fg_color='transparent', 
            # hover_color = self.selected_color,
            corner_radius = 0,
            state = "disabled"
            # command = lambda : self.switch_page( indicator = self.logging_btn) 
      )
      self.logging_btn.pack( side = 'top', expand = True, fill = 'both' )

      self.schedule_btn = ctk.CTkButton( 
            self.button_frame, 
            # image = self.schedule_icon, 
            width = self.btn_width, 
            height = self.btn_height, 
            text='' , 
            fg_color='transparent', 
            border_width = 0, 
            # hover_color = self.selected_color, 
            corner_radius=0,
            state = "disabled",
            # command = lambda : self.switch_page( indicator = self.schedule_btn) 
      )
      self.schedule_btn.pack( side = 'top', expand = True, fill = 'both' )

      self.github_btn = ctk.CTkButton( 
            self.button_frame, 
            # image = self.github_icon, 
            width = self.btn_width, 
            height = self.btn_height, 
            text='' , 
            fg_color='transparent', 
            border_width = 0, 
            # hover_color = self.selected_color, 
            corner_radius=0,
            state = "disabled",
            # command = lambda : self.switch_page( indicator = self.github_btn) 
      )
      self.github_btn.pack( side = 'top', expand = True, fill = 'both' )

      self.blank_btn_2 = ctk.CTkButton( 
            self.button_frame,
            text='' , 
            width = self.btn_width, 
            height = 180,
            fg_color='transparent', 
            state = 'disabled'
      )
      self.blank_btn_2.pack( side = 'top', expand = True, fill = 'both' )

      # Label Frame
      self.label_frame = ctk.CTkFrame( 
            self.menu_frame,
      )

      # Label 
      self.blk_label_1 = ctk.CTkButton( 
            self.label_frame, 
            text="", 
            height=20, 
            width=self.label_width,
            fg_color='transparent', 
            state = 'disabled',
            font = self.font_style,
      )
      self.blk_label_1.pack( side = 'top', expand = True, fill = 'both' )

      self.blk_label_2 = ctk.CTkButton( 
            self.label_frame, 
            text="", 
            height=151, 
            width=self.label_width,
            fg_color='transparent', 
            state = 'disabled',
            font = self.font_style,
      )
      self.blk_label_2.pack( side = 'top', expand = True, fill = 'both' )

      self.docker_label = ctk.CTkButton( 
            self.label_frame, 
            text = "Docker Page", 
            height = self.label_height, 
            width = self.label_width, 
            fg_color = 'transparent', 
            font = self.font_style,
            text_color = ["#2A2C2F", "#F2F7FC"],
            corner_radius = 0,
            # hover_color=self.selected_color,
            # command = lambda : self.switch_page( indicator = self.docker_btn )
      )
      self.docker_label.pack( side = 'top', expand = True, fill = 'both' )

      self.ansible_label = ctk.CTkButton( 
            self.label_frame, 
            text = "Ansible Page", 
            height = self.label_height, 
            width = self.label_width,
            fg_color = 'transparent', 
            font = self.font_style,
            corner_radius = 0,
            text_color = ["#2A2C2F", "#F2F7FC"],
            # hover_color=self.selected_color,
            # command = lambda : self.switch_page( indicator = self.ansible_btn )
      )
      self.ansible_label.pack( side = 'top', expand = True, fill = 'both' )

      self.logging_label = ctk.CTkButton( 
            self.label_frame, 
            # text="Logging Page", 
            text='',
            height = self.label_height, 
            width = self.label_width, 
            fg_color='transparent', 
            font = self.font_style,
            text_color = ["#2A2C2F", "#F2F7FC"],
            corner_radius = 0,
            # hover_color=self.selected_color,
            state = "disabled",
            # command= lambda : self.switch_page( indicator = self.logging_btn)
      )
      self.logging_label.pack( side = 'top', expand = True, fill = 'both' )

      self.schedule_label = ctk.CTkButton( 
            self.label_frame, 
            # text = "Schedule Page", 
            text='',
            height = self.label_height, 
            width = self.label_width,
            fg_color = 'transparent', 
            font = self.font_style,
            text_color = ["#2A2C2F", "#F2F7FC"],
            corner_radius = 0, 
            # hover_color=self.selected_color,
            state = "disabled",
            # command= lambda : self.switch_page( indicator = self.schedule_btn)
      )
      self.schedule_label.pack( side = 'top', expand = True, fill = 'both' )

      self.github_label = ctk.CTkButton( 
            self.label_frame, 
            # text = "Github Page", 
            text='',
            height = self.label_height, 
            width = self.label_width,
            fg_color = 'transparent', 
            font = self.font_style ,
            text_color = ["#2A2C2F", "#F2F7FC"],
            corner_radius = 0, 
            # hover_color=self.selected_color,
            state = "disabled",
            # command= lambda : self.switch_page( indicator = self.github_btn)
      )
      self.github_label.pack( side = 'top', expand = True,fill = 'both' )

      self.blk_label_3 = ctk.CTkButton( 
            self.label_frame, 
            text="", 
            height = 214,
            width = self.label_width,
            state = 'disabled',
            fg_color='transparent',
      )
      self.blk_label_3.pack( side = 'top', expand = True, fill = 'both' )

   def extending_animation( self ) :
      self.label_frame.grid( row = 0, column = 1, sticky = 'nsew' )
   
   def extend_menu_bar( self ) :
      self.extending_animation()
      self.menu_btn.configure( image = self.close_icon )
      self.menu_btn.configure( command = self.fold_menu_bar )

   def folding_animation( self ) :
      self.label_frame.grid_forget()
   
   def fold_menu_bar( self ) :
      self.folding_animation()
      self.menu_btn.configure( image = self.menu_icon )
      self.menu_btn.configure( command = self.extend_menu_bar )
   

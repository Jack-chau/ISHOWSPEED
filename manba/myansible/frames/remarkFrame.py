import customtkinter as ctk
import textwrap


# Remark content
_ansible_content = textwrap.dedent(f"""
        Welcome to Docker Management Tool!\n
          ◕‿◕ Ansible Page ◕‿◕\n
        ━━━━━━━━━━━━━━━━━━━━━━━━
            • Multi-container Control\n
            • Setup Ansible\n
            • Run Tasks\n
            Ready to manage your Docker!
    """)

class RemarkManager :
    def __init__( self, tab_frame, remark_frame ) :
        self.remark_frame = remark_frame
        self.tab_frame = tab_frame
        self.tab_frame.configure( command = self.on_tab_changed )
        self.setup_ui( )

    def setup_ui( self ) :
# Create remark frame
        self.remark_iner_frame = ctk.CTkFrame( 
            self.remark_frame,
            width = 400,
            # border_width = 2,
        )

        self.remark_iner_frame.grid( 
            row = 0, 
            column = 7,
            columnspan = 2,
            rowspan = 2,
            sticky = 'nsew',
        )

# Remark
        self.remark_tab = ctk.CTkTabview(
            self.remark_iner_frame,
            width = 400,
            height = 500,
        )
        self.remark_tab.pack(
            fill = 'both' ,
            expand = True,
            side = 'top',
            padx = ( 0, 0 ),
            pady = ( 0, 0 )
        )

        self.remark_tab.add( 'Remarks' )
        
        self.remark_scroll_frame = ctk.CTkScrollableFrame(
            self.remark_tab.tab( 'Remarks' ),
            height = 750,
            width = 380,
        )
        self.remark_scroll_frame.grid(
            row = 0,
            column = 0,
            columnspan = 4,
            rowspan = 2,
            padx= ( 10, 0 ),
            pady = ( 10, 0 ),
            sticky = "nsew" 
        )

        self.remark_label = ctk.CTkLabel(
            self.remark_scroll_frame,
            text = "Docker Management: ",
            font = ( "Comic Sans MS", 30 ),
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
            self.remark_scroll_frame, 
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
                _ansible_content
        )        

    def on_tab_changed( self ) :

        self.current_tab_name = self.tab_frame.get()

        self.remark.delete("0.0", "end")

        if self.current_tab_name == "Ansible" :
            self.remark.insert( 
                "0.0",
                _ansible_content
        )


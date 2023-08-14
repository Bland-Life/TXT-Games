from tkinter import *
from tkinter import font

class AppManager():

    MAIN_BG_COLOR = "#1F1F1F"
    MAIN_FG_COLOR = "#FFF"

    apps = {}

    @classmethod
    def __init__(self, root: Tk) -> None:
        self.root = root
        self.root.title("TXT Games")
        self.root.config(bg="red")
        
        # CONTAINS CONTENT
        self.container = Frame(self.root, bg=self.MAIN_BG_COLOR)
        self.container.grid(column=0, row=0)

        # ALLOWS FOR CONTAINER FRAME TO FILL WINDOW WHILE KEEPING CONTENT RESPONSIVE
        self.empty = Frame(self.container, bg="green")
        self.empty.grid(sticky=NSEW)
        self.empty.grid_propagate(False)
        self.empty.lower()
        self.load_widgets()

        self.root.bind("<Configure>", self.fill_window)

    @classmethod
    def fill_window(self, event):
        """
        Maintains the size of the 'empty' frame within the container equal to 
        the window size while not disturbing the placement of the other widgets.

        Conversely, it will also shrink the window size to the 'empty' frame size
        when widgets are changed, useful for when loading separate apps' widgets.
        """
        print(event.widget.winfo_name())
        if event.widget.winfo_name() in self.empty.__str__():
            self.root.geometry(f"{self.empty.winfo_width()}x{self.empty.winfo_height()}")

        if event.widget.winfo_name() == 'tk':
            grid_size = self.container.grid_size()
            columns = grid_size[0]
            rows = grid_size[1]
            self.empty.config(width=event.width, height=event.height)
            self.empty.grid_configure(columnspan=columns, rowspan=rows)
        

    @classmethod
    def start_application(self, app):
        self.clear_frame(self.container)
        self.root.geometry("0x0")
        app(self)

    @classmethod
    def load_widgets(self):
        heading = Label(self.container, text="Welcome to TXT Games!", font=("Courier", 24, font.BOLD))
        heading.grid(row=0, column=0, sticky=NSEW, ipady=20)

        desc_text = "Please select a game to play using one of the links below."
        description = Label(self.container, text=desc_text, font=("Courier", 14), wraplength=300)
        description.grid(row=1, column=0, sticky=NSEW)

        self.app_container = Frame(self.container, bg=self.MAIN_BG_COLOR, padx=100, pady=50)
        self.app_container.grid(row=2, column=0, sticky=NSEW)
        self.app_container.grid_columnconfigure(0, weight=1)
        self.app_container.grid_rowconfigure(0, weight=1)

    @classmethod
    def clear_frame(self, frame: Frame):
        for child in frame.winfo_children():
            if child == self.empty:
                continue
            if type(child) == Frame:
                self.clear_frame(child)
            child.grid_forget()
            child.destroy()
    
    @classmethod
    def add_application(self, text, app):
        btn = Button(
            master=self.app_container, 
            text=text, 
            command=lambda: self.start_application(app), 
            font=("Courier", 18, "italic underline"), 
            bg=self.MAIN_BG_COLOR, 
            fg=self.MAIN_FG_COLOR, 
            activebackground=self.MAIN_BG_COLOR, 
            activeforeground=self.MAIN_FG_COLOR, 
            border=0
        )
        btn.grid(sticky=EW, pady=20)
        self.apps[text] = app

    @classmethod
    def load_apps(self):
        for (app_name, app) in self.apps.items():
            self.add_application(text=app_name, app=app)
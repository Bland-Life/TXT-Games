from tkinter import *
from tkinter import font
from manager import AppManager
import logic

class TextAdventure():

    WINDOW_BACKGROUND = "#24242A"
    TEXT_COLOR = "#F9E6A9"

    @classmethod
    def __init__(self, manager: AppManager) -> None:
        self.root = manager.root
        self.container = manager.container
        self.empty = manager.empty
        self.manager = manager

        self.load_widgets()
        

    @classmethod
    def load_widgets(self):
        defaultFont = font.nametofont("TkDefaultFont")
        defaultFont.configure(family="High Tower Text", size=12)

        game_frame = Frame(self.container, bg="#64463F")
        game_frame.grid(row=0, column=0, sticky=NSEW)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        scrollbar = Scrollbar(self.container, bg=self.WINDOW_BACKGROUND)
        scrollbar.grid(row=0, column=1, rowspan=2, sticky="NSE")

        text_field = Text(game_frame, yscrollcommand=scrollbar.set, wrap=WORD)
        text_field.config(bg="#64463F", fg=self.TEXT_COLOR, font=("High Tower Text", 14, "bold"), border=0)
        text_field.insert(END, "Press ENTER to start!")
        text_field.config(state=DISABLED)
        text_field.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)
        scrollbar.config(command=text_field.yview)

        with open("story.txt", mode="r") as story:
            story_text = story.readlines()

        input_frame = Frame(self.container, bg=self.WINDOW_BACKGROUND)
        input_frame.grid(row=1, column=0, sticky="SEW")

        input_label = Label(input_frame, text="Type Here: ")
        input_label.config(bg=self.WINDOW_BACKGROUND, fg=self.TEXT_COLOR)
        input_label.grid(row=0, column=0, padx=10)


        # SETUP ENTRY FIELD FOR USER INPUT
        def callback(var):
            content = var.get()


        var = StringVar()
        var.trace("w", lambda name, index,mode, var=var: callback(var))
        input_field = Entry(input_frame, textvariable=var, state=DISABLED, bg="#41414D", fg=self.TEXT_COLOR, disabledbackground=self.WINDOW_BACKGROUND)
        input_field.grid(row=0, column=1, sticky=NSEW)
        input_frame.columnconfigure(1, weight=1)

        exit_btn = Button(input_frame, text="Exit", command=self.load_manager)
        exit_btn.grid(row=0, column=2, sticky=EW)

        # START GAME
        self.root.bind("<Return>", lambda event: logic.start_game(text_field, input_field))

    @classmethod
    def load_manager(self):
        self.manager.clear_frame(self.container)
        self.manager.load_widgets()
        self.manager.load_apps()
        self.root.geometry("0x0")
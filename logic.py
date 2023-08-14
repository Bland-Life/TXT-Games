from tkinter import *
import time
TEXT_SPEED = 20


def edit_field(func):
    def wrapper(**kwargs):
        if "field" in kwargs:
            kwargs["field"].config(state=NORMAL)
            func(**kwargs)
            kwargs["field"].config(state=DISABLED)
    return wrapper


@edit_field
def clear_field(field: Text):
    field.delete("1.0", END)


@edit_field
def write_field(field: Text, new_text):
    field.insert(END, new_text)


def listen_to_entry(entry: Entry, options: list) -> str:
    """Listens to and waits for changes to the Tkinter Entry Field, will return the choice once the input in the 
    entry field matches with one of the options provided."""
    entry.config(state=NORMAL)
    entry.focus()
    while entry.get().upper() not in options:
        entry.wait_variable(entry.cget("textvariable"))

    choice = entry.get().upper()
    entry.delete(0, END)
    entry.config(state=DISABLED)
    return choice


def start_game(text_field: Text, entry: Entry):

    # OPEN TEXT FILE WITH STORY
    with open("story.txt", mode="r", encoding='UTF8') as text:
        story = text.readlines()

    clear_field(field=text_field)

    # WRITE STORY TEXT
    options = False
    ignore = False
    current_choice = None
    skip = 0
    for i, line in enumerate(story):

        # THE NEXT LINE AFTER THIS IS TRUE SHOULD BE OUR OPTIONS
        if line.strip() == "[CHOOSE]":
            options = True
            continue

        # IF OPTIONS POP UP WHILE IGNORING TEXT, IF THOSE OPTIONS MATCH THE BLOCK WE'RE GOING TO THEN SKIP THOSE BLOCKS
        if options:
            option_list = [option.strip() for option in line.split(", ")]
            if ignore:
                print("True")
                if current_choice in option_list:
                    skip += 1
                print(skip)
                options = False
                continue  
            current_choice = listen_to_entry(entry, option_list)
            ignore = True
            options = False
            continue

        # IGNORES LINES UNTIL WE REACH THE BLOCK FOR THE CHOSEN OPTION, SKIP OVER SIMILAR OPTIONS
        if ignore:
            if line.strip() == f"|{current_choice}" and skip <= 0:
                ignore = False
                write_field(field=text_field, new_text="\n")
                continue
            elif line.strip() == f"|{current_choice}" and skip > 0:
                skip -= 1
                continue
            else:
                continue

        # A MINUS - SYMBOL SIGNIFIES THE END OF OUR GAME
        if line.strip() == "-":
            write_field(field=text_field, new_text="\nGAME END!")
            text_field.see(END)
            break

        # ADDS CHARACTERS ONE AT A TIME TO OUR TEXT FIELD
        for char in line:
            write_field(field=text_field, new_text=char)
            text_field.see(END)
            text_field.after(TEXT_SPEED)
            text_field.update()
    
import tkinter as tk
from PIL import ImageTk, Image
from character_generator import *

# Colors
clr_bg = "#fffaf0"
clr_btn_light = "#dbbb96"
clr_btn_dark = "#a07962"
clr_txt = "#43364a"


def clear_widgets(frame):
    '''
    This function clears all widgets from the parent frame
    '''
    for widget in frame.winfo_children():
        widget.destroy()


def main():

    # Initialize app
    root = tk.Tk()
    root.resizable(False, False)
    root.title("Character generator")
    root.eval("tk::PlaceWindow . center")

    # Create and load main frame 
    landing_frame = tk.Frame(root, width=800, height=400, bg=clr_bg)
    landing_frame.grid(row=0, column=0, columnspan=3, sticky='nesw')

    landing_frame.tkraise()
    landing_frame.pack_propagate(False)

    # Main frame widgets
    ## Title
    tk.Label(
        landing_frame,
        text="Roll your \nD&D character",
        bg=clr_bg,
        fg=clr_txt,
        font=("TkHeadingFont",24, "bold")
        ).pack(pady=50)

    ## Instructions
    tk.Label(
        landing_frame,
        text="Generate a level 1 player character for your next D&D 5th edition campaign.",
        bg=clr_bg,
        fg=clr_txt,
        font=("TkMenuFont",12)
    ).pack(pady=20)

    ## Button
    tk.Button(
        landing_frame,
        text="Roll character",
        bg=clr_btn_dark,
        fg=clr_btn_light,
        font=("TkHeadingFont", 16, "bold"),
        cursor="hand2",
        activebackground=clr_btn_light,
        activeforeground=clr_btn_dark,
        height=1, 
        width=18,
        command=lambda:load_character(root, landing_frame)
        ).pack(pady=20)

    root.mainloop()

    return root, landing_frame


def load_character(root, landing_frame):
    '''
    This function creates a random character and loads a selection of attributes and information to the character frame
    User is allowed to either roll a new character, or save the currently displayed character to a text file.
    '''

    # Character frames
    char_frame = tk.Frame(root, width=800, height=400, bg=clr_bg)
    char_frame.grid(row=0, column=0, columnspan=3, rowspan=6, sticky='nesw')

    # Clear all widgets
    clear_widgets(landing_frame)
    clear_widgets(char_frame)
    char_frame.tkraise()

    
    # Roll character
    my_character = generate_character("roll")

    # Character frame widgets

    ## Title
    tk.Label(
        char_frame,
        text="You rolled a...",
        bg=clr_bg,
        fg=clr_txt,
        font=("TkHeadingFont",24, "bold"),
        justify="center"
        ).grid(row=0, column=0, columnspan=3, pady=15)

    ## Character description
    tk.Label(
        char_frame,
        text=my_character.__str__(),
        bg=clr_bg,
        fg=clr_txt,
        font=("TkHeadingFont",16),
        justify="center",
        ).grid(row=1, column=0, columnspan=3, pady=15)

    ## Character image
    avatar=my_character.avatar
    avatar_resize=avatar.resize((400, 400))
    tk_img=ImageTk.PhotoImage(avatar_resize)
    img = tk.Label(char_frame, image=tk_img, bg=clr_bg)
    img.image = tk_img
    img.grid(row=2, rowspan=4, column=0, padx=5)

    ## Character ability scores
    tk.Label(
        char_frame,
        text=my_character.attribute_dict['Ability scores'],
        bg=clr_bg,
        fg=clr_txt,
        font=("TkMenuFont",19),
        justify='center',
        ).grid(row=2, rowspan=3, column=1, pady=5)

    ## Character skills
    for k,v in my_character.attribute_dict.items():
        if k == "Skills":
            tk.Label(
                char_frame,
                text=k + ': ' + v,
                bg=clr_bg,
                fg=clr_txt,
                font=("TkMenuFont",12),
                justify='left',
                wraplength=320
                ).grid(row=2, column=2, padx=20, pady=0, sticky='sw')

    ## Character prodiciencies
    for k,v in my_character.attribute_dict.items():
        if k == "Proficiencies":
            tk.Label(
                char_frame,
                text=k + ': ' + v,
                bg=clr_bg,
                fg=clr_txt,
                font=("TkMenuFont",12),
                justify='left',
                wraplength=320
                ).grid(row=3, column=2, padx=20, pady=0, sticky='w')

    ## Character deity
    for k,v in my_character.attribute_dict.items():
        if k == "Deity":
            tk.Label(
                char_frame,
                text=k + ': ' + v,
                bg=clr_bg,
                fg=clr_txt,
                font=("TkMenuFont",12),
                justify='left',
                wraplength=320
                ).grid(row=4, column=2, padx=20, pady=0, sticky='nw')

    ## Roll again button
    tk.Button(
        char_frame,
        text="Roll again",
        bg=clr_btn_dark,
        fg=clr_btn_light,
        font=("TkHeadingFont", 16, "bold"),
        cursor="hand2",
        activebackground=clr_btn_light,
        activeforeground=clr_btn_dark,
        height=1, 
        width=18,
        command=lambda:load_character(root, landing_frame)
        ).grid(row=5, column=1, pady=15,  padx=5)

    ## Save character button
    tk.Button(
        char_frame,
        text="Save character",
        bg=clr_btn_dark,
        fg=clr_btn_light,
        font=("TkHeadingFont", 16, "bold"),
        cursor="hand2",
        activebackground=clr_btn_light,
        activeforeground=clr_btn_dark,
        height=1, 
        width=18,
        command=lambda:write_character(my_character)
        ).grid(row=5, column=2, pady=15, padx=5)


# Run the app
if __name__ == '__main__':
    root, landing_frame = main()
    
#import libraries
from tkinter import *
import tkinter.font as tkFont
import tkinter.ttk as ttk
from random import *

# Method converts normal RGB values to something tkinter understands
def rgbTk(rgb):
    return "#%02x%02x%02x" % rgb


# Method to create label based on pixel size and not text size
# For better formatting
def create_label(master, x, y, w, h, txt):
    f = Frame(master, height=h, width=w)
    f.pack_propagate(0)
    f.place(x=x, y=y)
    label = Label(f, text=txt)
    label.pack(fill=BOTH, expand=1)
    return label


# Method to create all labels
def createLabels():

    # title label
    titleLabel = create_label(titleFrame, 15, 0, 800, 80, "Password Generator")
    titleLabel.config(bg=BLACK, fg=WHITE, font=BOLD_TIMES_28)

    # password length label
    sizeOptionLabel = create_label(
        settingsFrame, 50, 10, 250, 40, "Password Length: ")
    sizeOptionLabel.config(bg=BLACK, fg=WHITE, font=HEL_16)

    # create all labels for each checkbox
    settingsLabel = []
    for i in range(0, 5):
        settingsLabel.append(create_label(
            settingsFrame, 83, 87+70*i, 300, 40, checkBoxLabelText[i]))
        settingsLabel[i].config(bg=BLACK, fg=WHITE, font=HEL_16, anchor="w")


# Method creates a combobox
def createComboBox():

    # generate all the available size options for the password
    sizeOptions = generateSizeList()

    # set the default value to 5, also the smallest password length
    passLen.set(5)

    # create the combobox, readonly to prevent any alterations from user
    sizeOptionMenu = ttk.Combobox(
        settingsFrame, width=20, textvariable=passLen, state="readonly", font=HEL_14)

    # removes blue background highlighting after selecting a length
    sizeOptionMenu.bind("<<ComboboxSelected>>",
                        lambda e: settingsFrame.focus())

    # add all the possible options to the combobox
    sizeOptionMenu["values"] = sizeOptions

    # place the combobox
    sizeOptionMenu.place(x=300, y=15)


# method to generate available size options for the password
def generateSizeList():

    options = []

    # password length can be from 5 to 200
    for i in range(5, 201):
        options.append(i)

    # returns all the possible options
    return options


# method to create all the check boxes
def createCheckBoxes():

    # list to store the check boxes
    checkBoxes = []

    for i in range(0, 5):
        # initialize each element in the checkBoxVar list as a tkinter integer variable
        checkBoxVar[i] = IntVar()

        # checks every checkbox by default, unchecks the last checkbox
        if not i == 4:
            checkBoxVar[i].set(1)

        # create, configure and place each checkbox
        checkBoxes.append(Checkbutton(
            settingsFrame, text=checkBoxText[i], variable=checkBoxVar[i], onvalue=1, offvalue=0))
        checkBoxes[i].configure(font=HEL_14, bg=BLACK, activebackground=BLACK,
                                fg=WHITE, selectcolor=TEAL, width=20, height=1, anchor="w")
        checkBoxes[i].place(x=425, y=90+70*i)


# method to create all the buttons
def createButtons():

    # generate password button
    generateButton = Button(generationFrame, width=20, height=2, text="GENERATE PASSWORD",
                            bg=LIGHT_GREY, command=generatePassword)

    # copy password to clipboard button
    copyButton = Button(generationFrame, width=10, height=2,
                        text="COPY", bg=LIGHT_GREY, command=copyClipboard)

    # place buttons
    generateButton.place(x=85, y=10)
    copyButton.place(x=250, y=10)


# generate password using simple rng algorithm
def generatePassword():

    # create temp variables
    global password
    password = ""
    passwordBank = ""

    # loop through to check which checkboxes the user selected
    # to determine which characters to use in the generation
    for i in range(0, 5):
        if checkBoxVar[i].get() == 1:
            passwordBank += passwordCharacters[i]

    # generates the password
    for i in range(0, passLen.get()):
        password += choice(passwordBank)

    # clears previous generation
    passwordTextBox.configure(state=NORMAL)
    passwordTextBox.delete("1.0", "end")

    # Make the password appear in the textbox, prevents user from altering the textbox content
    passwordTextBox.insert(END, password)
    passwordTextBox.configure(state=DISABLED)


# method used to copy the password onto the clipboard of the user
def copyClipboard():
    window.clipboard_clear()            #clears previous clipboard copy
    window.clipboard_append(password)
    window.update()


# method creates the textbox
def createTextBox():

    # makes the textbox global for other methods to access
    global passwordTextBox

    # create textbox
    passwordTextBox = Text(generationFrame, width=70, height=2,
                           fg=BLACK, bg=WHITE, spacing3=10)

    # textbox default starting message
    passwordTextBox.insert(END, "Your Generated Password Will Appear Here")

    #prevents user alterations
    passwordTextBox.configure(state=DISABLED)

    #place the textbox
    passwordTextBox.place(x=85, y=70)


# Colour constants - RGB Values
BLACK = rgbTk((33, 33, 33))
TEAL = rgbTk((55, 164, 184))
WHITE = rgbTk((255, 255, 245))
LIGHT_GREY = rgbTk((174, 176, 175))
TEST = rgbTk((200, 10, 0))

# create and configure tkinter window
window = Tk()
window.title("Password Generator - Jack Song")
window.geometry("+376+60")  # centers the window on a 1920x1080 display
window.minsize(width=800, height=650)
window.configure(bg=BLACK)

# Normal and Tkinter Variables
passLen = IntVar()
password = ""
text = StringVar()

checkBoxVar = [0]*5  # store checkboxes value
checkBoxText = ["(ABCDEFGHIJK...)",  # text to display beside each checkbox
                "(abcdefghijk...)",
                "(1234567890)",
                "(!@#()$%^&*)",
                "(,.<>/?;:[]...)"]

checkBoxLabelText = ["Include Uppercase Letters: ",  # labels for each checkbox
                     "Include Lowercase Letters: ",
                     "Include Numerical characters: ",
                     "Include Symbols: ",
                     "Include Ambiguous Characters: ", ]

passwordCharacters = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ",  # characters avaiable to use for each setting
                      "abcdefghijklmnopqrstuvwxyz",
                      "1234567890",
                      "!@#$%^&*()",
                      ",./;'[]\\-=<>?:\"{|}_+"]

# Font Constants
BOLD_TIMES_28 = tkFont.Font(family="Times", size=28, weight="bold")
HEL_16 = tkFont.Font(family="Helvetica", size=16)
HEL_14 = tkFont.Font(family="Helvetica", size=14)

# create and configure frames
titleFrame = Frame(window, width=800, height=80, bg=BLACK)
settingsFrame = Frame(window, width=800, height=420, bg=BLACK)
generationFrame = Frame(window, width=800, height=150, bg=BLACK)

# place the frames
titleFrame.place(x=0, y=0)
settingsFrame.place(x=0, y=80)
generationFrame.place(x=0, y=500)

# call methods to create tkinter elements
createLabels()
createCheckBoxes()
createComboBox()
createButtons()
createTextBox()

# window mainloop
window.mainloop()

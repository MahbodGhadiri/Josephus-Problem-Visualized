from tkinter import messagebox

def showInvalidInputDialog(input):
    messagebox.showerror('Input Error', f'Error: {input} is not a valid integer')

def showInputTooLargeDialog(input):
    messagebox.showerror('Input Error', f'Error: {input} is too large!')

def showInputTooSmallDialog(input):
    messagebox.showerror('Input Error', f'Error: "{input}" is too small!')
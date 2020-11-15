import tkinter as tk
from tkinter import simpledialog

def popup(head, prompt):        
    ROOT = tk.Tk()
    ROOT.withdraw()
    USER_INP = simpledialog.askstring(title=head, prompt=prompt)
    return USER_INP

def passpopup(head, prompt):        
    ROOT = tk.Tk()
    ROOT.withdraw()
    USER_INP = simpledialog.askstring(title=head, prompt=prompt, show='*')
    return USER_INP

# def choice(head, prompt):
#     ROOT =tk.TK()
#     ROOT.withdraw()
#     USER_INP = simpledialog.


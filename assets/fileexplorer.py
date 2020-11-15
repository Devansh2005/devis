from tkinter import Tk     
from tkinter.filedialog import askopenfilename
# import filetype


def fileExplorer():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    file_path= askopenfilename() # show an "Open" dialog box and return the path to the selected file
    return file_path

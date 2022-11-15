""" broken off Windows 11's file manager app."""
import tkinter
from tkinter import ttk
import os
def FTRConfigSettings(path, data=None) -> tuple:
    if os.access(path, os.F_OK):
        with open(path) as read_config:
            config = read_config.read().splitlines()
    else:
        with open(path, "w") as FTR_write_config: #FirstTimeRun_Write_config, full form.
            FTR_write_config.write(data)
    return config
THEME_WINDOW_BG, THEME_FOREGROUND = FTRConfigSettings("theme_config.txt", f"Black\nWhite")
filepath = None
def lookUpFiles(path, ):
    global filepath
    print()
    addressBar.delete(0, tkinter.END)
    filepath = path
    addressBar.insert(tkinter.END, path)
    filesInFolder = os.listdir(path)
    for i in fileView.get_children():
        fileView.delete(i)
    for file in range(len(filesInFolder)):
        fileView.configure(style="Treeview")
        fileView.insert(parent='', iid=file, text='', index='end', values=[filesInFolder[file]],)
def openFileOrFolder(*event):
    global filepath
    SFI = fileView.selection()
    selectedFileIndex = fileView.focus()
    selectedFile = fileView.item(selectedFileIndex, 'values')[0]
    print(selectedFile, SFI, SFI[0])
    if os.path.isdir(f"{os.path.join(filepath, selectedFile)}"):
        filepath = os.path.join(filepath, selectedFile)
        lookUpFiles(filepath)
    else:
        os.startfile(f"{filepath}/{selectedFile}")

def goBackFolder(path: str):  
    if "\\" in path:
        path = path.replace("\\", "/")
        print(path)
    folderSplit = path.split("/")
    if folderSplit[-1] == '':
        folderSplit.pop(-1)
    folderSplit.pop(-1)
    print(folderSplit)
    path = str().join(f"{folder}/" for folder in folderSplit)
    print(path)
    addressBar.delete(0, tkinter.END)
    addressBar.insert(tkinter.END, path)
    lookUpFiles(path=path)
def createFolder():
    global addressBar, folderName
    """ create a folder in the active directory"""
    newFolderPath = os.path.join(addressBar.get(), folderName.get())
    os.mkdir(newFolderPath)
    lookUpFiles(newFolderPath)
fileManagerWindow = tkinter.Tk()
fileManagerWindow.configure(background=THEME_WINDOW_BG)
fileManagerWindow.title("File Manager")
ttk.Style(fileManagerWindow).configure("Treeview", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND)
mainFrame = tkinter.Frame(fileManagerWindow, background=THEME_WINDOW_BG)
mainFrame.grid(row=0, column=0)
addressBar = tkinter.Entry(mainFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, width=100)
addressBar.insert(tkinter.END, os.getcwd())
goButton = tkinter.Button(mainFrame, text="Go!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                        command=lambda: lookUpFiles(addressBar.get()))
goButton.grid(row=0, column=1, sticky="nw")
goBackButton = tkinter.Button(mainFrame, text="Go back!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                            command=lambda: goBackFolder(path=addressBar.get()))
goBackButton.grid(row=0, column=2, sticky="nw", padx=2)
addressBar.grid(row=0, column=0, sticky="n")
folderName = tkinter.Entry(mainFrame, background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND, width=50)
folderName.grid(row=1, column=0)
newFolder = tkinter.Button(mainFrame, text="New Folder!", background=THEME_WINDOW_BG, foreground=THEME_FOREGROUND,
                            command=createFolder)
newFolder.grid(row=1, column=1)
# driveSelection = ttk.Treeview(mainFrame, style="Treeview")
# driveSelection.grid(row=0, column=0, sticky="w")
# driveSelection['column'] = "Drives"
# driveSelection.column("#0", anchor=tkinter.W, width=0, stretch=tkinter.NO)
# driveSelection.column("Drives", anchor=tkinter.W, width=100)
# driveSelection.heading("Drives", text="Drives", anchor=tkinter.CENTER)
fileView = ttk.Treeview(mainFrame, style="Treeview")
fileView.grid(row=2, column=0, sticky="w")
fileView['column'] = "Files"
fileView.column("#0", anchor=tkinter.W, width=0, stretch=tkinter.NO)
fileView.column("Files", anchor=tkinter.W, width=600)
fileView.heading("Files", text="Files", anchor=tkinter.CENTER)
fileView.bind("<<TreeviewSelect>>", openFileOrFolder)
fileView.configure(style="Treeview")
fileManagerWindow.mainloop()
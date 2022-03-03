import os
import tkinter as tk
from tkinter import filedialog
from tkinter import font
from math import floor, log10


def openDir():
    dirName = filedialog.askdirectory(title='Choose the directory')
    dirVariable.set(dirName)


def changeConfigReplace():
    if replaceState.get():
        findEntry.config(state='normal')
        replaceEntry.config(state='normal')
    else:
        findEntry.config(state='disabled')
        replaceEntry.config(state='disabled')


def changeConfigOrder():
    if orderState.get():
        prefixRadio1.config(state='normal')
        prefixRadio2.config(state= 'normal')
        prefixRadio3.config(state= 'normal')
        upBtn['state'] = tk.NORMAL
        dwBtn['state'] = tk.NORMAL
    else:
        prefixRadio1.config(state='disabled')
        prefixRadio2.config(state='disabled')
        prefixRadio3.config(state='disabled')
        upBtn['state'] = tk.DISABLED
        dwBtn['state'] = tk.DISABLED


def getFileNamesDict():
    fileNamesList = list(listBoxRead.get(0, tk.END))
    fileNamesDict = {idx:fileName for idx, fileName in enumerate(fileNamesList)}
    return fileNamesDict


def cleanPrefix(aList):
    bList = []
    for fileName in aList:
        fileNameSeparated = fileName.partition('_')
        if fileNameSeparated[0].isdigit():
            fileName = fileNameSeparated[-1]
    
        fileNameSeparated = fileName.partition('-')
        if fileNameSeparated[0].isdigit():
            fileName = fileNameSeparated[-1]
    
        fileNameSeparated = fileName.partition(' ')
        if fileNameSeparated[0].isdigit():
            fileName = fileNameSeparated[-1]
    
        bList.append(fileName)
    return bList


def refreshListBox(listBox, nameList):
    listBox.delete(0, tk.END)
    for idx, name in enumerate(nameList):
        listBox.insert(idx, name)


def reviseFileList(fileNamesDict):
    keys = list(fileNamesDict.keys())
    keys.sort()

    nameList = [fileNamesDict[key] for key in keys]
    refreshListBox(listBoxRead, nameList)


def switchKey(aDict, keyOri, keyTgt):
    tmp = aDict[keyOri]
    aDict[keyOri] = aDict[keyTgt]
    aDict[keyTgt] = tmp


def readFileNames():
    tgtdirName = dirVariable.get()
    dirNames = os.listdir(tgtdirName)

    if applyValue.get() == 1:
        nameList = [dirName for dirName in dirNames if os.path.isfile(os.path.join(tgtdirName, dirName))]
    else:
        nameList = [dirName for dirName in dirNames if not os.path.isfile(os.path.join(tgtdirName, dirName))]

    refreshListBox(listBoxRead, nameList)


def moveFileName(inc):
    moved = False
    fileNamesDict = getFileNamesDict()

    if inc < 0:
        idLast = 0
    else:
        idLast = len(fileNamesDict) - 1

    idsSel = list(listBoxRead.curselection())
    for id_ in idsSel:
        if abs(id_ - idLast) > 0:
            idNext = id_ + inc
            switchKey(fileNamesDict, id_, idNext)
            moved = True

    if moved:
        reviseFileList(fileNamesDict)
        listBoxRead.select_set(idNext)


def replaceFileNames(fileNamesDict):
    if replaceState.get():
        findStr = findEntry.get()
        replaceStr = replaceEntry.get()
        fileNamesReplaced = [fileNamesDict[key].replace(findStr, replaceStr) for key in fileNamesDict.keys()]
    else:
        fileNamesReplaced = [fileNamesDict[key] for key in fileNamesDict.keys()]
    return fileNamesReplaced


def reorderFileNames(fileNamesReplaced):
    if orderState.get():
        fileNamesReplaced = cleanPrefix(fileNamesReplaced)

        if radioValue.get() == 1:
            sep = '_'
        elif radioValue.get() == 2:
            sep = '-'
        elif radioValue.get() == 3:
            sep = ' '

        fileNum = len(fileNamesReplaced)
        decimal = floor(log10(fileNum)) + 1
        fileNamesOrdered = ['{idx:{fill}{width}}{sep}{fileName}'.format(idx=idx, fill='0', width=decimal, sep=sep, fileName=fileName) for idx, fileName in enumerate(fileNamesReplaced)]
    else:
        fileNamesOrdered = fileNamesReplaced
    return fileNamesOrdered


def checkRepeatedItems(listBox, nameList):
    global nameRepeated
    nameRepeated = False

    for idx1, name1 in enumerate(nameList):
        for idx2, name2 in enumerate(nameList[idx1+1:]):
            if name2 == name1:
                nameRepeated = True
                listBox.itemconfig(idx1, {'bg':'red'})
                listBox.itemconfig(idx1+idx2+1, {'bg':'red'})


def previewFileNames():
    fileNamesDict = getFileNamesDict()
    fileNamesReplaced = replaceFileNames(fileNamesDict)
    fileNamesOrdered = reorderFileNames(fileNamesReplaced)

    refreshListBox(listBoxPreview, fileNamesOrdered)
    checkRepeatedItems(listBoxPreview, fileNamesOrdered)


def renameFiles():
    tgtdirName = dirVariable.get()
    fileNameListSrc = list(listBoxRead.get(0, tk.END))
    fileNameListDst = list(listBoxPreview.get(0, tk.END))

    try:
        if nameRepeated:
            raise Exception('There are repeated file names after renaming.')
        else:
            for fileNameSrc, fileNameDst in zip(fileNameListSrc, fileNameListDst):
                fileDirSrc = os.path.join(tgtdirName, fileNameSrc)
                fileDirDst = os.path.join(tgtdirName, fileNameDst)
                os.rename(src=fileDirSrc, dst=fileDirDst)
    except Exception as e:
        tk.messagebox.showerror("Error", e.args[0])
        listBoxPreview.delete(0, tk.END)
    else:
        tk.messagebox.showinfo("Message", "All files have been renamed successfully.")
        listBoxRead.delete(0, tk.END)
        listBoxPreview.delete(0, tk.END)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('QuickRename')
    root.resizable(width=0, height=0)
    root.configure()

    labelFont = font.Font(family='Helvetica', size=10)
    btnFont = font.Font(family='Helvetica', size=10)
    
    # frame up
    frameUp = tk.LabelFrame(root, text='Choose the directory')
    frameUp.grid(row=0, column=0, padx=4, pady=4, ipadx=1, ipady=1)
    frameUp['font'] = labelFont
    
    frameUpUp = tk.Frame(frameUp)
    frameUpUp.grid(row=0, column=0)

    frameUpDw = tk.Frame(frameUp)
    frameUpDw.grid(row=1, column=0, sticky=tk.W)

    frameUpRight = tk.Frame(frameUp)
    frameUpRight.grid(row=0, column=1, rowspan=2)

    dirVariable = tk.StringVar()
    tgtDirStrEntry = tk.Entry(frameUpUp, width=50, textvariable=dirVariable)
    tgtDirStrEntry.grid(row=0, column=0, padx=4, pady=4)

    applyLabel = tk.Label(frameUpDw, text='Apply to:')
    applyLabel.grid(row=0, column=0, padx=4)

    applyValue = tk.IntVar() 
    fileRadio = tk.Radiobutton(frameUpDw, text='Files', variable=applyValue, value=1)
    fileRadio.grid(row=0, column=1)
    
    folderRadio = tk.Radiobutton(frameUpDw, text='Folders', variable=applyValue, value=2)
    folderRadio.grid(row=0, column=2)
    applyValue.set(1)

    chooseBtn = tk.Button(frameUpRight, text='Choose', command=openDir, width=6)
    chooseBtn.grid(row=0, column=0, padx=4, pady=4, ipadx=1, ipady=1)
    chooseBtn['font'] = btnFont

    readBtn = tk.Button(frameUpRight, text='Read', command=readFileNames, width=6)
    readBtn.grid(row=1, column=0, padx=4, pady=4, ipadx=1, ipady=1)
    readBtn['font'] = btnFont

    # frame mid
    frameMid = tk.LabelFrame(root, text='Naming method')
    frameMid.grid(row=1, column=0, padx=4, pady=4, ipadx=1, ipady=1, sticky=tk.W)
    frameMid['font'] = labelFont

    frameMidUp = tk.Frame(frameMid)
    frameMidUp.grid(row=0, column=0, sticky=tk.W)

    frameMidDw = tk.Frame(frameMid)
    frameMidDw.grid(row=1, column=0, sticky=tk.W)

    replaceState = tk.IntVar()
    replaceCheckBtn = tk.Checkbutton(frameMidUp, text='Replace text', command=changeConfigReplace, variable=replaceState, onvalue=1, offvalue=0)
    replaceCheckBtn.grid(row=0, column=0, padx=4, pady=4)

    findLabel = tk.Label(frameMidUp, text='Find:')
    findLabel.grid(row=0, column=1, padx=4, pady=4)
    
    findEntry = tk.Entry(frameMidUp, width=13)
    findEntry.grid(row=0, column=2, padx=4, pady=4)
    findEntry.config(state='disabled')
    
    replaceLabel = tk.Label(frameMidUp, text='Replace:')
    replaceLabel.grid(row=0, column=3, padx=4, pady=4)
    
    replaceEntry = tk.Entry(frameMidUp, width=13)
    replaceEntry.grid(row=0, column=4, padx=4, pady=4)
    replaceEntry.config(state='disabled')

    orderState = tk.IntVar()
    orderCheckBtn = tk.Checkbutton(frameMidDw, text='Make an order', command=changeConfigOrder, variable=orderState, onvalue=1, offvalue=0)
    orderCheckBtn.grid(row=1, column=0, padx=4, pady=4)

    sepLabel = tk.Label(frameMidDw, text='Sep:')
    sepLabel.grid(row=1, column=1, padx=4, pady=4)

    radioValue = tk.IntVar() 
    prefixRadio1 = tk.Radiobutton(frameMidDw, text='_', variable=radioValue, value=1)
    prefixRadio1.grid(row=1, column=2, padx=4, pady=4)
    prefixRadio1.config(state='disabled')
    
    prefixRadio2 = tk.Radiobutton(frameMidDw, text='-', variable=radioValue, value=2)
    prefixRadio2.grid(row=1, column=3, padx=4, pady=4)
    prefixRadio2.config(state='disabled')
    
    prefixRadio3 = tk.Radiobutton(frameMidDw, text='space', variable=radioValue, value=3)
    prefixRadio3.grid(row=1, column=4, padx=4, pady=4)
    prefixRadio3.config(state='disabled')
    radioValue.set(1)

    # frame down
    frameDw = tk.LabelFrame(root, text='File list')
    frameDw.grid(row=2, column=0, padx=4, pady=4, ipadx=1, ipady=1, sticky=tk.W)
    frameDw['font'] = labelFont
    
    frameDwLeft = tk.Frame(frameDw)
    frameDwLeft.grid(row=0, column=0)

    frameDwRight = tk.Frame(frameDw)
    frameDwRight.grid(row=0, column=1)

    listBoxRead = tk.Listbox(frameDwLeft, width=24)
    listBoxRead.grid(row=0, column=0, padx=4, pady=4)

    listBoxPreview = tk.Listbox(frameDwLeft, width=24)
    listBoxPreview.grid(row=0, column=1, padx=4, pady=4)

    upBtn = tk.Button(frameDwRight, text='Up', command=lambda: moveFileName(-1), width=6)
    dwBtn = tk.Button(frameDwRight, text='Down', command=lambda: moveFileName(1), width=6)
    preBtn = tk.Button(frameDwRight, text='Preview', command=previewFileNames, width=6)
    runBtn = tk.Button(frameDwRight, text='Run',command=renameFiles, width=6)
    upBtn['state'] = tk.DISABLED
    dwBtn['state'] = tk.DISABLED

    for idx, widget in enumerate(frameDwRight.winfo_children()):
        widget.grid(row=idx, column=0, padx=4, pady=4, ipadx=1, ipady=1)
        widget['font'] = btnFont

    root.mainloop()
    
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
        prefixRadio.config(state='normal')
        suffixRadio.config(state= 'normal')
    else:
        prefixRadio.config(state='disabled')
        suffixRadio.config(state='disabled')


def getFileNamesDict():
    fileNamesList = list(listBoxRead.get(0, tk.END))
    fileNamesDict = {idx:fileName for idx, fileName in enumerate(fileNamesList)}
    return fileNamesDict


def cleanPrefix(aDict):
    for key in aDict.keys():
        fileNameSeparated = aDict[key].partition('_')
        if fileNameSeparated[0].isdigit():
            aDict[key] = fileNameSeparated[-1]
        
        fileNameSeparated = aDict[key].partition('-')
        if fileNameSeparated[0].isdigit():
            aDict[key] = fileNameSeparated[-1]
    return aDict


def reviseFileList(fileNamesDict):
    keys = list(fileNamesDict.keys())
    keys.sort()

    listBoxRead.delete(0, tk.END)
    for idx in keys:
        listBoxRead.insert(idx, fileNamesDict[idx])


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

    listBoxRead.delete(0, tk.END)
    for idx, fileName in enumerate(nameList):
        listBoxRead.insert(idx, fileName)


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


def previewFileNames():
    fileNamesDict = getFileNamesDict()
    fileNamesDict = cleanPrefix(fileNamesDict)

    if replaceState.get():
        findStr = findEntry.get()
        replaceStr = replaceEntry.get()
        fileNamesReplaced = [fileNamesDict[key].replace(findStr, replaceStr) for key in fileNamesDict.keys()]
    else:
        fileNamesReplaced = [fileNamesDict[key] for key in fileNamesDict.keys()]

    if orderState.get():
        if radioValue.get() == 1:
            sep = '_'
        else:
            sep = '-'

        fileNum = len(fileNamesDict)
        decimal = floor(log10(fileNum)) + 1
        fileNamesOrdered = ['{idx:{fill}{width}}{sep}{fileName}'.format(idx=idx, fill='0', width=decimal, sep=sep, fileName=fileName) for idx, fileName in enumerate(fileNamesReplaced)]
    else:
        fileNamesOrdered = fileNamesReplaced

    listboxPreview.delete(0, tk.END)
    for idx, fileName in enumerate(fileNamesOrdered):
        listboxPreview.insert(idx, fileName)


def renameFiles():
    tgtdirName = dirVariable.get()
    fileNameListSrc = list(listBoxRead.get(0, tk.END))
    fileNameListDst = list(listboxPreview.get(0, tk.END))

    try:
        for fileNameSrc, fileNameDst in zip(fileNameListSrc, fileNameListDst):
            fileDirSrc = os.path.join(tgtdirName, fileNameSrc)
            fileDirDst = os.path.join(tgtdirName, fileNameDst)
            os.rename(src=fileDirSrc, dst=fileDirDst)
    except:
        tk.messagebox.showerror("Error", ":(")
    else:
        tk.messagebox.showinfo("Message", "All files have been renamed successfully.")


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
    frameMid = tk.LabelFrame(root, text='Naming settings')
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
    
    findEntry = tk.Entry(frameMidUp, width=8)
    findEntry.grid(row=0, column=2, padx=4, pady=4)
    findEntry.config(state='disabled')
    
    replaceLabel = tk.Label(frameMidUp, text='Replace:')
    replaceLabel.grid(row=0, column=3, padx=4, pady=4)
    
    replaceEntry = tk.Entry(frameMidUp, width=8)
    replaceEntry.grid(row=0, column=4, padx=4, pady=4)
    replaceEntry.config(state='disabled')

    orderState = tk.IntVar()
    orderCheckBtn = tk.Checkbutton(frameMidDw, text='Make an order', command=changeConfigOrder, variable=orderState, onvalue=1, offvalue=0)
    orderCheckBtn.grid(row=1, column=0, padx=4, pady=4)

    sepLabel = tk.Label(frameMidDw, text='Sep:')
    sepLabel.grid(row=1, column=1, padx=4, pady=4)

    radioValue = tk.IntVar() 
    prefixRadio = tk.Radiobutton(frameMidDw, text='_', variable=radioValue, value=1)
    prefixRadio.grid(row=1, column=2, padx=4, pady=4)
    prefixRadio.config(state='disabled')
    
    suffixRadio = tk.Radiobutton(frameMidDw, text='-', variable=radioValue, value=2)
    suffixRadio.grid(row=1, column=3, padx=4, pady=4)
    suffixRadio.config(state='disabled')
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

    listboxPreview = tk.Listbox(frameDwLeft, width=24)
    listboxPreview.grid(row=0, column=1, padx=4, pady=4)

    upBtn = tk.Button(frameDwRight, text='Up', command=lambda: moveFileName(-1), width=6)
    dwBtn = tk.Button(frameDwRight, text='Down', command=lambda: moveFileName(1), width=6)
    preBtn = tk.Button(frameDwRight, text='Preview', command=previewFileNames, width=6)
    runBtn = tk.Button(frameDwRight, text='Run',command=renameFiles, width=6)
    
    for idx, widget in enumerate(frameDwRight.winfo_children()):
        widget.grid(row=idx, column=0, padx=4, pady=4, ipadx=1, ipady=1)
        widget['font'] = btnFont

    root.mainloop()
    
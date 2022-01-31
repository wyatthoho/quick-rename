import os
import tkinter as tk
from tkinter import filedialog
from tkinter import font
from math import floor, log10

def OpenDir():
    dirName = filedialog.askdirectory(title='Choose the directory')
    tgtDirStr.set(dirName)

def change_replace_config():
    if replaceState.get():
        findEntry.config(state='normal')
        replaceEntry.config(state='normal')
    else:
        findEntry.config(state='disabled')
        replaceEntry.config(state='disabled')

def change_order_config():
    if orderState.get():
        prefixRadio.config(state='normal')
        suffixRadio.config(state= 'normal')
    else:
        prefixRadio.config(state='disabled')
        suffixRadio.config(state='disabled')

def get_file_names_dict():
    file_names_list = list(listbox_read.get(0, tk.END))
    file_names_dict = {idx:file_name for idx, file_name in enumerate(file_names_list)}
    return file_names_dict

def clean_prefix(a_dict):
    for key in a_dict.keys():
        file_name_separated = a_dict[key].partition('_')
        if file_name_separated[0].isdigit():
            a_dict[key] = file_name_separated[-1]
        
        file_name_separated = a_dict[key].partition('-')
        if file_name_separated[0].isdigit():
            a_dict[key] = file_name_separated[-1]
    return a_dict


def revise_file_list(file_names_dict):
    keys = list(file_names_dict.keys())
    keys.sort()

    listbox_read.delete(0, tk.END)
    for idx in keys:
        listbox_read.insert(idx, file_names_dict[idx])

def switch_dict_key(aDict, key_ori, key_tgt):
    tmp = aDict[key_ori]
    aDict[key_ori] = aDict[key_tgt]
    aDict[key_tgt] = tmp

def read_dir_file_name():
    tgtDir = tgtDirStr.get()
    dir_names = os.listdir(tgtDir)

    if applyValue.get() == 1:
        names_list = [dir_name for dir_name in dir_names if os.path.isfile(os.path.join(tgtDir, dir_name))]
    else:
        names_list = [dir_name for dir_name in dir_names if not os.path.isfile(os.path.join(tgtDir, dir_name))]

    listbox_read.delete(0, tk.END)
    for idx, file_name in enumerate(names_list):
        listbox_read.insert(idx, file_name)

def move_file_name(inc):
    moved = False
    file_names_dict = get_file_names_dict()

    if inc < 0:
        id_last = 0
    else:
        id_last = len(file_names_dict) - 1

    ids_selected = list(listbox_read.curselection())
    for id_selected in ids_selected:
        if abs(id_selected - id_last) > 0:
            id_next = id_selected + inc
            switch_dict_key(file_names_dict, id_selected, id_next)
            moved = True

    if moved:
        revise_file_list(file_names_dict)
        listbox_read.select_set(id_next)

def preview_file_names():
    file_names_dict = get_file_names_dict()
    file_names_dict = clean_prefix(file_names_dict)

    if replaceState.get():
        find_chr = findEntry.get()
        replace_chr = replaceEntry.get()
        file_names_rep = [file_names_dict[key].replace(find_chr, replace_chr) for key in file_names_dict.keys()]
    else:
        file_names_rep = [file_names_dict[key] for key in file_names_dict.keys()]

    if orderState.get():
        if radioValue.get() == 1:
            sep = '_'
        else:
            sep = '-'

        file_num = len(file_names_dict)
        decimal = floor(log10(file_num)) + 1
        file_names_ord = ['{idx:{fill}{width}}{sep}{file_name}'.format(idx=idx, fill='0', width=decimal, sep=sep, file_name=file_name) for idx, file_name in enumerate(file_names_rep)]
    else:
        file_names_ord = file_names_rep

    listbox_preview.delete(0, tk.END)
    for idx, file_name in enumerate(file_names_ord):
        listbox_preview.insert(idx, file_name)

def rename_files():
    tgtDir = tgtDirStr.get()
    file_names_list_src = list(listbox_read.get(0, tk.END))
    file_names_list_dst = list(listbox_preview.get(0, tk.END))

    try:
        for file_name_src, file_name_dst in zip(file_names_list_src, file_names_list_dst):
            file_dir_src = os.path.join(tgtDir, file_name_src)
            file_dir_dst = os.path.join(tgtDir, file_name_dst)
            os.rename(src=file_dir_src, dst=file_dir_dst)
    except:
        tk.messagebox.showerror("Error", ":(")
    else:
        tk.messagebox.showinfo("Message", "All files have been renamed successfully.")


if __name__ == '__main__':
    root = tk.Tk()
    root.title('QuickRename')
    root.geometry('500x400')
    root.resizable(width=0, height=0)
    root.configure()

    labelFont = font.Font(family='Helvetica', size=10)
    btnFont = font.Font(family='Helvetica', size=10)

    # frame up
    frameUp = tk.Frame(root)
    frameUp.grid(row=0, column=0)

    frameDir = tk.LabelFrame(frameUp, text='Choose the directory', width=450, height=60)
    frameDir.grid(row=0, column=0)
    frameDir['font'] = labelFont

    frameSubUp = tk.Frame(frameDir)
    frameSubUp.grid(row=0, column=0)
    
    tgtDirStr = tk.StringVar()
    tgtDirStrEntry = tk.Entry(frameSubUp, width=50, textvariable=tgtDirStr)
    tgtDirStrEntry.grid(row=0, column=0)

    btn1 = tk.Button(frameSubUp, text='Choose', command=OpenDir)
    btn1.grid(row=0, column=1)

    frameSubDw = tk.Frame(frameDir)
    frameSubDw.grid(row=1, column=0)

    applyLabel = tk.Label(frameSubDw, text='Apply to:')
    applyLabel.grid(row=0, column=0)

    applyValue = tk.IntVar() 
    fileRadio = tk.Radiobutton(frameSubDw, text='Files', variable=applyValue, value=1)
    fileRadio.grid(row=0, column=1)
    
    folderRadio = tk.Radiobutton(frameSubDw, text='Folders', variable=applyValue, value=2)
    folderRadio.grid(row=0, column=2)
    applyValue.set(1)

    btn2 = tk.Button(frameSubDw, text='Read', command=read_dir_file_name, height=1, width=6)
    btn2.grid(row=0, column=3, padx=2, pady=5)
    btn2['font'] = btnFont

    # frame mid
    frameMid = tk.Frame(root)
    frameMid.grid(row=1, column=0)

    frameMidSub = tk.LabelFrame(frameMid, text='Naming settings', width=450, height=60)
    frameMidSub.grid(row=0, column=0)
    frameMidSub['font'] = labelFont

    replaceState = tk.IntVar()
    replaceCheckBtn = tk.Checkbutton(frameMidSub, text='Replace text', command=change_replace_config, variable=replaceState, onvalue=1, offvalue=0)
    replaceCheckBtn.grid(row=0, column=0)

    findLabel = tk.Label(frameMidSub, text='Find:')
    findLabel.grid(row=0, column=1)
    
    findEntry = tk.Entry(frameMidSub, width=5)
    findEntry.grid(row=0, column=2,)
    
    replaceLabel = tk.Label(frameMidSub, text='Replace:')
    replaceLabel.grid(row=0, column=3)
    
    replaceEntry = tk.Entry(frameMidSub, width=5)
    replaceEntry.grid(row=0, column=4)

    findEntry.config(state='disabled')
    replaceEntry.config(state='disabled')

    orderState = tk.IntVar()
    orderCheckBtn = tk.Checkbutton(frameMidSub, text='Make an order', command=change_order_config, variable=orderState, onvalue=1, offvalue=0)
    orderCheckBtn.grid(row=1, column=0)

    sepLabel = tk.Label(frameMidSub, text='Sep:')
    sepLabel.grid(row=1, column=1)

    radioValue = tk.IntVar() 
    prefixRadio = tk.Radiobutton(frameMidSub, text='_', variable=radioValue, value=1)
    prefixRadio.grid(row=1, column=2)
    
    suffixRadio = tk.Radiobutton(frameMidSub, text='-', variable=radioValue, value=2)
    suffixRadio.grid(row=1, column=3)

    prefixRadio.config(state='disabled')
    suffixRadio.config(state='disabled')
    radioValue.set(1)
    

    # frame down
    frameDw = tk.Frame(root, width=450, height=400)
    frameDw.grid(row=2, column=0)

    frameDwLeft = tk.LabelFrame(frameDw, text='Files list', width=330, height=200)
    frameDwLeft.grid(row=0, column=0, padx=10, pady=5)
    frameDwLeft.pack_propagate(0)

    listbox_read = tk.Listbox(frameDwLeft)
    listbox_read.grid(row=0, column=0)

    listbox_preview = tk.Listbox(frameDwLeft)
    listbox_preview.grid(row=0, column=1)
    
    frameDwRight = tk.LabelFrame(frameDwLeft, text='Action')
    frameDwRight.grid(row=0, column=2, padx=10, pady=5)

    btn3 = tk.Button(frameDwRight, text='Up', command=lambda: move_file_name(-1), height=1, width=6)
    btn4 = tk.Button(frameDwRight, text='Down', command=lambda: move_file_name(1), height=1, width=6)
    btn5 = tk.Button(frameDwRight, text='Preview', command=preview_file_names, height=1, width=6)
    btn6 = tk.Button(frameDwRight, text='Run',command=rename_files, height=1, width=6)
    
    for idx, widget in enumerate(frameDwRight.winfo_children()):
        widget.grid(row=idx, column=0, padx=2, pady=5)
        widget['font'] = btnFont

    root.mainloop()
    
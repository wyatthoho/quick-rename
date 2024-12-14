import os
import tkinter as tk
from math import floor, log10
from pathlib import Path
from tkinter import filedialog
from tkinter import font
from typing import TypedDict


def replace_names(names: list, find_entry: tk.Entry, replace_entry: tk.Entry):
    find_str = find_entry.get()
    replace_str = replace_entry.get()
    return [name.replace(find_str, replace_str) for name in names]


def add_suffix(names: list, suffix_entry: tk.Entry):
    suffix = suffix_entry.get()
    return [''.join([_str + suffix if idx == 0 else _str for idx, _str in enumerate(name.rpartition('.'))]) for name in names]


def clean_prefix(names: list):
    new_names = []
    for name in names:
        name_separated = name.partition('_')
        if name_separated[0].isdigit():
            name = name_separated[-1]

        name_separated = name.partition('-')
        if name_separated[0].isdigit():
            name = name_separated[-1]

        name_separated = name.partition(' ')
        if name_separated[0].isdigit():
            name = name_separated[-1]

        new_names.append(name)
    return new_names


def reorder_names(names: list, radio_value: tk.IntVar):
    names = clean_prefix(names)
    if radio_value.get() == 1:
        sep = '_'
    elif radio_value.get() == 2:
        sep = '-'
    elif radio_value.get() == 3:
        sep = ' '

    num_name = len(names)
    decimal = floor(log10(num_name)) + 1
    return ['{idx:{fill}{width}}{sep}{name}'.format(idx=idx, fill='0', width=decimal, sep=sep, name=name) for idx, name in enumerate(names)]


def check_repeated(list_box: tk.Listbox, names: list):
    global name_repeated
    name_repeated = False

    for idx1, name1 in enumerate(names):
        for idx2, name2 in enumerate(names[idx1+1:]):
            if name2 == name1:
                name_repeated = True
                list_box.itemconfig(idx1, {'bg': 'red'})
                list_box.itemconfig(idx1+idx2+1, {'bg': 'red'})


class AppWidgets(TypedDict):
    strvar_tgtdir: tk.StringVar
    intvar_applyto: tk.IntVar
    intvar_replace: tk.IntVar
    entry_find: tk.Entry
    entry_replace: tk.Entry
    intvar_suffix: tk.IntVar
    entry_suffix: tk.Entry
    intvar_make_order: tk.IntVar
    intvar_sep: tk.IntVar
    listbox_read: tk.Listbox
    listbox_preview: tk.Listbox
    radiobutton_prefix_1: tk.Radiobutton
    radiobutton_prefix_2: tk.Radiobutton
    radiobutton_prefix_3: tk.Radiobutton
    button_up: tk.Button
    button_down: tk.Button


class App:
    NAME = 'QuickRename'
    PADS = {'padx': 4, 'pady': 4}
    IPADS = {'ipadx': 1, 'ipady': 1}
    BUTTON_WIDTH = 6

    def __init__(self):
        self.root = self.initialize_main_window()
        self.font_label = font.Font(family='Helvetica', size=10)
        self.font_button = font.Font(family='Helvetica', size=10)
        self.app_widgets = AppWidgets()
        self.create_frame_target_directory()
        self.create_frame_naming_method()
        self.create_frame_name_list()
        self.root.mainloop()

    # typesetting
    def initialize_main_window(self):
        root = tk.Tk()
        root.title(App.NAME)
        logopath = Path(__file__).parent.parent.joinpath('image', 'w.ico')
        root.iconbitmap(logopath)
        root.resizable(width=0, height=0)
        return root
    
    def create_frame_target_directory(self):
        frame = tk.LabelFrame(self.root, text='Choose the directory')
        frame.grid(row=0, column=0, sticky=tk.W, **App.PADS, **App.IPADS)
        frame['font'] = self.font_label

        frame_up = tk.Frame(frame)
        frame_up.grid(row=0, column=0)

        frame_dw = tk.Frame(frame)
        frame_dw.grid(row=1, column=0, sticky=tk.W)

        frame_right = tk.Frame(frame)
        frame_right.grid(row=0, column=1, rowspan=2)

        strvar_tgtdir = tk.StringVar()
        entry_tgtdir = tk.Entry(frame_up, width=50, textvariable=strvar_tgtdir)
        entry_tgtdir.grid(row=0, column=0, **App.PADS)

        label_applyto = tk.Label(frame_dw, text='Apply to:')
        label_applyto.grid(row=0, column=0, **App.PADS)

        intvar_applyto = tk.IntVar()
        radiobutoon_file = tk.Radiobutton(frame_dw, text='Files', variable=intvar_applyto, value=1)
        radiobutoon_file.grid(row=0, column=1)

        radiobutton_folder = tk.Radiobutton(frame_dw, text='Folders', variable=intvar_applyto, value=2)
        radiobutton_folder.grid(row=0, column=2)
        intvar_applyto.set(1)

        button_choose = tk.Button(frame_right, text='Choose', command=self.open_dir, width=App.BUTTON_WIDTH)
        button_choose.grid(row=0, column=0, **App.PADS, **App.IPADS)
        button_choose['font'] = self.font_button

        button_read = tk.Button(frame_right, text='Read', command=self.read_names, width=App.BUTTON_WIDTH)
        button_read.grid(row=1, column=0, **App.PADS, **App.IPADS)
        button_read['font'] = self.font_button

        self.app_widgets['strvar_tgtdir'] = strvar_tgtdir
        self.app_widgets['intvar_applyto'] = intvar_applyto


    def create_frame_naming_method(self):
        frame = tk.LabelFrame(self.root, text='Naming method')
        frame.grid(row=1, column=0, sticky=tk.W, **App.PADS, **App.IPADS)
        frame['font'] = self.font_label

        frame_up = tk.Frame(frame)
        frame_up.grid(row=0, column=0, sticky=tk.W)

        frame_mid = tk.Frame(frame)
        frame_mid.grid(row=1, column=0, sticky=tk.W)

        frame_dw = tk.Frame(frame)
        frame_dw.grid(row=2, column=0, sticky=tk.W)

        intvar_replace = tk.IntVar()
        checkbutton_replace = tk.Checkbutton(frame_up, text='Replace text', command=self.config_replace, variable=intvar_replace, onvalue=1, offvalue=0)
        checkbutton_replace.grid(row=0, column=0, **App.PADS)

        label_find = tk.Label(frame_up, text='Find:')
        label_find.grid(row=0, column=1, **App.PADS)

        entry_find = tk.Entry(frame_up, width=13)
        entry_find.grid(row=0, column=2, **App.PADS)
        entry_find.config(state='disabled')

        label_replace = tk.Label(frame_up, text='Replace:')
        label_replace.grid(row=0, column=3, **App.PADS)

        entry_replace = tk.Entry(frame_up, width=13)
        entry_replace.grid(row=0, column=4, **App.PADS)
        entry_replace.config(state='disabled')

        intvar_suffix = tk.IntVar()
        checkbutton_suffix = tk.Checkbutton(frame_mid, text='Add suffix', command=self.config_suffix, variable=intvar_suffix, onvalue=1, offvalue=0)
        checkbutton_suffix.grid(row=0, column=0, **App.PADS)

        label_suffix = tk.Label(frame_mid, text='Suffix:')
        label_suffix.grid(row=0, column=1, **App.PADS)

        entry_suffix = tk.Entry(frame_mid, width=13)
        entry_suffix.grid(row=0, column=2, **App.PADS)
        entry_suffix.config(state='disabled')

        intvar_make_order = tk.IntVar()
        checkbutton_order = tk.Checkbutton(frame_dw, text='Make an order', command=self.config_order, variable=intvar_make_order, onvalue=1, offvalue=0)
        checkbutton_order.grid(row=1, column=0, **App.PADS)

        label_sep = tk.Label(frame_dw, text='Sep:')
        label_sep.grid(row=1, column=1, **App.PADS)

        intvar_sep = tk.IntVar()
        radiobutton_prefix_1 = tk.Radiobutton(frame_dw, text='_', variable=intvar_sep, value=1)
        radiobutton_prefix_1.grid(row=1, column=2, **App.PADS)
        radiobutton_prefix_1.config(state='disabled')

        radiobutton_prefix_2 = tk.Radiobutton(frame_dw, text='-', variable=intvar_sep, value=2)
        radiobutton_prefix_2.grid(row=1, column=3, **App.PADS)
        radiobutton_prefix_2.config(state='disabled')

        radiobutton_prefix_3 = tk.Radiobutton(frame_dw, text='space', variable=intvar_sep, value=3)
        radiobutton_prefix_3.grid(row=1, column=4, **App.PADS)
        radiobutton_prefix_3.config(state='disabled')
        intvar_sep.set(1)

        self.app_widgets['intvar_replace'] = intvar_replace
        self.app_widgets['entry_find'] = entry_find
        self.app_widgets['entry_replace'] = entry_replace
        self.app_widgets['intvar_suffix'] = intvar_suffix
        self.app_widgets['entry_suffix'] = entry_suffix
        self.app_widgets['intvar_make_order'] = intvar_make_order
        self.app_widgets['intvar_sep'] = intvar_sep
        self.app_widgets['radiobutton_prefix_1'] = radiobutton_prefix_1
        self.app_widgets['radiobutton_prefix_2'] = radiobutton_prefix_2
        self.app_widgets['radiobutton_prefix_3'] = radiobutton_prefix_3

    def create_frame_name_list(self):
        frame = tk.LabelFrame(self.root, text='Name list')
        frame.grid(row=2, column=0, sticky=tk.W, **App.PADS, **App.IPADS)
        frame['font'] = self.font_label

        frame_left = tk.Frame(frame)
        frame_left.grid(row=0, column=0)

        scrollbar_read_x = tk.Scrollbar(frame_left, orient=tk.HORIZONTAL)
        scrollbar_read_y = tk.Scrollbar(frame_left, orient=tk.VERTICAL)

        scrollbar_read_x.grid(row=1, column=0, sticky=tk.EW)
        scrollbar_read_y.grid(row=0, column=1, sticky=tk.NS)

        listbox_read = tk.Listbox(frame_left, width=22, xscrollcommand=scrollbar_read_x.set, yscrollcommand=scrollbar_read_y.set)
        listbox_read.grid(row=0, column=0, **App.PADS)

        scrollbar_read_x.config(command=listbox_read.xview)
        scrollbar_read_y.config(command=listbox_read.yview)

        scrollbar_preview_x = tk.Scrollbar(frame_left, orient=tk.HORIZONTAL)
        scrollbar_preview_y = tk.Scrollbar(frame_left, orient=tk.VERTICAL)

        scrollbar_preview_x.grid(row=1, column=2, sticky=tk.EW)
        scrollbar_preview_y.grid(row=0, column=3, sticky=tk.NS)

        listbox_preview = tk.Listbox(frame_left, width=22, xscrollcommand=scrollbar_preview_x.set, yscrollcommand=scrollbar_preview_y.set)
        listbox_preview.grid(row=0, column=2, **App.PADS)

        scrollbar_preview_x.config(command=listbox_preview.xview)
        scrollbar_preview_y.config(command=listbox_preview.yview)

        frame_right = tk.Frame(frame)
        frame_right.grid(row=0, column=1)

        button_up = tk.Button(frame_right, text='Up', command=lambda: self.move_name(-1), width=App.BUTTON_WIDTH)
        button_down = tk.Button(frame_right, text='Down', command=lambda: self.move_name(1), width=App.BUTTON_WIDTH)
        button_preview = tk.Button(frame_right, text='Preview', command=self.preview_names, width=App.BUTTON_WIDTH)
        button_run = tk.Button(frame_right, text='Run', command=self.run_rename, width=App.BUTTON_WIDTH)
        button_up['state'] = tk.DISABLED
        button_down['state'] = tk.DISABLED

        for idx, widget in enumerate(frame_right.winfo_children()):
            widget.grid(row=idx, column=0, **App.PADS, **App.IPADS)
            widget['font'] = self.font_button

        self.app_widgets['listbox_read'] = listbox_read
        self.app_widgets['listbox_preview'] = listbox_preview
        self.app_widgets['button_up'] = button_up
        self.app_widgets['button_down'] = button_down

    # actions
    def open_dir(self):
        strvar_tgtdir = self.app_widgets['strvar_tgtdir']
        dir_name = filedialog.askdirectory(title='Choose the directory')
        strvar_tgtdir.set(dir_name)

    def refresh_listbox(self, listbox: tk.Listbox, names: list):
        listbox.delete(0, tk.END)
        for idx, name in enumerate(names):
            listbox.insert(idx, name)

    def read_names(self):
        strvar_tgtdir = self.app_widgets['strvar_tgtdir']
        intvar_applyto = self.app_widgets['intvar_applyto']
        listbox_read = self.app_widgets['listbox_read']
        tgtdir = strvar_tgtdir.get()
        tgtnames = os.listdir(tgtdir)
        if intvar_applyto.get() == 1:
            names = [name for name in tgtnames if os.path.isfile(os.path.join(tgtdir, name))]
        else:
            names = [name for name in tgtnames if not os.path.isfile(os.path.join(tgtdir, name))]
        self.refresh_listbox(listbox_read, names)

    def config_replace(self):
        intvar_replace = self.app_widgets['intvar_replace']
        entry_find = self.app_widgets['entry_find']
        entry_replace = self.app_widgets['entry_replace']
        if intvar_replace.get():
            entry_find.config(state='normal')
            entry_replace.config(state='normal')
        else:
            entry_find.config(state='disabled')
            entry_replace.config(state='disabled')

    def config_suffix(self):
        intvar_suffix = self.app_widgets['intvar_suffix']
        entry_suffix = self.app_widgets['entry_suffix']
        if intvar_suffix.get():
            entry_suffix.config(state='normal')
        else:
            entry_suffix.config(state='disabled')

    def config_order(self):
        intvar_make_order = self.app_widgets['intvar_make_order']
        radiobutton_prefix_1 = self.app_widgets['radiobutton_prefix_1']
        radiobutton_prefix_2 = self.app_widgets['radiobutton_prefix_2']
        radiobutton_prefix_3 = self.app_widgets['radiobutton_prefix_3']
        button_up = self.app_widgets['button_up']
        button_down = self.app_widgets['button_down']
        if intvar_make_order.get():
            radiobutton_prefix_1.config(state='normal')
            radiobutton_prefix_2.config(state='normal')
            radiobutton_prefix_3.config(state='normal')
            button_up['state'] = tk.NORMAL
            button_down['state'] = tk.NORMAL
        else:
            radiobutton_prefix_1.config(state='disabled')
            radiobutton_prefix_2.config(state='disabled')
            radiobutton_prefix_3.config(state='disabled')
            button_up['state'] = tk.DISABLED
            button_down['state'] = tk.DISABLED

    def move_name(self, inc: int):
        listbox_read = self.app_widgets['listbox_read']
        moved = False
        names = list(listbox_read.get(0, tk.END))
        names_dict = {idx: name for idx, name in enumerate(names)}
        if inc < 0:
            id_boundary = 0
        else:
            id_boundary = len(names_dict) - 1
        id_sel = listbox_read.curselection()[0]
        if abs(id_sel - id_boundary) > 0:
            id_next = id_sel + inc
            names_dict[id_sel], names_dict[id_next] = names_dict[id_next], names_dict[id_sel]
            moved = True
        if moved:
            keys = list(names_dict.keys())
            keys.sort()
            names = [names_dict[key] for key in keys]
            self.refresh_listbox(listbox_read, names)
            listbox_read.select_set(id_next)

    def preview_names(self):
        listbox_read = self.app_widgets['listbox_read']
        listbox_preview = self.app_widgets['listbox_preview']
        intvar_replace = self.app_widgets['intvar_replace']
        intvar_suffix = self.app_widgets['intvar_suffix']
        intvar_make_order = self.app_widgets['intvar_make_order']
        entry_find = self.app_widgets['entry_find']
        entry_replace = self.app_widgets['entry_replace']
        entry_suffix = self.app_widgets['entry_suffix']
        intvar_sep = self.app_widgets['intvar_sep']
        names = list(listbox_read.get(0, tk.END))
        if intvar_replace.get():
            names = replace_names(names, entry_find, entry_replace)
        if intvar_suffix.get():
            names = add_suffix(names, entry_suffix)
        if intvar_make_order.get():
            names = reorder_names(names, intvar_sep)
        self.refresh_listbox(listbox_preview, names)
        check_repeated(listbox_preview, names)

    def run_rename(self):
        strvar_tgtdir = self.app_widgets['strvar_tgtdir']
        listbox_read = self.app_widgets['listbox_read']
        listbox_preview = self.app_widgets['listbox_preview']
        tgt_dir_name = strvar_tgtdir.get()
        names_src = list(listbox_read.get(0, tk.END))
        names_dst = list(listbox_preview.get(0, tk.END))
        try:
            if name_repeated:
                raise Exception('There are repeated names after renaming.')
            else:
                for name_src, name_dst in zip(names_src, names_dst):
                    path_src = os.path.join(tgt_dir_name, name_src)
                    path_dst = os.path.join(tgt_dir_name, name_dst)
                    os.rename(src=path_src, dst=path_dst)
        except Exception as e:
            tk.messagebox.showerror("Error", e.args[0])
            listbox_preview.delete(0, tk.END)
        else:
            tk.messagebox.showinfo("Message", "Renamed successfully.")
            listbox_read.delete(0, tk.END)
            listbox_preview.delete(0, tk.END)


if __name__ == '__main__':
    App()

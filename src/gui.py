import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import font
from typing import TypedDict

from manipulate_names import *
from manipulate_tk_widgets import *


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
    ROOT_MINSIZE = {'width': 680, 'height': 500}
    PADS = {'padx': 4, 'pady': 4}
    IPADS = {'ipadx': 1, 'ipady': 1}
    BUTTON_WIDTH = 6
    ENTRY_WIDTH = 30

    def __init__(self):
        self.root = self.initialize_main_window()
        self.font_label = font.Font(family='Helvetica', size=10)
        self.font_button = font.Font(family='Helvetica', size=10)
        self.app_widgets = AppWidgets()
        self.name_repeated = False
        self.create_frame_target_directory()
        self.create_frame_renaming_method()
        self.create_frame_name_list()
        self.root.mainloop()

    # typesetting
    def initialize_main_window(self):
        root = tk.Tk()
        root.title(App.NAME)
        logopath = Path(__file__).parent.parent.joinpath('img', 'favicon.ico')
        root.iconbitmap(logopath)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=0)
        root.rowconfigure(1, weight=0)
        root.rowconfigure(2, weight=1)
        root.state('zoomed')
        root.minsize(**App.ROOT_MINSIZE)
        return root
    
    def create_frame_target_directory(self):
        frame = tk.LabelFrame(self.root, text='Choose the directory')
        frame.grid(row=0, column=0, sticky=tk.NSEW, **App.PADS, **App.IPADS)
        frame.columnconfigure(0, weight=1)
        frame['font'] = self.font_label

        frame_up = tk.Frame(frame)
        frame_up.grid(row=0, column=0, sticky=tk.NSEW)
        frame_up.rowconfigure(0, weight=1)
        frame_up.columnconfigure(0, weight=1)

        frame_dw = tk.Frame(frame)
        frame_dw.grid(row=1, column=0, sticky=tk.NSEW)

        frame_right = tk.Frame(frame)
        frame_right.grid(row=0, column=1, rowspan=2, sticky=tk.NSEW)

        strvar_tgtdir = tk.StringVar()
        entry_tgtdir = tk.Entry(frame_up, width=50, textvariable=strvar_tgtdir)
        entry_tgtdir.grid(row=0, column=0, sticky=tk.NSEW, **App.PADS)

        label_applyto = tk.Label(frame_dw, text='Apply to:')
        label_applyto.grid(row=0, column=0, **App.PADS)

        intvar_applyto = tk.IntVar()
        radiobutoon_file = tk.Radiobutton(frame_dw, text='Files', variable=intvar_applyto, value=1)
        radiobutoon_file.grid(row=0, column=1)

        radiobutton_folder = tk.Radiobutton(frame_dw, text='Folders', variable=intvar_applyto, value=2)
        radiobutton_folder.grid(row=0, column=2)
        intvar_applyto.set(1)

        button_choose = tk.Button(frame_right, text='Choose', command=self.choose_target_directory, width=App.BUTTON_WIDTH)
        button_choose.grid(row=0, column=0, sticky=tk.E, **App.PADS, **App.IPADS)
        button_choose['font'] = self.font_button

        button_read = tk.Button(frame_right, text='Read', command=self.load_target_names, width=App.BUTTON_WIDTH)
        button_read.grid(row=1, column=0, **App.PADS, **App.IPADS)
        button_read['font'] = self.font_button

        self.app_widgets['strvar_tgtdir'] = strvar_tgtdir
        self.app_widgets['intvar_applyto'] = intvar_applyto


    def create_frame_renaming_method(self):
        frame = tk.LabelFrame(self.root, text='Renaming method')
        frame.grid(row=1, column=0, sticky=tk.NSEW, **App.PADS, **App.IPADS)
        frame['font'] = self.font_label

        frame_up = tk.Frame(frame)
        frame_up.grid(row=0, column=0, sticky=tk.NSEW)

        frame_mid = tk.Frame(frame)
        frame_mid.grid(row=1, column=0, sticky=tk.NSEW)

        frame_dw = tk.Frame(frame)
        frame_dw.grid(row=2, column=0, sticky=tk.NSEW)

        intvar_replace = tk.IntVar()
        checkbutton_replace = tk.Checkbutton(frame_up, text='Replace text', command=self.config_replace, variable=intvar_replace, onvalue=1, offvalue=0)
        checkbutton_replace.grid(row=0, column=0, **App.PADS)

        label_find = tk.Label(frame_up, text='Find:')
        label_find.grid(row=0, column=1, **App.PADS)

        entry_find = tk.Entry(frame_up, width=App.ENTRY_WIDTH)
        entry_find.grid(row=0, column=2, **App.PADS)
        entry_find.config(state='disabled')

        label_replace = tk.Label(frame_up, text='Replace:')
        label_replace.grid(row=0, column=3, **App.PADS)

        entry_replace = tk.Entry(frame_up, width=App.ENTRY_WIDTH)
        entry_replace.grid(row=0, column=4, **App.PADS)
        entry_replace.config(state='disabled')

        intvar_suffix = tk.IntVar()
        checkbutton_suffix = tk.Checkbutton(frame_mid, text='Add suffix', command=self.config_suffix, variable=intvar_suffix, onvalue=1, offvalue=0)
        checkbutton_suffix.grid(row=0, column=0, **App.PADS)

        label_suffix = tk.Label(frame_mid, text='Suffix:')
        label_suffix.grid(row=0, column=1, **App.PADS)

        entry_suffix = tk.Entry(frame_mid, width=App.ENTRY_WIDTH)
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
        frame.grid(row=2, column=0, sticky=tk.NSEW, **App.PADS, **App.IPADS)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=0)
        frame.rowconfigure(2, weight=0)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=0)
        frame['font'] = self.font_label

        scrollbar_read_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scrollbar_read_y = tk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar_read_x.grid(row=1, column=0, sticky=tk.EW)
        scrollbar_read_y.grid(row=0, column=1, sticky=tk.NS)
        listbox_read = tk.Listbox(frame, width=22, xscrollcommand=scrollbar_read_x.set, yscrollcommand=scrollbar_read_y.set)
        listbox_read.grid(row=0, column=0, sticky=tk.NSEW, **App.PADS)
        scrollbar_read_x.config(command=listbox_read.xview)
        scrollbar_read_y.config(command=listbox_read.yview)

        scrollbar_preview_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scrollbar_preview_y = tk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar_preview_x.grid(row=1, column=2, sticky=tk.EW)
        scrollbar_preview_y.grid(row=0, column=3, sticky=tk.NS)
        listbox_preview = tk.Listbox(frame, width=22, xscrollcommand=scrollbar_preview_x.set, yscrollcommand=scrollbar_preview_y.set)
        listbox_preview.grid(row=0, column=2, sticky=tk.NSEW, **App.PADS)
        scrollbar_preview_x.config(command=listbox_preview.xview)
        scrollbar_preview_y.config(command=listbox_preview.yview)

        frame_bottomleft = tk.Frame(frame)
        frame_bottomleft.grid(row=2, column=0, columnspan=2)
        button_up = tk.Button(frame_bottomleft, text='Up', command=lambda: self.move_name(-1), width=App.BUTTON_WIDTH)
        button_up.grid(row=0, column=1, **App.PADS, **App.IPADS)
        button_up['font'] = self.font_button
        button_up['state'] = tk.DISABLED
        button_down = tk.Button(frame_bottomleft, text='Down', command=lambda: self.move_name(1), width=App.BUTTON_WIDTH)
        button_down.grid(row=0, column=2, **App.PADS, **App.IPADS)
        button_down['font'] = self.font_button
        button_down['state'] = tk.DISABLED

        frame_bottomright = tk.Frame(frame)
        frame_bottomright.grid(row=2, column=2, columnspan=2)
        button_preview = tk.Button(frame_bottomright, text='Preview', command=self.preview_names, width=App.BUTTON_WIDTH)
        button_preview.grid(row=0, column=1, **App.PADS, **App.IPADS)
        button_preview['font'] = self.font_button
        button_run = tk.Button(frame_bottomright, text='Run', command=self.run_rename, width=App.BUTTON_WIDTH)
        button_run.grid(row=0, column=2, **App.PADS, **App.IPADS)
        button_run['font'] = self.font_button

        self.app_widgets['listbox_read'] = listbox_read
        self.app_widgets['listbox_preview'] = listbox_preview
        self.app_widgets['button_up'] = button_up
        self.app_widgets['button_down'] = button_down

    # actions
    def choose_target_directory(self):
        strvar_tgtdir = self.app_widgets['strvar_tgtdir']
        dir_name = filedialog.askdirectory(title='Choose the directory')
        strvar_tgtdir.set(dir_name)

    def update_listbox_content(self, listbox: tk.Listbox, names: list):
        listbox.delete(0, tk.END)
        for idx, name in enumerate(names):
            listbox.insert(idx, name)

    def load_target_names(self):
        strvar_tgtdir = self.app_widgets['strvar_tgtdir']
        intvar_applyto = self.app_widgets['intvar_applyto']
        listbox_read = self.app_widgets['listbox_read']
        tgtdir = strvar_tgtdir.get()
        tgtnames = os.listdir(tgtdir)
        if intvar_applyto.get() == 1:
            names = [name for name in tgtnames if os.path.isfile(os.path.join(tgtdir, name))]
        else:
            names = [name for name in tgtnames if not os.path.isfile(os.path.join(tgtdir, name))]
        self.update_listbox_content(listbox_read, names)

    def config_replace(self):
        intvar_replace = self.app_widgets['intvar_replace']
        entry_find = self.app_widgets['entry_find']
        entry_replace = self.app_widgets['entry_replace']
        enable = bool(intvar_replace.get())
        toggle_widget_state(entry_find, enable)
        toggle_widget_state(entry_replace, enable)

    def config_suffix(self):
        intvar_suffix = self.app_widgets['intvar_suffix']
        entry_suffix = self.app_widgets['entry_suffix']
        enable = bool(intvar_suffix.get())
        toggle_widget_state(entry_suffix, enable)

    def config_order(self):
        intvar_make_order = self.app_widgets['intvar_make_order']
        radiobutton_prefix_1 = self.app_widgets['radiobutton_prefix_1']
        radiobutton_prefix_2 = self.app_widgets['radiobutton_prefix_2']
        radiobutton_prefix_3 = self.app_widgets['radiobutton_prefix_3']
        button_up = self.app_widgets['button_up']
        button_down = self.app_widgets['button_down']
        enable = bool(intvar_make_order.get())
        toggle_widget_state(radiobutton_prefix_1, enable)
        toggle_widget_state(radiobutton_prefix_2, enable)
        toggle_widget_state(radiobutton_prefix_3, enable)
        toggle_widget_state(button_up, enable)
        toggle_widget_state(button_down, enable)

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
            self.update_listbox_content(listbox_read, names)
            listbox_read.select_set(id_next)

    def highlight_duplicates(self, listbox: tk.Listbox, names: list):
        self.name_repeated = False
        for idx1, name1 in enumerate(names):
            for idx2, name2 in enumerate(names[idx1+1:]):
                if name2 == name1:
                    self.name_repeated = True
                    listbox.itemconfig(idx1, {'bg': 'red'})
                    listbox.itemconfig(idx1+idx2+1, {'bg': 'red'})

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
            names = replace_names(names, entry_find.get(), entry_replace.get())
        if intvar_suffix.get():
            names = add_suffix(names, entry_suffix.get())
        if intvar_make_order.get():
            separator = {1: '_', 2: '-', 3: ' '}[intvar_sep.get()]
            names = reorder_names(names, separator)
        self.update_listbox_content(listbox_preview, names)
        self.highlight_duplicates(listbox_preview, names)

    def run_rename(self):
        strvar_tgtdir = self.app_widgets['strvar_tgtdir']
        listbox_read = self.app_widgets['listbox_read']
        listbox_preview = self.app_widgets['listbox_preview']
        tgt_dir_name = strvar_tgtdir.get()
        names_src = list(listbox_read.get(0, tk.END))
        names_dst = list(listbox_preview.get(0, tk.END))
        try:
            if self.name_repeated:
                raise Exception('There are repeated names after renaming.')
            else:
                for name_src, name_dst in zip(names_src, names_dst):
                    path_src = os.path.join(tgt_dir_name, name_src)
                    path_dst = os.path.join(tgt_dir_name, name_dst)
                    os.rename(src=path_src, dst=path_dst)
        except Exception as e:
            tk.messagebox.showerror('Error', e.args[0])
            listbox_preview.delete(0, tk.END)
        else:
            tk.messagebox.showinfo('Message', 'Renamed successfully.')
            listbox_read.delete(0, tk.END)
            listbox_preview.delete(0, tk.END)


if __name__ == '__main__':
    App()

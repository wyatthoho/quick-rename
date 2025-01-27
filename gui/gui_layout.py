import tkinter as tk
from tkinter import font
from collections.abc import Callable

import logic.logic as logic


class App:
    NAME = 'QuickRename'
    ROOT_MINSIZE = {'width': 680, 'height': 500}
    LOGO_PATH = 'img\\favicon.ico'
    FONT_FAMILY = 'Helvetica'
    FONT_SIZE = 10
    PADS = {'padx': 4, 'pady': 4}
    IPADS = {'ipadx': 1, 'ipady': 1}
    BUTTON_WIDTH = 6
    ENTRY_WIDTH = 30
    STICKY_FRAME = tk.NSEW

    def __init__(self):
        self.root = self.initialize_main_window()
        self.font = font.Font(family=App.FONT_FAMILY, size=App.FONT_SIZE)
        self.logic_widgets = logic.LogicWidgets()
        self.create_label_frame_target_directory()
        self.create_label_frame_renaming_method()
        self.create_label_frame_name_list()
        self.root.mainloop()

    def initialize_main_window(self):
        root = tk.Tk()
        root.title(App.NAME)
        root.iconbitmap(App.LOGO_PATH)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=0)
        root.rowconfigure(1, weight=0)
        root.rowconfigure(2, weight=1)
        root.state('zoomed')
        root.minsize(**App.ROOT_MINSIZE)
        return root

    def create_label_frame(self, master: tk.Tk, row: int, col: int, text: str) -> tk.LabelFrame:
        labelframe = tk.LabelFrame(master, text=text)
        labelframe.grid(row=row, column=col, sticky=App.STICKY_FRAME, **App.PADS, **App.IPADS)
        labelframe['font'] = self.font
        return labelframe

    def create_frame(self, master: tk.LabelFrame, row: int, col: int, rowspan: int = 1, columnspan: int = 1, sticky: bool = True) -> tk.Frame:
        frame = tk.Frame(master)
        frame.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=App.STICKY_FRAME if sticky else None, **App.PADS, **App.IPADS)
        return frame

    def create_button(self, master: tk.Frame, row: int, column: int, text: str, command: Callable) -> tk.Button:
        button = tk.Button(master, text=text, command=command, width=App.BUTTON_WIDTH)
        button.grid(row=row, column=column, **App.PADS, **App.IPADS, sticky=tk.E)
        button['font'] = self.font
        return button

    def create_listbox_with_scrollbar(self, master: tk.LabelFrame, row: int, col: int) -> tk.Listbox:
        master.rowconfigure(row, weight=1)
        master.rowconfigure(row+1, weight=0)
        master.columnconfigure(col, weight=1)
        master.columnconfigure(col+1, weight=0)
        scrollbar_x = tk.Scrollbar(master, orient=tk.HORIZONTAL)
        scrollbar_y = tk.Scrollbar(master, orient=tk.VERTICAL)
        scrollbar_x.grid(row=row+1, column=0, sticky=tk.EW)
        scrollbar_y.grid(row=0, column=col+1, sticky=tk.NS)
        listbox = tk.Listbox(master, xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        listbox.grid(row=row, column=col, sticky=tk.NSEW, **App.PADS)
        scrollbar_x.config(command=listbox.xview)
        scrollbar_y.config(command=listbox.yview)
        return listbox

    def create_label_frame_target_directory(self):
        labelframe = self.create_label_frame(self.root, 0, 0, 'Choose the directory')
        frame_up = self.create_frame(labelframe, 0, 0)
        frame_dw = self.create_frame(labelframe, 1, 0)
        frame_right = self.create_frame(labelframe, 0, 1, 2)
        labelframe.columnconfigure(0, weight=1)
        frame_up.rowconfigure(0, weight=1)
        frame_up.columnconfigure(0, weight=1)

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

        button_choose = self.create_button(frame_right, 0, 0, 'Chooose', lambda: logic.choose_target_directory(self.logic_widgets))
        button_read = self.create_button(frame_right, 1, 0, 'Read', lambda: logic.load_target_names(self.logic_widgets))

        self.logic_widgets['strvar_tgtdir'] = strvar_tgtdir
        self.logic_widgets['intvar_applyto'] = intvar_applyto

    def create_label_frame_renaming_method(self):
        labelframe = self.create_label_frame(self.root, 1, 0, 'Renaming method')
        frame_up = self.create_frame(labelframe, 0, 0)
        frame_mid = self.create_frame(labelframe, 1, 0)
        frame_dw = self.create_frame(labelframe, 2, 0)

        intvar_replace = tk.IntVar()
        checkbutton_replace = tk.Checkbutton(frame_up, text='Replace text', command=lambda: logic.config_replace(self.logic_widgets), variable=intvar_replace, onvalue=1, offvalue=0)
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
        checkbutton_suffix = tk.Checkbutton(frame_mid, text='Add suffix', command=lambda: logic.config_suffix(self.logic_widgets), variable=intvar_suffix, onvalue=1, offvalue=0)
        checkbutton_suffix.grid(row=0, column=0, **App.PADS)

        label_suffix = tk.Label(frame_mid, text='Suffix:')
        label_suffix.grid(row=0, column=1, **App.PADS)

        entry_suffix = tk.Entry(frame_mid, width=App.ENTRY_WIDTH)
        entry_suffix.grid(row=0, column=2, **App.PADS)
        entry_suffix.config(state='disabled')

        intvar_make_order = tk.IntVar()
        checkbutton_order = tk.Checkbutton(frame_dw, text='Make an order', command=lambda: logic.config_order(self.logic_widgets), variable=intvar_make_order, onvalue=1, offvalue=0)
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

        self.logic_widgets['intvar_replace'] = intvar_replace
        self.logic_widgets['entry_find'] = entry_find
        self.logic_widgets['entry_replace'] = entry_replace
        self.logic_widgets['intvar_suffix'] = intvar_suffix
        self.logic_widgets['entry_suffix'] = entry_suffix
        self.logic_widgets['intvar_make_order'] = intvar_make_order
        self.logic_widgets['intvar_sep'] = intvar_sep
        self.logic_widgets['radiobutton_prefix_1'] = radiobutton_prefix_1
        self.logic_widgets['radiobutton_prefix_2'] = radiobutton_prefix_2
        self.logic_widgets['radiobutton_prefix_3'] = radiobutton_prefix_3

    def create_label_frame_name_list(self):
        labelframe = self.create_label_frame(self.root, 2, 0, 'Name list')
        
        listbox_read = self.create_listbox_with_scrollbar(labelframe, 0, 0)
        frame_bottomleft = self.create_frame(labelframe, 2, 0, columnspan=2, sticky=False)
        button_up = self.create_button(frame_bottomleft, 0, 1, 'Up', lambda: logic.move_name(self.logic_widgets, -1))
        button_down = self.create_button(frame_bottomleft, 0, 2, 'Down', lambda: logic.move_name(self.logic_widgets, 1))
        button_up['state'] = tk.DISABLED
        button_down['state'] = tk.DISABLED

        listbox_preview = self.create_listbox_with_scrollbar(labelframe, 0, 2)
        frame_bottomright = self.create_frame(labelframe, 2, 2, columnspan=2, sticky=False)
        button_preview = self.create_button(frame_bottomright, 0, 1, 'Preview', lambda: logic.preview_names(self.logic_widgets))
        button_run = self.create_button(frame_bottomright, 0, 2, 'Run', lambda: logic.run_rename(self.logic_widgets))

        self.logic_widgets['listbox_read'] = listbox_read
        self.logic_widgets['listbox_preview'] = listbox_preview
        self.logic_widgets['button_up'] = button_up
        self.logic_widgets['button_down'] = button_down

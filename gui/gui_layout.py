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

    def create_label(self, master: tk.Frame, row: int, col: int, text: str) -> tk.Label:
        label = tk.Label(master, text=text)
        label.grid(row=row, column=col, **App.PADS)
        return label

    def create_frame(self, master: tk.LabelFrame, row: int, col: int, rowspan: int = 1, columnspan: int = 1, sticky: bool = True) -> tk.Frame:
        frame = tk.Frame(master)
        frame.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=App.STICKY_FRAME if sticky else None, **App.PADS, **App.IPADS)
        return frame

    def create_entry(self, master: tk.Frame, row: int, col: int, width: int = None, textvariable: tk.StringVar = None) -> tk.Entry:
        entry = tk.Entry(master, width=width if width else App.ENTRY_WIDTH, textvariable=textvariable if textvariable else None)
        entry.grid(row=row, column=col, sticky=App.STICKY_FRAME, **App.PADS)
        return entry

    def create_button(self, master: tk.Frame, row: int, column: int, text: str, command: Callable) -> tk.Button:
        button = tk.Button(master, text=text, command=command, width=App.BUTTON_WIDTH)
        button.grid(row=row, column=column, **App.PADS, **App.IPADS)
        button['font'] = self.font
        return button

    def create_checkbutton(self, master: tk.Frame, row: int, column: int, text: str, command: Callable, variable: tk.IntVar) -> tk.Checkbutton:
        checkbutton = tk.Checkbutton(master, text=text, command=command, variable=variable, onvalue=1, offvalue=0)
        checkbutton.grid(row=row, column=column, **App.PADS)
        return checkbutton

    def create_radiobutton(self, master: tk.Frame, row: int, column: int, text: str, variable: tk.IntVar, value: int) -> tk.Radiobutton:
        radiobutton = tk.Radiobutton(master, text=text, variable=variable, value=value)
        radiobutton.grid(row=row, column=column, **App.PADS)
        return radiobutton

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
        labelframe.columnconfigure(0, weight=1)
        frame_up = self.create_frame(labelframe, 0, 0)
        frame_up.rowconfigure(0, weight=1)
        frame_up.columnconfigure(0, weight=1)
        strvar_tgtdir = tk.StringVar()
        self.create_entry(frame_up, 0, 0, 50, strvar_tgtdir)
        frame_dw = self.create_frame(labelframe, 1, 0)
        self.create_label(frame_dw, 0, 0, 'Apply to:')
        intvar_applyto = tk.IntVar()
        self.create_radiobutton(frame_dw, 0, 1, 'Files', intvar_applyto, 1)
        self.create_radiobutton(frame_dw, 0, 2, 'Folders', intvar_applyto, 2)
        intvar_applyto.set(1)
        frame_right = self.create_frame(labelframe, 0, 1, 2)
        self.create_button(frame_right, 0, 0, 'Choose', lambda: logic.choose_target_directory(self.logic_widgets))
        self.create_button(frame_right, 1, 0, 'Read', lambda: logic.load_target_names(self.logic_widgets))

        self.logic_widgets['strvar_tgtdir'] = strvar_tgtdir
        self.logic_widgets['intvar_applyto'] = intvar_applyto

    def create_label_frame_renaming_method(self):
        labelframe = self.create_label_frame(self.root, 1, 0, 'Renaming method')
        frame_up = self.create_frame(labelframe, 0, 0)
        intvar_replace = tk.IntVar()
        self.create_checkbutton(frame_up, 0, 0, 'Replace text', lambda: logic.config_replace(self.logic_widgets), intvar_replace)
        self.create_label(frame_up, 0, 1, 'Find:')
        entry_find = self.create_entry(frame_up, 0, 2)
        entry_find.config(state='disabled')
        self.create_label(frame_up, 0, 3, 'Replace:')
        entry_replace = self.create_entry(frame_up, 0, 4)
        entry_replace.config(state='disabled')
        frame_mid = self.create_frame(labelframe, 1, 0)
        intvar_suffix = tk.IntVar()
        self.create_checkbutton(frame_mid, 0, 0, 'Add suffix', lambda: logic.config_suffix(self.logic_widgets), intvar_suffix)
        self.create_label(frame_mid, 0, 1, 'Suffix:')
        entry_suffix = self.create_entry(frame_mid, 0, 2)
        entry_suffix.config(state='disabled')
        frame_dw = self.create_frame(labelframe, 2, 0)
        intvar_make_order = tk.IntVar()
        self.create_checkbutton(frame_dw, 1, 0, 'Make an order', lambda: logic.config_order(self.logic_widgets), intvar_make_order)
        self.create_label(frame_dw, 1, 1, 'Sep:')
        intvar_sep = tk.IntVar()
        radiobutton_prefix_1 = self.create_radiobutton(frame_dw, 1, 2, '_', intvar_sep, 1)
        radiobutton_prefix_2 = self.create_radiobutton(frame_dw, 1, 3, '-', intvar_sep, 2)
        radiobutton_prefix_3 = self.create_radiobutton(frame_dw, 1, 4, 'space', intvar_sep, 3)
        radiobutton_prefix_1.config(state='disabled')
        radiobutton_prefix_2.config(state='disabled')
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
        listbox_preview = self.create_listbox_with_scrollbar(labelframe, 0, 2)
        frame_bottomleft = self.create_frame(labelframe, 2, 0, columnspan=2, sticky=False)
        button_up = self.create_button(frame_bottomleft, 0, 1, 'Up', lambda: logic.move_name(self.logic_widgets, -1))
        button_down = self.create_button(frame_bottomleft, 0, 2, 'Down', lambda: logic.move_name(self.logic_widgets, 1))
        button_up['state'] = tk.DISABLED
        button_down['state'] = tk.DISABLED
        frame_bottomright = self.create_frame(labelframe, 2, 2, columnspan=2, sticky=False)
        self.create_button(frame_bottomright, 0, 1, 'Preview', lambda: logic.preview_names(self.logic_widgets))
        self.create_button(frame_bottomright, 0, 2, 'Run', lambda: logic.run_rename(self.logic_widgets))

        self.logic_widgets['listbox_read'] = listbox_read
        self.logic_widgets['listbox_preview'] = listbox_preview
        self.logic_widgets['button_up'] = button_up
        self.logic_widgets['button_down'] = button_down

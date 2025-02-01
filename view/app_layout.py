import tkinter as tk
from tkinter import font

import logic.app_logic as logic
from components.LabelFrame import LabelFrame
from components.Label import Label
from components.Frame import Frame
from components.Entry import Entry
from components.Button import Button
from components.Checkbutton import Checkbutton
from components.Radiobutton import Radiobutton
from components.Listbox import Listbox


NAME = 'QuickRename'
FAVICON = 'icon\\favicon.ico'
STATE = 'zoomed'
ROOT_MINSIZE = {'width': 680, 'height': 500}
FONT_FAMILY = 'Helvetica'
FONT_SIZE = 10


class App:
    def __init__(self):
        self.root = self.initialize_main_window()
        self.font = font.Font(family=FONT_FAMILY, size=FONT_SIZE)
        self.logic_widgets = logic.LogicWidgets()
        self.create_label_frame_target_directory()
        self.create_label_frame_renaming_method()
        self.create_label_frame_name_list()
        self.root.mainloop()

    def initialize_main_window(self):
        root = tk.Tk()
        root.title(NAME)
        root.iconbitmap(FAVICON)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=0)
        root.rowconfigure(1, weight=0)
        root.rowconfigure(2, weight=1)
        root.state(STATE)
        root.minsize(**ROOT_MINSIZE)
        return root

    def create_label_frame_target_directory(self):
        labelframe = LabelFrame(self.root, 0, 0, 'Target directory', self.font)
        labelframe.columnconfigure(0, weight=1)

        frame_up = Frame(labelframe, 0, 0)
        frame_up.rowconfigure(0, weight=1)
        frame_up.columnconfigure(0, weight=1)
        strvar_tgtdir = tk.StringVar()
        Entry(frame_up, 0, 0, self.font, 50, strvar_tgtdir)

        frame_down = Frame(labelframe, 1, 0)
        intvar_applyto = tk.IntVar(value=1)
        Label(frame_down, 0, 0, 'Apply to:', self.font)
        Radiobutton(frame_down, 0, 1, 'Files', self.font, intvar_applyto, 1)
        Radiobutton(frame_down, 0, 2, 'Folders', self.font, intvar_applyto, 2)

        frame_right = Frame(labelframe, 0, 1, 2)
        Button(frame_right, 0, 0, 'Choose', self.font, self.choose)
        Button(frame_right, 1, 0, 'Read', self.font, self.read)

        self.logic_widgets['strvar_tgtdir'] = strvar_tgtdir
        self.logic_widgets['intvar_applyto'] = intvar_applyto

    def create_label_frame_renaming_method(self):
        labelframe = LabelFrame(self.root, 1, 0, 'Renaming method', self.font)

        frame_up = Frame(labelframe, 0, 0)
        intvar_replace = tk.IntVar()
        Checkbutton(
            frame_up, 0, 0, 'Replace text', self.font,
            self.replace, intvar_replace
        )
        Label(frame_up, 0, 1, 'Find:', self.font)
        entry_find = Entry(frame_up, 0, 2, self.font)
        entry_find['state'] = tk.DISABLED
        Label(frame_up, 0, 3, 'Replace:', self.font)
        entry_replace = Entry(frame_up, 0, 4, self.font)
        entry_replace['state'] = tk.DISABLED

        frame_mid = Frame(labelframe, 1, 0)
        intvar_suffix = tk.IntVar()
        Checkbutton(
            frame_mid, 0, 0, 'Add suffix', self.font,
            self.suffix, intvar_suffix
        )
        Label(frame_mid, 0, 1, 'Suffix:', self.font)
        entry_suffix = Entry(frame_mid, 0, 2, self.font)
        entry_suffix['state'] = tk.DISABLED

        frame_down = Frame(labelframe, 2, 0)
        intvar_make_order = tk.IntVar()
        Checkbutton(
            frame_down, 1, 0, 'Make an order', self.font,
            self.order, intvar_make_order
        )
        Label(frame_down, 1, 1, 'Sep:', self.font)
        intvar_sep = tk.IntVar(value=1)
        radiobutton_prefix_1 = Radiobutton(
            frame_down, 1, 2, '_', self.font, intvar_sep, 1
        )
        radiobutton_prefix_2 = Radiobutton(
            frame_down, 1, 3, '-', self.font, intvar_sep, 2
        )
        radiobutton_prefix_3 = Radiobutton(
            frame_down, 1, 4, 'space', self.font, intvar_sep, 3
        )
        radiobutton_prefix_1['state'] = tk.DISABLED
        radiobutton_prefix_2['state'] = tk.DISABLED
        radiobutton_prefix_3['state'] = tk.DISABLED

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
        labelframe = LabelFrame(self.root, 2, 0, 'Name list', self.font)

        listbox_read = Listbox(labelframe, 0, 0, self.font)
        listbox_preview = Listbox(labelframe, 0, 2, self.font)

        frame_downleft = Frame(labelframe, 2, 0, columnspan=2, sticky=False)
        button_up = Button(frame_downleft, 0, 1, 'Up', self.font, self.up)
        button_down = Button(frame_downleft, 0, 2, 'Down', self.font, self.down)
        button_up['state'] = tk.DISABLED
        button_down['state'] = tk.DISABLED

        frame_downright = Frame(labelframe, 2, 2, columnspan=2, sticky=False)
        Button(frame_downright, 0, 1, 'Preview', self.font, self.preview)
        Button(frame_downright, 0, 2, 'Run', self.font, self.rename)

        self.logic_widgets['listbox_read'] = listbox_read
        self.logic_widgets['listbox_preview'] = listbox_preview
        self.logic_widgets['button_up'] = button_up
        self.logic_widgets['button_down'] = button_down

    def choose(self): return logic.choose_target_directory(self.logic_widgets)
    def read(self): return logic.load_target_names(self.logic_widgets)
    def replace(self): return logic.config_replace(self.logic_widgets)
    def suffix(self): return logic.config_suffix(self.logic_widgets)
    def order(self): return logic.config_order(self.logic_widgets)
    def up(self): return logic.move_name(self.logic_widgets, -1)
    def down(self): return logic.move_name(self.logic_widgets, 1)
    def preview(self): return logic.preview_names(self.logic_widgets)
    def rename(self): return logic.run_rename(self.logic_widgets)

import tkinter as tk
from tkinter import font

import components.components as comps
import logic.app_logic as logic


NAME = 'QuickRename'
ROOT_MINSIZE = {'width': 680, 'height': 500}
FAVICON = 'icon\\favicon.ico'
# FONT_FAMILY = 'Helvetica'
FONT_FAMILY = 'Times New Roman'
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
        root.state('zoomed')
        root.minsize(**ROOT_MINSIZE)
        return root

    def create_label_frame_target_directory(self):
        labelframe = comps.create_label_frame(
            self.root, 0, 0, 'Choose the directory', self.font
        )
        labelframe.columnconfigure(0, weight=1)

        frame_up = comps.create_frame(labelframe, 0, 0)
        frame_up.rowconfigure(0, weight=1)
        frame_up.columnconfigure(0, weight=1)
        strvar_tgtdir = tk.StringVar()
        comps.create_entry(frame_up, 0, 0, 50, strvar_tgtdir)

        frame_down = comps.create_frame(labelframe, 1, 0)
        intvar_applyto = tk.IntVar(value=1)
        comps.create_label(frame_down, 0, 0, 'Apply to:')
        comps.create_radiobutton(frame_down, 0, 1, 'Files', intvar_applyto, 1)
        comps.create_radiobutton(frame_down, 0, 2, 'Folders', intvar_applyto, 2)

        frame_right = comps.create_frame(labelframe, 0, 1, 2)
        comps.create_button(
            frame_right, 0, 0, 'Choose', self.font,
            lambda: logic.choose_target_directory(self.logic_widgets)
        )
        comps.create_button(
            frame_right, 1, 0, 'Read', self.font,
            lambda: logic.load_target_names(self.logic_widgets)
        )

        self.logic_widgets['strvar_tgtdir'] = strvar_tgtdir
        self.logic_widgets['intvar_applyto'] = intvar_applyto

    def create_label_frame_renaming_method(self):
        labelframe = comps.create_label_frame(
            self.root, 1, 0, 'Renaming method', self.font
        )

        frame_up = comps.create_frame(labelframe, 0, 0)
        intvar_replace = tk.IntVar()
        comps.create_checkbutton(
            frame_up, 0, 0, 'Replace text',
            lambda: logic.config_replace(self.logic_widgets), intvar_replace
        )
        comps.create_label(frame_up, 0, 1, 'Find:')
        entry_find = comps.create_entry(frame_up, 0, 2)
        entry_find.config(state='disabled')
        comps.create_label(frame_up, 0, 3, 'Replace:')
        entry_replace = comps.create_entry(frame_up, 0, 4)
        entry_replace.config(state='disabled')

        frame_mid = comps.create_frame(labelframe, 1, 0)
        intvar_suffix = tk.IntVar()
        comps.create_checkbutton(
            frame_mid, 0, 0, 'Add suffix',
            lambda: logic.config_suffix(self.logic_widgets), intvar_suffix
        )
        comps.create_label(frame_mid, 0, 1, 'Suffix:')
        entry_suffix = comps.create_entry(frame_mid, 0, 2)
        entry_suffix.config(state='disabled')

        frame_down = comps.create_frame(labelframe, 2, 0)
        intvar_make_order = tk.IntVar()
        comps.create_checkbutton(
            frame_down, 1, 0, 'Make an order',
            lambda: logic.config_order(self.logic_widgets), intvar_make_order
        )
        comps.create_label(frame_down, 1, 1, 'Sep:')
        intvar_sep = tk.IntVar(value=1)
        radiobutton_prefix_1 = comps.create_radiobutton(
            frame_down, 1, 2, '_', intvar_sep, 1
        )
        radiobutton_prefix_2 = comps.create_radiobutton(
            frame_down, 1, 3, '-', intvar_sep, 2
        )
        radiobutton_prefix_3 = comps.create_radiobutton(
            frame_down, 1, 4, 'space', intvar_sep, 3
        )
        radiobutton_prefix_1.config(state='disabled')
        radiobutton_prefix_2.config(state='disabled')
        radiobutton_prefix_3.config(state='disabled')

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
        labelframe = comps.create_label_frame(
            self.root, 2, 0, 'Name list', self.font
        )

        listbox_read = comps.create_listbox_with_scrollbar(labelframe, 0, 0)
        listbox_preview = comps.create_listbox_with_scrollbar(labelframe, 0, 2)

        frame_downleft = comps.create_frame(
            labelframe, 2, 0, columnspan=2, sticky=False
        )
        button_up = comps.create_button(
            frame_downleft, 0, 1, 'Up', self.font,
            lambda: logic.move_name(self.logic_widgets, -1)
        )
        button_down = comps.create_button(
            frame_downleft, 0, 2, 'Down', self.font,
            lambda: logic.move_name(self.logic_widgets, 1)
        )
        button_up['state'] = tk.DISABLED
        button_down['state'] = tk.DISABLED

        frame_downright = comps.create_frame(
            labelframe, 2, 2, columnspan=2, sticky=False
        )
        comps.create_button(
            frame_downright, 0, 1, 'Preview', self.font,
            lambda: logic.preview_names(self.logic_widgets)
        )
        comps.create_button(
            frame_downright, 0, 2, 'Run', self.font,
            lambda: logic.run_rename(self.logic_widgets)
        )

        self.logic_widgets['listbox_read'] = listbox_read
        self.logic_widgets['listbox_preview'] = listbox_preview
        self.logic_widgets['button_up'] = button_up
        self.logic_widgets['button_down'] = button_down

import tkinter as tk
from tkinter import font

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

    def __init__(self):
        self.root = self.initialize_main_window()
        self.font = font.Font(family=App.FONT_FAMILY, size=App.FONT_SIZE)
        self.logic_widgets = logic.LogicWidgets()
        self.create_frame_target_directory()
        self.create_frame_renaming_method()
        self.create_frame_name_list()
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

    def create_frame_target_directory(self):
        frame = tk.LabelFrame(self.root, text='Choose the directory')
        frame.grid(row=0, column=0, sticky=tk.NSEW, **App.PADS, **App.IPADS)
        frame.columnconfigure(0, weight=1)
        frame['font'] = self.font

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

        button_choose = tk.Button(frame_right, text='Choose', command=lambda: logic.choose_target_directory(self.logic_widgets), width=App.BUTTON_WIDTH)
        button_choose.grid(row=0, column=0, sticky=tk.E, **App.PADS, **App.IPADS)
        button_choose['font'] = self.font

        button_read = tk.Button(frame_right, text='Read', command=lambda: logic.load_target_names(self.logic_widgets), width=App.BUTTON_WIDTH)
        button_read.grid(row=1, column=0, **App.PADS, **App.IPADS)
        button_read['font'] = self.font

        self.logic_widgets['strvar_tgtdir'] = strvar_tgtdir
        self.logic_widgets['intvar_applyto'] = intvar_applyto

    def create_frame_renaming_method(self):
        frame = tk.LabelFrame(self.root, text='Renaming method')
        frame.grid(row=1, column=0, sticky=tk.NSEW, **App.PADS, **App.IPADS)
        frame['font'] = self.font

        frame_up = tk.Frame(frame)
        frame_up.grid(row=0, column=0, sticky=tk.NSEW)

        frame_mid = tk.Frame(frame)
        frame_mid.grid(row=1, column=0, sticky=tk.NSEW)

        frame_dw = tk.Frame(frame)
        frame_dw.grid(row=2, column=0, sticky=tk.NSEW)

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
        frame['font'] = self.font

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
        button_up = tk.Button(frame_bottomleft, text='Up', command=lambda: logic.move_name(self.logic_widgets, -1), width=App.BUTTON_WIDTH)
        button_up.grid(row=0, column=1, **App.PADS, **App.IPADS)
        button_up['font'] = self.font
        button_up['state'] = tk.DISABLED
        button_down = tk.Button(frame_bottomleft, text='Down', command=lambda: logic.move_name(self.logic_widgets, 1), width=App.BUTTON_WIDTH)
        button_down.grid(row=0, column=2, **App.PADS, **App.IPADS)
        button_down['font'] = self.font
        button_down['state'] = tk.DISABLED

        frame_bottomright = tk.Frame(frame)
        frame_bottomright.grid(row=2, column=2, columnspan=2)
        button_preview = tk.Button(frame_bottomright, text='Preview', command=lambda: logic.preview_names(self.logic_widgets), width=App.BUTTON_WIDTH)
        button_preview.grid(row=0, column=1, **App.PADS, **App.IPADS)
        button_preview['font'] = self.font
        button_run = tk.Button(frame_bottomright, text='Run', command=lambda: logic.run_rename(self.logic_widgets), width=App.BUTTON_WIDTH)
        button_run.grid(row=0, column=2, **App.PADS, **App.IPADS)
        button_run['font'] = self.font

        self.logic_widgets['listbox_read'] = listbox_read
        self.logic_widgets['listbox_preview'] = listbox_preview
        self.logic_widgets['button_up'] = button_up
        self.logic_widgets['button_down'] = button_down

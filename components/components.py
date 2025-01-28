import tkinter as tk
from collections.abc import Callable
from tkinter import font


PADS = {'padx': 4, 'pady': 4}
IPADS = {'ipadx': 1, 'ipady': 1}
BUTTON_WIDTH = 6
ENTRY_WIDTH = 30
STICKY = tk.NSEW


def create_label_frame(master: tk.Tk, row: int, col: int, text: str, font: font) -> tk.LabelFrame:
    labelframe = tk.LabelFrame(master, text=text)
    labelframe.grid(row=row, column=col, sticky=STICKY, **PADS, **IPADS)
    labelframe['font'] = font
    return labelframe


def create_label(master: tk.Frame, row: int, col: int, text: str) -> tk.Label:
    label = tk.Label(master, text=text)
    label.grid(row=row, column=col, **PADS)
    return label


def create_frame(master: tk.LabelFrame, row: int, col: int, rowspan: int = 1, columnspan: int = 1, sticky: bool = True) -> tk.Frame:
    frame = tk.Frame(master)
    frame.grid(
        row=row, column=col, rowspan=rowspan, columnspan=columnspan,
        sticky=STICKY if sticky else None,
        **PADS, **IPADS
    )
    return frame


def create_entry(master: tk.Frame, row: int, col: int, width: int = None, textvariable: tk.StringVar = None) -> tk.Entry:
    entry = tk.Entry(
        master,
        width=width if width else ENTRY_WIDTH,
        textvariable=textvariable if textvariable else None
    )
    entry.grid(row=row, column=col, sticky=STICKY, **PADS)
    return entry


def create_button(master: tk.Frame, row: int, col: int, text: str, font: font, command: Callable) -> tk.Button:
    button = tk.Button(
        master, text=text, command=command, width=BUTTON_WIDTH
    )
    button.grid(row=row, column=col, **PADS, **IPADS)
    button['font'] = font
    return button


def create_checkbutton(master: tk.Frame, row: int, col: int, text: str, command: Callable, variable: tk.IntVar) -> tk.Checkbutton:
    checkbutton = tk.Checkbutton(
        master, text=text, command=command, variable=variable,
        onvalue=1, offvalue=0
    )
    checkbutton.grid(row=row, column=col, **PADS)
    return checkbutton


def create_radiobutton(master: tk.Frame, row: int, col: int, text: str, variable: tk.IntVar, value: int) -> tk.Radiobutton:
    radiobutton = tk.Radiobutton(
        master, text=text, variable=variable, value=value
    )
    radiobutton.grid(row=row, column=col, **PADS)
    return radiobutton


def create_listbox_with_scrollbar(master: tk.LabelFrame, row: int, col: int) -> tk.Listbox:
    master.rowconfigure(row, weight=1)
    master.rowconfigure(row+1, weight=0)
    master.columnconfigure(col, weight=1)
    master.columnconfigure(col+1, weight=0)
    scrollbar_x = tk.Scrollbar(master, orient=tk.HORIZONTAL)
    scrollbar_y = tk.Scrollbar(master, orient=tk.VERTICAL)
    scrollbar_x.grid(row=row+1, column=0, sticky=tk.EW)
    scrollbar_y.grid(row=0, column=col+1, sticky=tk.NS)
    listbox = tk.Listbox(
        master,
        xscrollcommand=scrollbar_x.set,
        yscrollcommand=scrollbar_y.set
    )
    listbox.grid(row=row, column=col, sticky=tk.NSEW, **PADS)
    scrollbar_x.config(command=listbox.xview)
    scrollbar_y.config(command=listbox.yview)
    return listbox

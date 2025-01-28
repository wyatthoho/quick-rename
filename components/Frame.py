import tkinter as tk

from typing import Union


PADS = {'padx': 4, 'pady': 4}
IPADS = {'ipadx': 1, 'ipady': 1}
STICKY = tk.NSEW

type master = Union[tk.Tk, tk.Frame, tk.LabelFrame]


class Frame(tk.Frame):
    def __init__(self, master: master, row: int, col: int, rowspan: int = 1, columnspan: int = 1, sticky: bool = True):
        super().__init__(master)
        self.grid(
            row=row, column=col, rowspan=rowspan, columnspan=columnspan,
            sticky=STICKY if sticky else None,
            **PADS, **IPADS
        )

import tkinter as tk

from typing import Union


PADS = {'padx': 4, 'pady': 4}
IPADS = {'ipadx': 1, 'ipady': 1}
STICKY = tk.NSEW

type master = Union[tk.Tk, tk.Frame, tk.LabelFrame]


class Listbox(tk.Listbox):
    def __init__(self, master: master, row: int, col: int, font: tk.font):
        master.rowconfigure(row, weight=1)
        master.rowconfigure(row+1, weight=0)
        master.columnconfigure(col, weight=1)
        master.columnconfigure(col+1, weight=0)
        scrollbar_x = tk.Scrollbar(master, orient=tk.HORIZONTAL)
        scrollbar_y = tk.Scrollbar(master, orient=tk.VERTICAL)
        scrollbar_x.grid(row=row+1, column=0, sticky=tk.EW)
        scrollbar_y.grid(row=0, column=col+1, sticky=tk.NS)
        super().__init__(
            master, font=font,
            xscrollcommand=scrollbar_x.set,
            yscrollcommand=scrollbar_y.set
        )
        self.grid(row=row, column=col, sticky=STICKY, **PADS, **IPADS)
        scrollbar_x.config(command=self.xview)
        scrollbar_y.config(command=self.yview)

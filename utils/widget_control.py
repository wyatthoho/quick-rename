import tkinter as tk

type Names = list[str]
type Indices = list[int]


def toggle_widget_state(widget: tk.Widget, enable: bool):
    '''Enable or disable a widget based on the enable flag.'''
    widget.config(state='normal' if enable else 'disabled')


def update_listbox_content(listbox: tk.Listbox, names: Names):
    listbox.delete(0, tk.END)
    for idx, name in enumerate(names):
        listbox.insert(idx, name)


def highlight_duplicates(listbox: tk.Listbox, indices: Indices, bg_color: str = 'red'):
    for idx in indices:
        listbox.itemconfig(idx, {'bg': bg_color})

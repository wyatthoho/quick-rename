import tkinter as tk


def toggle_widget_state(widget: tk.Widget, enable: bool):
    '''Enable or disable a widget based on the enable flag.'''
    widget.config(state='normal' if enable else 'disabled')


def update_listbox_content(listbox: tk.Listbox, names: list):
    listbox.delete(0, tk.END)
    for idx, name in enumerate(names):
        listbox.insert(idx, name)


def highlight_duplicates(listbox: tk.Listbox, indices: list, bg_color: str = 'red') -> bool:
    for idx in indices:
        listbox.itemconfig(idx, {'bg': bg_color})

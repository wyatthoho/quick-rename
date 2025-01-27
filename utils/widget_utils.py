import tkinter as tk


def toggle_widget_state(widget: tk.Widget, enable: bool):
    '''Enable or disable a widget based on the enable flag.'''
    widget.config(state='normal' if enable else 'disabled')


def update_listbox_content(listbox: tk.Listbox, names: list):
    listbox.delete(0, tk.END)
    for idx, name in enumerate(names):
        listbox.insert(idx, name)


def highlight_duplicates(listbox: tk.Listbox, names: list) -> bool:
    for idx1, name1 in enumerate(names):
        for idx2, name2 in enumerate(names[idx1+1:]):
            if name2 == name1:
                listbox.itemconfig(idx1, {'bg': 'red'})
                listbox.itemconfig(idx1+idx2+1, {'bg': 'red'})
                return True
    return False

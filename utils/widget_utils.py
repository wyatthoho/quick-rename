import tkinter as tk


def toggle_widget_state(widget: tk.Widget, enable: bool):
    '''Enable or disable a widget based on the enable flag.'''
    widget.config(state='normal' if enable else 'disabled')

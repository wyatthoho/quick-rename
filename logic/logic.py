import os
import tkinter as tk
from tkinter import filedialog
from typing import TypedDict

import utils.stringlist_utils as stringlist_utils
import utils.widget_utils as widget_utils


class LogicWidgets(TypedDict):
    strvar_tgtdir: tk.StringVar
    intvar_applyto: tk.IntVar
    intvar_replace: tk.IntVar
    entry_find: tk.Entry
    entry_replace: tk.Entry
    intvar_suffix: tk.IntVar
    entry_suffix: tk.Entry
    intvar_make_order: tk.IntVar
    intvar_sep: tk.IntVar
    listbox_read: tk.Listbox
    listbox_preview: tk.Listbox
    radiobutton_prefix_1: tk.Radiobutton
    radiobutton_prefix_2: tk.Radiobutton
    radiobutton_prefix_3: tk.Radiobutton
    button_up: tk.Button
    button_down: tk.Button


def choose_target_directory(logic_widgets: LogicWidgets):
    strvar_tgtdir = logic_widgets['strvar_tgtdir']
    dir_name = filedialog.askdirectory(title='Choose the directory')
    strvar_tgtdir.set(dir_name)


def load_target_names(logic_widgets: LogicWidgets):
    strvar_tgtdir = logic_widgets['strvar_tgtdir']
    intvar_applyto = logic_widgets['intvar_applyto']
    listbox_read = logic_widgets['listbox_read']
    tgtdir = strvar_tgtdir.get()
    tgtnames = os.listdir(tgtdir)
    if intvar_applyto.get() == 1:
        names = [name for name in tgtnames if os.path.isfile(os.path.join(tgtdir, name))]
    else:
        names = [name for name in tgtnames if not os.path.isfile(os.path.join(tgtdir, name))]
    widget_utils.update_listbox_content(listbox_read, names)


def config_replace(logic_widgets: LogicWidgets):
    intvar_replace = logic_widgets['intvar_replace']
    entry_find = logic_widgets['entry_find']
    entry_replace = logic_widgets['entry_replace']
    enable = bool(intvar_replace.get())
    widget_utils.toggle_widget_state(entry_find, enable)
    widget_utils.toggle_widget_state(entry_replace, enable)


def config_suffix(logic_widgets: LogicWidgets):
    intvar_suffix = logic_widgets['intvar_suffix']
    entry_suffix = logic_widgets['entry_suffix']
    enable = bool(intvar_suffix.get())
    widget_utils.toggle_widget_state(entry_suffix, enable)


def config_order(logic_widgets: LogicWidgets):
    intvar_make_order = logic_widgets['intvar_make_order']
    radiobutton_prefix_1 = logic_widgets['radiobutton_prefix_1']
    radiobutton_prefix_2 = logic_widgets['radiobutton_prefix_2']
    radiobutton_prefix_3 = logic_widgets['radiobutton_prefix_3']
    button_up = logic_widgets['button_up']
    button_down = logic_widgets['button_down']
    enable = bool(intvar_make_order.get())
    widget_utils.toggle_widget_state(radiobutton_prefix_1, enable)
    widget_utils.toggle_widget_state(radiobutton_prefix_2, enable)
    widget_utils.toggle_widget_state(radiobutton_prefix_3, enable)
    widget_utils.toggle_widget_state(button_up, enable)
    widget_utils.toggle_widget_state(button_down, enable)


def move_name(logic_widgets: LogicWidgets, inc: int):
    listbox_read = logic_widgets['listbox_read']
    moved = False
    names = list(listbox_read.get(0, tk.END))
    names_dict = {idx: name for idx, name in enumerate(names)}
    if inc < 0:
        id_boundary = 0
    else:
        id_boundary = len(names_dict) - 1
    id_sel = listbox_read.curselection()[0]
    if abs(id_sel - id_boundary) > 0:
        id_next = id_sel + inc
        names_dict[id_sel], names_dict[id_next] = names_dict[id_next], names_dict[id_sel]
        moved = True
    if moved:
        keys = list(names_dict.keys())
        keys.sort()
        names = [names_dict[key] for key in keys]
        widget_utils.update_listbox_content(listbox_read, names)
        listbox_read.select_set(id_next)


def preview_names(logic_widgets: LogicWidgets):
    listbox_read = logic_widgets['listbox_read']
    listbox_preview = logic_widgets['listbox_preview']
    intvar_replace = logic_widgets['intvar_replace']
    intvar_suffix = logic_widgets['intvar_suffix']
    intvar_make_order = logic_widgets['intvar_make_order']
    entry_find = logic_widgets['entry_find']
    entry_replace = logic_widgets['entry_replace']
    entry_suffix = logic_widgets['entry_suffix']
    intvar_sep = logic_widgets['intvar_sep']
    names = list(listbox_read.get(0, tk.END))
    if intvar_replace.get():
        names = stringlist_utils.replace_names(names, entry_find.get(), entry_replace.get())
    if intvar_suffix.get():
        names = stringlist_utils.add_suffix(names, entry_suffix.get())
    if intvar_make_order.get():
        separator = {1: '_', 2: '-', 3: ' '}[intvar_sep.get()]
        names = stringlist_utils.reorder_names(names, separator)
    widget_utils.update_listbox_content(listbox_preview, names)
    widget_utils.highlight_duplicates(listbox_preview, names)


def run_rename(logic_widgets: LogicWidgets):
    strvar_tgtdir = logic_widgets['strvar_tgtdir']
    listbox_read = logic_widgets['listbox_read']
    listbox_preview = logic_widgets['listbox_preview']
    tgt_dir_name = strvar_tgtdir.get()
    names_src = list(listbox_read.get(0, tk.END))
    names_dst = list(listbox_preview.get(0, tk.END))
    name_repeated = widget_utils.highlight_duplicates(listbox_preview, names_dst)
    try:
        if name_repeated:
            raise Exception('There are repeated names after renaming.')
        else:
            for name_src, name_dst in zip(names_src, names_dst):
                path_src = os.path.join(tgt_dir_name, name_src)
                path_dst = os.path.join(tgt_dir_name, name_dst)
                os.rename(src=path_src, dst=path_dst)
    except Exception as e:
        tk.messagebox.showerror('Error', e.args[0])
        listbox_preview.delete(0, tk.END)
    else:
        tk.messagebox.showinfo('Message', 'Renamed successfully.')
        listbox_read.delete(0, tk.END)
        listbox_preview.delete(0, tk.END)

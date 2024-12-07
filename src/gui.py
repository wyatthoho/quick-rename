import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import font
from math import floor, log10


def open_dir(dir_variable: tk.StringVar):
    dir_name = filedialog.askdirectory(title='Choose the directory')
    dir_variable.set(dir_name)


def config_replace(replace_state: tk.IntVar, find_entry: tk.Entry, replace_entry: tk.Entry):
    if replace_state.get():
        find_entry.config(state='normal')
        replace_entry.config(state='normal')
    else:
        find_entry.config(state='disabled')
        replace_entry.config(state='disabled')


def config_suffix(suffix_state: tk.IntVar, suffix_entry: tk.Entry):
    if suffix_state.get():
        suffix_entry.config(state='normal')
    else:
        suffix_entry.config(state='disabled')


def config_order(order_state: tk.IntVar, prefix_radio1: tk.Radiobutton, prefix_radio2: tk.Radiobutton, prefix_radio3: tk.Radiobutton, up_btn: tk.Button, dw_btn: tk.Button):
    if order_state.get():
        prefix_radio1.config(state='normal')
        prefix_radio2.config(state='normal')
        prefix_radio3.config(state='normal')
        up_btn['state'] = tk.NORMAL
        dw_btn['state'] = tk.NORMAL
    else:
        prefix_radio1.config(state='disabled')
        prefix_radio2.config(state='disabled')
        prefix_radio3.config(state='disabled')
        up_btn['state'] = tk.DISABLED
        dw_btn['state'] = tk.DISABLED


def refresh_list_box(list_box: tk.Listbox, names: list):
    list_box.delete(0, tk.END)
    for idx, name in enumerate(names):
        list_box.insert(idx, name)


def read_names(dir_variable: tk.StringVar, apply_value: tk.IntVar, list_box_read: tk.Listbox):
    tgt_dir_name = dir_variable.get()
    dir_names = os.listdir(tgt_dir_name)

    if apply_value.get() == 1:
        names = [dir_name for dir_name in dir_names if os.path.isfile(os.path.join(tgt_dir_name, dir_name))]
    else:
        names = [dir_dame for dir_dame in dir_names if not os.path.isfile(os.path.join(tgt_dir_name, dir_dame))]

    refresh_list_box(list_box_read, names)


def move_name(inc: int, list_box_read: tk.Listbox):
    moved = False
    names = list(list_box_read.get(0, tk.END))
    names_dict = {idx: name for idx, name in enumerate(names)}

    if inc < 0:
        id_boundary = 0
    else:
        id_boundary = len(names_dict) - 1

    id_sel = list_box_read.curselection()[0]
    if abs(id_sel - id_boundary) > 0:
        id_next = id_sel + inc
        names_dict[id_sel], names_dict[id_next] = names_dict[id_next], names_dict[id_sel]
        moved = True

    if moved:
        keys = list(names_dict.keys())
        keys.sort()
        names = [names_dict[key] for key in keys]
        refresh_list_box(list_box_read, names)
        list_box_read.select_set(id_next)


def replace_names(names: list, find_entry: tk.Entry, replace_entry: tk.Entry):
    find_str = find_entry.get()
    replace_str = replace_entry.get()
    return [name.replace(find_str, replace_str) for name in names]


def add_suffix(names: list, suffix_entry: tk.Entry):
    suffix = suffix_entry.get()
    return [''.join([_str + suffix if idx == 0 else _str for idx, _str in enumerate(name.rpartition('.'))]) for name in names]


def clean_prefix(names: list):
    new_names = []
    for name in names:
        name_separated = name.partition('_')
        if name_separated[0].isdigit():
            name = name_separated[-1]

        name_separated = name.partition('-')
        if name_separated[0].isdigit():
            name = name_separated[-1]

        name_separated = name.partition(' ')
        if name_separated[0].isdigit():
            name = name_separated[-1]

        new_names.append(name)
    return new_names


def reorder_names(names: list, radio_value: tk.IntVar):
    names = clean_prefix(names)
    if radio_value.get() == 1:
        sep = '_'
    elif radio_value.get() == 2:
        sep = '-'
    elif radio_value.get() == 3:
        sep = ' '

    num_name = len(names)
    decimal = floor(log10(num_name)) + 1
    return ['{idx:{fill}{width}}{sep}{name}'.format(idx=idx, fill='0', width=decimal, sep=sep, name=name) for idx, name in enumerate(names)]


def check_repeated(list_box: tk.Listbox, names: list):
    global name_repeated
    name_repeated = False

    for idx1, name1 in enumerate(names):
        for idx2, name2 in enumerate(names[idx1+1:]):
            if name2 == name1:
                name_repeated = True
                list_box.itemconfig(idx1, {'bg': 'red'})
                list_box.itemconfig(idx1+idx2+1, {'bg': 'red'})


def preview_names(list_box_read: tk.Listbox, list_box_preview: tk.Listbox, replace_state: tk.IntVar, suffix_state: tk.IntVar, order_state: tk.IntVar, find_entry: tk.Entry, replace_entry: tk.Entry, suffix_entry: tk.Entry, radio_value: tk.IntVar):
    names = list(list_box_read.get(0, tk.END))
    if replace_state.get():
        names = replace_names(names, find_entry, replace_entry)
    if suffix_state.get():
        names = add_suffix(names, suffix_entry)
    if order_state.get():
        names = reorder_names(names, radio_value)

    refresh_list_box(list_box_preview, names)
    check_repeated(list_box_preview, names)


def run_rename(dir_variable: tk.StringVar, list_box_read: tk.Listbox, list_box_preview: tk.Listbox):
    tgt_dir_name = dir_variable.get()
    names_src = list(list_box_read.get(0, tk.END))
    names_dst = list(list_box_preview.get(0, tk.END))

    try:
        if name_repeated:
            raise Exception('There are repeated names after renaming.')
        else:
            for name_src, name_dst in zip(names_src, names_dst):
                path_src = os.path.join(tgt_dir_name, name_src)
                path_dst = os.path.join(tgt_dir_name, name_dst)
                os.rename(src=path_src, dst=path_dst)
    except Exception as e:
        tk.messagebox.showerror("Error", e.args[0])
        list_box_preview.delete(0, tk.END)
    else:
        tk.messagebox.showinfo("Message", "Renamed successfully.")
        list_box_read.delete(0, tk.END)
        list_box_preview.delete(0, tk.END)


class App:
    NAME = 'QuickRename'

    def __init__(self):
        self.root = self.initialize_main_window()
        self.font_label = font.Font(family='Helvetica', size=10)
        self.font_btn = font.Font(family='Helvetica', size=10)
        self.create_frame_up()
        self.create_frame_mid()
        self.create_frame_dw()
        self.root.mainloop()

    def initialize_main_window(self):
        root = tk.Tk()
        root.title(App.NAME)
        logopath = Path(__file__).parent.parent.joinpath('image', 'w.ico')
        root.iconbitmap(logopath)
        root.resizable(width=0, height=0)
        return root
    
    def create_frame_up(self):
        frame_up = tk.LabelFrame(self.root, text='Choose the directory')
        frame_up.grid(row=0, column=0, padx=4, pady=4, ipadx=1, ipady=1, sticky=tk.W)
        frame_up['font'] = self.font_label

        frame_up_up = tk.Frame(frame_up)
        frame_up_up.grid(row=0, column=0)

        frame_up_dw = tk.Frame(frame_up)
        frame_up_dw.grid(row=1, column=0, sticky=tk.W)

        frame_up_right = tk.Frame(frame_up)
        frame_up_right.grid(row=0, column=1, rowspan=2)

        self.dir_variable = tk.StringVar()
        tgt_dir_str_entry = tk.Entry(frame_up_up, width=50, textvariable=self.dir_variable)
        tgt_dir_str_entry.grid(row=0, column=0, padx=4, pady=4)

        apply_label = tk.Label(frame_up_dw, text='Apply to:')
        apply_label.grid(row=0, column=0, padx=4)

        self.apply_value = tk.IntVar()
        file_radio = tk.Radiobutton(frame_up_dw, text='Files', variable=self.apply_value, value=1)
        file_radio.grid(row=0, column=1)

        folder_radio = tk.Radiobutton(frame_up_dw, text='Folders', variable=self.apply_value, value=2)
        folder_radio.grid(row=0, column=2)
        self.apply_value.set(1)

        choose_btn = tk.Button(frame_up_right, text='Choose', command=lambda: open_dir(self.dir_variable), width=6)
        choose_btn.grid(row=0, column=0, padx=4, pady=4, ipadx=1, ipady=1)
        choose_btn['font'] = self.font_btn

        read_btn = tk.Button(frame_up_right, text='Read', command=lambda: read_names(self.dir_variable, self.apply_value, self.list_box_read), width=6)
        read_btn.grid(row=1, column=0, padx=4, pady=4, ipadx=1, ipady=1)
        read_btn['font'] = self.font_btn

    def create_frame_mid(self):
        frame_mid = tk.LabelFrame(self.root, text='Naming method')
        frame_mid.grid(row=1, column=0, padx=4, pady=4, ipadx=1, ipady=1, sticky=tk.W)
        frame_mid['font'] = self.font_label

        frame_mid_up = tk.Frame(frame_mid)
        frame_mid_up.grid(row=0, column=0, sticky=tk.W)

        frame_mid_mid = tk.Frame(frame_mid)
        frame_mid_mid.grid(row=1, column=0, sticky=tk.W)

        frame_mid_dw = tk.Frame(frame_mid)
        frame_mid_dw.grid(row=2, column=0, sticky=tk.W)

        self.replace_state = tk.IntVar()
        replace_check_btn = tk.Checkbutton(frame_mid_up, text='Replace text', command=lambda: config_replace(self.replace_state, self.find_entry, self.replace_entry), variable=self.replace_state, onvalue=1, offvalue=0)
        replace_check_btn.grid(row=0, column=0, padx=4, pady=4)

        find_label = tk.Label(frame_mid_up, text='Find:')
        find_label.grid(row=0, column=1, padx=4, pady=4)

        self.find_entry = tk.Entry(frame_mid_up, width=13)
        self.find_entry.grid(row=0, column=2, padx=4, pady=4)
        self.find_entry.config(state='disabled')

        replace_label = tk.Label(frame_mid_up, text='Replace:')
        replace_label.grid(row=0, column=3, padx=4, pady=4)

        self.replace_entry = tk.Entry(frame_mid_up, width=13)
        self.replace_entry.grid(row=0, column=4, padx=4, pady=4)
        self.replace_entry.config(state='disabled')

        self.suffix_state = tk.IntVar()
        suffix_sheck_btn = tk.Checkbutton(frame_mid_mid, text='Add suffix', command=lambda: config_suffix(self.suffix_state, self.suffix_entry), variable=self.suffix_state, onvalue=1, offvalue=0)
        suffix_sheck_btn.grid(row=0, column=0, padx=4, pady=4)

        suffix_label = tk.Label(frame_mid_mid, text='Suffix:')
        suffix_label.grid(row=0, column=1, padx=4, pady=4)

        self.suffix_entry = tk.Entry(frame_mid_mid, width=13)
        self.suffix_entry.grid(row=0, column=2, padx=4, pady=4)
        self.suffix_entry.config(state='disabled')

        self.order_state = tk.IntVar()
        order_check_btn = tk.Checkbutton(frame_mid_dw, text='Make an order', command=lambda: config_order(self.order_state, prefix_radio1, prefix_radio2, prefix_radio3, self.up_btn, self.dw_btn), variable=self.order_state, onvalue=1, offvalue=0)
        order_check_btn.grid(row=1, column=0, padx=4, pady=4)

        sep_label = tk.Label(frame_mid_dw, text='Sep:')
        sep_label.grid(row=1, column=1, padx=4, pady=4)

        self.radio_value = tk.IntVar()
        prefix_radio1 = tk.Radiobutton(frame_mid_dw, text='_', variable=self.radio_value, value=1)
        prefix_radio1.grid(row=1, column=2, padx=4, pady=4)
        prefix_radio1.config(state='disabled')

        prefix_radio2 = tk.Radiobutton(frame_mid_dw, text='-', variable=self.radio_value, value=2)
        prefix_radio2.grid(row=1, column=3, padx=4, pady=4)
        prefix_radio2.config(state='disabled')

        prefix_radio3 = tk.Radiobutton(frame_mid_dw, text='space', variable=self.radio_value, value=3)
        prefix_radio3.grid(row=1, column=4, padx=4, pady=4)
        prefix_radio3.config(state='disabled')
        self.radio_value.set(1)

    def create_frame_dw(self):
        frame_dw = tk.LabelFrame(self.root, text='Name list')
        frame_dw.grid(row=2, column=0, padx=4, pady=4, ipadx=1, ipady=1, sticky=tk.W)
        frame_dw['font'] = self.font_label

        frame_dw_left = tk.Frame(frame_dw)
        frame_dw_left.grid(row=0, column=0)

        scrollbar_read_x = tk.Scrollbar(frame_dw_left, orient=tk.HORIZONTAL)
        scrollbar_read_y = tk.Scrollbar(frame_dw_left, orient=tk.VERTICAL)

        scrollbar_read_x.grid(row=1, column=0, sticky=tk.EW)
        scrollbar_read_y.grid(row=0, column=1, sticky=tk.NS)

        self.list_box_read = tk.Listbox(frame_dw_left, width=22, xscrollcommand=scrollbar_read_x.set, yscrollcommand=scrollbar_read_y.set)
        self.list_box_read.grid(row=0, column=0, padx=4, pady=4)

        scrollbar_read_x.config(command=self.list_box_read.xview)
        scrollbar_read_y.config(command=self.list_box_read.yview)

        scrollbar_preview_x = tk.Scrollbar(frame_dw_left, orient=tk.HORIZONTAL)
        scrollbar_preview_y = tk.Scrollbar(frame_dw_left, orient=tk.VERTICAL)

        scrollbar_preview_x.grid(row=1, column=2, sticky=tk.EW)
        scrollbar_preview_y.grid(row=0, column=3, sticky=tk.NS)

        list_box_preview = tk.Listbox(frame_dw_left, width=22, xscrollcommand=scrollbar_preview_x.set, yscrollcommand=scrollbar_preview_y.set)
        list_box_preview.grid(row=0, column=2, padx=4, pady=4)

        scrollbar_preview_x.config(command=list_box_preview.xview)
        scrollbar_preview_y.config(command=list_box_preview.yview)

        frame_dw_right = tk.Frame(frame_dw)
        frame_dw_right.grid(row=0, column=1)

        up_btn = tk.Button(frame_dw_right, text='Up', command=lambda: move_name(-1, self.list_box_read), width=6)
        dw_btn = tk.Button(frame_dw_right, text='Down', command=lambda: move_name(1, self.list_box_read), width=6)
        pre_btn = tk.Button(frame_dw_right, text='Preview', command=lambda: preview_names(self.list_box_read, list_box_preview, self.replace_state, self.suffix_state, self.order_state, self.find_entry, self.replace_entry, self.suffix_entry, self.radio_value), width=6)
        run_btn = tk.Button(frame_dw_right, text='Run', command=lambda: run_rename(self.dir_variable, self.list_box_read, list_box_preview), width=6)
        up_btn['state'] = tk.DISABLED
        dw_btn['state'] = tk.DISABLED

        for idx, widget in enumerate(frame_dw_right.winfo_children()):
            widget.grid(row=idx, column=0, padx=4, pady=4, ipadx=1, ipady=1)
            widget['font'] = self.font_btn


if __name__ == '__main__':
    App()

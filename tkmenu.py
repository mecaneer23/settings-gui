#!/usr/bin/env python3
# pyright: reportMissingImports=false

import customtkinter as ctk
import json


def read_file_json(filename):
    with open(filename) as f:
        return json.load(f)


def write_file_json(filename, contents):
    with open(filename, "w") as f:
        json.dump(contents, f, indent=4)


def get_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Settings file to open")
    return parser.parse_args()


RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
RESET = "\033[0m"


def info(message):
    print(f"{CYAN}INFO:{RESET} {message}")


class App(ctk.CTk):
    def __init__(self, filename, filetype="json", **kwargs):
        ctk.CTk.__init__(self, **kwargs)
        self.title(filename)
        self.geometry("400x150")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = Menu(
            master=self,
            filename=filename,
            filetype=filetype,
            width=300,
            height=200,
            corner_radius=0,
            fg_color="transparent",
        )
        self.my_frame.grid(row=0, column=0, sticky="nsew")


class Menu(ctk.CTkScrollableFrame):
    def __init__(self, filename, filetype, **kwargs):
        ctk.CTkScrollableFrame.__init__(self, **kwargs)
        self.filename = filename
        self.items = read_file_json(self.filename)
        self.display_rows = []
        for index, (key, value) in enumerate(self.items.items()):
            self.make_display_box(index, key, value)

    def make_display_box(self, index, key, value):
        self.display_rows.insert(index, [ctk.CTkLabel(self, text=key), None, None])
        self.display_rows[index][1] = self.display(index, key, value)
        self.display_rows[index][0].grid(row=index, column=0)
        self.display_rows[index][1].grid(row=index, column=1, padx=10)

    def display_boolean(self, index, key, value):
        switch = ctk.CTkSwitch(
            self,
            text=" ",
            command=lambda: self.update_bool(index, key, switch),
        )
        switch.select() if value else switch.deselect()
        return switch

    def update_bool(self, index, key, switch):
        item = self.display_rows[index][1]
        item.select() if switch.get() else item.deselect()
        self.write(key, bool(switch.get()))

    def display_int(self, index, key, value):
        box = ctk.CTkFrame(self)
        entry_var = ctk.StringVar(box, value=str(value))
        entry = ctk.CTkEntry(box, textvariable=entry_var)
        entry.grid(row=0, column=0, rowspan=2)
        entry.bind(
            "<Return>", lambda _: self.update_int(index, key, int(entry_var.get()))
        )
        ctk.CTkButton(
            box,
            text="▲",
            width=10,
            height=8,
            command=lambda: self.update_int(index, key, int(entry_var.get()) + 1),
        ).grid(row=0, column=1)
        ctk.CTkButton(
            box,
            text="▼",
            width=10,
            height=8,
            command=lambda: self.update_int(index, key, int(entry_var.get()) - 1),
        ).grid(row=1, column=1)
        self.display_rows[index][2] = entry_var
        return box

    def update_int(self, index, key, value):
        self.display_rows[index][2].set(value)
        self.write(key, value)

    def display_string(self, index, key, value):
        box = ctk.CTkFrame(self)
        entry_var = ctk.StringVar(box, value=str(value))
        entry = ctk.CTkEntry(box, textvariable=entry_var)
        entry.grid(row=0, column=0)
        entry.bind(
            "<Return>", lambda _: self.update_string(index, key, entry_var.get())
        )
        self.display_rows[index][2] = entry_var
        return box

    def update_string(self, index, key, value):
        self.display_rows[index][2].set(value)
        self.write(key, value)

    def write(self, key, value):
        original_value = self.items[key]
        self.items[key] = value
        write_file_json(self.filename, self.items)
        info(f"set `{key}` to `{value}` (was `{original_value}`)")

    def display(self, index, key, value):
        if isinstance(value, bool):
            return self.display_boolean(index, key, value)
        elif isinstance(value, int):
            return self.display_int(index, key, value)
        elif isinstance(value, str):
            return self.display_string(index, key, value)
        else:
            print(f"Unknown type for {{{key}: {value}}}:", type(value))


def main(filename):
    menu = App(filename)
    menu.mainloop()


if __name__ == "__main__":
    main(get_args().filename)

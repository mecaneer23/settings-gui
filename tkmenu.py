#!/usr/bin/env python3
# pyright: reportMissingImports=false

import customtkinter as ctk


def read_file_json(filename):
    import json

    with open(filename) as f:
        return json.load(f)


def write_file_json(filename, contents):
    import json

    with open(filename, "w") as f:
        json.dump(contents, f, indent=4)


def get_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Settings file to open")
    return parser.parse_args()


class Menu(ctk.CTk):
    def __init__(self, filename, filetype="json", **kwargs):
        ctk.CTk.__init__(self, **kwargs)
        self.title(filename)
        self.geometry("400x150")
        self.filename = filename
        self.items = read_file_json(self.filename)
        for index, (key, value) in enumerate(self.items.items()):
            self.make_display_box(index, key, value)

    def make_display_box(self, index, key, value):
        ctk.CTkLabel(self, text=key).grid(row=index, column=0)
        self.display(index, key, value).grid(row=index, column=1, padx=10)

    def display_boolean(self, index, key, value):
        switch_value = ctk.StringVar(value=value)
        switch = ctk.CTkSwitch(self, text=" ", command=lambda: self.write(index, key, bool(int(switch_value.get()))), variable=switch_value)
        return switch

    def display_int(self, index, key, value):
        # box = ctk.Box()
        # entry = Gtk.Entry()
        # entry.set_text(str(value))
        # box.pack_start(entry, False, True, 0)
        # button_box = Gtk.VBox()
        # up_button = Gtk.Button()
        # up_button.add(
        #     Gtk.Arrow(arrow_type=Gtk.ArrowType.UP, shadow_type=Gtk.ShadowType.NONE)
        # )
        # up_button.connect("clicked", lambda _: self.write_int(index, key, value + 1))
        # button_box.pack_start(up_button, True, True, 0)
        # down_button = Gtk.Button()
        # down_button.add(
        #     Gtk.Arrow(arrow_type=Gtk.ArrowType.DOWN, shadow_type=Gtk.ShadowType.NONE)
        # )
        # down_button.connect("clicked", lambda _: self.write_int(index, key, value - 1))
        # button_box.pack_start(down_button, True, True, 0)
        # box.pack_start(button_box, True, True, 0)
        # return box
        return ctk.CTkLabel(self, text="hello world")

    def write(self, index, key, value):
        self.items[key] = value
        write_file_json(self.filename, self.items)
        self.make_display_box(index, key, value)

    def display(self, index, key, value):
        if isinstance(value, bool):
            return self.display_boolean(index, key, value)
        elif isinstance(value, int):
            return self.display_int(index, key, value)
        else:
            print(f"Unknown type for {{{key}: {value}}}:", type(value))


def main(filename):
    menu = Menu(filename)
    menu.mainloop()


if __name__ == "__main__":
    main(get_args().filename)

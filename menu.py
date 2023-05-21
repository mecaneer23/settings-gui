#!/usr/bin/env python3

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


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


class Menu(Gtk.Window):
    def __init__(self, filename, filetype="json", **kwargs):
        Gtk.Window.__init__(self, **kwargs)
        self.connect("destroy", Gtk.main_quit)
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.filename = filename
        self.items = read_file_json(self.filename)
        for index, (key, value) in enumerate(self.items.items()):
            self.make_display_box(index, key, value)

    def make_display_box(self, index, key, value):
        box = Gtk.Box()
        box.set_spacing(5)
        box.pack_start(Gtk.Label(label=key), False, True, 0)
        box.pack_start(self.display(index, key, value), True, False, 0)
        self.grid.attach(box, 0, index, 1, 1)

    def display_boolean(self, index, key, value):
        switch = Gtk.Switch()
        switch.set_active(value)
        switch.connect("notify::active", lambda s, _: self.write_boolean(index, key, s))
        return switch

    def write_boolean(self, index, key, switch):
        self.items[key] = switch.get_active()
        write_file_json(self.filename, self.items)
        self.make_display_box(index, key, switch.get_active())

    def display_int(self, index, key, value):
        box = Gtk.Box()
        entry = Gtk.Entry()
        entry.set_text(str(value))
        box.pack_start(entry, False, True, 0)
        button_box = Gtk.VBox()
        up_button = Gtk.Button()
        up_button.add(
            Gtk.Arrow(arrow_type=Gtk.ArrowType.UP, shadow_type=Gtk.ShadowType.NONE)
        )
        up_button.connect("clicked", lambda _: self.write_int(index, key, value + 1))
        button_box.pack_start(up_button, True, True, 0)
        down_button = Gtk.Button()
        down_button.add(
            Gtk.Arrow(arrow_type=Gtk.ArrowType.DOWN, shadow_type=Gtk.ShadowType.NONE)
        )
        down_button.connect("clicked", lambda _: self.write_int(index, key, value - 1))
        button_box.pack_start(down_button, True, True, 0)
        box.pack_start(button_box, True, True, 0)
        return box

    def write_int(self, index, key, value):
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
    menu = Menu(filename, title=filename)
    menu.show_all()
    Gtk.main()


if __name__ == "__main__":
    main(get_args().filename)

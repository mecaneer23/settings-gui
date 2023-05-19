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
            self.grid.attach(Gtk.Label(label=key), 0, index, 1, 1)
            self.grid.attach(self.display(key, value), 1, index, 1, 1)

    def display_boolean(self, key, value):
        switch = Gtk.Switch()
        switch.set_active(value)
        switch.connect("notify::active", lambda s, _: self.write_boolean(key, s))
        return switch

    def display_int(self, key, value):
        return Gtk.Entry()

    def display(self, key, value):
        if isinstance(value, bool):
            return self.display_boolean(key, value)
        elif isinstance(value, int):
            return self.display_int(key, value)
        else:
            print(f"Unknown type for {{{key}: {value}}}:", type(value))

    def write_boolean(self, key, switch,):
        self.items[key] = switch.get_active()
        write_file_json(self.filename, self.items)


def main(filename):
    menu = Menu(filename, title=filename)
    menu.show_all()
    Gtk.main()


if __name__ == "__main__":
    main(get_args().filename)

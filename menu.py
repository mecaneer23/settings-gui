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
        json.dump(contents, f)


def get_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Settings file to open")
    return parser.parse_args()


def display_boolean(value):
    return Gtk.Switch()


def display_int(value):
    return Gtk.Entry()


def display(value):
    if isinstance(value, bool):
        return display_boolean(value)
    elif isinstance(value, int):
        return display_int(value)
    else:
        print("Unknown type:", type(value))


def main(filename):
    window = Gtk.Window(title=filename)
    grid = Gtk.Grid()
    for i, (k, v) in enumerate(read_file_json(filename).items()):
        grid.attach(Gtk.Label(label=k), 0, i, 1, 1)
        grid.attach(display(v), 1, i, 1, 1)
    window.add(grid)
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    args = get_args()
    main(args.filename)

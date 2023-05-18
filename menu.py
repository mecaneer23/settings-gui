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


def display_boolean():
    pass


def display_int():
    pass


def main(filename):
    window = Gtk.Window()
    window.add(Gtk.Label(label=filename))
    button = Gtk.Button(label="CLick me")
    button.connect("clicked", lambda e: print("clicked"))
    window.add(button)
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    args = get_args()
    main(args.filename)

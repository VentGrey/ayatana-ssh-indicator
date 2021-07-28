#!/usr/bin/python3
# -*- coding: utf-8 -*-
#


import os
from subprocess import Popen
import sys

from gi.repository import Gtk, GObject
from gi.repository import AyatanaAppIndicator3 as appindicator

from gi import require_version

require_version('AyatanaAppIndicator3', '0.1')
require_version('Gtk', '3.0')


class StormIndicator(object):

    def __init__(self):

        self.app = appindicator.Indicator.new(
            "storm-ssh-indicator",
            "gnome-netstatus-tx",
            3
        )

        self.app.set_status(appindicator.IndicatorStatus.ACTIVE)

        self.menu = Gtk.Menu()

    def menu_item_callback(self, w, identifier):
        if identifier == 'about':
            self.pop_dialog("storm-indicator is a helper for connecting to your servers easily."
                            "\n\nyou can use the <a href='https://github.com/emre/storm-indicator/issues'>issue"
                            "tracker</a> for bug reports and feature requests")

        elif identifier == 'quit':
            sys.exit(0)
        else:
            self.run_program(["gnome-terminal", "-e", "bash -c \"ssh %s; exec bash;\"" % identifier])

    def add_menu_item(self, text, value=None, sensitive=True):
        menu_item = Gtk.MenuItem(text)
        menu_item.set_sensitive(sensitive)
        menu_item.show()

        if sensitive:
            menu_item.connect("activate", self.menu_item_callback, value)

        self.menu.append(menu_item)

    def add_seperator(self):
        separator = Gtk.SeparatorMenuItem()
        separator.show()
        self.menu.append(separator)

    def run(self):
        self.app.set_menu(self.menu)
        Gtk.main()

    def run_program(self, cmd):
        Popen(cmd)

    def pop_dialog(self, message, error=False):
        if error:
            icon = Gtk.MESSAGE_ERROR
        else:
            icon = Gtk.MESSAGE_INFO
        md = Gtk.MessageDialog(None, 0, icon, Gtk.BUTTONS_OK)
        try:
            md.set_markup("<b>storm-indicator</b>")
            md.format_secondary_markup(message)
            md.run()
        finally:
            md.destroy()

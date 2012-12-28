#!/usr/bin/python
# GTk FX Notification
# Copyright (C) 2012 TANIGUCHI Takaki <takaki@asis.media-as.org>
# This program is free software: you can redistribute it and/or modify
# 
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

ICON_PATH = '/usr/share/icons/gfxn.png'
RATE_URL = "https://fx.click-sec.com/ygmo/rate.csv?client=FxFlashQuoteRIA_2008101"


from gi.repository import Gtk,Gdk
import glib
import cairo
from StringIO import StringIO
import urllib
import csv

NAME = 'GFXN'
VERSION = '0.5'

class GFXNIcon:
    def __init__(self):

        self.currencies = []
        self.currency = 'USD/JPY'
        self.interval = 5
        self.val = 0

        self.statusicon = Gtk.StatusIcon.new()
        self.statusicon.connect("popup-menu", self.right_click_event)
        self.statusicon.set_title("gfxn")
        self.statusicon.set_tooltip_text(NAME + '\n' + self.currency)

        self.update_icon()
        self.taskid = glib.timeout_add(self.interval * 1000, self.update_icon)

    def update_currency(self, widget, currency):
        self.currency = currency
        self.statusicon.set_tooltip_text('fx icon\n' + self.currency)
        self.update_icon()

    def update_interval(self, widget, interval):
        self.interval = interval
        glib.source_remove(self.taskid)
        self.taskid = glib.timeout_add(self.interval * 1000, self.update_icon)

    def right_click_event(self, icon, button, time):
        menu = Gtk.Menu()

        currency = Gtk.MenuItem()
        currency.set_label("Currency")
        submenu = Gtk.Menu()
        for i in self.currencies:
            c = Gtk.RadioMenuItem('currency')
            c.set_label(i)
            if i == self.currency:
                c.set_active(True)
            c.connect("toggled", self.update_currency, i)
            submenu.append(c)
        currency.set_submenu(submenu)
        menu.append(currency)

        interval = Gtk.MenuItem()
        interval.set_label("Update interval")
        submenu = Gtk.Menu()
        for i in [1, 3, 5, 10, 30, 60]:
            c = Gtk.RadioMenuItem('interval')
            c.set_label(str(i))
            if i == self.interval:
                c.set_active(True)
            c.connect("toggled", self.update_interval, i)
            submenu.append(c)
        interval.set_submenu(submenu)
        menu.append(interval)

        about = Gtk.MenuItem()
        about.set_label("About")
        about.connect("activate", self.show_about_dialog)
        menu.append(about)

        quit = Gtk.MenuItem()
        quit.set_label("Quit")
        quit.connect("activate", Gtk.main_quit)
        menu.append(quit)

        menu.show_all()

        def pos(menu, icon):
            return (Gtk.StatusIcon.position_menu(menu, icon))

        menu.popup(None, None, pos, self.statusicon, button, time)

    def update_icon(self):

        val = 0
        self.currencies = []
        try:
            rate = urllib.urlopen(RATE_URL)
        except IOError:
            return True

        for i in csv.reader(rate):
            self.currencies.append(i[0])
            if i[0] == self.currency:
                val = i[1]

        s1 = val[0:-3]
        s2 = val[-3:]

        image = cairo.ImageSurface.create_from_png(ICON_PATH)
        width = image.get_width()
        height = image.get_height()

        bg = cairo.ImageSurface(cairo.FORMAT_ARGB32,width, height)
        crbg = cairo.Context(bg)
        if float(val) > self.val:
            crbg.set_source_rgb(0.8, 1.0, 0.8)
        elif float(val) < self.val:
            crbg.set_source_rgb(1.0, 0.8, 0.8)
        else:
            crbg.set_source_rgb(1,1,1)
        self.val = float(val)
        crbg.rectangle(0,0,width,height)
        crbg.fill()
        
        cr = cairo.Context(image)
        cr.set_font_size(120)
        cr.select_font_face("monospace", cairo.FONT_SLANT_NORMAL,
            cairo.FONT_WEIGHT_BOLD)
        cr.set_source_rgb(0,0,0)
        cr.move_to(0,128 - 16)
        cr.show_text("%s" % s1)
        cr.move_to(0,256-16)
        cr.show_text("%s" % s2)
        crbg.set_source_surface(image)
        crbg.paint()

        pixbuf = Gdk.pixbuf_get_from_surface(bg, 0,0,width,height)

        self.statusicon.set_from_pixbuf(pixbuf)

        return True

    def show_about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("Gtk FX Notification")
        about_dialog.set_version(VERSION)
        about_dialog.set_copyright("2012 Copyright(c) TANIGUCHI Takaki")
        about_dialog.set_comments("Gtk FX Notification")
        about_dialog.set_website("http://github.com/takaki/gfxn")
        about_dialog.set_website_label("Website(GitHub)")
        about_dialog.set_authors(["TANIGUCHI, Takaki"])

        about_dialog.set_license_type(Gtk.License.GPL_3_0)

        about_dialog.run()
        about_dialog.destroy()

from gi.repository import Gtk




def run():
    gfxn = GFXNIcon()
    Gtk.main()

if __name__ == "__main__":
    run()

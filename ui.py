"""
UNRFavorites (C) 2009 Erik Youngren <artanis.00@gmail.com>
"""
import os
import gtk
import gtk.glade
from glib import GError

from SimpleGladeApp import SimpleGladeApp

import GConfFavs

DEFAULT_ICON = "gnome-fs-bookmark"
WINDOW_ICON  = "gnome-fs-bookmark"

def load_icon(path, size=64):
    theme = gtk.icon_theme_get_default()
    pixbuf = theme.load_icon(DEFAULT_ICON, size, gtk.ICON_LOOKUP_FORCE_SVG)
    
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(path, size, size)
    except GError:
        try:
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                "/usr/share/app-install/icons/%s" % (path,) ,size, size)
        except GError:
            pixbuf = theme.load_icon(path, size, gtk.ICON_LOOKUP_FORCE_SVG)
    
    return pixbuf

class FavoritesStore(gtk.ListStore):
    def __init__(self):
        gtk.ListStore.__init__(self, gtk.gdk.Pixbuf, str, str)
        
        self.favlist = GConfFavs.FavoritesList()
        
        for fav in self.favlist.list_active():
            favorite = GConfFavs.Favorite(fav)
            self.append([load_icon(favorite.icon_path), favorite.name, favorite.entry_name])

class FavoritesManager(SimpleGladeApp):
    def __init__(self):
        SimpleGladeApp.__init__(self,
            os.path.dirname(__file__)+"/ui.glade")
        
        store = FavoritesStore()
        
        self.wxIconView.set_model(store)
        self.wxIconView.set_text_column(1)
        self.wxIconView.set_pixbuf_column(0)
        
        gtk.window_set_default_icon(load_icon(WINDOW_ICON))
    
    def on_wxToolbarBtnSave_clicked(self, button):
        model = self.wxIconView.get_model()
        
        new_order = []
        for row in model:
            new_order.append(row[2])
        
        favlist = GConfFavs.FavoritesList()
        favlist.replace(new_order)
    
    def run(self):
        self.wxMain.show_all()
        SimpleGladeApp.run(self)


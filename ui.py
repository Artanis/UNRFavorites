import gtk
import gtk.glade

from SimpleGladeApp import SimpleGladeApp

import GConfFavs

class FavoritesStore(gtk.ListStore):
    def __init__(self):
        gtk.ListStore.__init__(self, gtk.gdk.Pixbuf, str, str)
        
        self.favlist = GConfFavs.FavoritesList()
        
        for fav in self.favlist.list_active():
            favorite = GConfFavs.Favorite(fav)
            icon_path = favorite.icon_path
            pixbuf = None
            theme = gtk.icon_theme_get_default()
            if icon_path is not None:
                if icon_path[0] == "/":
                    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icon_path, 64, 64)
                else:
                    pixbuf = theme.load_icon(icon_path, 64, gtk.ICON_LOOKUP_FORCE_SVG)
            else:
                pixbuf = theme.load_icon("gnome-fs-bookmark", 64, gtk.ICON_LOOKUP_FORCE_SVG)
            
            self.append([pixbuf, favorite.name, favorite.entry_name])

class FavoritesManager(SimpleGladeApp):
    def __init__(self):
        SimpleGladeApp.__init__(self, "ui.glade")
        
        store = FavoritesStore()
        
        self.wxIconView.set_model(store)
        self.wxIconView.set_text_column(1)
        self.wxIconView.set_pixbuf_column(0)
    
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


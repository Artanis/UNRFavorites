import re
import gconf
import PyGConf

client = gconf.client_get_default()

favorites_key = "/apps/netbook-launcher/favorites"
favorites_list = "%s/favorites_list" % favorites_key
favorites_desktop = "%s/%%s/desktop_file" % favorites_key
favorites_type = "%s/%%s/type" % favorites_key

class FavoritesList(PyGConf.List):
    def __init__(self):
        PyGConf.List.__init__(self, favorites_list, gconf.VALUE_STRING)
    
    def add(self, favorite):
        if favorite.name not in self:
            self.append(favorite.name)
    
    def remove(self, favorite):
        if favorite.name in self:
            del self[self.index(favorite.name)]
    
    def list_active(self):
        for fav in self:
            yield fav
    
    @staticmethod
    def list_all():
        favorites = client.all_dirs(favorites_key)
        for fav in favorites:
            yield fav[fav.rindex("/")+1:]

class Favorite(object):
    def __init__(self, name):
        self.entry_name = name
        
        self.desktop_file = PyGConf.String(favorites_desktop % self.entry_name)
        self.type = PyGConf.String(favorites_type % self.entry_name)
    
    @property
    def name(self):
        return self.__from_desktop_file("Name")
    
    def __from_desktop_file(self, regex):
        desktop_file = open(str(self.desktop_file)).read()
        
        match = re.search(regex+"=(.*)", desktop_file)
        
        if match is not None:
            return match.group(1)
        else:
            return None
    
    def is_active(self):
        return self.name in FavoritesList.list_all()
    
    @property
    def icon_path(self):
        return self.__from_desktop_file("Icon")
    
    @staticmethod
    def new(name, desktop_file, type_):
        favorite = Favorite(name)
        
        favorite.desktop_file._write(desktop_file)
        favorite.type._write(type_)
        
        return favorite
    
    def __str__(self):
        fav_list = FavoritesList()
        return """[%s] %s (%s)""" % (self.type, self.name,
            "Active" if self.is_active() else "Inactive")
    
    def __repr__(self):
        return """Favorite("%s")""" % (self.name,)

import gconf

client = gconf.client_get_default()

class Key(object):
    def __init__(self, key, type_):
        self.key = key
        self.type = type_
    
    def _read(self):
        raise NotImplementedError
    
    def _write(self, value):
        raise NotImplementedError
    
    def __repr__(self):
        raise NotImplementedError
    
    def __str__(self):
        return str(self._read())

class Integer(Key):
    def __init__(self, key):
        Key.__init__(self, key, gconf.VALUE_INT)
        
    def _read(self):
        return client.get_int(self.key)
    
    def _write(self, value):
        raise NotImplementedError

class Boolean(Key):
    def __init__(self, key):
        Key.__init__(self, key, gconf.VALUE_BOOL)
        
    def _read(self):
        return client.get_bool(self.key)
    
    def _write(self, value):
        raise NotImplementedError

class String(Key):    
    def __init__(self, key):
        Key.__init__(self, key, gconf.VALUE_STRING)
    
    def _read(self):
        return client.get_string(self.key)
    
    def _write(self, value):
        return client.set_string(self.key, value)

class Float(Key):
    def __init__(self, key):
        Key.__init__(self, key, gconf.VALUE_FLOAT)
    
    def _read(self):
        return client.get_float(self.key)
    
    def _write(self, value):
        raise NotImplementedError

class List(Key):
    def __init__(self, key, type_):
        Key.__init__(self, key, gconf.VALUE_LIST)
        self.list_type = type_
    
    def append(self, value):
        data = self._read()
        data.append(value)
        self._write(data)
    
    def extend(self, value):
        data = self._read()
        data.extend(value)
        self._write(data)
    
    def index(self, x, i=None, j=None):
        return self._read().__index__(x, i, j)
    
    def replace(self, value):
        """ Replaces the all values of the key with the provided values.
        
        """
        
        self._write(value)
    
    def _read(self):
        return client.get_list(self.key, self.list_type)
    
    def _write(self, data):
        client.set_list(self.key, self.list_type, data)
    
    def __getitem__(self, index):
        data = self._read()
        return data.__getitem__(index)
    
    def __setitem__(self, index, value):
        data = self._read()
        data.__setitem__(index, value)
        self._write(data)
    
    def __delitem__(self, index):
        data = self._read()
        data.__delitem__(index)
        self._write(data)
    
    def __len__(self):
        return len(self._read())
    
    def __contains__(self, item):
        return item in self._read()
    
    def __iter__(self):
        return iter(self._read())
    
    def __reversed__(self):
        return reversed(self._read())
    
    def __missing__(self):
        raise NotImplementedError
    
    def __length_hint__(self):
        raise NotImplementedError
    
    def __str__(self):
        return str(self[:])

if __name__ == "__main__":
    lst = List("/testing/list", gconf.VALUE_STRING)
    


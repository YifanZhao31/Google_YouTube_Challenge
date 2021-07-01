"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    playlists_dict = {} 
    lists_dict = {}

    def __init__(self, name: str, contents):
        self._playlists = {}
        self._name = name
        self._contents = contents
        l_name = name.lower()
        Playlist.playlists_dict[l_name] = self
        Playlist.lists_dict[name] = self
    
    def contents(self):
        return self

"""Dictionary with auto-expiring values for caching purposes."""

from time import time
from threading import RLock
from collections import OrderedDict


class ExpiringDict(OrderedDict):
    """Dictionary with auto-expiring values for caching purposes."""

    def __init__(self, max_len, max_age_seconds, callback=None):  # noqa
        super().__init__(self)
        self.max_len = max_len
        self.max_age = max_age_seconds
        self.callback = callback
        self.lock = RLock()
        self._safe_keys = lambda: list(self.keys())

    def inform(self, key, value, type_of="evicting"):
        """Dispatch callback for ttl items."""
        if self.callback is not None:
            self.callback(key, value, type_of)

    def __contains__(self, key):
        """Return True if the dict has a key, else return False."""
        try:
            with self.lock:
                item = super().__getitem__(key)
                if time() - item[1] < self.max_age:
                    return True
                del self[key]
                self.inform(key, item[0])
        except KeyError:
            pass
        return False

    def __getitem__(self, key, with_age=False):
        """Return the item of the dict.

        Raises a KeyError if key is not in the map.
        """
        with self.lock:
            item = super().__getitem__(key)
            item_age = time() - item[1]
            if item_age < self.max_age:
                if with_age:
                    return item[0], item_age
                return item[0]
            del self[key]
            self.inform(key, item[0])
            # return None
            raise KeyError(key)

    def __setitem__(self, key, value):
        """Set d[key] to value."""
        with self.lock:
            if len(self) == self.max_len:
                try:
                    old_key, old_value = self.popitem(last=False)
                    self.inform(old_key, old_value, type_of="dropping")
                except KeyError:
                    pass
            super().__setitem__(key, (value, time()))

    def pop(self, key, default=None):
        """Get item from the dict and remove it.

        Return default if expired or does not exist. Never raise KeyError.
        """
        with self.lock:
            try:
                item = super().__getitem__(key)
                del self[key]
                return item[0]
            except KeyError:
                return default

    def ttl(self, key):
        """Return TTL of the `key` (in seconds).

        Returns None for non-existent or expired keys.
        """
        key_value, key_age = self.get(key, with_age=True)  # noqa: E501; pylint: disable=unused-variable
        if key_age:
            key_ttl = self.max_age - key_age
            if key_ttl > 0:
                return key_ttl
        return None

    def get(self, key, default=None, with_age=False):
        """Return the value for key if key is in the dictionary, else default."""  # noqa: E501;
        try:
            return self.__getitem__(key, with_age)
        except KeyError as ex:  # noqa
            if with_age:
                return default, None
            return default

    def items(self):
        """Return a copy of the dictionary's list of (key, value) pairs."""
        # res_list = []
        for key in self._safe_keys():
            try:
                yield (key, self[key])
                # res_list.append((key, self[key]))
            except KeyError:
                pass
        # return res_list

    def values(self):
        """Return a copy of the dictionary's list of values.

        See the note for dict.items().
        """
        # res_list = []
        for key in self._safe_keys():
            try:
                yield self[key]
                # res_list.append(self[key])
            except KeyError:
                pass
        # return res_list

    def fromkeys(self):
        """Create a new dictionary with keys from seq and values set to value."""  # noqa: E501;
        raise NotImplementedError()

    def iteritems(self):
        """Return an iterator over the dictionary's (key, value) pairs."""
        raise NotImplementedError()

    def itervalues(self):
        """Return an iterator over the dictionary's values."""
        raise NotImplementedError()

    def viewitems(self):
        """Return a new view of the dictionary's items ((key, value) pairs)."""
        raise NotImplementedError()

    def viewkeys(self):
        """Return a new view of the dictionary's keys."""
        raise NotImplementedError()

    def viewvalues(self):
        """Return a new view of the dictionary's values."""
        raise NotImplementedError()

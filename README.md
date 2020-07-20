
## TTL Dict
## Base on https://github.com/mailgun/expiringdict

expiringdict is a Python caching library. The core of the library is ExpiringDict class which is an ordered dictionary with auto-expiring values for caching purposes. Expiration happens on any access, object is locked during cleanup from expired values. ExpiringDict can not store more than max_len elements - the oldest will be deleted.

Note: Iteration over dict and also keys() do not remove expired values! 
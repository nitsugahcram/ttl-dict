"""Dictionary with auto-expiring values for caching purposes.

Expiration happens on any access, object is locked during cleanup from expired
values. Can not store more than max_len elements - the oldest will be deleted.

>>> ExpiringDict(max_len=100, max_age_seconds=10)

The values stored in the following way:
{
    key1: (value1, created_time1),
    key2: (value2, created_time2)
}

NOTE: iteration over dict and also keys() do not remove expired values!
"""
from .ttldict import ExpiringDict

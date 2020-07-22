import sys
import time
import resource
from time import sleep
from unittest.mock import Mock, patch
from ttldict import ExpiringDict


def test_ttl_dict_perf():
    cache = ExpiringDict(max_len=1000000, max_age_seconds=10)
    m = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    t = time.clock()
    for i in range(1100000):
        cache[i] = i

    print("Time : %r s, Memory : %r Kb" %
          (time.clock() - t,
           resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - m))

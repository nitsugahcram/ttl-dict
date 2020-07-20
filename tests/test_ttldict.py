from time import sleep
from mock import Mock, patch
from precogs.toolbox.ttldict import ExpiringDict


def test_ttl():
    _ttl_dict = ExpiringDict(max_len=3, max_age_seconds=0.01)

    # assert _ttl_dict.get('a') == None
    _ttl_dict['a'] = 'x'
    assert _ttl_dict.get('a') == 'x'

    sleep(0.01)
    assert _ttl_dict.get('a') == None

    _ttl_dict['a'] = 'y'
    assert _ttl_dict.get('a') == 'y'

    assert 'b' not in _ttl_dict
    _ttl_dict['b'] = 'y'
    assert 'b' in _ttl_dict

    sleep(0.01)
    assert 'b' not in _ttl_dict


def test_size_items():
    _ttl_dict = ExpiringDict(max_len=3, max_age_seconds=10)
    # a is still in expiringdict, next values should expire it
    _ttl_dict['c'] = 'x'
    _ttl_dict['d'] = 'y'
    _ttl_dict['e'] = 'z'

    # dict if full
    assert 'c' in _ttl_dict
    assert 'd' in _ttl_dict

    _ttl_dict['f'] = '1'
    # c should gone after that
    assert 'c' not in _ttl_dict


def test_apis():
    _ttl_dict = ExpiringDict(max_len=3, max_age_seconds=0.01)
    _ttl_dict['c'] = 'x'
    _ttl_dict['d'] = 'y'
    _ttl_dict['e'] = 'z'
    #test __delitem__
    del _ttl_dict['e']
    assert 'e' not in _ttl_dict
    #test pop
    _ttl_dict['a'] = 'x'
    assert 'x' == _ttl_dict.pop('a')
    sleep(0.01)
    assert None == _ttl_dict.pop('a')


def test_repr():
    _ttl_dict = ExpiringDict(max_len=2, max_age_seconds=1)
    _ttl_dict['a'] = 'x'
    assert str(_ttl_dict) == "ExpiringDict([('a', 'x')])"
    sleep(1)
    assert str(_ttl_dict) == "ExpiringDict([])"


def test_iter():
    _ttl_dict = ExpiringDict(max_len=10, max_age_seconds=0.01)
    assert [k for k in _ttl_dict] == []
    _ttl_dict['a'] = 'x'
    _ttl_dict['b'] = 'y'
    _ttl_dict['c'] = 'z'
    assert [k for k in _ttl_dict] == ['a', 'b', 'c']
    assert [k for k in _ttl_dict.values()] == ['x', 'y', 'z']
    sleep(0.01)
    assert [k for k in _ttl_dict.values()] == []


def test_clear():
    _ttl_dict = ExpiringDict(max_len=10, max_age_seconds=10)
    _ttl_dict['a'] = 'x'
    for i in range(110):
        _ttl_dict[i] = i
    assert len(_ttl_dict) == 10
    _ttl_dict.clear()
    assert len(_ttl_dict) == 0


def test_ttl_over():
    _ttl_dict = ExpiringDict(max_len=10, max_age_seconds=10)
    _ttl_dict['a'] = 'x'

    # existent non-expired key
    assert 0 < _ttl_dict.ttl('a') < 10

    # non-existent key
    assert None == _ttl_dict.ttl('b')

    # expired key
    with patch.object(
            ExpiringDict, '__getitem__', Mock(return_value=('x', 10**9))):
        assert None == _ttl_dict.ttl('a')


def test_setdefault():
    d = ExpiringDict(max_len=10, max_age_seconds=0.01)

    assert 'x' == d.setdefault('a', 'x')
    assert 'x' == d.setdefault('a', 'y')
    sleep(0.01)
    assert 'y' == d.setdefault('a', 'y')


# def test_not_implemented():
#     d = ExpiringDict(max_len=10, max_age_seconds=10)
# assert NotImplementedError == d.fromkeys()
# assert_raises(NotImplementedError, d.iteritems)
# assert_raises(NotImplementedError, d.itervalues)
# assert_raises(NotImplementedError, d.viewitems)
# assert_raises(NotImplementedError, d.viewkeys)
# assert_raises(NotImplementedError, d.viewvalues)

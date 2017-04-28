from firebird.aardvark import pyccd_chip_spec_queries
from firebird.aardvark import ubids
from firebird.aardvark import byubid
from firebird.aardvark import sort
from firebird.aardvark import dates
from hypothesis import given
import hypothesis.strategies as st
import urllib
from fixtures import chip_specs


@given(url=st.sampled_from(('http://localhost',
                            'https://localhost',
                            'http://localhost/',
                            'http://127.0.0.1')))
def test_pyccd_chip_spec_queries(url):
    def check(query):
        url = urllib.parse.urlparse(query)
        assert url.scheme
        assert url.netloc
    queries = pyccd_chip_spec_queries(url)
    [check(query) for query in queries.values()]


def test_byubid():
    inputs = list()
    inputs.append({'ubid': 'a', 'data': None})
    inputs.append({'ubid': 'b', 'data': None})
    inputs.append({'ubid': 'c', 'data': None})
    results = byubid(inputs)
    # check that dicts were rekeyed into a new dict
    assert all(map(lambda r: r in results, ['a', 'b', 'c']))
    # check structure of new dict values
    assert all(map(lambda r: 'ubid' in r and 'data' in r, results.values()))


def test_ubids():
    data = ({'ubid': 'a/b/c'}, {'ubid': 'd/e/f'}, {'ubid': 'g'}, {'nope': 'z'})
    good = filter(lambda f: 'ubid' in f, data)
    assert set(map(lambda u: u['ubid'], good)) == set(ubids(data))


def test_ubids_from_chip_specs():
    assert len(ubids(chip_specs('blue'))) == 4


def test_sort():
    inputs = list()
    inputs.append({'acquired': '2015-04-01'})
    inputs.append({'acquired': '2017-04-01'})
    inputs.append({'acquired': '2017-01-01'})
    inputs.append({'acquired': '2016-04-01'})
    results = sort(inputs)
    assert(results[0]['acquired'] < results[1]['acquired'] <
           results[2]['acquired'] < results[3]['acquired'])


def test_dates():
    inputs = list()
    inputs.append({'acquired': '2015-04-01'})
    inputs.append({'acquired': '2017-04-01'})
    inputs.append({'acquired': '2017-01-01'})
    inputs.append({'acquired': '2016-04-01'})
    assert set(dates(inputs)) == set(map(lambda d: d['acquired'], inputs))


def test_intersection():
    pass


def test_filter():
    pass


def test_to_numpy():
    pass


def test_split():
    pass


def test_merge():
    pass


def test_rodify():
    assert True is True

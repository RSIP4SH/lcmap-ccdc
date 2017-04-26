from firebird import cassandra


def test_save_detect():
    # in travis-ci, cant yet connect to container running cassandra
    results = {'y': 999888, 'result_ok': True, 'algorithm': 'pyccd-1.1.0', 'inputs_md5': 'xoxoxo', 'tile_x':-123456,
               'result': 'a pile of result', 'result_produced': '2014-07-30T06:51:36Z', 'result_md5': 'result_md5',
               'x': -134567, 'tile_y': 888999}
    assert cassandra.save_pyccd_result(results)
    assert True
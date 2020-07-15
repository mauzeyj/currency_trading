from get_data.get_historical_data import get_data


def test_get_data():
    assert get_data().shape == (1, 1)
    pass

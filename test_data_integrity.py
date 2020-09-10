import unittest
import pandas as pd

data = pd.read_csv('data/cleaned_data.csv')


class TestLinks(unittest.TestCase):
    def test_maps_link(self):
        # TODO complete this test
        # Get list of links in data
        data_maps = data[data.Maps != 'nan']
        # Get list of current files
        return False

    def test_flags_link(self):
        data_flags = data.Flag.dropna()
        print(data_flags)


if __name__ == '__main__':
    unittest.main()

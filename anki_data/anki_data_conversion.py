# coding: utf-8
import logging
import pandas as pd

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="anki_data_conversion.log",
                    level=logging.INFO,
                    format=LOG_FORMAT,
                    filemode='w')
logger = logging.getLogger()


def extract_url(name):
    if type(name) is str:
        return name[13:len(name)-4].replace('.svg', '.png')
    else:
        return name


class Data:

    def __init__(self, path):
        self.header = ['Country', 'Country info', 'Capital', 'Capital info', 'Capital hint', 'Flag',
                       'Flag similarity', 'Map', 'tags']
        self.data = pd.read_csv(path)
        self.data = self.data.filter(self.header)
        # Remove html from urls
        self.data['Map'] = self.data['Map'].apply(extract_url)
        self.data['Flag'] = self.data['Flag'].apply(extract_url)
        # Quick sort by Country
        self.data = self.data.sort_values(['Country'])
        self.data = self.data.reset_index(drop=True)
        self.manual_replacements()

    def manual_replacements(self):
        self.data.loc[27, 'Flag'] = 'flag-bali.png'
        self.data.loc[42, 'Flag'] = 'flag-bolivia.png'
        self.data.loc[92, 'Flag'] = 'flag-el_salvador.png'
        self.data.loc[120, 'Flag'] = 'flag-guam.png'
        self.data.loc[201, 'Flag'] = 'flag-nicaragua.png'
        self.data.loc[221, 'Flag'] = 'flag-paraguay.png'

    def replace(self, value, replacement):
        temporary = self.data.copy(deep=True)
        self.data = self.data.replace(value, replacement)

        if not self.data.equals(temporary):
            logger.info('Changing from /{}/ to /{}/'.format(value, replacement))
        else:
            logger.warning('Could not find /{}/ to replace it by /{}/'.format(value, replacement))

    def add_line(self, line):
        line = dict(zip(self.header, line))
        try:
            self.data.append(line, ignore_index=True)
            logger.info('Added a new line for /{}/'.format(line['Country']))
        except TypeError:
            logger.warning('Could not add new line for /{}/: {} != {}'.format(line['Country'], len(line),
                                                                              self.data.shape[0]))

    def remove(self, country):
        temporary = self.data.copy(deep=True)
        self.data = self.data[self.data.Country != country]

        if not self.data.equals(temporary):
            logger.info('Line containing {} was removed.'.format(country))
        else:
            logger.warning('No line was found containing /{}/'.format(country))

    def save(self, name):
        self.data.to_csv(name)


if __name__ == "__main__":
    tab = Data('data.csv')
    tab.replace('Australia (Oceania)', 'Oceania')
    # TODO check that the following line is correctly working
    tab.add_line(['Saint Pierre and Miquelon', 'Saint Pierre'] + ['' for i in range(7)])
    # tab.remove('United Kingdom')
    tab.save('cleaned_data.csv')
    print(tab.data.Country)

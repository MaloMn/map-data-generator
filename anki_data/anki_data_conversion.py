# coding: utf-8
import logging
import pandas as pd
import re

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="anki_data_conversion.log",
                    level=logging.INFO,
                    format=LOG_FORMAT,
                    filemode='w')
logger = logging.getLogger()


def extract_url(name):
    if type(name) is str:
        output = name[13:len(name)-4].replace('.svg', '.png')
        output = re.findall(r'-(.*)\.', output)[0]
        output = output.replace('-nobox', '')
    else:
        output = name
    return output


def replace_value_by_x(info):
    if type(info) is str:
        return 'x'
    else:
        return info


def extract_tags(tag):
    return '.'.join(re.findall(r'UG::(\w+)', tag))


class Data:

    def __init__(self, path):
        self.header = ['Country', 'Country info', 'Capital', 'Capital info', 'Capital hint', 'Flag',
                       'Flag similarity', 'Map', 'tags']
        self.data = pd.read_csv(path)
        self.data = self.data.filter(self.header)
        # Remove html from urls and get the shortname of the country
        self.data['Map'] = self.data['Map'].apply(extract_url)
        self.data['short'] = self.data['Map']
        # Copy Capital column to create the Pinpoint column
        self.data['Pinpoint'] = self.data['Capital']
        # Replacing the values by x
        self.data['Flag'] = self.data['Flag'].apply(replace_value_by_x)
        self.data['Map'] = self.data['Map'].apply(replace_value_by_x)
        self.data['Pinpoint'] = self.data['Pinpoint'].apply(replace_value_by_x)
        self.data.rename(columns={'Map': 'Polygon'}, inplace=True)
        # Extract the tags
        self.data['tags'] = self.data['tags'].apply(extract_tags)
        # Quick sort by Country
        self.data = self.data.sort_values(['Country'])
        self.data = self.data.reset_index(drop=True)

        # Set the columns in a specific order
        self.data = self.data[['Country', 'Country info', 'Capital', 'Capital info', 'Capital hint', 'Flag',
                               'Flag similarity', 'Polygon', 'Pinpoint', 'short', 'tags']]

        print(self.data.iloc[0])

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
    # tab.add_line(['Saint Pierre and Miquelon', 'Saint Pierre'] + ['' for i in range(7)])
    # tab.remove('United Kingdom')
    tab.save('cleaned_data.csv')
    print(tab.data.iloc[27])

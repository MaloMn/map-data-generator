from bs4 import BeautifulSoup
import requests


def remove_values(array, value):
    while True:
        try:
            array.remove(value)
        except ValueError:
            break


def remove_duplicates(array):
    seen = []
    dupes = []

    for x in array:
        if x not in seen:
            seen.append(x)
        elif x not in dupes:
            dupes.append(x)

    return seen, dupes


def capitals():
    # Collecting capitals
    try:
        with open('wiki_capitals.txt', 'rb') as f:
            r = f.read()
    except:
        print('online')
        r = requests.get("https://en.wikipedia.org/wiki/List_of_national_capitals")
        with open("wiki_capitals.txt", 'wb') as f:
            f.write(r.content)
        r = r.content

    soup = BeautifulSoup(r, 'html.parser')

    # Main table containing the data
    table = soup.find("table", attrs={"class": "wikitable sortable"})
    table_data = table.tbody.find_all("tr")

    # Get three headings
    headings = []
    for th in table_data[0].find_all('th'):
        # remove any newlines and extra spaces from left and right
        headings.append(th.text.replace('\n', ' ').strip())

    headings[0], headings[1] = headings[1], headings[0]

    data = {}
    country = ''
    for i in range(1, len(table_data)):
        line = table_data[i].find_all('td')
        line = [a.text for a in line]
        if len(line) == 3:
            country = line[1].replace('\u00a0', '')
            data[country] = [line[0]]
        elif 1 <= len(line) <= 2:
            data[country].append(line[0])
        else:
            print('Problem encountered with: ', line)

    return data


def others():
    # Collecting oceans, rivers, seas, continents and other regions.
    continent = ['North America', 'South America', 'Antarctica', 'Asia', 'Europe', 'Africa', 'Oceania']


if __name__ == "__main__":
    import json
    countries = capitals()

    with open('data/countries.json', 'w') as f:
        json.dump(countries, f, indent=4)

    countries_solo, duplicates = remove_duplicates(countries)
    print('{} countries found. {} duplicates removed.'.format(len(countries), len(duplicates)))
    print('\t'.join(countries.keys()))


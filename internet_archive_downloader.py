# a program allowing us to download from archive.org repos
# TODO: refactor such that keyword search re-evaluates dl size and presents
# it to the user
# TODO: refactor get_sizes to use regex grouping instead of slices (maybe)

import requests
from bs4 import BeautifulSoup
from time import sleep
from os import chdir

# example link: r'https://archive.org/download/nointro.md'
url = input(
    "What is the website URL? (must be an archive.org link with .md extension)\n")
loc = input("Where would you like to download the files?\n")
chdir(loc)

# defining functions

# getting the size of the download


def get_size_list(soup):
    """Creates a list of strings with download sizes"""
    return [j for i in soup.find_all('tr') for j in i.find_all('td')[2]]


def get_sizes(dls):
    """getting size of download assuming \d+[KMG] format from list"""
    size = []
    for i in dls:
        i = i.replace(',', '')
        if i[-1] == 'K':
            size.append(float(i[:-1]) / 1000)
        elif i[-1] == 'G':
            size.append(float(i[:-1]) * 1000)
        else:
            size.append(float(i[:-1]))
    return size

# actually downloading the files


def file_getter(url, link_list, slowdown='y'):
    """
    Scrapes link of lists, downloading their contents.
    By default adds a short delay to prevent bans.
    """
    if url[-1] != '/':
        url += '/'  # prevents malformed urls

    for i in link_list:
        response = requests.get(f'{url}{i["link"]}')
        print(f'Downloading {i["title"]}...')
        with open(f'{i["title"]}', 'wb') as f:
            f.write(response.content)

    if slowdown == 'y':
        sleep(1)


def download_files(soup, url, slowdown, search_term):
    """Creates href list and then downloads files using file_getter"""
    # the code below works to get the link to a given game
    # soup.find_all('tr')[1].find('a').get('href')
    href_list = []
    games = soup.find_all('tr')
    for game in games[1:]:  # skip first link (not a game)
        if search_term.lower() in game.get_text().lower():
            href_list.append({
                'link': game.find('a')['href'],
                'title': game.find('a').get_text()
            })

    file_getter(url, href_list, slowdown)


response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

sizes_str = get_size_list(soup)
dl_size = sum(get_sizes(sizes_str))

print(
    f'The size of the download is {dl_size:.2f} Mb from {len(sizes_str)} files.')
proceed = input('Would you like to proceed? (y/n) ')

if proceed == 'y':
    slowdown = input(
        'Do you want to download slowly in order to prevent bans? (y/n) ')
    search = input('Do you want to filter by search term? (y/n) ')
    if search == 'y':
        search_term = input('What search term would you like to use?\n')
        download_files(soup, url, slowdown, search_term)
    elif search != 'y':
        download_files(soup, url, slowdown, search_term='')
else:
    print('abobobo')

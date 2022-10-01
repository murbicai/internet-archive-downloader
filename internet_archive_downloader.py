# a program allowing us to download from archive.org repos
# TODO: actually figure out code to download the files lol

import requests
from bs4 import BeautifulSoup
# r'https://archive.org/download/nointro.md'
url = input("What' the website URL? (must be an archive.org link)\n")
# defining functions
# getting the size of the download
def get_sizes(dls):
    """getting size of download assuming \d+[KMG] format"""
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

#actually downloading the files
def download_files():
    """Download files when given url"""

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

#getting list of the 
sizes_str = [j for i in soup.find_all('tr') for j in i.find_all('td')[2]]



dl_size = sum(get_sizes(sizes_str))

print(
    f'The size of the download is {dl_size:.2f} Mb from {len(sizes_str)} files.')
proceed = input("Would you like to proceed? (y/n) ")

if proceed == 'y':
    download_files()
else:
    print('bobobo')
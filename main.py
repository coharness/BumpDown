import getopt
import os
import sys
import requests
from urllib.request import urlretrieve

from bs4 import BeautifulSoup


class Category:
    def __init__(self, title, name):
        self.title = title
        self.name = name


as_bumps = Category('AS Bumps', 'bumps')
bw_cards = Category('B&W Cards', 'cards')
view_bump_builder = Category('Viewer & Bump Builder', 'vcbb')
toonami = Category('Toonami', 'toon')


def category_search(category):
    url = f'https://www.bumpworthy.com/bumps/all?categories%5B%5D={category.name}&sort=dateadded&sortdir=Desc'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Loop through each filtered result.
    for li in soup.find_all('div', {'id': 'bw-results'})[0].findChildren('li'):
        title = li['title']
        link = li.find('a')['href']

        # Find the link to the video.
        link_page = requests.get(link)
        link_soup = BeautifulSoup(link_page.content, 'html.parser')
        video_url = link_soup.find('source')['src']

        # Create destination directory.
        if not os.path.exists(category.title):
            os.mkdir(category.title)

        # Download the file.
        print(f'Downloading {title}.mp4')
        urlretrieve(video_url, os.path.join(category.title, f'{title}.mp4'))
        print('Complete\n')


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:', ['category'])
    except:
        print('BumpDown.py -c <Category>')
        sys.exit(2)

    for opt, arg, in opts:
        if opt == '-c':
            if arg == 'as_bumps':
                category_search(as_bumps)
            elif arg == 'bw_cards':
                category_search(bw_cards)
            elif arg == 'view_bump_builder':
                category_search(view_bump_builder)
            elif arg == 'toonami':
                category_search(toonami)
            elif arg == '*':
                category_search(as_bumps)
                category_search(bw_cards)
                category_search(view_bump_builder)
                category_search(toonami)
            else:
                print('Invalid category entered. Please use \'as_bumps\', \'bw_cards\', \'view_bump_builder\', \'toonami\', or \'*\'')

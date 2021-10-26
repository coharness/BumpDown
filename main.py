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

categories_dict = {
    'as': Category('AS Bumps', 'bumps'),
    'bw': Category('B&W Cards', 'cards'),
    'vbb': Category('Viewer & Bump Builder', 'vcbb'),
    'toon': Category('Toonami', 'toon')
}


def category_search(category):
    url = f'https://www.bumpworthy.com/bumps/all?categories%5B%5D={category.name}&sort=dateadded&sortdir=Desc'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Loop through each filtered result.
    links = soup.find_all('div', {'id': 'bw-results'})[0].findChildren('li')

    for li in links:
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
        path = os.path.join(category.title, f'{title}.mp4')

        # Skip existing files.
        if not os.path.exists(path):
            urlretrieve(video_url, path)
            print('Complete')
        else:
            print('File already exists')


if __name__ == '__main__':
    done = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:', ['category'])
    except:
        print(f'{sys.argv[0]} -c <Category>')
        sys.exit(2)

    for opt, arg, in opts:
        if opt == '-c':
            for cat_id, cat in categories_dict.items():
                if arg in ['*', cat_id]:
                    category_search(cat)
                    done = True

    if not done:
        print(f'Invalid category entered. Please use one of the following: {", ".join(categories_dict.keys())}')

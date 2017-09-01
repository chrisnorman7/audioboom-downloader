import string
import os
import os.path
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from requests import Session

session = Session()

parser = ArgumentParser()

parser.add_argument('rss_url', help='The URL of the user\'s rss feed')

parser.add_argument(
    'download_directory', default=None, nargs='?',
    help='The directory to download the files to'
)

if __name__ == '__main__':
    args = parser.parse_args()
    html = session.get(args.rss_url)
    soup = BeautifulSoup(html.content, 'html.parser')
    page_title = soup.title.text
    if args.download_directory is None:
        args.download_directory  = page_title
    if not os.path.isdir(args.download_directory):
        os.makedirs(args.download_directory)
    print('Downloading from %s.' % page_title)
    for number, item in enumerate(reversed(soup.find_all('item'))):
        url = item.enclosure['url']
        title = item.title.text
        filename = '%d - %s.mp3' % (number + 1, title)
        filename = ''.join(
            [
                char for char in filename if char in
                string.ascii_letters + string.digits + '.,!()[] -_=+'
            ]
        )
        filename = os.path.join(args.download_directory, filename)
        if os.path.isfile(filename):
            print('Skipping %s.' % title)
            continue
        print('Downloading %s to %s.' % (title, filename))
        r = session.get(url)
        with open(filename, 'wb') as f:
            f.write(r.content)
    print('Done.')

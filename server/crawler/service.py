import requests
import os
from core.settings import BASE_DIR, STATIC_URL
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Crawler:

    def __init__(self, seed_url, depth):
        # The seed url of the web page to be crawled.
        self._seed_url = seed_url
        seed_url_components = urlparse(seed_url)
        hash = self.hash_code(seed_url)
        self._domain = seed_url_components.netloc
        self._scheme = seed_url_components.scheme
        self._depth = depth  # The depth crawler should go into.
        self._static_url_prefix = STATIC_URL + 'downloads/' + hash + '/'
        self._download_folder = os.path.join(
            BASE_DIR, 'static', 'downloads', hash)
        if not os.path.exists(self._download_folder):
            os.makedirs(self._download_folder)

    def hash_code(self, string):
        """
        Generate unique id for the given string

        Args:
            string (str): The string for which unique id is to be generated.

        Returns:
            hash (int): A unique hash
        """
        hash = 0
        if len(string) > 0:
            for char in string:
                hash = ((hash << 5) - hash) + ord(char)
                hash &= hash
        return str(hash)

    def find_all_links(self, html):
        """
        Find all anchor tags from html

        Args:
            html (str): The html file from which urls should be identified

        Returns:
            paths (list): A list of al urls in the html
        """
        soup = BeautifulSoup(html, 'lxml')
        paths = set()
        for link in soup.find_all('a'):
            href = link.get('href')
            url_components = urlparse(href)
            if not href or not url_components.path:
                continue
            if href.startswith('/'):
                paths.add(url_components.path)
            else:
                if self._domain == url_components.netloc:
                    paths.add(url_components.path)
        return paths

    def start_crawl(self):
        """
        Crawl the webpage till and capture the save the images in each webpage.
        Do BFS traversal.

        Returns:
            results (list): A list of visited urls and the paths of the images saved for each url.
        """
        queue = [self._seed_url]
        new_url_queue = []  # List to add new urls for each depth
        crawled = []  # List to add visited urls
        depth = 0
        results = []
        while True:
            if not queue:
                depth += 1
                if not new_url_queue or self._depth == depth:
                    break
                queue.extend(new_url_queue)
                new_url_queue = []
            url = queue.pop(0)
            crawled.append(url)
            try:
                code = requests.get(url)
            except:
                continue
            html = code.text
            paths = self.find_all_links(html)
            images = self.find_all_images(html)
            if images:
                results.append({
                    'url': url,
                    'images': images
                })
            for path in paths:
                new_url = self._scheme + '://' + self._domain + path
                if new_url not in crawled:
                    new_url_queue.append(new_url)
        return results

    def find_all_images(self, html):
        """
        Save images from url to local folder

        Args:
            html (str): The html file from which images need to be downloaded

        Returns:
            images (list): A list of paths to the images.
        """
        soup = BeautifulSoup(html, 'lxml')
        images = set()
        files_in_dir = os.listdir(self._download_folder)
        for link in soup.find_all('img'):
            src = link.get('src')
            filename = self.hash_code(src)
            if filename in files_in_dir:
                images.add(self._static_url_prefix + filename)
                continue
            path = os.path.join(self._download_folder, filename)
            try:
                f = open(path, 'wb')
                f.write(requests.get(src).content)
                images.add(self._static_url_prefix + filename)
                f.close()
            except:
                continue
        return list(images)

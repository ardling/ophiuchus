#!/usr/bin/env python3

import os
import re
import html5lib
import posixpath

from six.moves import urllib
from pprint import pprint
from contextlib import closing
from six.moves.urllib.request import urlopen
from six.moves import xmlrpc_client

INDEX_URL = 'https://repo.dev.getmobit.ru/repository/pypi/pypi'
SIMPLE_URL = 'https://repo.dev.getmobit.ru/repository/pypi/simple'


def parse_link(link):
    url, hash_ = link.split('#')
    scheme, netloc, path, query, frag = urllib.parse.urlsplit(url)
    _, file_name = os.path.split(path)
    m = re.search(r'[^\.]+-(\d+\.\d+\.\d*)(.*)', file_name)
    version, tail = m.groups()
    print(version, tail)


class Package(object):
    def __init__(self, url_list):
        for i in url_list:
            parse_link(i)


class PyPi(object):
    def __init__(self, repo_url, index_url=None, simple_url=None):
        pass
        # self.repo_url = repo_url
        self.index_url = index_url or urllib.parse.urljoin(repo_url, 'pypi')
        self.simple_url = simple_url or urllib.parse.urljoin(repo_url, 'simple')

    def search(self, query):
        pypi = xmlrpc_client.ServerProxy(INDEX_URL)
        hits = pypi.search({'name': query, 'summary': query}, 'or')
        return hits

    def package(self, package):
        Package(self._find_links(package))

    def _find_links(self, package):
        pkg_url = posixpath.join(self.simple_url, package) + '/'
        print(pkg_url)
        with closing(urlopen(pkg_url)) as f:
            doc = html5lib.parse(f.read(),
                                 namespaceHTMLElements=False,
                                 transport_encoding=f.info().get_content_charset())
        links = doc.findall(".//a")
        return [urllib.parse.urljoin(pkg_url, l.get('href')) for l in links]


def main():
    pypi = PyPi('https://repo.dev.getmobit.ru/repository/pypi/')
    pypi.package('pluggy')
    # parse_link(pypi._find_links('pytest')[0])
    # pprint(pypi._find_links('pytest'))


main()

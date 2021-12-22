import os
import requests
from requests import exceptions
import datetime
import bs4
import re

"""
    Scrape from websites with ease! This class allows you scrape from a site and also saves efforts of having to create a new scraping object everytime.

    Also download files directly from your scripts and save yourself time
"""

TAGS = [
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "p",
    "div",
    "span",
    "section",
    "li",
    "tr",
    "th",
    "td"
]

def get_target_tag(url: str, tag: str) -> dict:
        """
        finds all occurences of a tag and return a dictionary of the data.
        it also appends a timestamp to keep track of the time it was collected

        inputs:

            url: site to scrape from

            tag -> the target tag

        outputs:

            a dictionary of occurences
        """
        res = {}
        if not _confirm_webpage(url):
            raise ValueError(f"Invalid url {url}")

        if tag not in TAGS:
            raise ValueError(f"Invalid tag {tag}")

        soup = _get_web_page_as_soup(url)

        target = soup.find_all(tag)
        values = [t.text for t in target]
        stamp = datetime.datetime.now()
        res["tag"] = tag
        res["values"] = values
        res["time-stamp"] = stamp
        return res

def download_from_site(url: str, dest: str = None) -> dict:
    """
    downloads files and resources from websites

    returns a ditionary of information relating to the resource downloaded
    """
    res = {}
    if not _confirm_webpage(url):
        raise ValueError(f"Invalid url {url}")

    if _is_downloadable(url):
        r = requests.get(url,allow_redirects=True)
        res["content-type"] = r.headers.get("content-type")
        res["file-size"] = r.headers.get("content-length", 0)
        res["file-name"] = _get_filename(r.headers.get("content-disposition"))
        res["time-stamp"] = datetime.datetime.now()
        if dest is not None:
            final = os.getcwd() + f"/{dest}"
            with open(final, 'wb') as obj:
                obj.write(r.content)
        else:
            final = os.getcwd() + f"/{res['file-name']}"
            with open(final, 'wb') as obj:
                obj.write(r.content)
        return res
    else:
        return {}
                


def _get_web_page_as_soup(url: str) -> bs4.BeautifulSoup:
    """
    A private method that converts a webpage to a soup object
    """
    try:
        response = requests.get(url, allow_redirects=True)
        soup =  bs4.BeautifulSoup(response.content,"html.parser")
        return soup
    except exceptions.HTTPError as httpe:
        print(f"Error occured {httpe}")
        return None

def _confirm_webpage(url: str) -> bool:
    """
    A function that confirms the existence of a webpage before the object is created
    """
    response = requests.get(url=url, allow_redirects=True)
    code = response.status_code
    return True if code == 200 else False

def _is_downloadable(url: str) -> bool:
    """
    checks if a url contains downloadable resources
    """
    h = requests.head(url, allow_redirects=True)
    headers = h.headers
    content_type = headers.get("content-type")
    if "text" in content_type.lower():
        return False
    elif "html" in content_type.lower():
        return False
    else:
        return True

def _get_filename(cd: str) -> str:
    """
    gets name of file from content disposition
    """

    if not cd:
        return None

    filename = re.findall("filename=(.+)", cd)
    if len(filename) == 0:
        return None
    return filename[0]
import re
import urllib.error as err
import urllib.request as req
from tkinter import messagebox

from bs4 import BeautifulSoup


def show_error(source_url, dest_folder):
    if source_url == "" and dest_folder == "":
        error_type = "both url and save folder are missing"

    elif source_url == "":
        error_type = "url is missing"

    else:
        error_type = "save folder is missing"

    messagebox.showerror("Something missing", error_type)


def check_url(source_url):
    if not re.match('(?:http|https)://', source_url):   # checks if there is no http or https
        source_url = 'http://{}'.format(source_url)     # then add http://

    request = req.Request(source_url,
                          headers={'User-Agent': "Fake Browser"})  # create fake header so websites won't block you.
    try:
        html = req.urlopen(request)  # get html code

        return html

    except err.URLError:
        messagebox.showerror("connection error", "no connection or website doesn't exist.")


def parser_html_to_images(html):
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img')  # gets img tags from html
    urls = [img['src'] for img in img_tags]  # gets the content of the image tags

    for i, url in enumerate(urls):
        if not re.match('(?:http|https)', url):  # checks if there is no http or https
            urls[i] = 'http:{}'.format(url)  # then add http://
    urls = list(set(urls))  # transform to set, to get rid of duplicates

    return urls


def fetch_images(source_url, dest_folder, download_type):
    if source_url is not "" and dest_folder is not "":
        connection = check_url(source_url)    # connects only if url exists.
        html = connection.read()  # read html from connection
        urls = parser_html_to_images(html)
        for url in urls:
            print(url)

    else:
        show_error(source_url, dest_folder)




from tkinter import messagebox
from bs4 import BeautifulSoup
import urllib.request as req
import urllib.error as err
import re

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
    pass


def fetch_images(source_url, dest_folder, download_type):
    if source_url is not "" and dest_folder is not "":
        connection = check_url(source_url)    # connects only if url exists.
        html = connection.read()  # read html from connection
        urls = parser_html_to_images(html)

    else:
        show_error(source_url, dest_folder)




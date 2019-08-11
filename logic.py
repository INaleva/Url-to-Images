import os
import re
import threading
import urllib.error as err
import urllib.request as req
from tkinter import messagebox

import requests
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


def download_images(urls, source_url, dest_folder, download_type):
    local_name, local_ext = os.path.splitext(os.path.basename(source_url))  # split url into path and basename

    if not os.path.exists(dest_folder + '/' + local_name + local_ext):  # crate folder if not exists.
        os.makedirs(dest_folder + '/' + local_name + local_ext)

    if download_type == "image":
        for url in urls:
            name, ext = os.path.splitext(os.path.basename(url))  # split url into path and basename

            try:
                request = requests.get(url)
                with open(dest_folder + '/' + local_name + local_ext + '/' + name + ext, 'wb') as outfile:
                    outfile.write(request.content)
            except OSError or requests.exceptions.InvalidURL:
                continue

    elif download_type == "url":
        text_file = open(dest_folder + '/' + local_name + local_ext + '/' + source_url + ".txt",
                         "w")  # create text file and write urls into it.
        for url in urls:
            text_file.write(url + "\n")
        text_file.close()


def fetch_images(source_url, dest_folder, download_type):
    if source_url is not "" and dest_folder is not "":
        connection = check_url(source_url)    # connects only if url exists.
        html = connection.read()  # read html from connection
        urls = parser_html_to_images(html)
        download_task = threading.Thread(target=download_images, args=(urls, source_url, dest_folder, download_type))
        download_task.start()

    else:
        show_error(source_url, dest_folder)

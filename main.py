import errno

import pypub
import progressbar
import os
import subprocess
import requests
from bs4 import BeautifulSoup, element


index_url = "https://exiledrebelsscanlations.com/novels/grandmaster-of-demonic-cultivation/"


def get_chapter_urls(index_soup):
    chapter_urls = []
    flrichtext = index_soup.find_all("div", class_="fl-rich-text")[0]
    for tag in flrichtext.contents:
        if type(tag) == element.Tag and tag.get_text().startswith("CHAPTERS"):
            break

    while tag:
        if type(tag) is element.NavigableString:
            tag = tag.next_sibling
            continue

        catlists = tag.find_all("div", class_="lcp_catlist")
        if len(catlists) > 0:
            # This is the actual chapter list
            chapter_urls.extend([link.a.get('href') for link in catlists[0]])
        elif tag.a:
            # For GDC, there is an extra link in between the heading and chapter list.
            # Let's get that too.
            chapter_urls.append(tag.a.get("href"))

        last_tag = tag
        tag = tag.next_sibling
        if type(last_tag) == element.Tag:
            last_tag.decompose()

    return chapter_urls


def remove_cruft(page_soup):
    to_remove = []

    content = page_soup.find_all("div", class_="entry-content")[0]
    for tag in content.contents:
        if type(tag) == element.Tag:
            if "fl-builder-content" not in tag.get("class", []) and "wtr-content" != tag.get("id"):
                to_remove.append(tag)

    to_remove.extend(
        page_soup.find_all("header", class_="entry-header")
    )
    to_remove.extend(
        page_soup.find_all("footer", class_="entry-footer")
    )

    for tag in to_remove:
        tag.decompose()

    return page_soup


def create_epub_and_get_filename():
    epub = pypub.Epub(
        "Grandmaster of Demonic Cultivation",
        creator="Mo Xiang Tong Xiu (translated by Exiled Rebels Scanlations)",
        publisher="Exiled Rebels Scanlations"
    )

    r = requests.get(index_url)
    soup = BeautifulSoup(r.text, "html.parser")

    chapter_urls = get_chapter_urls(soup)

    print("Adding intro page to epub")
    epub.add_chapter(pypub.create_chapter_from_string(str(remove_cruft(soup))))

    print("Adding {count} chapters to epub".format(count=len(chapter_urls)))
    progbar = progressbar.ProgressBar(len(chapter_urls))
    progbar.setup()

    for url in chapter_urls:
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")

            c = pypub.create_chapter_from_string(str(remove_cruft(soup)))
            epub.add_chapter(c)
            progbar.update(chunk=1)
        except ValueError:
            pass

    progbar.finish()

    print("Creating epub")
    return epub.create_epub(os.getcwd())


def generate_mobi(epub_filename):
    print("Generating mobi from epub")
    with open("/dev/null", "w") as null:
        try:
            subprocess.run(['kindlegen', '-c2', epub_filename])
        except OSError as e:
            if e.errno == errno.ENOENT:
                print("Couldn't generate mobi! Please add kindlegen to your path and try again")
            else:
                raise


if __name__ == "__main__":
    filename = create_epub_and_get_filename()
    generate_mobi(filename)

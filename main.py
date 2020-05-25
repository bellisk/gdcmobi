import errno

import pypub
import progressbar
import os
import subprocess

chapter_urls = [
    "https://exiledrebelsscanlations.com/novels/grandmaster-of-demonic-cultivation/",
    "https://exiledrebelsscanlations.com/gdc-character-and-sect-guide/",
    "https://exiledrebelsscanlations.com/gdc-chapter-1/",
    "https://exiledrebelsscanlations.com/gdc-chapter-2/",
    "https://exiledrebelsscanlations.com/gdc-chapter-3/",
    "https://exiledrebelsscanlations.com/gdc-chapter-4/",
    "https://exiledrebelsscanlations.com/gdc-chapter-5/",
    "https://exiledrebelsscanlations.com/gdc-chapter-6/",
    "https://exiledrebelsscanlations.com/gdc-chapter-7/",
    "https://exiledrebelsscanlations.com/gdc-chapter-8/",
    "https://exiledrebelsscanlations.com/gdc-chapter-9/",
    "https://exiledrebelsscanlations.com/gdc-chapter-10/",
    "https://exiledrebelsscanlations.com/gdc-chapter-11/",
    "https://exiledrebelsscanlations.com/gdc-chapter-12/",
    "https://exiledrebelsscanlations.com/gdc-chapter-13/",
    "https://exiledrebelsscanlations.com/gdc-chapter-14/",
    "https://exiledrebelsscanlations.com/gdc-chapter-15/",
    "https://exiledrebelsscanlations.com/gdc-chapter-16/",
    "https://exiledrebelsscanlations.com/gdc-chapter-17/",
    "https://exiledrebelsscanlations.com/gdc-chapter-18/",
    "https://exiledrebelsscanlations.com/gdc-chapter-19/",
    "https://exiledrebelsscanlations.com/gdc-chapter-20/",
    "https://exiledrebelsscanlations.com/gdc-chapter-21/",
    "https://exiledrebelsscanlations.com/gdc-chapter-22/",
    "https://exiledrebelsscanlations.com/gdc-chapter-23/",
    "https://exiledrebelsscanlations.com/gdc-chapter-24/",
    "https://exiledrebelsscanlations.com/gdc-chapter-25/",
    "https://exiledrebelsscanlations.com/gdc-chapter-26/",
    "https://exiledrebelsscanlations.com/gdc-chapter-27/",
    "https://exiledrebelsscanlations.com/gdc-chapter-28/",
    "https://exiledrebelsscanlations.com/gdc-chapter-29/",
    "https://exiledrebelsscanlations.com/gdc-chapter-30/",
    "https://exiledrebelsscanlations.com/gdc-chapter-31/",
    "https://exiledrebelsscanlations.com/gdc-chapter-32/",
    "https://exiledrebelsscanlations.com/gdc-chapter-33/",
    "https://exiledrebelsscanlations.com/gdc-chapter-34/",
    "https://exiledrebelsscanlations.com/gdc-chapter-35/",
    "https://exiledrebelsscanlations.com/gdc-chapter-36/",
    "https://exiledrebelsscanlations.com/gdc-chapter-37/",
    "https://exiledrebelsscanlations.com/gdc-chapter-38/",
    "https://exiledrebelsscanlations.com/gdc-chapter-39/",
    "https://exiledrebelsscanlations.com/gdc-chapter-40/",
    "https://exiledrebelsscanlations.com/gdc-chapter-41/",
    "https://exiledrebelsscanlations.com/gdc-chapter-42/",
    "https://exiledrebelsscanlations.com/gdc-chapter-43/",
    "https://exiledrebelsscanlations.com/gdc-chapter-44/",
    "https://exiledrebelsscanlations.com/gdc-chapter-45/",
    "https://exiledrebelsscanlations.com/gdc-chapter-46/",
    "https://exiledrebelsscanlations.com/gdc-chapter-47/",
    "https://exiledrebelsscanlations.com/gdc-chapter-48/",
    "https://exiledrebelsscanlations.com/gdc-chapter-49/",
    "https://exiledrebelsscanlations.com/gdc-chapter-50/",
    "https://exiledrebelsscanlations.com/gdc-chapter-51/",
    "https://exiledrebelsscanlations.com/gdc-chapter-52/",
    "https://exiledrebelsscanlations.com/gdc-chapter-53/",
    "https://exiledrebelsscanlations.com/gdc-chapter-54/",
    "https://exiledrebelsscanlations.com/gdc-chapter-55/",
    "https://exiledrebelsscanlations.com/gdc-chapter-56/",
    "https://exiledrebelsscanlations.com/gdc-chapter-57/",
    "https://exiledrebelsscanlations.com/gdc-chapter-58/",
    "https://exiledrebelsscanlations.com/gdc-chapter-59/",
    "https://exiledrebelsscanlations.com/gdc-chapter-60/",
    "https://exiledrebelsscanlations.com/gdc-chapter-61/",
    "https://exiledrebelsscanlations.com/gdc-chapter-62/",
    "https://exiledrebelsscanlations.com/gdc-chapter-63/",
    "https://exiledrebelsscanlations.com/gdc-chapter-64/",
    "https://exiledrebelsscanlations.com/gdc-chapter-65/",
    "https://exiledrebelsscanlations.com/gdc-chapter-66/",
    "https://exiledrebelsscanlations.com/gdc-chapter-67/",
    "https://exiledrebelsscanlations.com/gdc-chapter-68/",
    "https://exiledrebelsscanlations.com/gdc-chapter-69/",
    "https://exiledrebelsscanlations.com/gdc-chapter-70/",
    "https://exiledrebelsscanlations.com/gdc-chapter-71/",
    "https://exiledrebelsscanlations.com/gdc-chapter-72/",
    "https://exiledrebelsscanlations.com/gdc-chapter-73/",
    "https://exiledrebelsscanlations.com/gdc-chapter/",
    "https://exiledrebelsscanlations.com/gdc-chapter-75/",
    "https://exiledrebelsscanlations.com/gdc-chapter-76/",
    "https://exiledrebelsscanlations.com/gdc-chapter-77/",
    "https://exiledrebelsscanlations.com/gdc-chapter-78/",
    "https://exiledrebelsscanlations.com/gdc-chapter-79/",
    "https://exiledrebelsscanlations.com/gdc-chapter-80/",
    "https://exiledrebelsscanlations.com/gdc-chapter-81/",
    "https://exiledrebelsscanlations.com/gdc-chapter-82/",
    "https://exiledrebelsscanlations.com/gdc-chapter-83/",
    "https://exiledrebelsscanlations.com/gdc-chapter-84/",
    "https://exiledrebelsscanlations.com/gdc-chapter-85/",
    "https://exiledrebelsscanlations.com/gdc-chapter-86/",
    "https://exiledrebelsscanlations.com/gdc-chapter-87/",
    "https://exiledrebelsscanlations.com/gdc-chapter-88/",
    "https://exiledrebelsscanlations.com/gdc-chapter-89/",
    "https://exiledrebelsscanlations.com/gdc-chapter-90/",
    "https://exiledrebelsscanlations.com/gdc-chapter-91/",
    "https://exiledrebelsscanlations.com/gdc-chapter-92/",
    "https://exiledrebelsscanlations.com/gdc-chapter-93/",
    "https://exiledrebelsscanlations.com/gdc-chapter-94/",
    "https://exiledrebelsscanlations.com/gdc-chapter-95/",
    "https://exiledrebelsscanlations.com/gdc-chapter-96/",
    "https://exiledrebelsscanlations.com/gdc-chapter-97/",
    "https://exiledrebelsscanlations.com/gdc-chapter-98/",
    "https://exiledrebelsscanlations.com/gdc-chapter-99/",
    "https://exiledrebelsscanlations.com/gdc-chapter-100/",
    "https://exiledrebelsscanlations.com/gdc-chapter-101/",
    "https://exiledrebelsscanlations.com/gdc-chapter-102/",
    "https://exiledrebelsscanlations.com/gdc-chapter-103/",
    "https://exiledrebelsscanlations.com/gdc-chapter-104/",
    "https://exiledrebelsscanlations.com/gdc-chapter-105/",
    "https://exiledrebelsscanlations.com/gdc-chapter-106/",
    "https://exiledrebelsscanlations.com/gdc-chapter-107/",
    "https://exiledrebelsscanlations.com/gdc-chapter-108/",
    "https://exiledrebelsscanlations.com/gdc-chapter-109/",
    "https://exiledrebelsscanlations.com/gdc-chapter-110/",
    "https://exiledrebelsscanlations.com/gdc-chapter-111/",
    "https://exiledrebelsscanlations.com/gdc-chapter-112/",
    "https://exiledrebelsscanlations.com/gdc-chapter-113/",
    "https://exiledrebelsscanlations.com/gdc-chapter-113-5/",
    "https://exiledrebelsscanlations.com/gdc-chapter-114/",
    "https://exiledrebelsscanlations.com/gdc-chapter-115/",
    "https://exiledrebelsscanlations.com/gdc-chapter-116/",
    "https://exiledrebelsscanlations.com/gdc-chapter-117/",
    "https://exiledrebelsscanlations.com/gdc-chapter-118/",
    "https://exiledrebelsscanlations.com/gdc-chapter-119/",
    "https://exiledrebelsscanlations.com/gdc-chapter-120/",
    "https://exiledrebelsscanlations.com/gdc-chapter-120-5/",
    "https://exiledrebelsscanlations.com/gdc-chapter-121/",
    "https://exiledrebelsscanlations.com/gdc-chapter-122/",
    "https://exiledrebelsscanlations.com/gdc-chapter-123/",
    "https://exiledrebelsscanlations.com/gdc-chapter-124/",
    "https://exiledrebelsscanlations.com/gdc-chapter-125/",
    "https://exiledrebelsscanlations.com/gdc-chapter-126/",
]


def create_epub():
    epub = pypub.Epub(
        "Grandmaster of Demonic Cultivation",
        creator="Mo Xiang Tong Xiu (translated by Exiled Rebels Scanlations)",
        publisher="Exiled Rebels Scanlations"
    )

    print("Adding chapters to epub")
    progbar = progressbar.ProgressBar(len(chapter_urls))
    progbar.setup()

    for url in chapter_urls:
        try:
            c = pypub.create_chapter_from_url(url)
            epub.add_chapter(c)
            progbar.update(chunk=1)
        except ValueError:
            pass

    progbar.finish()

    print("Creating epub")
    epub_path = epub.create_epub(os.getcwd())
    print(epub_path)


def generate_mobi(epub_filename, mobi_filename):
    with open("/dev/null", "w") as null:
        try:
            subprocess.run(['kindlegen', '-c2', '-o', mobi_filename, epub_filename])
        except OSError as e:
            if e.errno == errno.ENOENT:
                print
                "Warning: kindlegen was not on your path; not generating .mobi version"
            else:
                raise

if __name__ == "__main__":
    print('Starting script')
    create_epub()
    print("Done")
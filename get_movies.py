import requests
from bs4 import BeautifulSoup
import wikipedia
import os


def get_wiki_titles(wiki_path_list):
    wiki_titles = set()  # avoid repetitive titles
    for path in wiki_path_list:
        print("Looking up {}.".format(path))

        website_url = requests.get('https://en.wikipedia.org' + path).text

        soup = BeautifulSoup(website_url, 'lxml')

        table = soup.find('table', {'class': 'wikitable sortable'})
        movie_titles = table.findAll('i')  # only titles are in italic
        links = movie_titles
        for link in links:
            if link.a is None:
                wiki_titles.add(link.text)  # some <i> only has text in it
                continue

            title = link.a.get('title')
            wiki_titles.add(title)

    return list(wiki_titles)


def put_document_helper(corpus_path, wiki_title):
    article_text = wikipedia.page(wiki_title).content

    file_title = "_".join(wiki_title.split(" "))  # replaces spaces with _

    complete_path = os.path.join(corpus_path, file_title)

    if os.path.exists(complete_path):
        print("{} already exists.".format(wiki_title))
        return

    f = open(complete_path, "a")
    f.write(article_text)
    f.close()
    return


def put_document_in_subdirectory(corpus_path, wiki_title):
    try:
        put_document_helper(corpus_path, wiki_title)
        return 0

    except:
        try:
            # some files have multiple sub-titles, try again by adding " - Wikipedia" after it
            put_document_helper(corpus_path, wiki_title + " - Wikipedia")
            return 0

        except:
            print("====Skipped " + wiki_title + "====")
            return 1


def populate_corpus_from_titles(corpus_path, wiki_titles):
    for wiki_title in wiki_titles:
        put_document_in_subdirectory(corpus_path, wiki_title)


def count_files(dir_path):
    length = len([name for name in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, name))])
    print("{} has {} files.".format(dir_path, length))


def main():
    wiki_path_list = [
        "/wiki/List_of_American_films_of_2020",
        "/wiki/List_of_American_films_of_2019",
        "/wiki/List_of_American_films_of_2018",
        "/wiki/List_of_American_films_of_2017",
        "/wiki/List_of_American_films_of_2016",
        "/wiki/List_of_American_films_of_2015",
        "/wiki/List_of_American_films_of_2014",
        "/wiki/List_of_American_films_of_2013",
        "/wiki/List_of_American_films_of_2012",
        "/wiki/List_of_American_films_of_2011",
        "/wiki/List_of_American_films_of_2010",
        "/wiki/List_of_American_films_of_2009",
        "/wiki/List_of_American_films_of_2008",
        "/wiki/List_of_American_films_of_2007",
        "/wiki/List_of_American_films_of_2006",
        "/wiki/List_of_American_films_of_2005",
        "/wiki/List_of_American_films_of_2004",
        "/wiki/List_of_American_films_of_2003",
        "/wiki/List_of_American_films_of_2002",
        "/wiki/List_of_American_films_of_2001",
        "/wiki/List_of_American_films_of_2000"
    ]

    # wiki_titles = get_wiki_titles(wiki_path_list)
    # print("Found {} wiki_titles.".format(len(wiki_titles)))
    #
    corpus_path = "./movie_corpus"
    # populate_corpus_from_titles(corpus_path, wiki_titles)
    count_files(corpus_path)


if __name__ == "__main__":
    main()

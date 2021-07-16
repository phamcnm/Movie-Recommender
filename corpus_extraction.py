import wikipedia
import random
import os
from os import path

def put_document_helper(corpus_path, wiki_title):
	article_text = wikipedia.page(wiki_title).content

	file_title = "_".join(wiki_title.split(" ")) # replaces spaces with _

	complete_path = os.path.join(corpus_path, file_title)
	
	if path.exists(complete_path):
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


def count_files(dir_path):
	length = len([name for name in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, name))])
	print("{} has {} files.".format(dir_path, length)) 


def remove_start_with(dir_list, string):
	for dir in dir_list:
		for file_name in os.listdir(dir):
			if file_name.startswith(string):
				os.remove(os.path.join(dir, file_name))	


def addToCorpus():
	# film
	film_list_of_lists_wiki_title = [
		"List of American films of 2020 - Wikipedia"
	]
	# tennis
	tennis_list_of_lists_wiki_title = [
		"List of Wimbledon Open Era champions - Wikipedia",
		"List of Australian Open champions - Wikipedia"
	]
	# 
	drink_list_of_lists_wiki_title = [
		"List of brand name soft drink products - Wikipedia",
		"List of alcoholic drinks - Wikipedia"
	]

	#game
	game_list_of_lists_wiki_title = [
		"List of Xbox games"
	]

	film_doc_titles = []
	tennis_doc_titles = []
	drink_doc_titles = []
	game_doc_titles = []

	for wiki_title in film_list_of_lists_wiki_title:
		links = wikipedia.page(wiki_title).links
		film_doc_titles += links


	# for wiki_title in tennis_list_of_lists_wiki_title:
	# 	links = wikipedia.page(wiki_title).links
	# 	tennis_doc_titles += links

	for wiki_title in drink_list_of_lists_wiki_title:
		links = wikipedia.page(wiki_title).links
		drink_doc_titles += links

	for wiki_title in game_list_of_lists_wiki_title:
		links = wikipedia.page(wiki_title).links
		game_doc_titles += links
	
	# tennis_doc_titles = random.sample(tennis_doc_titles, 1)
	film_doc_titles = random.sample(film_doc_titles, 250)
	drink_doc_titles = random.sample(drink_doc_titles, 250)
	game_doc_titles = random.sample(game_doc_titles, 250)

	film_path = "./corpus/film"
	tennis_path = "./corpus/tennis"
	drink_path = "./corpus/drink"
	game_path = "./corpus/game"

	skip_count = 0
	for wiki_title in film_doc_titles:
		skip_count += put_document_in_subdirectory(film_path, wiki_title)
	
	print("Film skipped {} files".format(skip_count))

	# skip_count = 0
	# for wiki_title in tennis_doc_titles:
	# 	skip_count += put_document_in_subdirectory(tennis_path, wiki_title)

	# print("Tennis skipped {} files".format(skip_count))

	skip_count = 0
	for wiki_title in drink_doc_titles:
		skip_count += put_document_in_subdirectory(drink_path, wiki_title)
	
	print("Drink skipped {} files".format(skip_count))

	skip_count = 0
	for wiki_title in game_doc_titles:
		skip_count += put_document_in_subdirectory(game_path, wiki_title)
	
	print("Video Game skipped {} files".format(skip_count))

	count_files(film_path)
	count_files(tennis_path)
	count_files(drink_path)
	count_files(game_path)


def test():
	wiki_path = ["List of American films of 2020 - Wikipedia"]
	for wiki_title in wiki_path:
		links = wikipedia.page(wiki_title).links
		print(links)


def main():
	test()
	# film_path = "./corpus/film"
	# tennis_path = "./corpus/tennis"
	# drink_path = "./corpus/drink"
	# game_path = "./corpus/game"
	#
	# movie_path = "./movie_corpus"
	#
	# # print("Adding")
	# # addToCorpus()
	#
	# print("Before remove")
	# count_files(film_path)
	# # count_files(tennis_path)
	# count_files(drink_path)
	# count_files(game_path)
	#
	# print("Removing")
	# string = "List_of_"
	# # string = "Xbox"
	# path_list = [film_path, drink_path, game_path]
	# remove_start_with(path_list, string)
	#
	# print("After remove files that start with {}".format(string))
	# count_files(film_path)
	# # count_files(tennis_path)
	# count_files(drink_path)
	# count_files(game_path)

if __name__ == "__main__":
	main()
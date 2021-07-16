from doc2vec import *
import sys
from mchain import *
from parse_info import *
from textblob import TextBlob
import string

top_5_texts = []

def query_with_title(query_title):
	"""
	Helper function for get_list_of_tokens_from_queries()
	Finds the article text of the query title
	Parameters:
		query_title: a wiki title to search for
	Returns:
		article_text: the text of the article
	"""
	article_text = wikipedia.page(query_title).content
	# print("Found {}.".format(query_title))
	return article_text


def get_list_of_tokens_from_queries(queries):
	"""
	Helper function for query_model()
	Finds the wiki article for the queries, and tokenize them
	Parameters:
		queries: the query topics
	Returns:
		tokenized_queries: a list of tokenized text
	"""
	queries_texts = []
	tokenized_queries = []
	stopwords = create_stopwords()
	article_content = []

	for wiki_title in queries:
		try:
			query_title = wiki_title + " (film)"
			article_text = query_with_title(query_title)
			queries_texts.append(article_text)

		except:
			try:
				query_title = wiki_title + " (film) - Wikipedia"
				article_text = query_with_title(query_title)
				queries_texts.append(article_text)

			except:
				try:
					query_title = wiki_title + " - Wikipedia"
					article_text = query_with_title(query_title)
					queries_texts.append(article_text)

				except:
					try:
						query_title = wiki_title
						article_text = query_with_title(query_title)
						queries_texts.append(article_text)

					except:
						print("{} does not exist on wiki.".format(wiki_title))
						queries_texts.append(wiki_title)

	for text in queries_texts:
		tokenized_text = tokenize(text, stopwords)
		tokenized_queries.append(tokenized_text)

	return tokenized_queries


def get_list_of_content_from_queries(queries):
	"""
	Helper function for query_model()
	Gets the list of texts of the top 5 most similar titles
	Parameters:
		queries: a list of query topics
	Returns:
		queries_texts: a list of text
	"""
	queries_texts = []

	for wiki_title in queries:
		try:
			query_title = wiki_title
			article_text = query_with_title(query_title)
			queries_texts.append(article_text)

		except:
			try:
				query_title = wiki_title + " - Wikipedia"
				article_text = query_with_title(query_title)
				queries_texts.append(article_text)

			except:
				print("{} does not exist on wiki. SHOULD NOT EVER REACH THIS".format(wiki_title))

	return queries_texts


def query_model(queries, matrix_path, model_path, verbose=False):
	"""
	Finds the top 5 similar movies to the query topics
	Parameters:
		queries: the query topics
		matrix_path: the path to the doc2vec matrix
		model_path: the path to the doc2vec model
	Returns:
		title_score: a list of the 5 similar titles and their similarity scores
		keyword_sentence: a list of keywords for the titles
	"""
	global top_5_texts
	top_5_texts = []

	if verbose:
		print("Looking up query.")

	queries_tokens = get_list_of_tokens_from_queries(queries)

	if verbose:
		print("Comparing query with on matrix.")
	matrix = load_dat(matrix_path)
	model = Doc2Vec.load(model_path)
	queries_vectors = []
	for query_token in queries_tokens:
		vector = model.infer_vector(query_token)
		queries_vectors.append(vector)

	title_score = get_top5_of_queries(matrix, queries_vectors, queries)
	top_5_titles = [tup[0] for tup in title_score]
	top_5_texts = get_list_of_content_from_queries(top_5_titles)
	
	keyword_sentence = []
	for text in top_5_texts:
		pick_top_three_result = pick_top_three(text)
		person_sentences = find_keyword_chunks(text, pick_top_three_result[0])
		place_sentences = find_keyword_chunks(text, pick_top_three_result[1])

		# remove tabs and newlines
		person_sentences = [re.sub(r"[\n\t]*", "", person_string) for person_string in person_sentences]
		place_sentences = [re.sub(r"[\n\t]*", "", place_string) for place_string in place_sentences]

		keyword_sentence.append({
			"keywords_person": pick_top_three_result[0],
			"keywords_place": pick_top_three_result[1],
			"sentences_person": person_sentences,
			"sentences_place": place_sentences
		})
	
	return (title_score, keyword_sentence)


def break_line(string, max_length):
	"""
	Helper method for display_result(). Breaks a line by max length.
	Parameters:
		string: a string to check
		max_length: the length to break the line at if the string is too long
	Returns:
		return_list: a list of string after breaking line
	"""
	return_list = []
	string_list = string.split(" ")
	char_count = 0
	current_string = ""
	for s in string_list:
		if len(s) > max_length: # found extremely long string
			return_list.append(current_string)
			return_list.append(s)
			char_count = 0
			current_string = ""
			continue

		char_count += len(s)
		if char_count > max_length:
			return_list.append(current_string)
			char_count = 0
			current_string = ""
		else:
			current_string += s + " "

	return_list.append(current_string)
	return return_list


def display_result(title_score, rating_score, keyword_sentence):
	"""
	Pretty-prints the results on the command prompt
	Parameters:
		title_score: the list of titles and their similarity scores
		rating_score: the list of reviews and their rating
		keyword_sentence: the summary that contains the keywords in the movies
	
	"""
	top_5_titles = [tup[0] for tup in title_score]
	top_5_scores = [tup[1] for tup in title_score]
	line_length = 150
	one_forth_length = int(line_length / 4)
	one_eight_length = int(line_length / 8)
	one_forth_space = " " * one_forth_length
	one_eight_space = " " * one_eight_length

	line = "=" * line_length
	light_line = "-" * line_length

	full_summary_strings = []
	for i in range(5):
		# prints Title
		print(line)
		title = clean_title_string(top_5_titles[i])
		space_before_title = " " * (int(((line_length/2) - (len(title)/2))) - 3)
		print("{}{}. {}".format(space_before_title, i, title))
		
		# prints Scores
		match_string = "Match: {}/10".format(top_5_scores[i])
		rating_string = "Rating: {}/10".format(rating_score[i][1])
		print(light_line)
		print("{}{:<35}{:>35}{}".format(one_forth_space, match_string, rating_string, one_forth_space))
		print(light_line)

		# prints Summary
		keyword_string = " | ".join(keyword_sentence[i]["keywords_person"]) + " | " + " | ".join(keyword_sentence[i]["keywords_place"])
		print("{}{} {:<80}{}".format(one_eight_space, "Keywords:", keyword_string, one_eight_space))
		print(light_line)
		
		keyword_list = []
		summary_list = []
		random_indices = random.sample(range(0, 6), 3)
		for random_int in random_indices:
			if random_int < 3:
				sentence = keyword_sentence[i]["sentences_person"][random_int]
				summary_list.append(sentence)
				keyword = keyword_sentence[i]["keywords_person"][random_int]
				keyword_list.append(keyword)
			else:
				sentence = keyword_sentence[i]["sentences_place"][random_int - 3]
				summary_list.append(sentence)
				keyword = keyword_sentence[i]["keywords_place"][random_int - 3]
				keyword_list.append(keyword)
		
		full_summary_strings.append(summary_list)

		isFirst = True
		sum_header = "Rephrased Summaries:"
		for j in range(len(summary_list)):
			rephrased_sentence = rephrase(summary_list[j], keyword[j])
			if isFirst:
				print("{}{} {}".format(one_eight_space, sum_header, rephrased_sentence))
				isFirst = False
			else:
				print("{}{} {}".format(one_eight_space, (" "*len(sum_header)), rephrased_sentence))
			print()
		print(light_line)

		# prints Reviews
		print("{}{} {:<80}{}".format(one_eight_space, "Reviews:", rating_score[i][0][0], one_eight_space))

		print()
		# prints two more Reviews
		for j in range(len(rating_score[i][0]) - 1):
			print("{}{} {:<60}{}".format(one_eight_space, "        ", rating_score[i][0][j+1], one_eight_space))
			print()
		
		print(line)
		print()
	
	yes_or_no = input("Do you want to see the full spoliers for all 5 movies? [yes/no]: ")
	print("\n")

	if yes_or_no.lower() == "yes":
		for i in range(5):
			# prints Title
			print(line)
			title = clean_title_string(top_5_titles[i])
			space_before_title = " " * (int(((line_length/2) - (len(title)/2))) - 3)
			print("{}{}. {}".format(space_before_title, i, title))
			print(light_line)
			print()

			summary_list = full_summary_strings[i]
			sum_header = "Full Summaries:"
			isFirst = True
			for j in range(len(summary_list)):
				cleaned_summary_list = break_line(summary_list[j], 80)
				for cleaned_string in cleaned_summary_list:
					if isFirst:
						print("{}{} {}".format(one_eight_space, sum_header, cleaned_string))
						isFirst = False
					else:
						print("{}{} {}".format(one_eight_space, (" "*len(sum_header)), cleaned_string))
				print()
			print(line)

def generate_rating_and_score(SLM_model, num_movie=0, num_review_per_movie=1):
	"""
	Generates reviews and ratings from a SLM model
	Parameters:
		SLM_model: a trained SLM model
		num_movies: number of movies to review
		num_review_per_movie: number of reviews per movie
	Returns:
		review_score: a list of tuples where each tuple has two things: the review and the score	
	"""
	review_score = []
	for i in range(num_movie):
		tmp_list = []
		tmp_score = 0
		for j in range(num_review_per_movie):
			review_string = clean_review(SLM_model.generate(15))         
			se = TextBlob(review_string)
			score = se.sentiment.polarity
			tmp_score += (score+1)*5
			tmp_list.append((review_string))

		average_score = round(tmp_score / num_review_per_movie, 2)
		review_score.append((tmp_list, average_score))

	return review_score


def search_engine(SLM_model, matrix_path, model_path):
	"""
	Interacts with the user
	Parameter:
		SLM_model: the SLM model to generate reviews for movies
		matrix_path: the path to the doc2vec matrix
		model_path: the path to the doc2vec model
	"""
	query_topics = []
	print("\n\n\n")
	print("Enter a movie you want to look up! Type \"done\" to exit.")
	is_done = False
	while True:	
		print("\n\n\n")
		query_topics = []
		query_input = input("Enter a topic: ")

		if (query_input.lower() == "done"):
			print("\nBye!!\n")
			sys.exit(1)

		query_topics.append(query_input)

		query_result = query_model(query_topics, matrix_path, model_path)
		title_score = query_result[0]
		keyword_sentence = query_result[1]

		rating_score = generate_rating_and_score(SLM_model, num_movie=5, num_review_per_movie=3)
		display_result(title_score, rating_score, keyword_sentence)


def clean_review(s):
	"""
	Cleans up a sentence by fixing capitalization, punctuations, and spaces
	Parameters:
		s: the stirng to be cleaned
	Returns:
		the cleaned up string
	"""
	s = s.replace("\n", "")
	l = list(s)
	l[0] = l[0].upper()
	i = 0
	while i < len(l) - 2:
		if l[i] == "\"":
			l.pop(i)
		elif l[i] == ".":
			i += 2
			l[i] = l[i].upper()
		i += 1
	if l[-1] == " ":
		if l[-2]  in string.punctuation:
			l.pop(-1)
			l[-1] = "."
		else:
			l[-1] = "."
	elif l[-1] != ".":
		l.append(".")
	s = "".join(l)
	s = s.replace(" i ", " I ")
	return s


def main():
	"""
	The main method to test
	"""
	# call search_engine
	matrix_path = "./bot_dependencies/matrix.dat"
	model_path = "./bot_dependencies/doc2vec.model"
	
	title_score = [('Hulk (film)', 9.21), ('Glass (2019 film)', 6.55), ('Spider-Man (2002 film) - Wikipedia', 6.53), ('Unbreakable (film)', 6.35), ('X-Men (film)', 6.18)]
	test = "Shyamalan realized the opportunity he had to create a trilogy of works, and used the ending of Split to establish the film as within the Unbreakable narrative."

	rando_sentence = "Meanwhile, a crazed Norman sports advanced Oscorp armor and military equipment, and disrupts an experiment by Oscorp's corporate rival, Quest Aerospace, killing several people in the process."
	rando2 = "Notary stated that this Kong is an adolescent, and he tried to play Kong like a \"14-year-old that's trapped in the life of an adult\", saying it took three days to film the motion capture scenes."

	text_list = ['Meanwhile, Norman Osborn, owner of scientific corporation Oscorp, tries to land a major military contract.', 'Stylistically, there was heavy criticism of the Green Goblin\'s costume, which led IGN\'s Richard George to comment years later: "We\'re not saying the comic book costume is exactly thrilling, but the Goblin armor (the helmet in particular) from Spider-Man is almost comically bad...', 'Jameson later dubs the mysterious villain the "Green Goblin."']

	keyword = "SpiderMan"
	# res = break_line(text_list[1], 80)
	# print(res)

	SLM_model = train_markov("./clean_reviews.txt")
	rating_score = generate_rating_and_score(SLM_model, num_movie=5, num_review_per_movie=3)
	search_engine(SLM_model, matrix_path, model_path)


if __name__ == "__main__":
	main()
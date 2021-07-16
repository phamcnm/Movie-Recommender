import os
import string
import numpy as np
import re
import wikipedia
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from scipy import spatial
import nltk

nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


def load_dat(path):
    infile = open(path, 'rb')
    saved = np.load(infile, allow_pickle=True)
    return saved


def tokenize(s, stopwords):
    # get rid of all non-alphanumeric characters
    regex = re.compile('[^a-zA-Z\d]')
    list = s.lower().split()
    return_list = []
    for i in range(len(list)):
        w = list[i].strip(string.punctuation)
        if w not in stopwords and w != "":
            for split_word in regex.sub(' ', w).split():
                return_list.append(lemmatizer.lemmatize(split_word).lower())

    return return_list


def compare(arr1, arr2):
    return (1 - spatial.distance.cosine(arr1, arr2))


def create_stopwords():
    sf = open("stopwords.txt")
    stopwords = (" ").join(sf).split()
    return set(stopwords)


def get_top5_of_queries(matrix, queries_vectors, queries):
    queries_scores = []
    for i in range(len(queries_vectors)):
        queries_scores.append([])  # initialize empty list for each query

    for i in range(len(matrix)):

        arr = matrix[i][1]
        title = matrix[i][0]
        for j in range(len(queries_vectors)):
            vector = queries_vectors[j]
            score = compare(arr, vector)
            score_tuple = (score, title)
            queries_scores[j].append(score_tuple)

    for i in range(len(queries_scores)):
        scores = queries_scores[i]
        wiki_title = queries[i]
        sorted_scores = sorted(scores, key=lambda score: score[0], reverse=True)

        print("Titles of top five similar articles for {} are:".format(wiki_title))
        for j in range(5):
            title = sorted_scores[j][1]
            cosine_score = sorted_scores[j][0]

            print("{:<40s}{:>20}".format(title, str(cosine_score)))
            print(("=" * 50))


def doc2vec(corpus_dir_path, matrix_to_save_path, model_to_save_path):

    mark_new_topic = []
    all_tokens = set()
    num_docs = 0
    list_of_docs = []
    # list of set where each set represents all the tokens that are inside that topic
    list_of_docs_set = []
    stopwords = create_stopwords()
    doc_index_to_name_dict = {}

    for filename in os.listdir(corpus_dir_path):
        doc_index_to_name_dict[num_docs] = filename
        file = open(corpus_dir_path + "/" + filename, "r")
        doc_tokens = tokenize((" ").join(file), stopwords)

        # for wrapper
        doc_index_to_name_dict[num_docs] = filename

        all_tokens = all_tokens.union(doc_tokens)
        list_of_docs.append(doc_tokens)
        list_of_docs_set.append(set(doc_tokens))
        num_docs += 1

    mark_new_topic.append(num_docs)

    # removes token that only exists in one document
    tmp_list_of_docs = []
    count = 0
    removed_token = set()
    print("removing unique words from docs")
    for doc in list_of_docs:
        print(".", end="")
        tmp_list_of_docs.append([])
        for token in doc:

            if token in removed_token:
                continue

            exist_count = 0
            for doc_set in list_of_docs_set:
                if token in doc_set:
                    exist_count += 1;

                if exist_count > 1:
                    break

            # 1 if exists in only one doc
            if exist_count <= 1:
                removed_token.add(token)
                if token in all_tokens:  # might have already been removed
                    all_tokens.remove(token)
            else:
                tmp_list_of_docs[count].append(token)

        count += 1
    print("\nprocessed {} docs".format(len(list_of_docs)))

    list_of_docs = tmp_list_of_docs

    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(list_of_docs)]
    model = Doc2Vec(documents, vector_size=100, window=5, min_count=1, workers=4)
    document_vectors = [model.dv[i] for i in range(len(documents))]

    model_export_data = []
    for doc_id in range(len(list_of_docs)):
        document_vector = document_vectors[doc_id]
        document_name = doc_index_to_name_dict[doc_id]  # TODO MAKE THIS WORK
        document_entry = (document_name, document_vector)
        model_export_data.append(document_entry)

    # Convert to numpy array and save to file
    model_export_data_array = np.array(model_export_data)
    outfile = open(matrix_to_save_path, 'wb')
    np.save(outfile, model_export_data_array)
    outfile.close()

    # Save model
    model.save(model_to_save_path)


def get_list_of_tokens_from_queries(queries):
    queries_texts = []
    tokenized_queries = []
    stopwords = create_stopwords()
    return_queries = []

    for wiki_title in queries:
        try:
            article_text = wikipedia.page(wiki_title).content
            queries_texts.append(article_text)
            return_queries.append(wiki_title)
            print("Found {}.".format(wiki_title))

        except:
            print("{} does not exist on wiki.".format(wiki_title))
            queries_texts.append(wiki_title)

    for text in queries_texts:
        tokenized_text = tokenize(text, stopwords)
        tokenized_queries.append(tokenized_text)

    return tokenized_queries


def query_model(queries, matrix_path, model_path):
    queries_tokens = get_list_of_tokens_from_queries(queries)

    matrix = load_dat(matrix_path)
    model = Doc2Vec.load(model_path)
    queries_vectors = []
    for query_token in queries_tokens:
        vector = model.infer_vector(query_token)
        queries_vectors.append(vector)

    get_top5_of_queries(matrix, queries_vectors, queries)


def search_engine():
    query_topics = []
    print("\n\n\n")
    print("Enter the topics(one at a time) you want to look up, separated by ENTER and type \"done\" when finished.")
    print("\n\n\n")
    while True:
        query_input = input("Enter a wiki_topic: ")
        if query_input.lower() == "done":
            break
        query_topics.append(query_input)

    query_model(query_topics)


def main():
    matrix_path = "./bot_dependencies/matrix.dat"
    model_path = "./bot_dependencies/word2vec.model"
    corpus_path = "./movie_corpus"

    # doc2vec(corpus_path, matrix_path, model_path)

    queries = [
    	"Mulan (2020 film) - Wikipedia",
    	"Moscato d'Asti - Wikipedia",
    	"Fortnite - Wikipedia",
        "pqodjpadm"
    ]

    query_model(queries, matrix_path, model_path)


if __name__ == '__main__':
    main()
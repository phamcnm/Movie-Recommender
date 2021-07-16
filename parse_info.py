import spacy 

nlp = spacy.load("en_core_web_sm")

def parse_label_from_text(text, person_dict, loc_dict):
	"""
	Parses all the spacy objects in the given text that match one of the labels
	given in the label_lst

	Parameter:
	label_lst: list of label strings
	text: text to be parsed
	attempt_count: integer of the current iteration

	Return:
	list of spacy_object.ents that matches one of the labels in label_lst or None if 
	no such object exists
	"""
	global nlp 

	doc = nlp(text)
	# parse PERSON entities
	for ent in doc.ents:
		if ent.label_ in ["PERSON"]:
			if ent.text not in person_dict:
				person_dict[ent.text] = 1
			else:
				person_dict[ent.text]+=1
		elif ent.label_ in ["LOC", "GPE"]:
			if ent.text not in loc_dict:
				loc_dict[ent.text] = 1 
			else:
				loc_dict[ent.text]+=1
		else:
			continue
	dict_list = [person_dict, loc_dict]
	return dict_list


def pick_top_three(text):
	"""
	Finds the top 3 most appeared persons and top 3 most appeared locations from the text
	Parameters:
		text: the text to look at
	Returns: 
		result_list: a list of 2 lists, one is top 3 persons, the other one is top 3 locations
	"""
	person_dict = {}
	loc_dict = {} 

	result_list = []
	dict_list = parse_label_from_text(text, person_dict, loc_dict)
	for dictionary in dict_list:
		sorted_tuples = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
		picked = []
		for i in range(min(len(sorted_tuples), 3)):
			picked.append(sorted_tuples[i][0])
		result_list.append(picked)

	return result_list


def find_keyword_chunks(text, keywords):
	doc = nlp(text)
	summary_candidates = {}
	for sentence in doc.sents:
		summary_candidates[sentence.text] = 0
		for noun_chunk in sentence:
			if noun_chunk.text in keywords:
				summary_candidates[sentence.text] += 1
	
	sorted_tuple = sorted(summary_candidates.items(), key=lambda item: item[1], reverse=True)
	picked_sentences = []
	# print(sorted_tuples)
	for i in range(min(len(sorted_tuple), 3)):
		picked_sentences.append(sorted_tuple[i][0])
			
	return picked_sentences

def subj_verb_prep_obj_chunk(doc):
	for noun_chunk in doc.noun_chunks:
		if noun_chunk.root.dep_ != 'nsubj':
			continue
		subj = noun_chunk.root
		verb = subj.head
		for child in verb.children:
			if child.dep_ == 'prep':
				prep = child
				for prep_child in child.children:
					if prep_child.dep_ == 'pobj':
						obj = prep_child
						subj_verb_prep_obj_chunk = {
							"subject": subj,
							"verb": verb,
							"preposotion": prep,
							"object": obj	
						}
						return subj_verb_prep_obj_chunk

	return None

def find_verb_chunk(doc):
	"""
	Returns a dictionary representing a simple verb chunk
	with a subject, verb, object.
	"""
	for noun_chunk in doc.noun_chunks:
		if noun_chunk.root.dep_ != 'nsubj':
			continue
		subj = noun_chunk.root
		verb = subj.head
		for child in verb.children:
			obj = child
			if child.dep_ == 'dobj':
				verb_chunk = {
					"subject": subj,
					"verb": verb,
					"object": obj
				}
				return verb_chunk
		return None

def find_subj_verb_chunk(doc):
	"""
	Returns a dictionary representing a simple verb chunk
	with a subject and verb.
	"""
	for noun_chunk in doc.noun_chunks:
		if noun_chunk.root.dep_ != 'nsubj':
			continue
		subj = noun_chunk.root
		verb = subj.head
		return({					
			"subject": subj,
			"verb": verb
		})

	return None


def find_subj_chunk(doc):
	"""
	Returns a dictionary representing a simple verb chunk
	with a subject.
	"""
	for noun_chunk in doc.noun_chunks:
		if noun_chunk.root.dep_ != 'nsubj':
			continue
		subj = noun_chunk.root
		return({					
			"subject": subj
		})

	return None


def get_chunk(sentence):
	doc = nlp(sentence)
	result = subj_verb_prep_obj_chunk(doc)
	if result != None:
		return result
	result = find_verb_chunk(doc)
	if result != None:
		return result
	result = find_subj_verb_chunk(doc)
	if result != None:
		return result
	result = find_subj_chunk(doc)
	return result


def rephrase(sentence, keyword):
	chunk = get_chunk(sentence)
	subj = chunk["subject"] if chunk is not None and "subject" in chunk else keyword
	verb = chunk["verb"] if chunk is not None and "verb" in chunk else "did"
	prep = chunk["preposotion"] if chunk is not None and "preposotion" in chunk else None
	obj = chunk["object"] if chunk is not None and "object" in chunk else "some mysterious stuff"

	if prep != None:
		rephrased_sentence = "{} {} {} {}.".format(subj, verb, prep, obj)
	else:
		rephrased_sentence = "{} {} {}.".format(subj, verb, obj)

	return rephrased_sentence


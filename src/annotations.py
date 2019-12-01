import nltk
nltk.download('wordnet')
nltk.download('wordnet_ic')
from nltk.corpus import wordnet
from pattern.text.en import lemma, lexeme
from tqdm import tqdm


with open('out/annotation_dataset.txt', 'r') as file:
	annotations_data = file.readlines()

annotations_data = [line[:-1].split('\t') for line in annotations_data]

synonyms, related = {}, {}
part_of, made_of = {}, {}
hyponyms, hyperonyms = {}, {}
cohyponyms = {}

for annotation in annotations_data:
	# structure of an annotation is ['kind', 'first_neigh', 'second_neigh']
	kind, first, second = annotation[0], annotation[1].lower(), annotation[2].lower()

	if kind == 's':
		if first not in synonyms:
			synonyms[first] = []
		if second not in synonyms:
			synonyms[second] = []
		synonyms[first].append(second)
		synonyms[second].append(first)

	elif kind == 't':
		if first not in related:
			related[first] = []
		if second not in related:
			related[second] = []
		related[first].append(second)
		related[second].append(first)

	# those two are inverse of one another
	elif kind == 'm':
		if first not in part_of:
			part_of[first] = []
		if second not in made_of:
			made_of[second] = []
		part_of[first].append(second)
		made_of[second].append(first)
	elif kind == 'M':
		if first not in made_of:
			made_of[first] = []
		if second not in part_of:
			part_of[second] = []
		made_of[first].append(second)
		part_of[second].append(first)
	
	# those two are inverse of one another
	elif kind in ['h', 'hyponym']:
		if first not in hyponyms:
			hyponyms[first] = []
		if second not in hyperonyms:
			hyperonyms[second] = []
		hyponyms[first].append(second)
		hyperonyms[second].append(first)
	elif kind in ['H', 'hypernym']:
		if first not in hyperonyms:
			hyperonyms[first] = []
		if second not in hyponyms:
			hyponyms[second] = []
		hyperonyms[first].append(second)
		hyponyms[second].append(first)

	elif kind in ['S', 'cohyponym', 'distributional', 'functional', 'visual']:
		if first not in cohyponyms:
			cohyponyms[first] = []
		if second not in cohyponyms:
			cohyponyms[second] = []
		cohyponyms[first].append(second)
		cohyponyms[second].append(first)


def get_hypo_cohypo_hyper(word):
	hyponyms, cohyponyms, hypernyms = [], [], []
	for syn in wordnet.synsets(word):
		if syn.lemmas()[0].name().lower() == word:
			for l in syn.hyponyms():
				hyponyms.append(l.lemmas()[0].name().lower())
			for l in syn.hypernyms():
				hypernyms.append(l.lemmas()[0].name().lower())

	for hyper in hypernyms:
		for syn in wordnet.synsets(hyper):
			if syn.lemmas()[0].name().lower() == hyper:
				for l in syn.hyponyms():
					cohyponyms.append(l.lemmas()[0].name().lower())

	return set(hyponyms), set(cohyponyms), set(hypernyms)


def get_partof_madeof(word):
	partof, madeof = [], []
	for syn in wordnet.synsets(word):
		if syn.lemmas()[0].name().lower() == word:
			for l in syn.part_meronyms():
				partof.append(l.lemmas()[0].name().lower())
			for l in syn.substance_meronyms():
				partof.append(l.lemmas()[0].name().lower())
			for l in syn.part_holonyms():
				madeof.append(l.lemmas()[0].name().lower())
			for l in syn.substance_holonyms():
				madeof.append(l.lemmas()[0].name().lower())
	return set(partof), set(madeof)
 

def get_syn_ant(word):
	synonyms, antonyms = [], []
	for syn in wordnet.synsets(word):
		if syn.lemmas()[0].name().lower() == word:
			for l in syn.lemmas():
				synonyms.append(l.name().lower())
				if l.antonyms():
					antonyms.append(l.antonyms()[0].name())
	return set(synonyms), set(antonyms)



with open('out/voisins', 'r') as file:
	lines = file.readlines()

annotations = []

"""
def tqdm(anything):
	return anything
"""

for line in tqdm(lines):
	line = line.split()
	word, n_neighbors, neighbors = line[0], line[1], line[2:]

	try:
		word_basis = lemma(word)
	except RuntimeError:
		word_basis = lemma(word)

	word_lex = lexeme(word)

	hypo, cohypo, hyper = get_hypo_cohypo_hyper(word_basis)
	partof, madeof = get_partof_madeof(word_basis)
	syn, ant = get_syn_ant(word_basis)
	
	hypo.discard(word_basis)
	cohypo.discard(word_basis)
	hyper.discard(word_basis)
	syn.discard(word_basis)
	ant.discard(word_basis)
	partof.discard(word_basis)
	madeof.discard(word_basis)

	annotated_neighbors = []
	
	for neigh in neighbors:
		
		kinds = ''

		########## USING NLTK LISTS ##########

		if neigh in ant:
			kinds += '[ANTONYM]'
		if neigh in hypo:
			kinds += '[HYPO]'
		if neigh in hyper:
			kinds += '[HYPER]'

		if kinds == '' and neigh in word_lex:
			kinds += '[MORPHO]'
		if kinds == '' and word[:2] == neigh[:2] and nltk.edit_distance(word, neigh) == 1:
			kinds += '[MORPHO]'

		if '[MORPHO]' not in kinds:

			if neigh in syn:
				kinds += '[SYNONYM]'
			if neigh in partof:
				kinds += '[PARTOF]'
			if neigh in madeof:
				kinds += '[MADEOF]'

			if '[ANTONYM]' not in kinds and '[SYNONYM]' not in kinds:
				if neigh in cohypo:
					kinds += '[COHYPO]'

		########## USING OTHER LISTS ##########

		if neigh in related and word in related[neigh]:
			kinds += '[RELATED]'
		if neigh in hyponyms and word in hyponyms[neigh] and '[HYPO]' not in kinds:
			kinds += '[HYPO]'
		if neigh in hyperonyms and word in hyperonyms[neigh] and '[HYPER]' not in kinds:
			kinds += '[HYPER]'

		if '[MORPHO]' not in kinds:

			if neigh in synonyms and word in synonyms[neigh] and '[SYNONYM]' not in kinds:
				kinds += '[SYNONYM]'
			if neigh in part_of and word in part_of[neigh] and '[PARTOF]' not in kinds:
				kinds += '[PARTOF]'
			if neigh in made_of and word in made_of[neigh] and '[MADEOF]' not in kinds:
				kinds += '[MADEOF]'

			if '[ANTONYM]' not in kinds and '[SYNONYM]' not in kinds:
				if neigh in cohyponyms and word in cohyponyms[neigh] and '[COHYPO]' not in kinds:
					kinds += '[COHYPO]'


		if kinds == '':
			if nltk.edit_distance(word, neigh) <= abs(len(word) - len(neigh)) and word[:2] == neigh[:2] \
				and ('_' in word and '_' in neigh or '_' not in word and '_' not in neigh):
				kinds += '[MORPHO]'
		
		if kinds != '':
			annotated_neighbors.append(neigh + kinds)
	
	if len(annotated_neighbors) > 1:
		annotations.append([word] + [n_neighbors] + [annotated_neighbors])

with open('out/annotations', 'w') as file:
	for entry in annotations:
		word, n_neighbors, neighbors = entry[0], entry[1], ' '.join(entry[2])
		file.write('%-25s %-4s %s\n' % (word, n_neighbors, neighbors))

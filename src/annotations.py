def write_to_csv(filename, neigh_pairs):
	path = 'out/' + filename + '.csv'
	with open(path, 'w') as file:
		for pair in neigh_pairs:
			file.write('\t'.join(pair) + '\n')


with open('out/annotation_dataset.txt', 'r') as file:
	annotations = file.readlines()

annotations = [line[:-1].split('\t') for line in annotations]

synonyms, related = {}, {}
part_of, made_of = {}, {}
hyponyms, hyperonyms = {}, {}
cohyponyms = {}

for annotation in annotations:
	# structure of an annotation is ['kind', 'first_neigh', 'second_neigh']
	kind, first, second = annotation

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

	elif kind in ['S', 'cohyponym']:
		if first not in cohyponyms:
			cohyponyms[first] = []
		if second not in cohyponyms:
			cohyponyms[second] = []
		cohyponyms[first].append(second)
		cohyponyms[second].append(first)

"""
write_to_csv('synonyms', synonyms)
write_to_csv('related', related)
write_to_csv('part_of', part_of)
write_to_csv('made_of', made_of)
write_to_csv('hyponyms', hyponyms)
write_to_csv('hyperonyms', hyperonyms)
write_to_csv('cohyponyms', cohyponyms)
"""

new_content = []

with open('out/voisins', 'r') as file:
	i = 0
	for line in file:
		line = line.split()
		word, n_neighbors, neighbors = line[0], line[1], line[2:]

		new_neighbors = []
		for neigh in neighbors:
			kinds = ''
			if neigh in synonyms and word in synonyms[neigh]:
				kinds += '[SYNONYM]'
			if neigh in related and word in related[neigh]:
				kinds += '[RELATED]'
			if neigh in part_of and word in part_of[neigh]:
				kinds += '[PARTOF]'
			if neigh in made_of and word in made_of[neigh]:
				kinds += '[MADEOF]'
			if neigh in hyponyms and word in hyponyms[neigh]:
				kinds += '[HYPO]'
			if neigh in cohyponyms and word in cohyponyms[neigh]:
				kinds += '[COHYPO]'
			if neigh in hyperonyms and word in hyperonyms[neigh]:
				kinds += '[HYPER]'

			if kinds != '':
				new_neighbors.append(neigh + kinds)

		if len(new_neighbors) > 1:
			new_content.append([word] + [n_neighbors] + [new_neighbors])
		#file.write('%-25s %-4s %s\n' % (neigh, n_neighbors[idx], neighbors))

		i += 1
		if i > 1000:
			break

print(new_content)
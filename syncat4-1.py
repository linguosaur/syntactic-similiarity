import operator, re, string, sys

def sim(context1, context2):
	c1 = context1.split(' ')
	c2 = context2.split(' ')
	simScore = 0.0
	for i in range(len(c1)):
		if c1[i] == '' or c2[i] == '': continue
		elif c1[i] == c2[i]: simScore += 1.0
		elif c1[i] in sims and c2[i] in sims[c1[i]]: 
			simScore += sims[c1[i]][c2[i]]
	return simScore/len(c1)

def stripPunc(string):
	newString = re.sub('[^\w\d\s]+(?=[\s$])', '', string)
	newString = re.sub('(?<=[\s^])[^\w\d\s]+', '', newString)
	newString = re.sub('_', '', newString)
	newString = re.sub('[^\w\d\.\'\-\s]', '', newString)
	newString = re.sub('(?<=\s)[\-](?=\s)', '', newString)
	return newString

def printNearestNeighbours(neighbours=-1):
	for word1 in sims:
		print word1
		print '-----'
		if neighbours > -1:
			for word2, simScore in sorted(sims[word1].iteritems(), key=operator.itemgetter(1), reverse=True)[:n]:
				if word1 != word2:
					print word2 + '\t' + repr(simScore)
		elif neighbours == -1:
			for word2, simScore in sorted(sims[word1].iteritems(), key=operator.itemgetter(1), reverse=True):
				if word1 != word2:
					print word2 + '\t' + repr(simScore)
		else:
			sys.stderr.write('Bad parameter for printNearestNeighbours')
			return
		print

# every word in its own cluster to start, then adding edges from most similar to least
def getClusters(k):
	wordTypes = sims.keys()
	if len(wordTypes) < k: 
		sys.stderr.write('Number of clusters requested is greater than number of wordTypes.')
		return -1

	clusters2words = {}
	words2clusters = {}
	wordpairs2simScores = {}
	for i in range(len(wordTypes)):
		clusters2words[i] = set([wordTypes[i]])
		words2clusters[wordTypes[i]] = i
	if len(clusters2words) == k: return clusters2words

	for word1 in sims:
		for word2 in sims[word1]:
			if word1 != word2 and word2 + ' ' + word1 not in wordpairs2simScores:
				wordpairs2simScores[word1 + ' ' + word2] = sims[word1][word2]
	wordpairsAndScoresSorted = sorted(wordpairs2simScores.iteritems(), key=operator.itemgetter(1), reverse=True)

	print
	for wordpair, simScore in wordpairsAndScoresSorted[:100]:
		print wordpair + ': ' + repr(simScore)
	print

	print
	edgeCount = 0
	for wordpairAndScore in wordpairsAndScoresSorted:
		[word1, word2] = wordpairAndScore[0].split()
		cluster1 = words2clusters[word1]
		cluster2 = words2clusters[word2]
		if cluster1 != cluster2:
			clusters2words[cluster1] |= clusters2words[cluster2]
			for word in clusters2words[cluster2]:
				words2clusters[word] = cluster1
			clusters2words.pop(cluster2)

			edgeCount += 1
			print repr(edgeCount) + ': adding ' + repr(wordpairAndScore)

			if len(clusters2words) == k:
				return clusters2words

def printClusters(clusters2words):
	for cluster in clusters2words.keys():
		print repr(cluster) + ':'
		print '-----'
		for word in clusters2words[cluster]:
			print word
		print

sims = {}
newSims = {}
contexts = {}

textFile = open(sys.argv[1])
textFileLines = textFile.readlines()
textFile.close()

contextLength = 1 
lineNum = 0
for line in textFileLines:
	sys.stderr.write(repr(lineNum) + ', ')
	lineNum += 1
	splitLine = line.lower().split()
	lineLength = len(splitLine)
	for i in range(lineLength):
		word_i = splitLine[i]
		if i >= contextLength:
			thisContext = splitLine[i-contextLength:i] 
		else:
			thisContext = (contextLength-i)*['^'] + splitLine[0:i]
		if i <= lineLength-contextLength-1:
			thisContext += splitLine[i+1:i+contextLength+1]
		else:
			thisContext += splitLine[i+1:lineLength] + (i-(lineLength-contextLength-1))*['$']
		thisContext = ' '.join(thisContext)

		if word_i not in contexts: contexts[word_i] = set([thisContext])
		else: contexts[word_i].add(thisContext)
sys.stderr.write('\n\n')

# print contexts
for word in contexts:
	print word + '\t' + repr(contexts[word])
print

vocabSize = len(contexts.keys())
minAvgDiff = 0.00001
iteration = 0
while (True):
	sys.stderr.write(repr(iteration) + '\t')
	iteration += 1
	newSims = {}
	simsNotEmpty = len(sims.keys()) > 0
	if simsNotEmpty: avgDiff = 0.0
	wordNum = 0
	for word1 in contexts:
		wordNum += 1
		totalWord1Contexts = len(contexts[word1])
		newSims[word1] = {}
		for word2 in contexts:
			if word2 not in newSims[word1]:
				newSims[word1][word2] = 0.0

			if word1 == word2:
				newSims[word1][word2] = 1.0
			elif word2 in newSims and word1 in newSims[word2]:
				newSims[word1][word2] = newSims[word2][word1]
			else:
				set1 = contexts[word1]
				set2 = contexts[word2]
				intersection = set1.intersection(set2)
				set1unique = set1.difference(intersection)
				set2unique = set2.difference(intersection)
				
				newSims[word1][word2] += 1.0 * len(intersection)
				if len(set2unique) > 0:
					for context1 in set1unique:
						simScores = []
						for context2 in set2:
							simScores.append(sim(context1, context2))
						newSims[word1][word2] += max(simScores)
				if len(set1unique) > 0:
					for context2 in set2unique:
						simScores = []
						for context1 in set1:
							simScores.append(sim(context1, context2))
						newSims[word1][word2] += max(simScores)
				newSims[word1][word2] /= len(set1.union(set2))

				if simsNotEmpty:
					avgDiff += abs(newSims[word1][word2] - sims[word1][word2])
	
	sims = newSims
	if simsNotEmpty: 
		avgDiff /= vocabSize * (vocabSize-1) / 2.0
		sys.stderr.write('\naverage difference: ' + repr(avgDiff))
		if avgDiff < minAvgDiff: 
			sys.stderr.write('\n')
			break
	sys.stderr.write('\n')

NEAREST_NEIGHBOURS = 50
#NUM_OF_CLUSTERS = 20

#printNearestNeighbours(NEAREST_NEIGHBOURS)
printNearestNeighbours()

#print
#print
#sys.stderr.write('\nclustering . . . \n')
#clusters = getClusters(NUM_OF_CLUSTERS)
#if clusters != -1:
#	printClusters(clusters)

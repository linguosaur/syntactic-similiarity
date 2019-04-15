from __future__ import with_statement
from bigfloat import factorial, precision
import operator, sys

bigFloatPrecision = 6100

def c(n, k):
	with precision(bigFloatPrecision):
		return factorial(n) / factorial(n-k) / factorial(k)

def precisionSum(n, k):
	if (n,k) in precisions: return precisions[(n,k)]

	zeroK = [(a,b) for (a,b) in precisions if b == 0]
	nEqualsK = [(a,b) for (a,b) in precisions if a == b]
	maxNWithZeroK = 0
	if len(zeroK) > 0:
		maxNWithZeroK = max(zeroK)[0]
	maxNEqualsK = k
	if len(nEqualsK) > 0:
		maxNEqualsK = max(nEqualsK)[0]

	for i in range(maxNWithZeroK+1, n+1):
		for j in range(max(0, k-(n-i)), i-maxNWithZeroK+1) + range(maxNEqualsK+1, min(i, k)+1):
			if i == j:
				precisions[(i,j)] = 1.0 * i
			elif j == 0:
				precisions[(i,j)] = 0.0
			else:
				precisions[(i,j)] = precisions[(i-1, j)] + precisions[(i-1, j-1)] + c(i-1, j-1) * 1.0 * j/i
	
	return precisions[(n,k)]

def precisionSumRecursive(n, k):
	if k == n:
		return 1.0 * n
	if k == 0:
		return 0.0
	if (n, k) in precisions:
		return precisions[(n,k)]
	if (n-1, k) not in precisions:
		precisions[(n-1, k)] = precisionSum(n-1, k)
	if (n-1, k-1) not in precisions:
		precisions[(n-1, k-1)] = precisionSum(n-1, k-1)
	precisions[(n,k)] = precisions[(n-1, k)] + precisions[(n-1, k-1)] + c(n-1, k-1) * 1.0 * k/n
	
	return precisions[(n,k)]

def randomP(ref, ranking):
	ranksOfRels = []

	for rank in range(1, len(ranking)+1):
		if len(ref & ranking[rank-1]) > 0:
			ranksOfRels.append(len(ranksOfRels)+1)

	if len(ranksOfRels) > 0:
		return precisionSum(len(ranking), len(ranksOfRels)) / len(ranksOfRels) / c(len(ranking), len(ranksOfRels))

	return -1.0

def avgP(ref, ranking):
	precisionSum = 0.0
	numOfRels = 0

	for rank in range(1, len(ranking)+1):
		if len(ref & ranking[rank-1]) > 0:
			numOfRels += 1
			precisionSum += 1.0 * numOfRels / rank

	if numOfRels > 0:
		return precisionSum / numOfRels

	return -1.0

if len(sys.argv) < 2:
	sys.exit('Not enough arguments.\n')

precisions = {}
words2tags = {}
thisWordsTags = set([])
rankedTagList = []
avgPrecisions = {}
randomPrecisions = {}
thisWord = ''
avgPrecisionSum = 0.0
randomPrecisionSum = 0.0
numOfLists = 0

goldstdfile = open(sys.argv[2])
for line in goldstdfile:
	splitline = line.strip().split()
	if len(splitline) > 4:
		word = splitline[1].lower()
		pos = splitline[3]
		if pos[0].isalpha():
			if word in words2tags:
				words2tags[word].add(pos)
			else:
				words2tags[word] = set([pos])
goldstdfile.close()

print 'Vocabulary size' + '\t' + repr(len(words2tags))

outputfile = open(sys.argv[1])
wordNum = 0
sys.stderr.write('calculating . . . \n')
sys.stderr.write(repr(wordNum))
for line in outputfile:
	splitline = line.strip().split()
	if len(splitline) == 0 and len(thisWordsTags) > 0:
		avgPrecision = avgP(thisWordsTags, rankedTagList)
		randomPrecision = float(randomP(thisWordsTags, rankedTagList))
		avgPrecisions[thisWord] = avgPrecision
		randomPrecisions[thisWord] = randomPrecision
		if avgPrecision != -1.0:
			avgPrecisionSum += avgPrecision
		if randomPrecision != -1.0:
			randomPrecisionSum += randomPrecision
		numOfLists += 1
		thisWordsTags = []
		rankedTagList = []
		thisWord = ''
		wordNum += 1
		if wordNum % 10 == 0: 
			sys.stderr.write('\n' + repr(wordNum))
		else: 
			sys.stderr.write('.')
		sys.stderr.flush()
	elif len(splitline) == 1:
		word = splitline[0]
		if word != '-----':
			thisWord = word
			thisWordsTags = words2tags[thisWord]
	elif len(splitline) == 2:
		word = splitline[0]
		rankedTagList.append(words2tags[word])

sys.stderr.write('\n\nprinting\n')

for word, avgPrecision in sorted(avgPrecisions.iteritems(), key=operator.itemgetter(1), reverse=True):
	print word + '\t' + repr(avgPrecision) + '\t' + repr(randomPrecisions[word])

if numOfLists == len(words2tags):
	print 'Mean Average Precision' + '\t' + repr(avgPrecisionSum / numOfLists) + '\t' + repr(randomPrecisionSum / numOfLists)
elif numOfLists < len(words2tags):
	sys.exit('Rankings missing.')
else:
	sys.exit('Too many rankings.')

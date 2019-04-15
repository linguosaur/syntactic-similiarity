import sys

rankedWords = []
contexts = {}

wordListFile = open(sys.argv[2], 'r')
for line in wordListFile:
	word = line.strip()
	rankedWords.append(word)
wordListFile.close()

inputFile = open(sys.argv[1], 'r')

for line in inputFile:
	splitLine = line.strip().split('\t')
	if len(splitLine) < 2: break

	word = splitLine[0]
	contextSet = splitLine[1]
	contexts[word] = contextSet
	
for word in rankedWords:
	if word not in contexts:
		sys.exit(word + ' not in contexts.\n')

	print word + '\t' + contexts[word]

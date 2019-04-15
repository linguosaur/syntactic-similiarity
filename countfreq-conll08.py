import sys, operator

rankedWords = []

wordListFile = open(sys.argv[2], 'r')
for line in wordListFile:
	word = line.strip()
	rankedWords.append(word)
wordListFile.close()

inputFile = open(sys.argv[1], 'r')
freq = {}

for line in inputFile:
	splitLine = line.split('\t')
	if len(splitLine) < 4: continue

	word = splitLine[1].lower()
	pos = splitLine[3]
	
	if pos[0].isalpha():
		if word not in freq: freq[word] = 1
		else: freq[word] += 1

for word in rankedWords:
	if word not in freq:
		sys.exit(word + ' not in freq.\n')

	print word + '\t' + repr(freq[word])

import sys

textfile = open(sys.argv[1])
sent = []
for line in textfile:
	if line.strip() != "":
		splitline = line.split('\t')
		word = splitline[1]
		pos = splitline[3]
		if pos != '_':
			sent.append(word)
	else:
		print ' '.join(sent)
		sent = []

if sent != []:
	print ' '.join(sent)

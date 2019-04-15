from __future__ import with_statement
from bigfloat import factorial, precision
import sys

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
			if len(precisions) % 10000 == 0:
				sys.stdout.write(repr(len(precisions)))
				sys.stdout.flush()
			elif len(precisions) % 1000 == 0:
				sys.stdout.write('.')
				sys.stdout.flush()
	
	return precisions[(n,k)]

def precisionSumRecursive(n, k):
	if k == n:
		return 1.0 * n
	if k == 0:
		return 0.0
	if (n, k) in precisions:
		return precisions[(n,k)]
	if (n-1, k) not in precisions:
		precisions[(n-1, k)] = precisionSumRecursive(n-1, k)
	if (n-1, k-1) not in precisions:
		precisions[(n-1, k-1)] = precisionSumRecursive(n-1, k-1)
	precisions[(n,k)] = precisions[(n-1, k)] + precisions[(n-1, k-1)] + c(n-1, k-1) * 1.0 * k/n
	
	return precisions[(n,k)]


def getRanking(numMatches):
	return numMatches*[set([1])] + (rankingLength - numMatches)*[set([2])]

def getRanksOfRels(ranking, ref):
	ranks = []
	for rank in range(1, rankingLength+1):
		if len(ref & ranking[rank-1]) > 0:
			ranks.append(len(ranks)+1)
	return ranks

def getSetup(numMatches, ref):
	r = getRanking(numMatches)
	return [r, getRanksOfRels(r, ref)]
	

ref = set([1])
precisions = {}
rankingLength = 5
[ranking, ranksOfRels] = getSetup(0, ref)
print repr(float(precisionSum(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels))))

#precisions = {}
#rankingLength = 467
#
#print 'non-recursion:'
#
#[ranking, ranksOfRels] = getSetup(100, ref)
#print repr(precisionSum(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(60, ref)
#print repr(precisionSum(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(30, ref)
#print repr(precisionSum(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(200, ref)
#print repr(precisionSum(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(50, ref)
#print repr(precisionSum(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(30, ref)
#print repr(precisionSum(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(28, ref)
#print repr(precisionSum(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(60, ref)
#print repr(precisionSum(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(100, ref)
#print repr(precisionSum(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#
#precisions = {}
#
#print 'recursion:'
#
#[ranking, ranksOfRels] = getSetup(100, ref)
#print repr(precisionSumRecursive(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(60, ref)
#print repr(precisionSumRecursive(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(30, ref)
#print repr(precisionSumRecursive(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(200, ref)
#print repr(precisionSumRecursive(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(50, ref)
#print repr(precisionSumRecursive(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(30, ref)
#print repr(precisionSumRecursive(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(28, ref)
#print repr(precisionSumRecursive(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(60, ref)
#print repr(precisionSumRecursive(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))
#
#[ranking, ranksOfRels] = getSetup(100, ref)
#print repr(precisionSumRecursive(rankingLength, len(ranksOfRels)) / len(ranksOfRels) / c(rankingLength, len(ranksOfRels)))


#while True:
#	precisionSum = 0.0
#	for i in range(len(ranksOfRels)):
#		precisionSum += 1.0 * (i+1) / ranksOfRels[i]
#	permutations += 1
#
#	avgPrecision = precisionSum / len(ranksOfRels)
#	print repr(ranksOfRels) + '\t' + repr(avgPrecision)
#	avgPrecisionSum += avgPrecision
#
#	incremented = False
#	for i in range(len(ranksOfRels)-1, -1, -1):
#		if ranksOfRels[i] < len(ranking) - len(ranksOfRels) + i + 1:
#			ranksOfRels[i] += 1
#			incremented = True
#			if i < len(ranksOfRels) - 1:
#				for j in range(i+1, len(ranksOfRels)):
#					ranksOfRels[j] = ranksOfRels[i] + j - i
#			break
#
#	if not incremented: break
#

import household as hh
import numpy as np
import random
from operator import itemgetter
import ndcg
import os



def loadPredict(fileName):
	dataFile = open(os.path.expanduser("~/Desktop/IntroML/expedia/svmRank/try/"+fileName))
	predicts = []
	for each in dataFile:
		each = each.rstrip('\n')
		each = float(each)
		predicts.append(each)
	return predicts

def loadTest(fileName):
	dataFile = open(os.path.expanduser("~/Desktop/IntroML/expedia/svmRank/try/"+fileName))
	ids = []
	labels = []
	for each in dataFile:
		each = each.split()
		label = int(each[0])
		id = each[1]
		id = id.split(':')
		id = id[1]
		ids.append(id)
		labels.append(label)
		
	return labels, ids
	
# position higher better#
def writeForSVMRank(filename,matrix):
	file = open(filename+".dat","w")
	chosenFeatures = range(0,51)#+ range(54,117)
	# exclude booking and clicked and gross amount[0:50]+[54:117]
	featNumber = len(chosenFeatures)
	for i in range(len(matrix)):
		label = 0
		if (matrix[i][53] == 1) :
			label = 2
		elif (matrix[i][51] == 1):
			label = 1
		file.write(str(label)+" qid:"+str(int(matrix[i][0]))+" ")
		for j in range(len(chosenFeatures)):
			featNo = chosenFeatures[j]
			file.write(str(j+1)+":")
			file.write(str(matrix[i][featNo])+" ")
		file.write("\n")
	return 0


result = loadPredict('predictions')
[labelEval, searchID] = loadTest('test.dat')
# print predict
# print labels
# print ids


ourRank = []
results = hh.splitColumnsForEachID(searchID, result)
labels = hh.splitColumnsForEachID(searchID, labelEval)


for i in range(len(results)):
	rank = []
	for j in range(len(results[i])):
		rank.append((results[i][j], labels[i][j]))
	rank = sorted(rank, key=itemgetter(0))
	ourRank.append(rank)

# for each in ourRank:
# 	for eeach in each:
# 		print eeach
# 	print "\n"
	

ourRanksinTrueLabel = []
for each in ourRank:
	eachOurRank =  []
	for eeach in each:
		eachOurRank.append(eeach[1])
	ourRanksinTrueLabel.append(eachOurRank)

score = {2:5,1:1,0:0}
index = 0
count = 0
for each in ourRanksinTrueLabel:
	each.reverse()
	val =ndcg.calculateIndex(score,each)
	if val != 0:
		count += 1
		index += val

print "Total score: ", index/count


		
	
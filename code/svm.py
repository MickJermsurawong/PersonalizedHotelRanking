from pylab import *
from sklearn import svm
import household as hh
import numpy as np
import random

from operator import itemgetter
import ndcg

#Breakdown of features
previousRecord = [4,5]
hotelProp = [8,9,10,11,12,13,15,16]
typeOftrip = [18,19,20,21,22,23]
etc = [24,25]
comp = range(27,51)
relativeFreq = [54,55,56,57]
oneHotHotel = range(58,110)
sumComp = [110,111,112]
ratio = range(113,117)

#Separate data to train and evaluate set
allData = hh.getCSVmatrix("smalltrainOld&New2",20000)
trainData = allData[:3*(len(allData))/4]
evalData = allData[3*(len(allData))/4::]


#Separate three data sets 
#Positive - clicked , postivePos- Purchase, negative - Ignored
positive = []
positivePos = []
negative = []
for each in trainData:
	if (each[53] == "1"):
		positivePos.append(each)
	elif (each[51] == "1"):
		positive.append(each)
	else:
		negative.append(each)

#Find the minimum of the purchased or clicked
#and use that as the size of all the three sets	
sizePos = len(positive)
sizePosPos = len(positivePos)
size = min(sizePos, sizePosPos)
negative = random.sample(negative, 2*size)
positive = random.sample(positive, size)
positivePos = random.sample(positivePos, size)
trainData = positive + negative + positivePos

#Convert them to float value
trainData = hh.convertMatrixtoFloat(trainData)
evalData = hh.convertMatrixtoFloat(evalData)

#Get label for training set
label = []
for i in range(len(trainData)):
	if (trainData[i][53] == 1) :
		label.append(1)
	elif (trainData[i][51] == 1):
		label.append(1)
	else:
		label.append(0)
	trainData[i] = trainData[i][0:14]+ trainData[i][15:51]+trainData[i][54:117]

#Get label for evaluation set
labelEval = []
for i in range(len(evalData)):
	if (evalData[i][53] == 1 ):
		labelEval.append(1)
	elif (evalData[i][51] == 1):
		labelEval.append(1)
	else:
		labelEval.append(0)
	evalData[i] = evalData[i][0:14] +evalData[i][15:51] +evalData[i][54:117]

print "testing Size: ", len(evalData)
print "feature length: ", len(trainData[0])

print "Training"
c= -5
while (True):
	cval = 2**(c)
	c += 1
	print "C val: ", cval
	clf = svm.SVC(probability = True, C= cval, gamma = 0 )
	clf.fit(trainData, label) 
	result = clf.predict(evalData) 


	chosenCorrect = 0
	chosenWrong = 0
	ignoreCorrect = 0
	ignoreWrong = 0
	for i in range(len(result)):
		if labelEval[i] == 1:
			if result[i] == 1:
				chosenCorrect += 1
			else:
				chosenWrong += 1
		else:
			if result[i] == 1:
				ignoreWrong += 1
			else:
				ignoreCorrect +=1
	# #Check accuracy
# 	boughtCorrect = 0
# 	boughtWrong = 0
# 	clickCorrect = 0
# 	clickWrong = 0
# 	ignoreCorrect = 0
# 	ignoreWrong = 0
# 	for i in range(len(result)):
# 		if labelEval[i] == 2:
# 			if result[i] == 2:
# 				boughtCorrect += 1
# 			else:
# 				boughtWrong += 1
# 		elif labelEval[i] == 1:
# 			if result[i] == 1:
# 				clickCorrect +=1
# 			else:
# 				clickWrong +=1
# 		else:
# 			if result[i] == 1:
# 				ignoreWrong += 1
# 			else:
# 				ignoreCorrect +=1

	acB = float(chosenCorrect)/(chosenCorrect+chosenWrong)
	acIg = float(ignoreCorrect)/(ignoreCorrect+ignoreWrong)
# 	acClic = float(clickCorrect)/(clickCorrect+clickWrong)
	print "boughtCorrect:", chosenCorrect, "/", chosenCorrect+chosenWrong, " :", acB
	print "IgnoreCorrect:", ignoreCorrect, "/", ignoreCorrect+ignoreWrong, " :", acIg
# 	print "clickCorrect:", clickCorrect, "/", clickCorrect+clickWrong, " :", acClic

# 	print "Accuracy:", (acB + acIg + acClic) / 3
	print "Accuracy:", (acB + acIg) / 2
	
	
	#Get probability of each point
	allCheck = []
	refinedScore = []
	propResult = clf.decision_function(evalData)
	for i in range(len(result)):
		#Times (label+1) * max(value of the probability)
		refinedScore.append((result[i]+1)*max(propResult[i]))
	result = propResult

	#Get searchIDs
	searchID = hh.getColumn(evalData,0)

	#Put Truelabels, predicted labels(weighted with probability) back into list per searchID

	results = hh.splitColumnsForEachID(searchID, result)
	labels = hh.splitColumnsForEachID(searchID, labelEval)

	#Put our predicted labels and true label in a tuple
	#Rank the predicted labels
	ourRank = []
	for i in range(len(results)):
		rank = []
		for j in range(len(results[i])):
			rank.append((results[i][j], labels[i][j]))
		rank = sorted(rank, key=itemgetter(0))
		ourRank.append(rank)

	#Acesss the true label and put them in our predicted order
	ourRanksinTrueLabel = []
	for each in ourRank:
		eachOurRank =  []
		for eeach in each:
			eachOurRank.append(eeach[1])
		ourRanksinTrueLabel.append(eachOurRank)

	#Grade and calculate the score
	score = {2:5,1:1,0:0}
	index = 0
	count = 0
	for each in ourRanksinTrueLabel:
		each.reverse()
		val =ndcg.calculateIndex(score,each)
		# if it is zero, meaning the whole ranking doesn't contain bought/clicked
		# we don't count them
		if val != 0:
			count += 1
			index += val
	#Get average of all the scores
	print "Total score: ", index/count
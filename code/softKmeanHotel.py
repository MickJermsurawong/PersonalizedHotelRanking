from pylab import *
from sklearn import svm
import household as hh
import numpy as np
import random
from sklearn import tree
from sklearn import ensemble
from operator import itemgetter
import ndcg

def plotGraph2D(xData,xLabel,yData,yLabel,titleGraph):
	xArray= np.array(xData)
	yArray = np.array(yData)
	plot(xArray, yArray)
	xlabel(xLabel)
	ylabel(yLabel)
	title(titleGraph)
	grid(True)
	savefig(titleGraph+".png")
	clf()


def softKmean(X, crossX):
	import numpy as np
	from scipy import linalg
	import pylab as pl
	from sklearn import mixture
	
	X = np.array(X)
	crossX = np.array(crossX)
	lowest_bic = np.infty
	bic = []
	prop = []
	Allprop = []
	highest_prob = -np.infty
	n_components_range = range(1,30)
	cv_types = ['diag']
	for cv_type in cv_types:
		for n_components in n_components_range:
			# Fit a mixture of gaussians with EM
			gmm = mixture.GMM(n_components=n_components, covariance_type=cv_type)
			gmm.fit(X)
			print "fitting: ", cv_type, n_components,
			(logprob,respon) = gmm.score_samples(crossX)
			print "cross prob", sum(gmm.score(crossX)),
			bicScore = gmm.bic(crossX)
			print "bic", bicScore
			bic.append(bicScore)

			if bic[-1] < lowest_bic:
				lowest_bic = bic[-1]
				best_gmm = gmm
				print "Best so far: ", cv_type, n_components
	return best_gmm, n_components_range, bic
	

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
allData = hh.getCSVmatrix("smalltrainOld&New2",100000)
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
negative = random.sample(negative, size)
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
		label.append(2)
	elif (trainData[i][51] == 1):
		label.append(1)
	else:
		label.append(0)
	trainData[i] = trainData[i][0:14]+ trainData[i][15:51]+trainData[i][54:117]

#Get label for evaluation set
labelEval = []
for i in range(len(evalData)):
	if (evalData[i][53] == 1 ):
		labelEval.append(2)
	elif (evalData[i][51] == 1):
		labelEval.append(1)
	else:
		labelEval.append(0)
	evalData[i] = evalData[i][0:14] +evalData[i][15:51] +evalData[i][54:117]

for i in range(len(trainData)):
	trainData[i] = trainData[i][8:17]
for i in range(len(evalData)):
	evalData[i] = evalData[i][8:17]
	

(a,x,y) = softKmean(trainData, evalData)
plotGraph2D(x,"cluster size",y,"BIC","BIC VS Cluster Size")
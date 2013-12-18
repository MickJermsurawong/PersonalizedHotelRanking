import household as hh
import numpy as np
import random
from operator import itemgetter
import ndcg
import os

# position higher better#
def writeForSVMRank(filename,matrix):
	file = open(os.path.expanduser("~/Desktop/IntroML/expedia/svmRank/try/"+filename+".dat"),"w")
# 	chosenFeatures = range(0,51)+ range(54,117)
  	chosenFeatures = range(8,14)+ range(54,117)
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


previousRecord = [4,5]
hotelProp = [8,9,10,11,12,13,15,16]
typeOftrip = [18,19,20,21,22,23]
etc = [24,25]
comp = range(27,51)
relativeFreq = [54,55,56,57]
oneHotHotel = range(58,110)
sumComp = [110,111,112]
ratio = range(113,117)

allData = hh.getCSVmatrix("smalltrainOld&New2",100000)

trainData = allData[:3*(len(allData))/4]
evalData = allData[3*(len(allData))/4::]
print len(trainData)
print len(evalData)


trainData = hh.convertMatrixtoFloat(trainData)
evalData = hh.convertMatrixtoFloat(evalData)

writeForSVMRank('train',trainData)
writeForSVMRank('test',evalData)


		
	
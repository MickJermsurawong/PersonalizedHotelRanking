from math import log
import numpy as np

#Get nested list of according to IDS
def splitColumnsForEachID(searchIDs, column):
	previousID = searchIDs[0]
	newSearchIDInfo = []
	allInforPerSearch = []
	for i in range(len(searchIDs)):
		currentID = searchIDs[i]
		if (previousID != currentID):
			allInforPerSearch.append(newSearchIDInfo)
			newSearchIDInfo = []
		newSearchIDInfo.append(column[i])
		previousID = currentID
	allInforPerSearch.append(newSearchIDInfo)
	
# 	for i in range(len(allInforPerSearch)):
# 		print "SearchID: ", searchIDs[i] 
# 		for each in allInforPerSearch[i]:
# 			print each
	
	return allInforPerSearch


#
def withinIDReplaceNullMedian(column):
	data = []
	for i in range(len(column)):
		each = column[i]
		if each != 'NULL':
			data.append(float(each))
	if len(data) == 0:
# 		print "All values are NULL"
		return 
	data = np.array(data)
	median = np.median(data)
	
	for i in range(len(column)):
		if column[i] == 'NULL':
			column[i] = median
		else:
			column[i] = float(column[i])
	return column

#Access matrix and change it
def replaceNullwithMedian(matrix,nth):
	data = []
	rowSize = len(matrix)
	for i in range(rowSize):
		each = matrix[i][nth]
		if each != 'NULL':
			data.append(float(each))
	if len(data) == 0:
		print "All values are NULL"
		median = 1
	else:
		data = np.array(data)
		median = np.median(data)
	
	for i in range(rowSize):
		if matrix[i][nth] == 'NULL':
			matrix[i][nth] = median
		else:
			matrix[i][nth] = float(matrix[i][nth])
	return matrix

def normalizeColumn(matrix, nth):
	column = getColumn(matrix,nth)
	column = np.array(column)
	stdCol = np.std(column)
	if stdCol == 0:
		return matrix
	meanCol = np.std(column)
	normalizeCol = np.subtract(column,stdCol)
	normalizeCol = np.divide(normalizeCol,stdCol)
	matrix = setColumn(matrix,normalizeCol,nth)
	return matrix

def checkFrequency(column):
	unique = list(set(column))
	column = list(column)
	totalRec = len(column)
	dict = {}
	for each in unique:
		freq = column.count(each)
		freq = freq/float(totalRec)
		dict[each] = freq
	newColumn = []
	for each in column:
		newColumn.append(dict[each])
	return newColumn, dict
		
		
		

#put limi 0 to get the whole matrix
def getCSVmatrix(filename,limit):
	i = 0
	matrix = []
	a = open(filename+".txt","r")
	for row in a:
		row = row.rstrip("\n")
		row = row.rstrip(",")
		row = row.rstrip("\r")
		row = row.split(",")
		matrix.append(row)
		i += 1
		if i == limit:
			break
	a.close()
	return matrix

def writeMatrixCSV(filename,matrix):
	a = open(filename+".txt","w")
	column_size = len(matrix[0])
	for row in matrix:
		for element in range(column_size):
			a.write(str(row[element]))
			if element == (column_size -1):
				break
			a.write(",")
		a.write("\n")
	return 0
			
def getColumn(matrix,nth):
	column_size = len(matrix[0])
	if (nth >= column_size):
		print "Column index out of range"
		return 0
	column = []
	for row in matrix:
		column.append(row[nth])
	return column
	
def setColumn(matrix,column,nth):
	column_size = len(matrix[0])
	if (nth >= column_size):
		print "Column index out of range"
		return 0
	for i in range(len(matrix)):
		matrix[i][nth] = column[i]
	return matrix
					
def display_column():
	columnNames = ["0_srchId", "1_date_time", "2_searchDestination", "3_propCountryID", "4_prop_id", "5_prop_star", "6_prop_review", "7_prop_brand_bool", "8_localtionScore", "9_locationScore2", "10_historical_price", "11_position", "12 price", "13promotion" , "14likelihood on the web"]
	competitorsPrice = [str(i)+"compPValue" for i in range(15,39)]
	columnNames += competitorsPrice
	#Display column of data
	hotelFeats = open("hotel_feature.txt")
	for i in range(1):
		eachHotel = hotelFeats.readline()
		featureList = eachHotel.split(",")
		featureList.pop(len(featureList)-1)
		for j in range(len(featureList)):
			print columnNames[j], featureList[j]
		print("\n")
	return 

def convertMatrixtoFloat(matrix):
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			matrix[i][j] = float(matrix[i][j])
	return matrix

def normalizeMatrix(matrix):		
	stdMat = np.std(matrix, axis=0)
	meanMat = np.std(matrix,axis=0)
	normalizeMat = np.subtract(matrix,meanMat)
	normalizeMat = np.divide(normalizeMat,stdMat)
	return normalizeMat

def normalizeVec(column):
	column = np.array(column)
	stdCol = np.std(column)
	meanCol = np.std(column)
	normalizeCol = np.subtract(column,stdCol)
	normalizeCol = np.divide(normalizeCol,stdCol)
	return normalizeCol

def normalizeOneZeroVec(column):
	column = np.array(column)
	maxCol = np.max(column)
	minCol = np.min(column)
	rangeC = maxCol-minCol
	if rangeC == 0:
		return np.array([0.5 for i in range(len(column))])
	rangeCol = np.array([rangeC for i in range(len(column))])
	normalizeCol = np.subtract(column,minCol)
	normalizeCol = np.divide(normalizeCol,rangeCol)
	return normalizeCol


def concat_File(columnsFile1, columnsFile2, file1, file2):
	fileOb1 = open(file1+str(".txt"))
	data1 = []
	for each in fileOb1:
		eachdata1 = []
		each = each.rstrip('\n')
		feautres = each.split(',')
		for feature in features:
			eachdata1.append(feature)
		data1.append(eachdata1)
	fileOb1.close()
	fileOb2  = open(file2+str(".txt"))
	data2 = []
	
	for each in fileOb2:
		eachdata2 = []
		each = each.rstrip('\n')
		feautres = each.split(',')
		for feature in features:
			eachdata2.append(feature)
		data2.append(eachdata1)
	fileOb2.close()
	
	combinedData = []
	for i in range(len(data1)):
		eachCombined = []
		for j in range(len(columnsFile1)):
			eachCombined.append(data1[columnFile1[j]])
		for j in range(len(columnsFile2)):
			eachCombined.append(data2[columnFile2[j]])
	
	fileOutput = open("combined_"+file1+"_"+file2+".txt",w)
	for eachLine in combinedData:
		for eachParam in eachLine:
			fileOutput.write(each)
		fileOutput.write('\n')
	fileOutput.close()


			
from math import log

#Function - compute IDEAL - maximimum poosible score
# for it to be meaningful, it must be compared with the same set of items to be ranked
#Input relevance is list of relevance
#Output - the score
def getScore(relevance):
	sumGain = 0
	for i in range(len(relevance)):
		numerator = 2.0**(relevance[i]) -1.0
		denominator = log(i+2,2)
		temp = numerator/denominator
		sumGain += temp
	return sumGain

#Function - give the 2 dimensional arrays of grade is the best possible order
#Input - score (1*m) numeric value of the grade,
#        tupleFreq (n*m) n is size of data, m is the frequency of (not clicked, clicked, bought) per searchID
#Output - n*m best arrangement of the grades. eg [0,0,0,1,5] => [!clicked,!clicked,!clicked,clicked,bought]  
def getRelevanceInOrder(score, tupleFreq):
	master_relevance = []
	for freq in tupleFreq:
		relevance = []
		for i in range(len(freq)-1,-1,-1):
			relevance += [ score[i] for n in range(freq[i])]
		master_relevance.append(relevance)
	return master_relevance 

#Function - run through the file to get	frequency of the labels per searchID
#Input - file name - and if you want to save the result
#Output - tuple of the frequency
def getFreqLablePerID(filename, save_result):
	a = open(filename+".txt","r")
	firstline = a.readline().split(",")
	previous = int(firstline[0])
	print "previous: ", firstline[0]
	a = open(filename+".txt","r")
	label_per_id = []
	all_labels = []
	unique_IDs = []
	for i in a:
		print i
		eachline = i.rstrip(",\n")
		eachline = eachline.split(",")
		idSearch = eachline[0]
	   
		if idSearch == "srch_id":
			continue
		else:
			idSearch = int(idSearch)
		if previous != idSearch:
			print "New ID"
			all_labels.append(label_per_id)
			unique_IDs.append(idSearch)
			label_per_id = []
		if int(eachline[-1]):
			label = 2
		elif int(eachline[-3]):
			label = 1
		else:
			label = 0
		label_per_id.append(label)
		print label_per_id		
		previous = idSearch
	unique_IDs.append(idSearch)
	all_labels.append(label_per_id)
	print "Total unique search ids:\n ", unique_IDs
	print "Total labels for each hotel entry:\n ", all_labels
	master_label = []
	for i in range(len(unique_IDs)):
		count_label = (all_labels[i].count(0),all_labels[i].count(1),all_labels[i].count(2))
		print unique_IDs[i], count_label
		master_label.append(count_label)
	
	if save_result:
		b = open(filename+"_Labels.txt","w")
		for each in master_label:
			for label_freq in each:
				b.write(str(label_freq)+",")
			b.write("\n")
		b.close()	
	
	return master_label

def calculateIndex(score,predicted_ranking_true_label):
	gradeList= []
	for each in predicted_ranking_true_label:
		gradeList.append(score[each])
	idealGradeList = [each for each in gradeList]
	
	idealGradeList.sort()
	idealGradeList.reverse()
	idealScore = getScore(idealGradeList)
	score = getScore(gradeList)
	
	if idealScore == 0:
		return 0
	return float(score)/idealScore
	
	
			
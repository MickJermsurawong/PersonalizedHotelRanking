import household as hh
import numpy as np

feats = ['0.srch_id', '1.date_time', '2.site_id', '3.visitor_location_country_id', '4.visitor_hist_starrating', '5.visitor_hist_adr_usd', '6.prop_country_id', '7.prop_id', '8.prop_starrating', '9.prop_review_score', '10.prop_brand_bool', '11.prop_location_score1', '12.prop_location_score2', '13.prop_log_historical_price', '14.position', '15.price_usd  ', '16.promotion_flag', '17.srch_destination_id', '18.srch_length_of_stay', '19.srch_booking_window', '20.srch_adults_count', '21.srch_children_count', '22.srch_room_count', '23.srch_saturday_night_bool', '24.srch_query_affinity_score  ', '25.orig_destination_distance', '26.random_bool', '27.comp1_rate', '28.comp1_inv ', '29.comp1_rate_percent_diff', '30.comp2_rate', '31.comp2_inv ', '32.comp2_rate_percent_diff', '33.comp3_rate', '34.comp3_inv ', '35.comp3_rate_percent_diff', '36.comp4_rate', '37.comp4_inv ', '38.comp4_rate_percent_diff', '39.comp5_rate', '40.comp5_inv ', '41.comp5_rate_percent_diff', '42.comp6_rate', '43.comp6_inv ', '44.comp6_rate_percent_diff', '45.comp7_rate', '46.comp7_inv ', '47.comp7_rate_percent_diff', '48.comp8_rate', '49.comp8_inv ', '50.comp8_rate_percent_diff', '51.click_bool', '52.gross_bookings_usd ', '53.booking_bool', '54.hotelFreq', '55.countryFreq', '56.searchDesFreq', '57.weeksProp', '58.week-0', '59.week-1', '60.week-2', '61.week-3', '62.week-4', '63.week-5', '64.week-6', '65.week-7', '66.week-8', '67.week-9', '68.week-10', '69.week-11', '70.week-12', '71.week-13', '72.week-14', '73.week-15', '74.week-16', '75.week-17', '76.week-18', '77.week-19', '78.week-20', '79.week-21', '80.week-22', '81.week-23', '82.week-24', '83.week-25', '84.week-26', '85.week-27', '86.week-28', '87.week-29', '88.week-30', '89.week-31', '90.week-32', '91.week-33', '92.week-34', '93.week-35', '94.week-36', '95.week-37', '96.week-38', '97.week-39', '98.week-40', '99.week-41', '100.week-42', '101.week-43', '102.week-44', '103.week-45', '104.week-46', '105.week-47', '106.week-48', '107.week-49', '108.week-50', '109.week-51', '110.sum_rate_comp', '111.avail_comp', '112.pric_dif_comp', '113.ratioStar', '114.ratioProp', '115.ratio_loc1', '116.ratio_loc2']
totalRows = 0
firstInput = "smalltest"
step1Output = "smalltestProcessedStep1"
step2Output = "smalltestRelFreq"
step3_1Output =  "smalltestProcessedStep3"
step3_2Output = "smalltestRatios"
step4_FinalOutput = "smalltestOld&New2"

step1 = 0
step2 = 0
step3 = 0 
step4 = 0
step5 = 0
step6 = 0

if (step1 == 1):
	print "Step1 - Fill Null"
	allData = hh.getCSVmatrix(firstInput,totalRows)
	searchIDs = hh.getColumn(allData,0)
	#Date_time - Get weeks is [[0,..0,1,0],[0,..1,0,0]... ,[1,0,..]] 
	date = hh.getColumn(allData,1)
	booking = np.array(hh.getColumn(allData,19))
	date = hh.getColumn(allData,1)
	for i in range(len(date)):
		time = date[i]
		time = (time.split())[0]
		month = int(time[5:7])
		day = int(time[-11:-9])
		dictMonth = {1:31,2:59,3:90,4:120,5:151,6:181,7:212,8:243,9:273,10:304,11:334,12:365}
		num_week = (dictMonth[month] + day+ int(booking[i]) )
		if num_week>=365:
			num_week = num_week%365
		num_week = num_week//7
		if num_week > 51:
			num_week = num_week%51
		allData[i][1] = num_week

	#24 normalizing distance 
	dis = hh.replaceNullwithMedian(allData,25)
	dis = hh.getColumn(allData,25)
	dis = hh.splitColumnsForEachID(searchIDs, dis)

	for i in range(len(dis)):
		dis[i] = hh.normalizeOneZeroVec(dis[i])
	normDis = []
	for each in dis:
		normEach = [i for i in each]
		normDis += normEach
	allData = hh.setColumn(allData,normDis,25)

	#p27-50 - remove Nulls (24 features)


	toFillNull = [4,5,13,18,19,20,21,22,24]
	for i in toFillNull:
		allData = hh.replaceNullwithMedian(allData,i)

	toNormalize = [4,5,13,18,19,20,21,22,24]
	for i in toNormalize:
		allData = hh.normalizeColumn(allData,i)
	
	#Change competition values
	for k in range(len(allData)):
		eachComp = []
		each = allData[k]
		for j in range(3):
			comp = 0
			count =0
			for i in range(27,51,3):
				val = each[i+j]
				if val == 'NULL':
					allData[k][i+j] = 0
				elif val == "1":
					comp +=1
					allData[k][i+j] = 1
				elif val == "-1":
					comp -= 1
					allData[k][i+j] = -1
				elif val == "0":
					allData[k][i+j] = 0
				else:
					allData[k][i+j] = float(val)
				if j == 2:
					if val != "NULL":
						count += 1
						comp += float(val)
	
	hh.writeMatrixCSV(step1Output,allData)
	
if (step2 == 1):
	print "Step2 - Relative Freq"
	allData = hh.getCSVmatrix(step1Output,totalRows)
	allCompetition = []
	for k in range(len(allData)):
		eachComp = []
		each = allData[k]
		for j in range(3):
			comp = 0
			count =0
			for i in range(27,51,3):
				val = each[i+j]
				if val == "1":
					comp +=1
				elif val == "-1":
					comp -= 1
				elif val == "0":
					continue
				if j == 2:
					count += 1
					comp += float(val)
			if j == 2:
				if count != 0:
					comp = comp/count
			eachComp.append(comp)
		allCompetition.append(eachComp)

	#54-56 Relative Frequencies
	countryID = np.array(hh.getColumn(allData,6))
	hotelID = np.array(hh.getColumn(allData,7))
	searchDesID = np.array(hh.getColumn(allData,17))
	
	print "Country freq"
	countryFreqIDs = []
	[column,dict] = hh.checkFrequency(countryID)
	for i in range(len(allData)):
		countryFreqIDs.append(dict[allData[i][6]])
	
	print "Hotel freq"
	hotelFreqIDs = []
	[column,dict] = hh.checkFrequency(hotelID)
	for i in range(len(allData)):
		hotelFreqIDs.append(dict[allData[i][7]])
	
	print "SearchDesID freq"
	searchDesFreqIDs = []
	[column,dict] = hh.checkFrequency(searchDesID)
	for i in range(len(allData)):
		searchDesFreqIDs.append(dict[allData[i][17]])
	
	print "Normalizing"
	countryFreqIDs = hh.normalizeVec(countryFreqIDs)
	hotelFreqIDs = hh.normalizeVec(hotelFreqIDs)
	searchDesFreqIDs = hh.normalizeVec(searchDesFreqIDs)

	print "Week freq"
	weekProp = hh.getColumn(allData,1)
	weekProp = [int(each) for each in weekProp]
	#58-109 oneHotweeks
	oneHotweeks = []
	for num_week in weekProp:
		whichweek = [0 for j in range(52)]
		whichweek[num_week] = 1
		oneHotweeks.append(whichweek)

	#57 weekFreq
	searchIDs = hh.getColumn(allData,0)
	weeks_perID = hh.splitColumnsForEachID(searchIDs, weekProp)
	dictWeeks = [each[0] for each in weeks_perID]
	dictWeeks.sort()
	[column,dict] = hh.checkFrequency(dictWeeks)
	for i in range(len(weekProp)):
		weekProp[i] = dict[weekProp[i]]
	weekProp = hh.normalizeVec(weekProp)
	
	relFreq = []
	for i in range(len(allData)):
		relFreq.append([hotelFreqIDs[i]]+[countryFreqIDs[i]]+ [searchDesFreqIDs[i]]+ [weekProp[i]]+ oneHotweeks[i]+ allCompetition[i])
	
	hh.writeMatrixCSV(step2Output,relFreq)
	
if (step3 ==1):
	print "Step3 - Ratio"
	allData = hh.getCSVmatrix(step1Output,totalRows)

	#Fill NULL data
	toFillNull = [8,9,11,12]
	for i in toFillNull:
		allData = hh.replaceNullwithMedian(allData,i)

	#get price over quality
	allData = hh.replaceNullwithMedian(allData,15)
	price = np.array(hh.getColumn(allData,15))
	median = np.median(price)
	for i in range(len(price)):
		if price[i] == 0:
			price[i] = median
	star_rate = np.array(hh.getColumn(allData,8))
	prop_rev = np.array(hh.getColumn(allData,9))
	prop_loc1 = np.array(hh.getColumn(allData,11))
	prop_loc2 = np.array(hh.getColumn(allData,12))
	ratioStar = hh.normalizeVec(np.divide(star_rate,price))
	ratioprop_rev = hh.normalizeVec(np.divide(star_rate,price))
	ratio_loc1 = hh.normalizeVec(np.divide(prop_loc1,price))
	ratio_loc2 = hh.normalizeVec(np.divide(prop_loc2,price))

	toNormalize = [8,9,11,12]
	for i in toNormalize:
		allData = hh.normalizeColumn(allData,i)
	
	grossBooking = [0 for each in range(len(allData))]
	allData = hh.setColumn(allData,grossBooking,52)
	
	ratios = []
	for i in range(len(allData)):
		ratios.append([ratioStar[i]] + [ratioprop_rev[i]]+ [ratio_loc1[i]]+ [ratio_loc2[i]])

	hh.writeMatrixCSV(step3_1Output,allData)
	hh.writeMatrixCSV(step3_2Output,ratios)

if (step4 == 1):
	print "Step4 - Collating"
	allData = hh.getCSVmatrix(step3_1Output,totalRows)
	allDataFreq = hh.getCSVmatrix(step2Output,totalRows)
	allDataRatio = hh.getCSVmatrix(step3_2Output,totalRows)

	for i in range(len(allData)):
		allData[i] += allDataFreq[i]+allDataRatio[i]

	hh.writeMatrixCSV(step4_FinalOutput,allData)


if (step5 == 1):
	print "Step5 - Normalizing Price"
	allData = hh.getCSVmatrix(step4_FinalOutput,totalRows)
	toFillNull = [15]
	for i in toFillNull:
		allData = hh.replaceNullwithMedian(allData,i)

	toNormalize = [15]
	for i in toNormalize:
		allData = hh.normalizeColumn(allData,i)
	hh.writeMatrixCSV(step4_FinalOutput,allData)

if (step6 ==1 ):
	print "Step6"
	ranchose = 900
	allData =  hh.getCSVmatrix(step4_FinalOutput,5000)
  	allDataOri = hh.getCSVmatrix("smalltrainOld&New2",5000)
 	allDataUnp = hh.getCSVmatrix("smalltrain",5000)
	for i in range(len(allData[49])):
			if i <54:
				print feats[i], allDataUnp[ranchose][i], allDataOri[ranchose][i],allData[ranchose][i]
			else:
				print feats[i], allDataOri[ranchose][i], allData[ranchose][i]

# 	for i in range(len(allDataStep1)):
# 			if float(allDataStep1[i][50]) != 0:
# 				print i,allDataStep1[i][50]
				










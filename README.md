Kaggle competition to personalize hotel search
Learn from the historical data what types of hotels are bought/clicked
Rank those hotels higher.
Results evaluated by the common search ranking evaluation - normalized discounted cumulative gain
The dataset can be obtained at  http://www.kaggle.com/c/expedia-personalized-sort/data

The "code" folder contains the following:

1. household - module that manages matrices of datapoints in processing
2. ndcg - calculates normalized discounted gain for internal validation
3. processAllTrain - given data from Kaggle - this normalizes the data and add features
4. softKmeanHotel - implement Kmean on hotel
5. svm implement svm on hotel 
6. svmRank writes data in the form that works with SVM rank http://www.cs.cornell.edu/people/tj/svm_light/svm_rank.html
7. svmRankEval evaluates using ndcg from the predicted result
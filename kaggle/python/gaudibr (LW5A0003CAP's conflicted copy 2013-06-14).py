import csv as csv
import numpy as np



csv_file_object = csv.reader(open('../csv/train.csv', 'rb')) #Load in the csv file
header = csv_file_object.next() #Skip the fist line as it is a header
train_data=[] #Creat a variable called 'data'
for row in csv_file_object: #Skip through each row in the csv file
    train_data.append(row) #adding each row to the data variable
train_data = np.array(train_data) #Then convert from a list to an array

#in order to analyse the price collumn I need to bin up that data
#here are my binning parameters the problem we face is some of the fares are very large
#So we can either have a lot of bins with nothing in them or we can just absorb some
#information and just say anythng over 30 is just in the last bin so we add a ceiling
fare_ceiling = 40

train_data[train_data[0::,8].astype(np.float) >= fare_ceiling, 8] = fare_ceiling-1.0
fare_bracket_size = 10
number_of_price_brackets = fare_ceiling / fare_bracket_size
number_of_classes = 3 #There were 1st, 2nd and 3rd classes on board
number_of_age_groups = 5

#All the ages with no data make the median of the data
train_data[train_data[0::,4] == '',4] = np.median(train_data[train_data[0::,4] != '',4].astype(np.float))

train_data[train_data[0::,4].astype(np.float) <= 1, 4] = 0  												#babies
train_data[((train_data[0::,4].astype(np.float) > 1) & (train_data[0::,4].astype(np.float) <= 10)),4] = 1 	#infants
train_data[((train_data[0::,4].astype(np.float) > 10) & (train_data[0::,4].astype(np.float) <= 18)),4] = 2 	#minors
train_data[((train_data[0::,4].astype(np.float) > 18) & (train_data[0::,4].astype(np.float) <= 50)),4] = 3 	#adults
train_data[train_data[0::,4].astype(np.float) > 50,4] = 4  													#elderly
#Analyzing age group


#This reference table will show we the proportion of survivors as a function of
# Gender, class and ticket fare.
survival_table = np.zeros([3,number_of_classes,number_of_price_brackets,number_of_age_groups],float)

print survival_table

# I can now find the stats of all the women and men on board
for i in xrange(number_of_classes):
    for j in xrange(number_of_price_brackets):
    	for k in xrange(number_of_age_groups):

        women_only_stats = train_data[ (train_data[0::,3] == "female") \
                                 & (train_data[0::,1].astype(np.float) == i+1) \
                                 & (train_data[0:,8].astype(np.float) >= j*fare_bracket_size) \
                                 & (train_data[0:,8].astype(np.float) < (j+1)*fare_bracket_size) \
                                 & (train_data[0:,4].astype(np.float) >= k) \
                                 & (train_data[0:,4].astype(np.float) < (k+1)), 0]

        men_only_stats = train_data[ (train_data[0::,3] != "female") \
                                 & (train_data[0::,1].astype(np.float) == i+1) \
                                 & (train_data[0:,8].astype(np.float) >= j*fare_bracket_size) \
                                 & (train_data[0:,8].astype(np.float) < (j+1)*fare_bracket_size)\
                                 & (train_data[0:,4].astype(np.float) >= k) \
                                 & (train_data[0:,4].astype(np.float) < (k+1)), 0]

                                 #if i == 0 and j == 3:

        survival_table[0,i,j,k] = np.mean(women_only_stats.astype(np.float)) #Women stats
        survival_table[1,i,j,k] = np.mean(men_only_stats.astype(np.float)) #Men stats

#Since in python if it tries to find the mean of an array with nothing in it
#such that the denominator is 0, then it returns nan, we can convert these to 0
#by just saying where does the array not equal the array, and set these to 0.
survival_table[ survival_table != survival_table ] = 0.

open_file_object = csv.writer(open("../csv/gaudibr_test.csv", "wb"))


#First thing to do is bin up the price file
open_file_object.writerow(header)
for row in train_data:
    open_file_object.writerow(row)
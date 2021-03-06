import sys
import pandas as pd
import matplotlib.pyplot as plt
HIGH_PRICE = 0
MONTH_COLUMN = 7
DAY_COLUMN = 8
step = 22
#read the data_set based off argument value
data_list = ['ap_data.csv', 'ceb_data.csv', 'chib_data.csv', 'gtcap_data.csv', 'mbt_data.csv', 'meg_data.csv', 'rlc_data.csv']
def center_diff(y_minus, y_plus, step):
	return ( (y_plus - y_minus) / (2*step) )

fig = plt.figure()
fig.suptitle('Momentum of Price variable against time', fontsize=20)
for i in range(len(data_list)):
	df = pd.read_csv('../csv_files/'+data_list[i])
	price = df.iloc[:,HIGH_PRICE].copy().tolist() 
	months = df.iloc[:,MONTH_COLUMN].copy().tolist()
	days = df.iloc[:,DAY_COLUMN].copy().tolist()

	previous_month = months[0]
	x_values = []
	additor = 30
	the_additor = 0
	for x in range(0,len(months)):
		if(months[x] != previous_month):
			previous_month = months[x]
			the_additor = the_additor + additor + (months[x-1] % 2)
			if(months[x-1] == 2):
				the_additor = the_additor - 2		
		x_values.append(the_additor + days[x])


	true_x_values = []
	true_y_values = []
	checker1 = False
	checker2 = False
	comparator = x_values[step]
	x_at_negative = 0
	y_at_negative = 0
	x_at_positive = 0
	y_at_positive = 0
	for y in range(step,len(x_values)-step):
		checker1 = False
		checker2 = False
		comparator = x_values[y]	
		for z in range(1,step+1):
			# checks if data point at delta -step exists
			if(x_values[y-z] == comparator-step) and (not checker1):
				checker1 = True
				x_at_negative = x_values[y-z] 
				y_at_negative = months[y-z]	
			# checks if data point at delta +step exists
			if(x_values[y+z] == comparator+step) and (not checker2):
				checker2 = True
				x_at_positive = x_values[y+z] 
				y_at_positive = months[y+z]
		# now checks if it found a datapoint for both
		if (checker1) and (checker2):
			# apply centered difference
			true_y_values.append(center_diff(y_at_negative , y_at_positive, step))
			true_x_values.append(x_values[y])
		
	plt.plot(true_x_values,true_y_values)
	plt.xlabel('Days', fontsize=18)
	plt.ylabel('Price', fontsize=16)
	plt.legend(loc = 'upper right')

fig.savefig('all' + '_momentum_step_22')
plt.show()

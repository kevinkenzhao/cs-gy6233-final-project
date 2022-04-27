import os
#import glob
#import pandas as pd
import natsort
path = "C:/Users/Kevin/Desktop/CSV"
a = os.listdir(path)
arr = natsort.natsorted(a,reverse=False)
extension = 'csv'
count = 0;
for direct in arr:
	count+=1
	direct = str(direct)
	print(direct)
	if direct.endswith('.py'):
		continue
	elif direct.endswith('.csv'):
		continue
	else:
		base = os.path.splitext(direct)[0]
		os.rename(direct, base + ".csv")
		new_name = base + ".csv"
		print(new_name)
		ext = os.path.splitext(new_name)[1]
		count_str = str(count)
		os.rename(new_name, count_str + ext)
		csv_name = count_str + ext
		print(csv_name)
		with open(csv_name) as f:
			 with open("out.csv", "a") as f1:
			 	for line in f:
			 		f1.write(line)



#extension = 'csv'
#all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames], sort=True)
#combined_csv.to_csv( "combined.csv", index=False, encoding='utf-8-sig')

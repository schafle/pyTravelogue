csv_filepathname="../data/trains_route.csv"

import os, sys
SETTINGS_DIR = os.path.dirname(__file__)

PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
sys.path.append(PROJECT_PATH)
PROJECT_PATH +="\\pyTravelogue"
sys.path.append(PROJECT_PATH)
print(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


from journeys.models import Train

import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',')

for row in dataReader:
	if row[0] != 'train_code': # Ignore the header row, import everything else
		print(row)
		train = Train()
		train.train_code = row[0]
		train.train_name = train.train_code+row[1]
		train.train_route = row[2]
		train.save()
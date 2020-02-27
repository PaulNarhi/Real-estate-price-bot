import json
import csv

def read_json(file_name):
	return json.load(open(file_name))


def write_json(dict_, file_name):
	json.dump(dict_, open(file_name, 'w'))

def read_csv(file_name):
	data = list(csv.reader(open(file_name)))
	return data

def write_csv(arr, file_name):
	with open(file_name, "w") as f:
		writer = csv.writer(f)
		writer.writerows(arr)
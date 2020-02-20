import json

def read(file_name):
	return json.load(open(file_name))


def write(dict_, file_name):
	json.dump(dict_, open(file_name, 'w'))
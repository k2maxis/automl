import json, csv
from collections import defaultdict
from numpy import *

ms = json.loads(open('misspelling_to_correct_manufacturer.json', 'r').read())

MANUFACTURER = 2
MODEL = 3

outdict = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
mlistings = csv.reader(open('mlistings.csv'))

makemodelnada = csv.reader(open('MakeModelNADA.csv', 'r'))
carlotmodelnames = open('CarLotModelNames.csv', 'r').read()
carlotmodelnames = carlotmodelnames.split('\n')
carlotmodelnames.remove('')
for index, content in enumerate(carlotmodelnames):
	carlotmodelnames[index] = content.split(',')
	for index2, content2 in enumerate(carlotmodelnames[index]):
		carlotmodelnames[index][index2] = content2.strip().upper()
newarray = array(carlotmodelnames)


# Set up initial dict on makemodelnada
for row in makemodelnada:
	outdict[ms[row[0].upper().strip()]].update({row[1].upper().strip(): {row[1].upper().strip(): 0}})

for col in range(len(newarray[1, :]) - 1): #-1 to ignore the UNKNOWN at the end
	thislist = list(newarray[:, col])
	while 'null' in thislist:
		thislist.remove('null')
	manufacturer = thislist.pop(0)
	if manufacturer not in ms:
		print(manufacturer + '\n')
	else:
		for model in thislist:
			if model not in outdict[ms[manufacturer]]:
				outdict[ms[manufacturer]].update({model: {model: 0}})


# now, go through stuff in mlistings
for row in mlistings:
	if row[MANUFACTURER].upper().strip() in ms:
		tmp_ms = ms[row[MANUFACTURER].upper().strip()]
		if row[MODEL].upper().strip() in outdict[tmp_ms]:
			tmp_model = row[MODEL].upper().strip()

			outdict[tmp_ms][tmp_model][tmp_model] += 1

with open('models_with_hits.json', 'w') as outfile:
	outfile.write(json.dumps(outdict, sort_keys=True, indent=4))


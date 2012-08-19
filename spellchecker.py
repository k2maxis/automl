# coding: utf-8

import string, pickle, sys, pprint

alphabet = string.uppercase + ' '

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))

def edits3(word):
	return set(e3 for e1 in edits1(word) for e2 in edits1(e1) for e3 in edits1(e2))

###############
## Manufacturer Code
###############


###
# Original list based on Wikipedia
###
#LIST_OF_MANUFACTURERS = "Holden, Tickford, FPV, Gillet, Agrale, Lobini, TAC Motors, Troller, Bricklin, Studebaker, Avia, Kaipan, Praga, Skoda Auto, Tatra, ACMA, Aixam, Bugatti, Citroen, Cottin & Desgouttes, Facel Vega, Matra, Peugeot, Renault, Pescarolo Sport, Alpine, Audi, AWZ, Barkas, Bitter, BMW, Borgward, Büssing, DKW, Glas, Goliath, Hansa, Heinkel, Horch, Lloyd, Maybach, MAN, Mercedes-Benz, Multicar, NAG, Neoplan, Opel, Porsche, Robur, Simson, Trabant, Volkswagen, Wanderer, Wartburg, Ashok Leyland, Chinkara Motors, DC Design, Force Motors, Hindustan Motors, ICML, Mahindra & Mahindra Limited, Maruti Suzuki, Premier Automobiles Limited, Tata Motors, Eicher, Bahman Group, IKCO (Iran Khodro), Kish Khodro, MVM, Pars Khodro, SAIPA, Alfa Romeo, DR Motor, Ferrari, Fiat, Intermeccanica, Lamborghini, Lancia, Maserati, Pagani, Siata, Vignale, De Tomaso, Autobianchi, Cizeta, Acura, Daihatsu, Datsun, Hino, Honda, Infiniti, Isuzu, Lexus, Mazda, Mitsubishi Motors, Nissan, Subaru, Suzuki, Toyota, Yamaha, ASL, Bufori, Naza, Perodua, Proton, Mastretta, DINA, Tranvias-Cimex, Italika, Ramirez Automotive Industrial Group, VAM S.A., Venturi, DAF, Spyker, Atlas Honda, Dewan Farooque Motors, Ghandhara Industries, Ghandhara Nissan, Indus Motors Company, Nexus Automotive, Pak Suzuki Motors, Sigma Motors, Automobile Dacia, Avtoframos, GAZ, Kamaz, Lada, Marussia Motors, Volga, Zastava Automobiles, GM Korea, Hyundai Motor Company, Kia Motors, Renault Samsung Motors, SsangYong Motor Company, Proto Motors, SEAT, Koenigsegg, Jösse Car, Saab, Volvo, Enzmann, Stealth, Sbarro (automobile), AC, Allard, Alvis, Armstrong Siddeley, Ascari, Aston Martin, Austin-Healey, Bentley, Bristol, British Leyland, Caterham, Daimler, Elva, Ginetta, Gordon Keeble, Hillman, Humber, Jaguar, Jensen, Jowett, Lanchester, Land Rover, Lister, Lotus, Marcos, MG, MG Cars, Mini Cooper, Morgan, Morris, Noble, Riley, Rolls Royce, Rover, Singer, Sunbeam, Triumph, Trojan, TVR, Vauxhall, Wolseley, Buick, Cadillac, Chevrolet, Coda, Chrysler, DeLorean Motor Company, Dodge, Fisker, Ford, Global Electric Motorcars, GMC, International Harvester, Jeep, Lincoln, Navistar International, Scion, Tesla, Jay Leno, Callaway, Chaparral, Saleen, Panoz, Mosler, Leading Edge, American Motors, Apollo, Auburn, Cord, Davis Motor Car, Duesenberg, Eagle, Edsel, Geo, Graham-Paige, Hummer, Hupmobile, Kaiser Motors, Kissel Motor Car Company, Laforza, Marmon, Mercury, Nash Motors, Oldsmobile, Packard, Pierce-Arrow, Plymouth, Pontiac, Regal, REO, Saturn, Sterling, Studebaker, Tucker, Thomas B. Jeffery Company, Willys"
#LIST_OF_MANUFACTURERS = LIST_OF_MANUFACTURERS.upper().split(', ')
#LIST_OF_MANUFACTURERS.append('Continent'.upper())

PICKLE_FILE_LOCATION = r'C:\Users\JJ\Documents\Coding\Scott\Corrector\Manufacturer_dict.pickle'
with open(PICKLE_FILE_LOCATION, 'r') as infile:
	LIST_OF_MANUFACTURERS = pickle.load(infile)

def add_manufacturer(manufacturer, abbreviation = None):
	with open(PICKLE_FILE_LOCATION, 'w') as outfile:
		
		LIST_OF_MANUFACTURERS[manufacturer.upper()] = manufacturer.upper()
		if abbreviation:
			LIST_OF_MANUFACTURERS[abbreviation.upper()] = manufacturer.upper()

		pickle.dump(LIST_OF_MANUFACTURERS, outfile)

def print_list():
	pprint.pprint(LIST_OF_MANUFACTURERS)

######################################

def correct(word):
	word=word.upper()

	# Is the provided term already in our list?
	if word in LIST_OF_MANUFACTURERS:
		return LIST_OF_MANUFACTURERS[word]

	# Is the provided term the beginning of a manufacturer name?
	if len(word) >= 4:
		for key in set(LIST_OF_MANUFACTURERS.keys()):
			if key.startswith(word):
				return LIST_OF_MANUFACTURERS[key]

	# Is the provided term some subset of a manufacturer name?
	if len(word) >= 5:
		for key in set(LIST_OF_MANUFACTURERS.keys()):
			if word in key:
				return LIST_OF_MANUFACTURERS[key]

	# Do the standard mispelling correction tests
	for x in set(word) | edits1(word) | edits2(word):
		if x in LIST_OF_MANUFACTURERS:
			return LIST_OF_MANUFACTURERS[x]



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('word', nargs='?', action='store', help="Word to correct")
    parser.add_argument('-p', '--print_all', action='store_true', default=False,
    					dest='print_all', help='Print full list of manufacturers.')
    group = parser.add_argument_group('Add a manufacturer')
    group.add_argument('-m', action='store', dest='manufacturer', 
    					help='Name of manufacturer to add to list.')
    group.add_argument('-a', action='store', dest='abbreviation', nargs='?',
    				help='Abbreviation to add to list for manufacturer.  Optional.')

    all_input = parser.parse_args()

    if all_input.word:
    	print correct(all_input.word)
    if all_input.print_all:
    	print_list()

    if all_input.manufacturer:
    	if all_input.abbreviation:
    		add_manufacturer(all_input.manufacturer, all_input.abbreviation)
    	else:
    		add_manufacturer(all_input.manufacturer)
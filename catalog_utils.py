from collections import OrderedDict
from copy import deepcopy
from csv import reader

def gen_catalog():
	#build catalog dictionary
	catalog = {"entries":[], "versions":{}}
	entries = catalog["entries"]
	versions = catalog["versions"]

	#ATNF Pulsar Database
	file = open("sources/psrcat.db", "r")
	line = file.readline()
	versions["ATNF"] = line.split()[1]
	curr = None
	while line:
	    if line[0] == "#":
	        line = file.readline()
	        continue
	    if line[0] == "@":
	        if "RAJ" in curr.keys():  #temp fix, will want to convert ecliptic coords to raj and decj
	        	new_curr = {"Name":curr["PSRJ"][0], "RA":curr["RAJ"][0], "DEC":curr["DECJ"][0], "visible": True, "sources": [{"Name":"ATNF", "data":curr}]}
	        	entries.append(new_curr)
	        curr = None
	        line = file.readline()
	        continue
	    if curr == None:
	        curr = OrderedDict()
	    row = line.split()
	    curr[row[0]] = row[1:len(row)]
	    line = file.readline()
	file.close()


	#RRATalog
	file = open("sources/rratalog.txt", "r")
	line = file.readline()
	line = file.readline()
	versions["RRATalog"] = "June 25, 2017"
	while line:
		line = line.split()
		curr = OrderedDict()
		curr["Name"] = line[0].replace("*", "")
		curr["P"] = line[1]
		curr["Pdot"] = line[2]
		curr["DM"] = line[3]
		curr["RA"] = line[4]
		curr["DEC"] = line[5]
		curr["l"] = line[6]
		curr["b"] = line[7]
		curr["Rate"] = line[8]
		curr["logB"] = line[9]
		curr["logts"] = line[10]
		curr["Dhat"] = line[11]
		curr["FluxD"] = line[12]
		curr["Pulse Width"] = line[13]
		curr["Survey"] = line[14]
		if curr["Name"] in [x["Name"] for x in catalog["entries"]]:
			entry = [x for x in catalog["entries"] if x["Name"] == curr["Name"]][0]
			entry["sources"].append({"Name": "RRATalog", "data":curr})
		elif curr["Name"][0:-2] in [x["Name"] for x in catalog["entries"]]:
			entry = [x for x in catalog["entries"] if x["Name"] == curr["Name"][0:-2]][0]
			entry["sources"].append({"Name": "RRATalog", "data":curr})
		else:
			catalog["entries"].append({"Name":curr["Name"], "RA":curr["RA"], "DEC":curr["DEC"], "visible":True, "sources":[{"Name":"RRATalog", "data":curr}]})
		line = file.readline()
	file.close()

	#Parallaxes
	file = open("sources/Parallaxes.txt", "r")
	line = file.readline()
	line = file.readline()
	line = file.readline()
	versions["Parallaxes"] = line.split()[-1]
	curr = None
	while line:
		if line[0] == "#":
			line = file.readline()
			continue
		elif line[0] == "!":
			if curr == None:
				curr = OrderedDict()
				line = file.readline()
			else:
				if curr["JName"] in [x["Name"] for x in catalog["entries"]]:
					entry = [x for x in catalog["entries"] if x["Name"] == curr["JName"]][0]
					entry["sources"].append({"Name":"Parallaxes", "data":deepcopy(curr)})
				else:
					catalog["entries"].append({"Name":curr["JName"], "RA":"--", "DEC":"--", "visible":True, "sources":[{"Name":"Parallaxes", "data":deepcopy(curr)}]})
				line = file.readline()

		else:
			if line[0:5] == "JName":
				line = line.split(" = ")
				curr["JName"] = line[1].strip()
				line = file.readline()
				line = line.split(" = ")
				if len(line) == 1:
					curr["BName"] = "--"
				else:
					curr["BName"] = line[1].strip()
				curr["PIs"] = OrderedDict()
				line = file.readline()
			else:
				line = line.split(" = ")
				currPI = line[1].strip()
				curr["PIs"][currPI] = OrderedDict()
				line = file.readline()
				while line[0] != "#" and line[0:2] != "PI":
					line = line.split(" = ")
					curr["PIs"][currPI][line[0]] = line[1].strip()
					line = file.readline()
	file.close()


	#GCpsr
	file = open("sources/GCpsr.txt", "r")
	line = file.readline()
	currGC = None
	versions["GCpsr"] = "June 25, 2017"
	while line:
		if line[0] == "#" or line == "\n":
			line = file.readline()
			continue
		elif line[0] == "J" or line[0] == "B":
			line = line.split()
			curr = OrderedDict()
			curr["Name"] = line[0]
			curr["Offset"] = line[1]
			curr["Period"] = line[2]
			curr["dP/dt"] = line[3]
			curr["DM"] = line[4]
			curr["Pb"] = line[5]
			curr["x"] = line[6]
			curr["e"] = line[7]
			curr["m2"] = line[8]
			curr["GC"] = currGC
			if curr["Name"][0] == "J":
				if curr["Name"] in [x["Name"] for x in catalog["entries"]]:
					entry = [x for x in catalog["entries"] if x["Name"] == curr["Name"]][0]
					entry["sources"].append({"Name":"GCpsr", "data":curr})
				else:
					catalog["entries"].append({"Name":curr["Name"], "RA":"--", "DEC":"--", "visible":True, "sources":[{"Name":"GCpsr", "data":curr}]})
			elif curr["Name"][0] == "B":
				found = False
				for entry in catalog["entries"]:
					for source in entry["sources"]:
						if source["Name"] == "ATNF":
							if "PSRB" in source["data"]:
								if source["data"]["PSRB"][0] == curr["Name"]:
									entry["sources"].append({"Name":"GCpsr", "data":curr})
									found = True
									break
					if found:
						break
				if not found:
					catalog["entries"].append({"Name":curr["Name"], "RA":"--", "DEC":"--", "visible":True, "sources":[{"Name":"GCpsr", "data":curr}]})
			else:
				catalog["entries"].append({"Name":curr["Name"], "RA":"--", "DEC":"--", "visible":True, "sources":[{"Name":"GCpsr", "data":curr}]})


			line = file.readline()
		else:
			currGC = line
			line = file.readline()

	file.close()

	#frbcat
	file = open("sources/frbcat_2017-07-06.csv")
	lines = list(reader(file))
	titles = lines[0]
	versions["frbcat"] = "1.0"
	for line in lines[1:]:
		curr = OrderedDict()
		for i in range(len(line)):
			curr[titles[i]] = line[i]
		if curr["Name"] in [x["Name"] for x in catalog["entries"]]:
			entry = [x for x in catalog["entries"] if x["Name"] == curr["Name"]][0]
			entry["sources"].append({"Name":"frbcat", "data":curr})
		else:
			catalog["entries"].append({"Name":curr["Name"], "RA":curr["RAJ"], "DEC":curr["DECJ"], "visible":True, "sources":[{"Name":"frbcat", "data":curr}]})
	file.close()

	catalog["entries"].sort(key=lambda x: x["Name"])
	return catalog
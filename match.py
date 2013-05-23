
import codecs
import json

import csv


f = codecs.open("data/finance.csv", 'rU')
csvreader = csv.reader(f, delimiter=',', quotechar='"')

finance={}
performance={}

oecd_codes={}


for i, row in enumerate(csvreader):
	if i==0:
		continue
	if i>0:
		region=row[0].strip()
		fund=row[1].strip()
		country_id=row[2].strip()
		country=row[3].strip()
		project_id=row[4].strip()
		project=row[5].strip()
		activity_id=row[6].strip()
		activity=row[7].strip()
		dac_code=row[8].strip()
		dac_name=row[9].strip()
		fy=row[10].strip()
		fq=row[11].strip()
		disbursement=row[12].strip()
		obligation=row[13].strip()

		if fund not in finance.keys():
			finance[fund]={}

		if country not in finance[fund].keys():
			finance[fund][country]={}

		if project not in finance[fund][country].keys():
			finance[fund][country][project]=[]

		if activity not in finance[fund][country][project]:
			finance[fund][country][project].append(activity)

		if dac_code not in oecd_codes.keys():
			oecd_codes[dac_code]={"dac_name":dac_name}

f.close()

print json.dumps(finance, indent=4)

print json.dumps(oecd_codes, indent=4)

import sys
sys.exit(0)

#activities and kpis are KPIs related files to match

f = codecs.open("data/activities.csv", 'r', encoding='latin1')



for i, line in enumerate(f):
	line=line.rstrip('\n').split(",")
	if i==0:
		#print line
		#[u'country', u'project', u'activity', u'outcome\r']
		continue
	if i>0:
		country=line[0].strip()
		project=line[1].strip()
		activity=line[2].strip()

		if country not in performance.keys():
			performance[country]={}
			if project not in performance[country].keys():
				performance[country][project]=[]
				if activity not in performance[country][project]:
					performance[country][project].append(activity)
			else:
				if activity not in performance[country][project]:
					performance[country][project].append(activity)

		else:
			if project not in performance[country].keys():
				performance[country][project]=[]
				if activity not in performance[country][project]:
					performance[country][project].append(activity)	
			else:
				if activity not in performance[country][project]:
					performance[country][project].append(activity)
				else:
					print "duplicate activity ",	 country, " ",activity	

f.close()



#activities and kpis are KPIs related files to match

f = codecs.open("data/indicators.csv", 'r', encoding='latin1')

itts={}

for i, line in enumerate(f):
	line=line.rstrip('\n').split(",")
	if i==0:
		#print line
		#[u'country', u'project', u'activity', u'outcome\r']
		continue
	if i>0:
		pass

f.close()
#print finance
#print performance

print "----- finance"
for country in finance:
	if country in performance.keys():
		#skip all finance projects which are not part of performance/KPIs
		print u"",country
		for project in finance[country]:
			print u"	",project
			for activity in finance[country][project]:
				#print u"		",activity
				print country,", ", project,", ", activity
				pass

print "----- performance"
for country in performance:
	#print u"",country
	for project in performance[country]:
		#print u"	",project
		for activity in performance[country][project]:
			#print u"		",activity
				#print country,", ", project,", ", activity
				pass


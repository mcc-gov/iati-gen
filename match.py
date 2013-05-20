
import codecs

f = codecs.open("data/finance.csv", 'r', encoding='latin1')

finance={}

for i, line in enumerate(f):
	line=line.rstrip('\n').split(",")
	if i==0:
		continue
	if i>0:
		region=line[0].strip()
		fund=line[1].strip()
		country_id=line[2].strip()
		country=line[3].strip()
		project_id=line[4].strip()
		project=line[5].strip()
		activity_id=line[6].strip()
		activity=line[7].strip()
		dac_code=line[8].strip()
		dac_name=line[9].strip()
		fy=line[10].strip()
		fq=line[11].strip()
		disbursement=line[12].strip()
		obligation=line[13].strip()

		if fund=='Compact':
			#print line
			if country not in finance.keys():
				finance[country]={}
				finance[country][project]=[]
				finance[country][project].append(activity)

			else:
				if project not in finance[country].keys():
					finance[country][project]=[]

				if activity not in finance[country][project]:
					finance[country][project].append(activity)			

f.close()


#activities and kpis are KPIs related files to match

f = codecs.open("data/activities.csv", 'r', encoding='latin1')

performance={}

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
		#print u"",country
		for project in finance[country]:
			#print u"	",project
			for activity in finance[country][project]:
				#print u"		",activity
				#print country,", ", project,", ", activity
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


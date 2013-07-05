import codecs
import json

import csv

f = codecs.open("source/countrycodes.csv", 'rU')
csvreader = csv.reader(f, delimiter=',', quotechar='"')

codes={}
for i, row in enumerate(csvreader):
	if i==0:
		pass
	if i>0:
		code3=row[1].strip()
		code2=row[0].strip()
		codes[code3]=code2

f.close()

f = codecs.open("data/finance.csv", 'rU')
csvreader = csv.reader(f, delimiter=',', quotechar='"')

projects={}

for i, row in enumerate(csvreader):
	if i==0:
		pass
	if i>0:
		region=row[0].strip()
		fund=row[1].strip().upper()
		country_id=row[2].strip()
		country=row[3].strip().upper()
		project_id=row[4].strip()
		project=row[5].strip().upper()
		activity_id=row[6].strip()
		activity=row[7].strip().upper()
		dac_code=row[8].strip()
		dac_name=row[9].strip()
		fy=row[10].strip()
		fq=row[11].strip()
		disbursement=row[12].strip()
		obligation=row[13].strip()

		#projects[fund+"-"+country_id+"-"+project_id]={"fund":fund, "country_id":country_id, "project_id":project_id}
		projects[fund+"-"+country_id]={"fund":fund, "country_id":country_id}

print "fund,country_id,code2,type,start,end"
for project in projects:
	#print projects[project]["fund"]+","+projects[project]["country_id"]+","+projects[project]["project_id"]
	code=""
	projecttype=""
	if projects[project]["country_id"] in codes.keys():
		code=codes[projects[project]["country_id"]]

	if projects[project]["fund"] in set(["ADMIN", "I FORGOT WHICH OTHER FUND IS ADMIN. WAS IT 609G?"]):
		projecttype="ADMIN"

	print projects[project]["fund"]+","+projects[project]["country_id"]+","+code+","+projecttype+",,"
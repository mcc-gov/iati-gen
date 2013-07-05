# -*- coding: utf-8 -*-
import csv
import codecs
import json

from string import Template

from datetime import datetime
from datetime import date
timestamp=datetime.now().replace(microsecond=0).isoformat()

def load():

	countries={}

	#load list of country names and their codes
	f=open("source/countrycodes.csv","rU")

	csvreader = csv.reader(f, delimiter=',', quotechar='"')
	for i, row in enumerate(csvreader):
		code2, code3, countryname=row[0], row[1], row[2]
		if i!=0:
			countries[countryname.split(",")[0]]={"code2":code2, "code3":code3, "countryname":countryname}

	f.close()

	#load list of lat/lon for countries
	f=open("source/country_latlon.csv","rU")

	csvreader = csv.reader(f, delimiter=',', quotechar='"')
	for i, row in enumerate(csvreader):
		code2, lat, lon=row[0], row[1], row[2]
		if i!=0:
			for country in countries:
				if countries[country]["code2"]==code2:
					countries[country]["lat"]=lat
					countries[country]["lon"]=lon

	f.close()

	#load funds mappings (including admin fund or not, and start/end dates for activities related to project)
	f = codecs.open("source/funds.csv", 'rU')
	csvreader = csv.reader(f, delimiter=',', quotechar='"')

	funds={}
	for i, row in enumerate(csvreader):
		if i==0:
			pass
		if i>0:
			#fund,country_id,code2,type,start,end
			fund=row[0].strip()
			country_id=row[1].strip()
			code2=row[2].strip()
			projecttype=row[3].strip()
			start=row[4].strip()
			end=row[5].strip()
			funds[fund+"-"+country_id]={"fund":fund, "country_id":country_id,"code2":code2, "type":projecttype, "start":start, "end":end}

	f.close()


	#Region,Fund,CountryID,Country,ProjectID,Project,ActivityID,Activity,DAC CODE,DACName,FY,FQ,Disbursement,Obligation
	# header for finance.csv

	#generate hierachy of projects

	f = codecs.open("data/finance.csv", 'rU')
	csvreader = csv.reader(f, delimiter=',', quotechar='"')

	fin={}

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

			if fund not in fin.keys():
					fin[fund]={}

			if country_id not in fin[fund].keys():
				fin[fund][country_id]={}
				fin[fund][country_id]["country"]=country
				fin[fund][country_id]["projects"]={}

			if project_id not in fin[fund][country_id]["projects"].keys():
				fin[fund][country_id]["projects"][project_id]={}
				fin[fund][country_id]["projects"][project_id]["project"]=project
				fin[fund][country_id]["projects"][project_id]["activities"]={}

			if activity_id not in fin[fund][country_id]["projects"][project_id]["activities"].keys():
				fin[fund][country_id]["projects"][project_id]["activities"][activity_id]={}
				fin[fund][country_id]["projects"][project_id]["activities"][activity_id]["activity"]=activity
				fin[fund][country_id]["projects"][project_id]["activities"][activity_id]["dac_code"]=dac_code
				fin[fund][country_id]["projects"][project_id]["activities"][activity_id]["dac_name"]=dac_name

				fin[fund][country_id]["projects"][project_id]["activities"][activity_id]["transactions"]=[]

			#FY,FQ,Disbursement,Obligation
			transaction={"fy":fy,"fq":fq, "disbursement":disbursement, "obligation":obligation}

			fin[fund][country_id]["projects"][project_id]["activities"][activity_id]["transactions"].append(transaction)

			#print fin[fund][country_id]["projects"][project_id]["activities"][activity_id]["transactions"]


	return countries, funds, fin


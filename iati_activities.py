# -*- coding: utf-8 -*-
import csv
import codecs
import json

from string import Template

from datetime import datetime
from datetime import date

import load_data

timestamp=datetime.now().replace(microsecond=0).isoformat()

#load all the data
countries, funds, data = load_data.load()

mcc_id="US-18" # which one is actual ID? <- this one
#mcc_id="US-USG-MCC-18"

#translates "Fiscal Year, Fiscal Quarter" into ISO date for the start date of the quarter
def fiscal_date(date):
	try:
		fy,fq=date.split(',')
		fy=fy.strip()
		fq=fq.strip()
		
		fy=fy[3:]
		fy=int(fy)
		
		if fq=="FQ 1":
			return str(fy-1)+"-"+"10-01"
		elif fq=="FQ 2":
			return str(fy)+"-"+"01-01"
		elif fq=="FQ 3":
			return str(fy)+"-"+"04-01"
		elif fq=="FQ 4":
			return str(fy)+"-"+"07-01"
		else:
			return "n/a"
	except:
		return "n/a"

# converts dates from 20/3/06 format to 2006-03-20 and marks if date is in past/future
def convert_date(projectdate):
	try:
		month,day,year=projectdate.split("/")
		month=month.zfill(2)
		day=day.zfill(2)
		year="20"+year.zfill(2)

		project_date=date(int(year), int(month), int(day))
		
		today=date.today()

		if today<project_date:
			return year+"-"+month+"-"+day, "future"
		else:
			return year+"-"+month+"-"+day, "past"
	except:
		return "", ""

#print convert_date("09/13/06")
#print convert_date("9/1/16")
#import sys
#sys.exit(0)

#activities and kpis are KPIs related files to match
def get_performance(country):
	perf_template=Template("""
		<result type="2">
		  <title>$title</title>
		  <indicator measure="1">
		     <period>
		       <!--period-start iso-date = "YYYY-MM-DD" />
		       <period-end iso-date = "YYYY-MM-DD" /-->
		       <target value = "$target" />
		       <actual value = "$actual" />
		     </period>
		     <!--baseline year = "YYYY" value="0" /-->
		     <baseline value="$baseline" />
		  </indicator>
		</result>""")
	perf=""

	f = codecs.open("data/kpis.csv", 'rU')
	csvreader = csv.reader(f, delimiter=',', quotechar='"')
	for i, row in enumerate(csvreader):
		if i==0:
			#print line
			#[u'country', u'project', u'activity', u'outcome\r']
			continue
		if i>0:
			if country!=row[0].strip():
				continue

			kpi=row[3].strip().replace("&"," and ")
			baseline=row[4].strip()
			target=row[5].strip()
			actual=row[6].strip()
			perf=perf+perf_template.substitute({"title":kpi,"baseline":baseline,"target":target,"actual":actual})

	f.close()

	#perf=perf.replace(u"\xe9","e")

	return perf



# dump data as json for debug purposes
fo=open("dump.json","w")
fo.write(json.dumps(data, indent=4))
fo.close()

#import sys
#sys.exit(0)

header_t="""<?xml version="1.0" encoding="utf-8"?>
<iati-activities generated-datetime="%s" version="1.0">"""

footer_t="""
</iati-activities>"""

info_project="""		
		<default-flow-type code="10">ODA</default-flow-type>
		<default-finance-type code="110">Aid grant excluding debt reorganisation</default-finance-type>
		<collaboration-type code="1">Bilateral</collaboration-type>
		<default-aid-type code="C01">Project-type interventions</default-aid-type>
		<default-tied-status code="5">Untied</default-tied-status>
		<activity-status code="2">Implementation</activity-status>
		"""

info_admin="""		
		<default-flow-type code="10">ODA</default-flow-type>
		<default-finance-type code="110">Aid grant excluding debt reorganisation</default-finance-type>
		<collaboration-type code="1">Bilateral</collaboration-type>
		<default-aid-type code="G01">Administrative costs</default-aid-type>
		<default-tied-status code="4">Tied</default-tied-status>
		<activity-status code="2">Implementation</activity-status>
		"""


compact_t=Template("""
	<iati-activity default-currency="USD" xml:lang="en" hierarchy="1">
		<reporting-org ref="$orgid" type="10">Millennium Challenge Corporation</reporting-org>

		<iati-identifier>$iatiid</iati-identifier>
		<title>$title</title>

		$info

		$recipientcountry

		<participating-org ref="US" role="Funding" type="10">United States of America</participating-org>
		<participating-org ref="$orgid" role="Extending" type="10">Millennium Challenge Corporation</participating-org>
		<participating-org role="Implementing">$implorgid</participating-org>


		$activitydate

$relatedactivities
		$location
		$performance
	</iati-activity>
""")

project_t=Template("""
	<iati-activity default-currency="USD" xml:lang="en" hierarchy="2">
		<reporting-org ref="$orgid" type="10">Millennium Challenge Corporation</reporting-org>

		<iati-identifier>$iatiid</iati-identifier>
		<title>$title</title>

		$info

		$recipientcountry

		<participating-org ref="US" role="Funding" type="10">United States of America</participating-org>
		<participating-org ref="$orgid" role="Extending" type="10">Millennium Challenge Corporation</participating-org>
		<participating-org role="Implementing">$implorgid</participating-org>


		$activitydate

$relatedactivities
	</iati-activity>
""")

activity_t=Template("""
	<iati-activity default-currency="USD" xml:lang="en" hierarchy="3">
		<reporting-org ref="$orgid" type="10">Millennium Challenge Corporation</reporting-org>

		<iati-identifier>$iatiid</iati-identifier>
		<title>$title</title>

		$info

		$recipientcountry

		<participating-org ref="US" role="Funding" type="10">United States of America</participating-org>
		<participating-org ref="$orgid" role="Extending" type="10">Millennium Challenge Corporation</participating-org>
		<participating-org role="Implementing">$implorgid</participating-org>


		$activitydate

$relatedactivities
		$transactions
	</iati-activity>
""")

transaction_t=Template("""
		<transaction>
			<transaction-date iso-date="$date">$date</transaction-date>
			<transaction-type code="$code">$type</transaction-type>
			<value value-date="$date">$amount</value>
		</transaction>""")


result_t=Template("""
		<result type="" aggregation-status="">
			<title></title>
			<description></description>
			<indicator measure="" ascending="">
				<title></title>
				<description type=""></description>
				<baseline year="" value="">
					<comment></comment>
				</baseline>
				<period>
					<preiod-start iso-date=""></period-start>
					<period-end iso-date=""></period-end>
					<target value="">
						<comment>
						</comment>
					</target>
					<actual value="">
						<comment>
						</comment>
					</actual>
				</period>
			</indicator>
		</result>""")


fo=open("output/mcc-activities.xml", 'w')

fo.write(header_t % (timestamp))

#Region,Fund,CountryID,Country,ProjectID,Project,ActivityID,Activity,DAC CODE,DACName,FY,FQ,Disbursement,Obligation
# header for finance.csv

for fund in data:
	print "PROCESSING FUND: ",fund
	for country_id in data[fund]:
		country=data[fund][country_id]["country"]

		orgid=mcc_id
		title=fund+" - "+country

		countrycode=""
		if fund.upper()+"-"+country_id in funds.keys():
			countrycode=funds[fund.upper()+"-"+country_id]["code2"]

		countryname=country

		recipientcountry=""
		if countrycode!="":
			recipientcountry="""<recipient-country code="%s">%s</recipient-country>""" %(countrycode, countryname)

		iatiid=mcc_id+"-"+country_id

		implorgid = countryname
		if fund in set(["Compact", "ADD ANY OTHER FUND NAMES WHERE IMPLEMENTING ORG IS MCA"]):
			implorgid="Millennium Challenge Account - "+countryname

		print country_id, countrycode, country, countryname


		info=info_project

		if fund.upper()+"-"+country_id in funds.keys():
			if funds[fund.upper()+"-"+country_id]["type"]=="ADMIN":
				info=info_admin
			else:
				info=info_project


		if country_id=="KEN":
			continue

		if country_id!="NA":
			startdate=""
			enddate=""
			when="never"
			if fund+"-"+country_id in funds.keys():
				startdate = convert_date(funds[fund+"-"+country_id]["start"])[0]
				enddate, when = convert_date(funds[fund+"-"+country_id]["end"])
		else:
			when="never"
			startdate=""
			enddate=""

		activitydate=""
		if when=="never" or startdate=="" or enddate=="":
			activitydate=""
		elif when=="past":
			activitydate=Template("""		<activity-date iso-date="$startdate" type="start-actual">$startdate</activity-date>
			<activity-date iso-date="$enddate" type="end-actual">$enddate</activity-date>
			""").substitute({"startdate":startdate, "enddate":enddate})
		elif when=="future":
			activitydate=Template("""		<activity-date iso-date="$startdate" type="start-actual">$startdate</activity-date>
			<activity-date iso-date="$enddate" type="end-planned">$enddate</activity-date>
			""").substitute({"startdate":startdate, "enddate":enddate})



		#print countryname
		location=""
		try:
			lat=countries[countryname.upper()]["lat"] #add geocoded lat/lon for country
			lon=countries[countryname.upper()]["lon"]

			location=Template("""		<location>
			    <location-type code="PCL"/>
			    <name xml:lang="en"></name>
			    <description>$countryname</description>
			    <administrative country="$countrycode">$countryname</administrative>
			    <coordinates latitude="$lat" longitude="$lon" precision="9"/>
			</location>
			""").substitute({"lat":lat,"lon":lon})
		except:
			location=""

		relatedactivities="""\n"""
		for project_id in data[fund][country_id]["projects"]:
			iatiid2=iatiid+"-"+project_id
			iatiid2=iatiid2.replace("&"," AND ")
			title2=title+" - "+data[fund][country_id]["projects"][project_id]["project"]
			title2 = title2.replace("&", " AND ")

			related_child=Template("""			<related-activity ref="$ref" type="2">$name</related-activity>""")
			params={"ref":iatiid2, #encode &amp;
					"name":title2}
			relatedactivities=relatedactivities+"\n"+related_child.substitute(params)

			related_parent=Template("""			<related-activity ref="$ref" type="1">$name</related-activity>""")

			
			project_relatedactivities=related_parent.substitute({"ref":iatiid, "name":title})

			for activity_id in data[fund][country_id]["projects"][project_id]["activities"]:
				iatiid3=iatiid2+"-"+activity_id
				title3=title2+" - "+data[fund][country_id]["projects"][project_id]["activities"][activity_id]["activity"]
				title3=title3.replace("&", " AND ")
				project_relatedactivities=project_relatedactivities+"\n"+related_child.substitute({"ref":iatiid3, "name":title3})

				activity_relatedactivities=related_parent.substitute({"ref":iatiid2, "name":title2})

				transactions=""
				for trans in data[fund][country_id]["projects"][project_id]["activities"][activity_id]["transactions"]:
					#print data[fund][country_id]["projects"][project_id]["activities"][activity_id]["transactions"]
					transactions=transactions+transaction_t.substitute({"date":fiscal_date(trans["fy"]+","+trans["fq"]),"code":"C","type":"Commitment","amount":"{0:.0f}".format(round(float(trans["obligation"]),0))})
					transactions=transactions+transaction_t.substitute({"date":fiscal_date(trans["fy"]+","+trans["fq"]),"code":"D","type":"Disbursement","amount":"{0:.0f}".format(round(float(trans["disbursement"]),0))})

				#DEBUG: remove next line
				#transactions=""

				params3={"orgid":orgid,
						"implorgid":implorgid,
						"title":title3,
						"info":info,
						"relatedactivities":activity_relatedactivities,
						"recipientcountry":recipientcountry,
						"countryname":countryname,
						"iatiid":iatiid3,
						"transactions":transactions,
						"activitydate":activitydate}
				fo.write(activity_t.substitute(params3))

			params2={"orgid":orgid,
					"implorgid":implorgid,
					"title":title2,
					"info":info,
					"relatedactivities":project_relatedactivities,
					"recipientcountry":recipientcountry,
					"countryname":countryname,
					"iatiid":iatiid2,
					"activitydate":activitydate}
			fo.write(project_t.substitute(params2))

		perf=get_performance(countryname)
		params={"orgid":orgid,
				"implorgid":implorgid,
				"title":title,
				"info":info,
				"relatedactivities":relatedactivities,
				"recipientcountry":recipientcountry,
				"countryname":countryname,
				"iatiid":iatiid,
				"location":location,
				"activitydate":activitydate,
				"performance":perf}
		fo.write(compact_t.substitute(params))

fo.write(footer_t)

fo.close()



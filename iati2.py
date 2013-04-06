from datetime import datetime
timestamp=datetime.now().replace(microsecond=0).isoformat()

f=open("mcc_q4_2012.txt", 'rU')

mcc_id="US-MCC-xxxxxxxxx"

def fiscal_date(date):
	#translates "Fiscal Year, Fiscal Quarter" into ISO date for the start date of the quarter
	fy,fq=date.split(',')
	fy=fy.strip()
	fq=fq.strip()
	
	fy=fy[3:]
	fy=int(fy)
	
	if fq=="FQ 1":
		return str(fy-1)+"-"+"09-01"
	elif fq=="FQ 2":
		return str(fy-1)+"-"+"12-01"
	elif fq=="FQ 3":
		return str(fy)+"-"+"03-01"
	elif fq=="FQ 4":
		return str(fy)+"-"+"06-01"
	else:
		return "n/a"

header_t="""
<?xml version="1.0"?>
<iati-activities generated-datetime="%s" version="1.0">"""

footer_t="""
</iati-activities>"""

activity_start_t="""
	<iati-activity default-currency="USD" xml:lang="en">
		<reporting-org ref="%s" type="10">Millennium Challenge Corporation</reporting-org>

		<default-flow-type code="10">ODA</default-flow-type>
		<participating-org role="implementing">%s</participating-org>
		<iati-identifier>%s</iati-identifier>
		<title>%s</title>
		<sector code="%s" vocab="DAC">%s</sector>
		<recipient-country code="%s">%s</recipient-country>
		<participating-org ref="US" role="funding" type="10">United States of America</participating-org>
		<default-finance-type code="110">Aid grant excluding debt reorganisation</default-finance-type>
		<activity-date iso-date="%s" type="start-actual">%s</activity-date>
		<activity-date iso-date="%s" type="end-planned">%s</activity-date>
		<collaboration-type code="1">Bilateral</collaboration-type>
		<default-aid-type code="C01">Project-type interventions</default-aid-type>
		<default-tied-status code="5">Untied</default-tied-status>
		<participating-org ref="%s" role="extending" type="10">Millennium Challenge Corporation</participating-org>
		<activity-status code="2">Implementation</activity-status>
"""

activity_end_t="""
	</iati-activity>"""

transaction_t="""
		<transaction>
			<transaction-date iso-date="%s">%s</transaction-date>
			<transaction-type code="%s">%s</transaction-type>
			<value value-date="%s">%s</value>
		</transaction>"""

fund=""
region=""
country_id=""
country=""
project_id=""
project=""
activity_id=""
activity=""
dac_code=""
dac_name=""

year=[]
quarter=[]
transaction=[]

fy={}

print header_t % (timestamp)

for i, line in enumerate(f):
	line=line.rstrip('\n').split("	")
	#line=line.split("	")
	if i==3:
		#headers for years
		year=line
		continue
	if i==4:
		#headers for quarters
		quarter=line
		continue
	if i==5:
		#headers for disbursements/obligations
		transaction=line
		
		y=""
		q=""
		tr=""
		for j, el in enumerate(transaction):
			if j>9:
				if quarter[j]!='Total' and year[j]!='Grand Total':
					if len(year[j])>0: y=year[j].strip()
					q=quarter[j].strip()
					tr=transaction[j].strip()
					#print (y, q, tr)
					fy[j]={"fy":y,"quarter":q, "transaction":tr}
					
		
		continue
	if len(line)==1:
		continue
	#print len(line.split("	"))	
	#print i, line.split("	")
	#print i, len(line), line
	if line[1]=='Total' or line[2]=='Total' or line[3]=='Total' or line[0]=='Total':
		continue

	if i>6:
	
		if len(line[0])>0: fund=line[0]
		if len(line[1])>0: region=line[1]
		if len(line[2])>0: country_id=line[2]
		if len(line[3])>0: country=line[3]
		if len(line[4])>0: project_id=line[4]
		if len(line[5])>0: project=line[5]
		if len(line[6])>0: activity_id=line[6]
		if len(line[7])>0: activity=line[7]
		if len(line[8])>0: dac_code=line[8]
		if len(line[9])>0: dac_name=line[9]
	
		#print (fund,region,country_id,country,project_id,project,activity_id,activity,dac_code,dac_name)
		#print ""

		org_id="Millennium Challenge Account "+country+" MCA-"+country_id
		org_iati_id=country_id+"-MCA-xxxxxxxxx"
		
		activity_start=""
		activity_end=""
		
		print activity_start_t % (mcc_id, org_id, org_iati_id, project, dac_code, dac_name, country_id, country, activity_start, activity_start, activity_end, activity_end, mcc_id)

		for j, el in enumerate(line):
			if j>9:
				if j in fy.keys():
					date=fy[j]["fy"]+", "+fy[j]["quarter"]
					iso_date=fiscal_date(date)
					t_date=date
					t_type=fy[j]["transaction"]
					
					if t_type=="Disbursement":
						t_code="D"
					if t_type=="Obligation":
						t_type="Commitment"
						t_code="C"
	
					value=line[j]
					value_date=fiscal_date(date)

					if len(value)>0:
						print transaction_t % (iso_date, t_date, t_code, t_type, value_date, value)

		print activity_end_t 

print footer_t
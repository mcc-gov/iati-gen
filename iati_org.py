from datetime import datetime
timestamp=datetime.now().replace(microsecond=0).isoformat()

header_t="""
<iati-organisation version="1.01" last-updated-datetime="%s" xml:lang="en" default-currency="USD">
  <iati-identifier>US-MCC-1</iati-identifier>
  <ir:registry-record xmlns:ir="http://iatiregistry.org/ns/record#" xml:lang="en" file-id="US-MCC-1" 
	source-url="http://data.mcc.gov/raw/iati/organisation.xml" publisher-id="US-MCC-1" 
	publisher-role="Funding" contact-email="opendata@mcc.gov" donor-id="US-MCC-1" donor-type="10" 
	donor-country="US" title="MCC Organisation File" activity-period="All Periods" 
	last-updated-datetime="%s" 
	generated-datetime="%s" verification-status="1" format="xml" license="IATI" />
  <name>Millennium Challenge Corporation</name>
"""

footer_t="""
</iati-organisation>
"""

budget_t="""
<total-budget>
  <period-start iso-date="2010-04-01">01 April 2010</period-start>
  <period-end iso-date="2011-03-31">31 March 2011</period-end>
  <value value-date="2010-10-20">7800000000</value>
</total-budget>"""

country_budget_t="""
<recipient-country-budget>
  <recipient-country code="ZW">Zimbabwe</recipient-country>
  <period-start iso-date="2014-04-01">Start of Financial Year 2014/15</period-start>
  <period-end iso-date="2015-03-31">End of Financial Year 2014/15</period-end>
  <value currency="USD" value-date="2014-04-01">94000000</value>
</recipient-country-budget>"""

doc_t="""<document-link url="%s" format="%s">
  <title>%s</title>
  <category code="%s">%s</category>
</document-link>"""


fo=open("output/mcc-organisation.xml","w")

fo.write(header_t % (timestamp,timestamp,timestamp))

fi=open("source/documents.csv","rU")
for line in fi:
	category, code,title,url,format=line.strip().split("	")
	fo.write(doc_t % (url, format, title, code, category))
	fo.write("\n")

fo.write(footer_t)

